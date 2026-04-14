from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import simulation_manager
import protocols
from pydantic import BaseModel

app = FastAPI(title="Quantum Key Distribution Simulator API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mocked Auth Database
users = {"admin": "password123", "user": "securepass"}

class LoginRequest(BaseModel):
    username: str
    password: str

class SimulationRequest(BaseModel):
    protocols: List[str] = ["bb84"]
    n_bits: int = 100
    noise_levels: List[float] = [0.0, 0.05, 0.1]
    n_sim: int = 1

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/simulate")
def run_simulation(req: SimulationRequest):
    results = simulation_manager.compare_protocols(
        protocol_list=req.protocols,
        n_bits=req.n_bits,
        noise_levels=req.noise_levels,
        n_sim=req.n_sim,
        output_dir='./results',
        output_prefix='api_simulation'
    )
    return results

import visualization_helper

@app.post("/login")
def login(req: LoginRequest):
    if req.username in users and users[req.username] == req.password:
        return {"status": "success", "user": req.username, "role": "admin" if req.username == "admin" else "user"}
    return {"status": "error", "message": "Invalid credentials"}

@app.get("/admin/stats")
def get_admin_stats():
    # Return some mock data for the admin panel
    return {
        "total_simulations": 1240,
        "avg_qber": "4.2%",
        "uptime": "99.9%",
        "active_nodes": 42
    }

@app.get("/protocol/step-by-step")
def get_step_by_step(protocol: str = "bb84", n_bits: int = 20, eve: bool = False, noise: float = 0.0):
    """
    Returns a detailed step-by-step execution of a single protocol run for visualization.
    """
    if protocol == "bb84":
        return visualization_helper.simulate_bb84_detailed(n_bits=n_bits, eve_present=eve, noise_level=noise)
    else:
        # Fallback to BB84 for now as other protocols are not yet detailed
        return visualization_helper.simulate_bb84_detailed(n_bits=n_bits, eve_present=eve, noise_level=noise)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ... earlier code ...

@app.get("/")
def read_index():
    return FileResponse("index.html")

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Important: Start server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
