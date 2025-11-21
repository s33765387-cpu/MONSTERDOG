# MONSTERDOG Framework vΩ - Quick Start Guide

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🏁 Running the System

### 1. System Verification (Recommended First)
Run the verification script to ensure all components are working:
```bash
python verify_system.py
```

You should see all 5 tests pass:
- ✅ AEGIS Security
- ✅ Hardware Monitor
- ✅ Quantum Core
- ✅ Supreme Orchestrator
- ✅ Agentic System

### 2. Start the Server
Launch the MONSTERDOG Continuum:
```bash
python main.py
```

The system will:
1. Initialize AEGIS Security
2. Detect hardware configuration
3. Start the Quantum Core
4. Activate the Agentic System
5. Launch the FastAPI server on port 8888

### 3. Access the System

Once the server is running, access:

- **Dashboard (Web Interface)**: http://localhost:8888/dashboard
  - Real-time visualization of Quantum Core metrics
  - Live agent status monitoring
  - WebSocket connection for streaming data

- **API Documentation**: http://localhost:8888/docs
  - Interactive Swagger UI
  - Try out API endpoints directly

- **API Root**: http://localhost:8888/
  - System status overview

- **Status Endpoint**: http://localhost:8888/status
  - Detailed JSON status of quantum core, agents, and connections

## 📊 Using the Dashboard

The cyberpunk-themed dashboard displays:

1. **Quantum Core Metrics**:
   - Coherence level (bar gauge)
   - Entropy level (bar gauge)
   - Stability percentage

2. **Agentic System**:
   - Active agents list
   - Current operation mode (EXPLORATION/EXPLOITATION/CONSERVATION)

3. **System Logs**:
   - Real-time event stream
   - Connection status

The dashboard updates automatically at 11.987 Hz via WebSocket.

## 🧪 Running Tests

Run the unit test suite:
```bash
python -m pytest tests/test_core.py -v
```

All 13 tests should pass:
- 4 tests for Quantum Core
- 3 tests for Agentic System
- 3 tests for AEGIS Security
- 3 tests for Hardware Monitor

## 🔐 Security

Generate a manifest with integrity signatures:
```bash
python generate_manifest.py
```

This creates `MANIFEST_RELEASE.json` with SHA-512 hashes of all project files.

## 📦 Package Installation

Install MONSTERDOG as a Python package:
```bash
pip install -e .
```

After installation, you can use it from anywhere:
```python
from monsterdog import MonsterDogQuantumCore, AgenticSystem
```

## 🛑 Stopping the System

Press `Ctrl+C` in the terminal where the server is running. You'll see:
```
🛑 ARRÊT DU SYSTÈME. COHÉRENCE SAUVEGARDÉE.
```

## 📚 Documentation

For detailed technical documentation, see:
- [docs/MONSTERDOG_WHITEPAPER.md](docs/MONSTERDOG_WHITEPAPER.md) - Complete architecture documentation
- [README.md](README.md) - Project overview

## 🔧 Architecture

```
MONSTERDOG_FRAMEWORK_vΩ/
├── monsterdog/          # Main Python package
│   ├── core.py          # Quantum Core engine
│   ├── agents.py        # Multi-agent system
│   ├── orchestrator.py  # FastAPI server
│   ├── hardware.py      # Hardware monitoring
│   └── security.py      # AEGIS security
├── web/                 # Web interface
│   ├── index.html       # Dashboard
│   ├── style.css        # Styling
│   └── app.js           # WebSocket client
├── docs/                # Documentation
├── tests/               # Unit tests
├── main.py              # Application launcher
├── setup.py             # Package installer
└── requirements.txt     # Dependencies
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | System overview |
| `/status` | GET | Detailed system status |
| `/dashboard` | GET | Web dashboard |
| `/docs` | GET | API documentation (Swagger) |
| `/ws` | WebSocket | Real-time data stream |

## 💡 Tips

1. **First Time Setup**: Always run `verify_system.py` before launching the server
2. **Development**: Use the `/docs` endpoint to explore and test the API
3. **Monitoring**: Open the dashboard in your browser while the server runs to see live metrics
4. **Testing**: Run pytest regularly during development to ensure code integrity

## ⚡ Performance

- **Frequency**: 11.987 Hz (system refresh rate)
- **WebSocket Updates**: Real-time streaming
- **CSV Processing**: Handles files >60MB via chunking
- **Agents**: 3 specialized agents (Quantum, CSV, XR)

## 🐛 Troubleshooting

**Server won't start**: Check if port 8888 is already in use
```bash
lsof -i :8888
```

**Import errors**: Ensure dependencies are installed
```bash
pip install -r requirements.txt
```

**Tests failing**: Verify Python version (3.8+)
```bash
python --version
```

---

*Fréquence de cohérence: 11.987 Hz*
*Forgé par Samuel Cloutier / ZORG-MASTER*
