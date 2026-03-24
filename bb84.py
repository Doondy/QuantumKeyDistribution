import numpy as np
import matplotlib.pyplot as plt

def simulate_bb84_v2(n_bits=1000, eve_present=False, noise_level=0.02):
    """
    Enhanced BB84 simulation with channel noise and eavesdropping.
    noise_level: Probability of a bit flipping due to channel noise (0.00 to 1.00).
    """
    # Alice's random bits and bases
    alice_bits = np.random.randint(2, size=n_bits)
    alice_bases = np.random.randint(2, size=n_bits)
    
    # Photons sent to Bob
    qubits = np.copy(alice_bits)
    
    # 1. Eavesdropping (Optional)
    if eve_present:
        eve_bases = np.random.randint(2, size=n_bits)
        eve_results = []
        for i in range(n_bits):
            if alice_bases[i] == eve_bases[i]:
                eve_results.append(qubits[i])
            else:
                eve_results.append(np.random.randint(2))
        qubits = np.array(eve_results) # Eve re-sends her measurements

    # 2. Channel Noise (Bit Flips)
    for i in range(n_bits):
        if np.random.random() < noise_level:
            qubits[i] = 1 - qubits[i] # Bit flip

    # 3. Bob's Measurement
    bob_bases = np.random.randint(2, size=n_bits)
    bob_results = []
    for i in range(n_bits):
        # If Bob's basis matches the basis of the photon (disturbed by Eve or noise)
        # We model this by comparing with Alice's original basis and Eve's disturbance.
        if bob_bases[i] == alice_bases[i]:
            # If Eve was present and changed basis, 50% chance of disturbance
            if eve_present and alice_bases[i] != eve_bases[i]:
                 bob_results.append(np.random.randint(2))
            else:
                 bob_results.append(qubits[i]) # Still subject to noise above
        else:
            bob_results.append(np.random.randint(2))
    
    bob_results = np.array(bob_results)
    
    # 4. Sifting
    sifted_indices = np.where(alice_bases == bob_bases)[0]
    alice_key = alice_bits[sifted_indices]
    bob_key = bob_results[sifted_indices]
    
    # 5. QBER Calculation
    errors = np.sum(alice_key != bob_key)
    qber = (errors / len(alice_key)) * 100 if len(alice_key) > 0 else 0
    
    # 6. Privacy Amplification (Simplified)
    # Reducing key size to improve security if QBER is low
    final_key_len = 0
    if qber < 20:
        final_key_len = int(len(alice_key) * (1 - 2 * (qber / 100))) # Very simple model
        final_key_len = max(0, final_key_len)

    return qber, len(alice_key), final_key_len

def run_comprehensive_analysis():
    n_simulations = 100
    n_bits = 2000
    noise_levels = [0.00, 0.05, 0.10, 0.15] # 0%, 5%, 10%, 15% noise
    
    results = {
        'noise': [],
        'qber_no_eve': [],
        'qber_with_eve': [],
        'key_len_no_eve': [],
        'key_len_with_eve': []
    }
    
    for nl in noise_levels:
        q_no_eve, q_with_eve = [], []
        k_no_eve, k_with_eve = [], []
        
        for _ in range(n_simulations):
            q_absent, _, k_absent = simulate_bb84_v2(n_bits, False, nl)
            q_present, _, k_present = simulate_bb84_v2(n_bits, True, nl)
            
            q_no_eve.append(q_absent)
            q_with_eve.append(q_present)
            k_no_eve.append(k_absent)
            k_with_eve.append(k_present)
            
        results['noise'].append(nl * 100)
        results['qber_no_eve'].append(np.mean(q_no_eve))
        results['qber_with_eve'].append(np.mean(q_with_eve))
        results['key_len_no_eve'].append(np.mean(k_no_eve))
        results['key_len_with_eve'].append(np.mean(k_with_eve))

    # Visualization 1: QBER Comparison
    plt.figure(figsize=(12, 6))
    x = np.arange(len(noise_levels))
    width = 0.35
    
    plt.subplot(1, 2, 1)
    plt.bar(x - width/2, results['qber_no_eve'], width, label='Alice-Bob (No Eve)', color='#3498db')
    plt.bar(x + width/2, results['qber_with_eve'], width, label='Alice-Bob (With Eve)', color='#e67e22')
    plt.xlabel('Channel Noise Level (%)')
    plt.ylabel('Average QBER (%)')
    plt.title('QBER vs. Channel Noise & Eavesdropping')
    plt.xticks(x, [f"{n}%" for n in results['noise']])
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Visualization 2: Key Length after Privacy Amplification
    plt.subplot(1, 2, 2)
    plt.plot(results['noise'], results['key_len_no_eve'], 'o-', label='Secure Key (No Eve)', color='#2ecc71', linewidth=2)
    plt.plot(results['noise'], results['key_len_with_eve'], 'o-', label='Secure Key (With Eve)', color='#c0392b', linewidth=2)
    plt.xlabel('Channel Noise Level (%)')
    plt.ylabel('Final Key Length (Bits)')
    plt.title('Final Key Yield after Privacy Amplification')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('enhanced_qkd_analysis.png')
    print("Enhanced analysis graph saved as enhanced_qkd_analysis.png")
    
    # Save statistics for the report
    with open('enhanced_results.txt', 'w') as f:
        f.write("Noise % | QBER (No Eve) | QBER (With Eve) | Final Key (No Eve) | Final Key (With Eve)\n")
        f.write("-" * 80 + "\n")
        for i in range(len(noise_levels)):
            f.write(f"{results['noise'][i]:>7.1f}% | {results['qber_no_eve'][i]:>13.2f}% | {results['qber_with_eve'][i]:>15.2f}% | {results['key_len_no_eve'][i]:>18.0f} | {results['key_len_with_eve'][i]:>19.0f}\n")

if __name__ == "__main__":
    run_comprehensive_analysis()