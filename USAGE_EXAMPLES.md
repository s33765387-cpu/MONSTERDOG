# MONSTERDOG Framework vΩ - Usage Examples

## Quick Start

### 1. Basic System Launch

```bash
# Install dependencies
pip install -r requirements.txt

# Verify system integrity
python verify_system.py

# Launch the framework
python main.py
```

**Expected Output:**
```
🐺 INITIALISATION DU CONTINUUM MONSTERDOG vΩ...
✅ SÉCURITÉ AEGIS : ACTIVE (Token: 4f3fe24f...)
✅ HARDWARE DÉTECTÉ : Linux
   CPU: 2 coeurs | RAM: 10.2% utilisée
✅ MODE AUTO-PIVOT : PRÊT
✅ QUANTUM CORE : STANDBY
✅ AGENTIC SYSTEM : STANDBY

🚀 DÉMARRAGE DU SUPER-ORCHESTRATEUR (API + WS + DASHBOARD)...
   PORTAIL DISPONIBLE SUR : http://localhost:8888/dashboard
   DOCS API DISPONIBLE SUR : http://localhost:8888/docs
```

### 2. Using the Python Package

```python
from monsterdog import MonsterDogQuantumCore, AgenticSystem

# Initialize Quantum Core
quantum = MonsterDogQuantumCore()

# Run simulation
for i in range(10):
    state = quantum.step()
    print(f"Cycle {state['cycle']}: Coherence={state['coherence']:.4f}, Entropy={state['entropy']:.4f}")

# Initialize Agent System
agents = AgenticSystem()

# Execute agents asynchronously
import asyncio
result = asyncio.run(agents.execute_all())
print(f"Active agents: {result['active_count']}")
```

### 3. Using the REST API

```bash
# Get system status
curl http://localhost:8888/status

# Response:
{
  "quantum": {
    "coherence": 0.497502,
    "entropy": 0.504018,
    "stability": 0.998484,
    "cycle": 1,
    "frequency": 11.987
  },
  "agents": {
    "system_mode": "EXPLORATION",
    "agent_count": 3,
    "agents": {
      "QuantumAnalyzer": "EXPLORATION",
      "CSVProcessor": "EXPLORATION",
      "XRProcessor": "EXPLORATION"
    }
  },
  "connections": 0
}
```

### 4. WebSocket Connection

JavaScript example for real-time data:

```javascript
const socket = new WebSocket("ws://localhost:8888/ws");

socket.onopen = () => {
    console.log("Connected to MONSTERDOG");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Quantum Core:", data.quantum_core);
    console.log("Agents:", data.agents);
};
```

### 5. Security Token Generation

```python
from monsterdog.security import AegisSecurity

aegis = AegisSecurity()

# Generate token
token = aegis.generate_token()
print(f"Token: {token}")

# Verify token
is_valid = aegis.verify(token)
print(f"Token valid: {is_valid}")

# Hash a file
file_hash = aegis.hash_file("main.py")
print(f"File hash: {file_hash}")
```

### 6. Hardware Monitoring

```python
from monsterdog.hardware import MonsterDogHardwareMonitor

hw = MonsterDogHardwareMonitor()

# Get full report
report = hw.full_report()

print(f"System: {report['system']['system']}")
print(f"CPU Cores: {report['cpu']['physical_cores']}")
print(f"RAM Usage: {report['memory']['percent']}%")
print(f"Disk Usage: {report['disk']['percent']}%")
```

### 7. Processing Large CSV Files

```python
import asyncio
from monsterdog.agents import AgentCSV

async def process_csv():
    agent = AgentCSV()
    result = await agent.process_large_csv("large_dataset.csv")
    
    if result['status'] == 'SUCCESS':
        print(f"Processed {result['total_rows']} rows in {result['chunks']} chunks")
    else:
        print(f"Error: {result['error']}")

asyncio.run(process_csv())
```

### 8. Auto-Pivot Demonstration

```python
import asyncio
from monsterdog.core import MonsterDogQuantumCore
from monsterdog.agents import AgenticSystem

async def demonstrate_auto_pivot():
    quantum = MonsterDogQuantumCore()
    agents = AgenticSystem()
    
    for i in range(20):
        # Update quantum state
        state = quantum.step()
        
        # Auto-pivot based on quantum state
        agents.auto_pivot(state['coherence'], state['entropy'])
        
        # Execute agents
        result = await agents.execute_all()
        
        print(f"Cycle {i}: Mode={result['system_mode']}, "
              f"Coherence={state['coherence']:.4f}, "
              f"Entropy={state['entropy']:.4f}")
        
        await asyncio.sleep(0.1)

asyncio.run(demonstrate_auto_pivot())
```

### 9. Running Tests

```bash
# Run unit tests
python -m pytest tests/test_core.py -v

# Run specific test class
python -m pytest tests/test_core.py::TestQuantumCore -v

# Run with coverage
python -m pytest tests/test_core.py --cov=monsterdog --cov-report=html

# Run system verification
python verify_system.py
```

### 10. Generating Integrity Manifest

```bash
# Generate manifest with SHA-512 signatures
python generate_manifest.py

# View manifest
cat MANIFEST_RELEASE.json
```

## Advanced Usage

### Custom Agent Creation

```python
from monsterdog.agents import Agent, PivotMode

class CustomAgent(Agent):
    def __init__(self):
        super().__init__("CustomProcessor", PivotMode.MODE_A)
        
    async def execute(self):
        result = await super().execute()
        result["custom_data"] = "Processing..."
        return result

# Add to system
from monsterdog.agents import AgenticSystem
system = AgenticSystem()
system.agents.append(CustomAgent())
```

### Integration with FastAPI

```python
from fastapi import FastAPI
from monsterdog.orchestrator import app as monsterdog_app

# Mount MONSTERDOG as sub-application
main_app = FastAPI()
main_app.mount("/monsterdog", monsterdog_app)

# Or add custom endpoints
@main_app.get("/custom")
async def custom_endpoint():
    from monsterdog.core import MonsterDogQuantumCore
    core = MonsterDogQuantumCore()
    return core.get_state()
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8888
lsof -i :8888

# Kill the process
kill -9 <PID>

# Or run on different port
uvicorn monsterdog.orchestrator:app --port 8889
```

### Import Errors

```bash
# Ensure package is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in development mode
pip install -e .
```

### WebSocket Connection Issues

Check firewall settings and ensure server is running:
```bash
# Test server is accessible
curl http://localhost:8888/

# Check WebSocket with wscat
npm install -g wscat
wscat -c ws://localhost:8888/ws
```

## Performance Tuning

### Adjust Quantum Core Frequency

```python
from monsterdog.core import MonsterDogQuantumCore

core = MonsterDogQuantumCore()
core.FREQUENCY = 24.0  # Custom frequency (Hz)
```

### Optimize CSV Processing

```python
from monsterdog.agents import AgentCSV

agent = AgentCSV()
agent.chunk_size = 50000  # Larger chunks for better performance
```

---

*For more information, see [QUICKSTART.md](QUICKSTART.md) and [docs/MONSTERDOG_WHITEPAPER.md](docs/MONSTERDOG_WHITEPAPER.md)*
