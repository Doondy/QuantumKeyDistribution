import hashlib

def amplify_privacy(reconciled_key, qber):
    """
    Simulates simple Privacy Amplification:
    Alice and Bob use a hash function to transform the key into a shorter,
    more secure one, ensuring Eve has negligible knowledge.
    """
    # Use len() safely on the numpy array
    key_len = int(len(reconciled_key))
    if key_len == 0:
        return ""
        
    # Convert bit array to string for hashing
    key_str = "".join([str(int(b)) for b in reconciled_key])
    
    # Calculate target length (simplified bit pruning)
    reduction_factor = float(max(0.0, 1.0 - (qber / 20.0)))
    target_bits = int(key_len * reduction_factor)
    
    if target_bits <= 0:
        return ""
        
    # Use SHA-256 for the cryptographic compression
    hash_input = key_str.encode('utf-8')
    hash_obj = hashlib.sha256(hash_input)
    full_hex_hash = hash_obj.hexdigest()
    
    # Return first part of the hash as final secret bits
    # (hex characters represent 4 bits each)
    chars_to_keep = int(target_bits // 4)
    if chars_to_keep <= 0:
        return ""
        
    # Slicing the string hex hash
    return full_hex_hash[0:chars_to_keep]
