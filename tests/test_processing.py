import numpy as np
from reconciliation import cascade_reconciliation, simple_parity_check
from privacy_amplification import amplify_privacy


def test_cascade_reconciliation_corrects_single_error():
    alice = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0])
    bob = alice.copy()
    bob[3] = 1 - bob[3]

    alice_recon, bob_recon = cascade_reconciliation(alice, bob, block_size=10)
    assert np.array_equal(alice_recon, bob_recon)
    assert np.array_equal(alice_recon, alice)


def test_simple_parity_check_discards_bad_blocks():
    alice = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    bob = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    alice_recon, bob_recon = simple_parity_check(alice, bob, block_size=10)
    assert len(alice_recon) == 0
    assert len(bob_recon) == 0


def test_simple_parity_check_keeps_matching_blocks():
    alice = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1])
    bob = alice.copy()
    alice_recon, bob_recon = simple_parity_check(alice, bob, block_size=10)
    assert np.array_equal(alice_recon, alice)
    assert np.array_equal(bob_recon, bob)


def test_amplify_privacy_produces_shorter_key_with_noise():
    key = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    result = amplify_privacy(key, qber=10.0)
    assert isinstance(result, str)
    assert len(result) <= len(key) // 4


def test_amplify_privacy_returns_empty_for_full_error():
    key = np.array([1, 1, 1, 1])
    result = amplify_privacy(key, qber=100.0)
    assert result == ''
