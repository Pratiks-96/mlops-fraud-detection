from flask import Flask, request, jsonify
import subprocess
import requests
import datetime
import os

app = Flask(__name__)

LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def run_cmd(cmd):
    return subprocess.getoutput(cmd)

def collect_cluster_data(namespace):
    data = {}
    data["deployment"] = run_cmd(f"kubectl get deployment fraud-detection-deployment -n {namespace} -o yaml")
    data["replicasets"] = run_cmd(f"kubectl get rs -n {namespace}")
    data["pods"] = run_cmd(f"kubectl get pods -n {namespace} -o wide")
    data["events"] = run_cmd(f"kubectl get events -n {namespace} --sort-by=.metadata.creationTimestamp")
    data["hpa"] = run_cmd(f"kubectl get hpa -n {namespace}")
    return data

def ask_llm(prompt):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(LLM_ENDPOINT, headers=headers, json=body)
    return response.json()["choices"][0]["message"]["content"]

def save_solution(text):
    with open("/data/incident.log", "a") as f:
        f.write(f"\n\n--- {datetime.datetime.now()} ---\n")
        f.write(text)

@app.route("/webhook", methods=["POST"])
def webhook():
    alert_data = request.json
    alert = alert_data["alerts"][0]
    namespace = alert["labels"].get("namespace", "default")
    alert_name = alert["labels"]["alertname"]

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

    return jsonify({"status": "processed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
