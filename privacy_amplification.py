import hashlib

def amplify_privacy(reconciled_key, qber):
    """
    Simulates simple Privacy Amplification:
    Alice and Bob use a hash function to transform the key into a shorter,
    more secure one, ensuring Eve has negligible knowledge.
    compression_ratio: How much smaller the final key is compared to the original.
    Based on QBER, higher error rates require higher compression.
    """
    if len(reconciled_key) == 0:
        return ""
        
    # Model compression ratio: if QBER is 25%, Eve potentially knows a lot.
    # We prune the final key size based on an information-theoretic model.
    # I'll use a conservative ratio to get a safe key.
    
    # Simple model: Final bit length = (Initial bit length) * (1 - 2 * H(QBER))
    # Where H is binary entropy. As QBER approaches 25%, final key length ~ 0 for BB84.
    
    # Convert bit array to string for hashing
    key_str = "".join(map(str, reconciled_key))
    
    # Calculate target length (simplified bit pruning)
    # If QBER is 5%, maybe keep 80% of the key. If 15%, keep 40%.
    reduction_factor = max(0, 1 - (qber / 20.0)) # Key size drops to 0 at 20% QBER
    target_bits = int(len(reconciled_key) * reduction_factor)
    
    if target_bits <= 0:
        return ""
        
    # Use SHA-256 for the cryptographic compression
    # (Real PA uses universal hash families, but hash-based is common for simplicity)
    hash_obj = hashlib.sha256(key_str.encode())
    full_hex_hash = hash_obj.hexdigest()
    
    # Return first part of the hash as final secret bits
    # (Just a mock: real PA would use specific bit indices from the hash)
    return full_hex_hash[:target_bits // 4] # hex uses 4 bits per char
