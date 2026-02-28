function createProbabilityChart(probability) {

new Chart(document.getElementById('probChart'), {

type: 'bar',

data: {
labels: ['Fraud Probability'],
datasets: [{
label: '%',
data: [probability]
}]
}

})

}


async function loadHistory() {

const response = await fetch("/api/history")

const data = await response.json()

const labels = data.map(d => d.amount)

const probs = data.map(d => d.probability)

new Chart(document.getElementById("historyChart"), {

type: "line",

data: {

labels: labels,

datasets: [{

label: "Fraud Probability",

data: probs

}]

}

})

}

setInterval(loadHistory, 5000)
