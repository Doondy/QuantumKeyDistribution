import numpy as np
import matplotlib.pyplot as plt
import protocols

def compare_protocols(n_bits=5000, noise_levels=[0.0, 0.05, 0.10, 0.15]):
    """
    Compares BB84 and B92 protocols for QBER and FINAL key yield.
    """
    results = {
        'noise': noise_levels,
        'bb84_qber_no_eve': [],
        'bb84_qber_with_eve': [],
        'bb84_key_final_no_eve': [],
        'bb84_key_final_with_eve': []
    }
    
    n_sim = 50
    for noise in noise_levels:
        q_bb84_0, q_bb84_1 = [], []
        kf_bb84_0, kf_bb84_1 = [], []
        
        for _ in range(n_sim):
            q, sifted, final = protocols.bb84_protocol(n_bits, False, noise)
            q_bb84_0.append(q)
            kf_bb84_0.append(final)
            
            q, sifted, final = protocols.bb84_protocol(n_bits, True, noise)
            q_bb84_1.append(q)
            kf_bb84_1.append(final)
            
        results['bb84_qber_no_eve'].append(np.mean(q_bb84_0))
        results['bb84_qber_with_eve'].append(np.mean(q_bb84_1))
        results['bb84_key_final_no_eve'].append(np.mean(kf_bb84_0))
        results['bb84_key_final_with_eve'].append(np.mean(kf_bb84_1))
        
    # Visualization: Compare QBER and Final Key
    plt.figure(figsize=(14, 7))
    x = np.array([n * 100 for n in noise_levels])
    
    plt.subplot(1, 2, 1)
    plt.plot(x, results['bb84_qber_no_eve'], 'o-', label='QBER No Eve', color='#3498db', linewidth=2)
    plt.plot(x, results['bb84_qber_with_eve'], 's--', label='QBER With Eve', color='#e67e22', linewidth=2)
    plt.xlabel('Noise Level (%)')
    plt.ylabel('Average QBER (%)')
    plt.title('BB84: QBER vs Noise')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.subplot(1, 2, 2)
    plt.bar(x - 2, results['bb84_key_final_no_eve'], 4, label='Final Key (No Eve)', color='#2ecc71')
    plt.bar(x + 2, results['bb84_key_final_with_eve'], 4, label='Final Key (With Eve)', color='#c0392b')
    plt.xlabel('Noise Level (%)')
    plt.ylabel('Final Secret Key Length (Bits)')
    plt.title('BB84: Final Secure Key Yield')
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('full_protocol_analysis.png')
    print("Full analysis plot saved as full_protocol_analysis.png")
    
    # Text Analysis Summary
    with open('full_analysis_summary.txt', 'w') as f:
        f.write("Full QKD Simulation Summary (Post-Processing Included)\n")
        f.write("=" * 60 + "\n")
        f.write("Noise % | QBER (No Eve) | Final Key (No Eve) | QBER (With Eve) | Final Key (With Eve)\n")
        f.write("-" * 80 + "\n")
        for i, nl in enumerate(noise_levels):
            f.write(f"{nl*100:6.1f}% | {results['bb84_qber_no_eve'][i]:13.2f}% | {results['bb84_key_final_no_eve'][i]:18.1f} | {results['bb84_qber_with_eve'][i]:13.2f}% | {results['bb84_key_final_with_eve'][i]:19.1f}\n")

if __name__ == "__main__":
    compare_protocols()
