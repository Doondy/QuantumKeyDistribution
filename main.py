import simulation_manager
import os

def run_project():
    print("=" * 60)
    print("Welcome to the QKD Simulation Project (Advanced Analysis)")
    print("=" * 60)
    print("\nStarting comprehensive protocol comparison (BB84 vs B92)...")
    
    simulation_manager.compare_protocols(n_bits=2000, noise_levels=[0.0, 0.05, 0.1, 0.2])
    
    print("\nDONE: Full QKD analysis completed.")
    print("- Analysis graph: full_protocol_analysis.png")
    print("- Detailed stats: full_analysis_summary.txt")
    print("\nReading summary results...")
    
    if os.path.exists('full_analysis_summary.txt'):
         with open('full_analysis_summary.txt', 'r') as f:
             print("\n" + f.read())

if __name__ == "__main__":
    run_project()
