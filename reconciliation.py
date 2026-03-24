import numpy as np

def simple_parity_check(alice_key, bob_key, block_size=10):
    """
    Simulates a basic Reconciliation step:
    Alice and Bob divide keys into blocks and compare parities.
    Blocks with mismatched parities are discarded (simplest form).
    """
    if len(alice_key) == 0:
        return np.array([]), np.array([])
        
    n_blocks = len(alice_key) // block_size
    alice_reconciled = []
    bob_reconciled = []
    
    for i in range(n_blocks):
        start = i * block_size
        end = (i + 1) * block_size
        
        block_alice = alice_key[start:end]
        block_bob = bob_key[start:end]
        
        # Parity calculation (XOR of all bits)
        parity_alice = np.sum(block_alice) % 2
        parity_bob = np.sum(block_bob) % 2
        
        if parity_alice == parity_bob:
            # Block is likely correct, keep it
            alice_reconciled.extend(block_alice)
            bob_reconciled.extend(block_bob)
        else:
            # Error detected in block, discard in this simple version
            # Real Cascade would recursive split, but we'll prune it.
            pass
            
    return np.array(alice_reconciled), np.array(bob_reconciled)
