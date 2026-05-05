async function analyzeRisk() {
    const input = document.getElementById("inputText").value;
    const resultDiv = document.getElementById("result");
    const button = document.querySelector("button");

    if (!input.trim()) {
        resultDiv.innerHTML = "❌ Please enter some text";
        resultDiv.className = "result-box";
        return;
    }

    resultDiv.innerHTML = "Analyzing...";
    resultDiv.className = "result-box";
    button.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ input: input })
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = "❌ " + data.error;
            resultDiv.className = "result-box";
        } else {
            let riskClass = "low";

            if (data.risk_level === "HIGH") riskClass = "high";
            else if (data.risk_level === "MEDIUM") riskClass = "medium";

            resultDiv.className = "result-box " + riskClass;

            resultDiv.innerHTML =
                "Risk Level: " + data.risk_level + "<br>" +
                "Analysis: " + data.analysis;
        }

    } catch (error) {
        resultDiv.innerHTML = "❌ Server not reachable";
        resultDiv.className = "result-box";
    }

    button.disabled = false;
}