import numpy as np

def simulate_bb84_detailed(n_bits=20, eve_present=False, noise_level=0.0):
    """
    Returns a list of steps for BB84 visualization.
    """
    # Alice's random bits and bases
    alice_bits = np.random.randint(2, size=n_bits).tolist()
    alice_bases = np.random.randint(2, size=n_bits).tolist() # 0: rectilinear (+), 1: diagonal (x)
    
    steps = []
    
    # Photons sent to Bob
    current_qubits = list(alice_bits)
    
    # 1. Alice sends Photons
    steps.append({
        "step": "alice_sent",
        "data": {
            "bits": alice_bits,
            "bases": alice_bases
        }
    })

    # 2. Eavesdropping (Optional)
    eve_bases = []
    eve_bits = []
    if eve_present:
        eve_bases = np.random.randint(2, size=n_bits).tolist()
        for i in range(n_bits):
            if alice_bases[i] == eve_bases[i]:
                eve_bits.append(current_qubits[i])
            else:
                eve_bits.append(np.random.randint(2))
        current_qubits = list(eve_bits) 
        steps.append({
            "step": "eve_intercepted",
            "data": {
                "bases": eve_bases,
                "bits": eve_bits
            }
        })

    # 3. Channel Noise (Bit Flips)
    noise_indices = []
    for i in range(n_bits):
        if np.random.random() < noise_level:
            current_qubits[i] = 1 - current_qubits[i]
            noise_indices.append(i)
    
    if noise_indices:
        steps.append({
            "step": "channel_noise",
            "data": {
                "noise_indices": noise_indices,
                "qubits": current_qubits
            }
        })

    # 4. Bob's Measurement
    bob_bases = np.random.randint(2, size=n_bits).tolist()
    bob_results = []
    for i in range(n_bits):
        # We model the measurement result based on the current photon state
        # If Bob's basis matches Alice's (and no disturbance occurred)
        # However, for the simulation to be consistent with the logic in bb84.py:
        # Actually, if Bob measures in basis B, and state was prepared in basis A:
        # if A == B, result is state. if A != B, result is random.
        
        # Here we just use the current state from the channel:
        if bob_bases[i] == alice_bases[i]:
             # If Eve was present and changed basis, the state might have been randomized
             # But current_qubits[i] already reflects Eve's result.
             # So if Bob measures in same basis as Alice, he gets what's in the channel (unless Eve changed it)
             # Wait, the logic in simulate_bb84_v2 is a bit more manual.
             # Let's keep it simple: if Bob basis == Alice basis, he gets qubits[i]
             # EXCEPT if Eve changed the basis.
             if eve_present and alice_bases[i] != eve_bases[i]:
                  bob_results.append(np.random.randint(2))
             else:
                  bob_results.append(current_qubits[i])
        else:
            bob_results.append(np.random.randint(2))
    
    steps.append({
        "step": "bob_measured",
        "data": {
            "bases": bob_bases,
            "results": bob_results
        }
    })

    # 5. Sifting (Public Discussion)
    sifted_indices = [i for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    alice_sifted = [alice_bits[i] for i in sifted_indices]
    bob_sifted = [bob_results[i] for i in sifted_indices]
    
    steps.append({
        "step": "sifting",
        "data": {
            "indices": sifted_indices,
            "alice_key": alice_sifted,
            "bob_key": bob_sifted
        }
    })

    # 6. Final Results
    errors = sum(1 for i in range(len(alice_sifted)) if alice_sifted[i] != bob_sifted[i])
    qber = (errors / len(alice_sifted)) * 100 if len(alice_sifted) > 0 else 0
    
    steps.append({
        "step": "results",
        "data": {
            "qber": qber,
            "mismatches": [sifted_indices[i] for i in range(len(alice_sifted)) if alice_sifted[i] != bob_sifted[i]]
        }
    })

    return steps
