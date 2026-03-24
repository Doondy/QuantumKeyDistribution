import numpy as np
import qkd_core as core

import reconciliation
import privacy_amplification

def bb84_protocol(n_bits=100, eve_present=False, noise_level=0.0, apply_processing=True):
    alice = core.Alice(n_bits)
    bob = core.Bob(n_bits)
    channel = core.QuantumChannel(noise_level)
    
    # Alice prepares states
    alice_bits, alice_bases = alice.prepare_qubits()
    
    # Optional Eavesdropping
    bits_sent = alice_bits
    bases_sent = alice_bases
    if eve_present:
        eve = core.Eve(n_bits)
        bits_sent, bases_sent = eve.intercept(alice_bits, alice_bases)
    
    # Channel transmission
    noisy_bits = channel.transmit(bits_sent)
    
    # Bob measures
    bob_results = []
    for i in range(n_bits):
        if bob.bases[i] == bases_sent[i]:
            bob_results.append(noisy_bits[i])
        else:
            bob_results.append(np.random.randint(2))
    
    bob_results = np.array(bob_results)
    
    # Sifting: Keep bits where Alice and Bob's bases match
    sifted_indices = np.where(alice_bases == bob.bases)[0]
    alice_sifted = alice_bits[sifted_indices]
    bob_sifted = bob_results[sifted_indices]
    
    # QBER Calculation (on the sifted key)
    errors = np.sum(alice_sifted != bob_sifted)
    qber = (errors / len(alice_sifted)) * 100 if len(alice_sifted) > 0 else 0
    final_key_len = 0
    
    # Post-Processing
    if apply_processing and len(alice_sifted) > 0:
        # Reconciliation: Bob and Alice agree on a key
        alice_recon, bob_recon = reconciliation.simple_parity_check(alice_sifted, bob_sifted)
        
        # Privacy Amplification: Secure the key based on QBER
        final_key = privacy_amplification.amplify_privacy(alice_recon, qber)
        final_key_len = len(final_key) * 4 # Convert hex characters back to bit equivalent
        
    return qber, len(alice_sifted), final_key_len

def b92_protocol(n_bits=100, eve_present=False, noise_level=0.0):
    """
    B92 Protocol implementation:
    Alice prepares either |0> (Basis 0, State 0) or |45> (Basis 1, State 0).
    """
    # 1. Alice prepares her key (which determines her basis)
    alice_key_bits = np.random.randint(2, size=n_bits) 
    alice_bases = alice_key_bits.copy() 
    
    # 2. Physics: Alice always sends the "0" state of her chosen basis
    # qubits[i] represents whether the state is the "0" or "1" state of its current basis
    qubits = np.zeros(n_bits, dtype=int) 
    bases_sent = alice_bases
    
    if eve_present:
        # Eve measures Alice's states in random bases
        eve_bases = np.random.randint(2, size=n_bits)
        eve_results = []
        for i in range(n_bits):
            if eve_bases[i] == bases_sent[i]:
                # Eve used correct basis, she gets "0" (unless noise, handled later)
                eve_results.append(0)
            else:
                # Eve used wrong basis, 50/50 chance of getting "0" or "1"
                eve_results.append(np.random.randint(2))
        qubits = np.array(eve_results)
        bases_sent = eve_bases

    # 3. Channel Noise (Bit flips in the current basis)
    for i in range(n_bits):
        if np.random.random() < noise_level:
            qubits[i] = 1 - qubits[i]

    # 4. Bob's Measurement
    bob_bases = np.random.randint(2, size=n_bits)
    bob_results = []
    success_indices = []
    
    for i in range(n_bits):
        measurement = -1
        if bob_bases[i] == bases_sent[i]:
            # Consistent basis with whatever is arriving
            measurement = qubits[i]
        else:
            # Inconsistent basis, 50/50 chance
            # But wait, if qubits[i] was 0 in the previous basis, 
            # then in the new basis it's a superposition, so 50/50.
            # If qubits[i] was 1, it's also a superposition.
            measurement = np.random.randint(2)
            
        # Detect event: Bob got '1'
        if measurement == 1:
            # Bob knows Alice's basis MUST have been the opposite of his
            # (Because if Alice used his basis, he would have measured '0' - ignoring noise)
            bob_results.append(1 - bob_bases[i])
            success_indices.append(i)
    
    if not success_indices:
        return 0.0, 0
        
    alice_key = alice_key_bits[success_indices]
    bob_key = np.array(bob_results)
    
    errors = np.sum(alice_key != bob_key)
    qber = (errors / len(alice_key)) * 100
    
    return qber, len(alice_key)
