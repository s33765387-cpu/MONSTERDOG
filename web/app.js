const socket = new WebSocket("ws://localhost:8888/ws");
const statusSpan = document.getElementById("connection-status");
const logWindow = document.getElementById("log-output");

function log(msg) {
    const line = document.createElement("div");
    line.innerHTML = `> ${new Date().toLocaleTimeString()} : ${msg}`;
    logWindow.appendChild(line);
    logWindow.scrollTop = logWindow.scrollHeight;
}

socket.onopen = () => {
    statusSpan.textContent = "CONNECTÉ [SYSTEM ONLINE]";
    statusSpan.style.color = "#00ff9d";
    log("LIAISON WEBSOCKET ÉTABLIE.");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // Mise à jour Quantum
    if(data.quantum_core) {
        const q = data.quantum_core;
        document.getElementById("val-coherence").textContent = q.coherence.toFixed(4);
        document.getElementById("bar-coherence").style.width = (q.coherence * 100) + "%";
        
        document.getElementById("val-entropy").textContent = q.entropy.toFixed(4);
        document.getElementById("bar-entropy").style.width = (q.entropy * 100) + "%";
        
        document.getElementById("val-stability").textContent = (q.stability * 100).toFixed(1) + "%";
    }

    // Mise à jour Agents
    if(data.agents) {
        const list = document.getElementById("agent-list");
        list.innerHTML = "";
        for (const agent of data.agents) {
            const li = document.createElement("li");
            li.textContent = `${agent.name} : ${agent.status} [Mode: ${agent.mode}]`;
            list.appendChild(li);
        }
    }
};

socket.onclose = () => {
    statusSpan.textContent = "DÉCONNECTÉ [OFFLINE]";
    statusSpan.style.color = "red";
    log("PERTE DE SIGNAL...");
};
