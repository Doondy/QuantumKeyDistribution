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
            pass

    return np.array(alice_reconciled), np.array(bob_reconciled)


def _cascade_correct_block(alice_block, bob_block):
    """Recursively locate and correct single-bit differences using parity splits."""
    if len(alice_block) == 0:
        return np.array([]), np.array([])

    parity_alice = np.sum(alice_block) % 2
    parity_bob = np.sum(bob_block) % 2

    if parity_alice == parity_bob:
        return alice_block, bob_block

    if len(alice_block) == 1:
        return alice_block, alice_block

    mid = len(alice_block) // 2
    left_alice, left_bob = _cascade_correct_block(alice_block[:mid], bob_block[:mid])
    right_alice, right_bob = _cascade_correct_block(alice_block[mid:], bob_block[mid:])

    return np.concatenate((left_alice, right_alice)), np.concatenate((left_bob, right_bob))


def cascade_reconciliation(alice_key, bob_key, block_size=10):
    """
    Performs an enhanced reconciliation step by checking block parities and
    recursively locating mismatches within blocks that fail a parity check.
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

        reconciled_alice, reconciled_bob = _cascade_correct_block(block_alice, block_bob)
        alice_reconciled.extend(reconciled_alice)
        bob_reconciled.extend(reconciled_bob)

    return np.array(alice_reconciled), np.array(bob_reconciled)
