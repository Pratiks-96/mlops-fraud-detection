from flask import Flask, request, jsonify
import subprocess
import requests
import datetime
import os
import json

app = Flask(__name__)

LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_ENDPOINT = "https://api.openai.com/v1/chat/completions"


# -------------------------------
# Safe command runner
# -------------------------------
def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except Exception as e:
        return f"Error running command: {str(e)}"


# -------------------------------
# Collect cluster data safely
# -------------------------------
def collect_cluster_data(namespace):
    data = {}

    data["deployment"] = run_cmd(
        f"kubectl get deployment fraud-detection-deployment -n {namespace} -o yaml"
    )
    data["replicasets"] = run_cmd(f"kubectl get rs -n {namespace}")
    data["pods"] = run_cmd(f"kubectl get pods -n {namespace} -o wide")
    data["events"] = run_cmd(
        f"kubectl get events -n {namespace} --sort-by=.metadata.creationTimestamp"
    )
    data["hpa"] = run_cmd(f"kubectl get hpa -n {namespace}")

    return data


# -------------------------------
# Ask LLM safely
# -------------------------------
def ask_llm(prompt):

    if not LLM_API_KEY:
        return "LLM_API_KEY is not set in environment."

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    try:
        response = requests.post(LLM_ENDPOINT, headers=headers, json=body, timeout=30)

        if response.status_code != 200:
            return f"OpenAI API Error: {response.text}"

        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response from LLM")

    except Exception as e:
        return f"Error calling LLM: {str(e)}"


# -------------------------------
# Save solution safely
# -------------------------------
def save_solution(text):
    try:
        os.makedirs("/data", exist_ok=True)

        with open("/data/incident.log", "a") as f:
            f.write(f"\n\n--- {datetime.datetime.now()} ---\n")
            f.write(text)
    except Exception as e:
        print("Error saving solution:", str(e))


# -------------------------------
# Health check route
# -------------------------------
@app.route("/")
def home():
    return "AI Incident Manager Running", 200


# -------------------------------
# Webhook endpoint
# -------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        alert_data = request.json

        if not alert_data or "alerts" not in alert_data:
            return jsonify({"error": "Invalid alert format"}), 400

        alert = alert_data["alerts"][0]

        namespace = alert.get("labels", {}).get("namespace", "default")
        alert_name = alert.get("labels", {}).get("alertname", "Unknown")

        print(f"Received Alert: {alert_name} in namespace {namespace}")

        cluster_data = collect_cluster_data(namespace)

        prompt = f"""
Alert Fired: {alert_name}

Deployment:
{cluster_data["deployment"]}

ReplicaSets:
{cluster_data["replicasets"]}

Pods:
{cluster_data["pods"]}

Events:
{cluster_data["events"]}

HPA:
{cluster_data["hpa"]}

Provide:
1. Root cause
2. Impact
3. Recommended solution
"""

        solution = ask_llm(prompt)

        save_solution(solution)

        return jsonify({"status": "processed", "alert": alert_name})

    except Exception as e:
        print("Webhook Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
