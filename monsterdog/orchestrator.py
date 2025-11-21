#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONSTERDOG SUPREME ORCHESTRATOR - Partie IV
API FastAPI avec WebSocket pour le streaming temps réel
"""

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import json
import os

from .core import MonsterDogQuantumCore
from .agents import AgenticSystem

# Création de l'application FastAPI
app = FastAPI(
    title="MONSTERDOG CONTINUUM vΩ",
    description="Architecture IA Quantique & Agentique",
    version="11.987.0"
)

# Initialisation des systèmes
quantum_core = MonsterDogQuantumCore()
agentic_system = AgenticSystem()

# Liste des connexions WebSocket actives
active_connections: List[WebSocket] = []


class SupremeOrchestrator:
    """
    Orchestrateur suprême qui coordonne tous les systèmes.
    """
    
    def __init__(self):
        self.quantum = MonsterDogQuantumCore()
        self.agents = AgenticSystem()
        self.running = False
        
    async def main_loop(self):
        """Boucle principale de l'orchestrateur."""
        while self.running:
            # Mise à jour du noyau quantique
            quantum_state = self.quantum.step()
            
            # Auto-pivot des agents basé sur l'état quantique
            self.agents.auto_pivot(
                quantum_state["coherence"],
                quantum_state["entropy"]
            )
            
            # Exécution des agents
            agents_state = await self.agents.execute_all()
            
            # Préparation du message
            message = {
                "quantum_core": quantum_state,
                "agents": agents_state["agents"],
                "system_mode": agents_state["system_mode"]
            }
            
            # Diffusion aux clients WebSocket
            await broadcast(json.dumps(message))
            
            # Pause pour respecter la fréquence (11.987 Hz ≈ 83.5ms)
            await asyncio.sleep(0.0835)
    
    def start(self):
        """Démarre l'orchestrateur."""
        self.running = True
        
    def stop(self):
        """Arrête l'orchestrateur."""
        self.running = False


# Instance de l'orchestrateur
orchestrator = SupremeOrchestrator()


async def broadcast(message: str):
    """Diffuse un message à tous les clients WebSocket connectés."""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            disconnected.append(connection)
    
    # Nettoyage des connexions mortes
    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)


@app.on_event("startup")
async def startup_event():
    """Événement de démarrage de l'application."""
    orchestrator.start()
    # Lancement de la boucle principale en arrière-plan
    asyncio.create_task(orchestrator.main_loop())


@app.on_event("shutdown")
async def shutdown_event():
    """Événement d'arrêt de l'application."""
    orchestrator.stop()


@app.get("/")
async def root():
    """Page d'accueil."""
    return {
        "message": "MONSTERDOG CONTINUUM vΩ",
        "status": "ONLINE",
        "frequency": "11.987 Hz"
    }


@app.get("/status")
async def get_status():
    """Retourne le statut actuel du système."""
    return {
        "quantum": quantum_core.get_state(),
        "agents": agentic_system.get_state(),
        "connections": len(active_connections)
    }


@app.get("/dashboard")
async def dashboard():
    """Retourne le dashboard HTML."""
    # Cherche le fichier index.html dans le dossier web
    web_path = os.path.join(os.path.dirname(__file__), "..", "web", "index.html")
    if os.path.exists(web_path):
        return FileResponse(web_path)
    else:
        return HTMLResponse(content="""
        <html>
            <head><title>MONSTERDOG vΩ</title></head>
            <body>
                <h1>MONSTERDOG CONTINUUM vΩ</h1>
                <p>Dashboard à venir...</p>
                <p>Fichier web/index.html non trouvé.</p>
                <p>API disponible sur <a href="/docs">/docs</a></p>
            </body>
        </html>
        """)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket pour le streaming temps réel.
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Attend les messages du client (keepalive)
            data = await websocket.receive_text()
            # On peut traiter des commandes ici si nécessaire
    except WebSocketDisconnect:
        active_connections.remove(websocket)
