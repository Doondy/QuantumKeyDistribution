import numpy as np

class QuantumState:
    """Representation of a single qubit state in BB84 bases."""
    RECTILINEAR = 0  # + basis: 0 -> |0>, 1 -> |90>
    DIAGONAL = 1     # x basis: 0 -> |45>, 1 -> |135>

class Alice:
    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.bits = np.random.randint(2, size=n_bits)
        self.bases = np.random.randint(2, size=n_bits)

    def prepare_qubits(self):
        """Alice prepares qubits based on her bits and bases."""
        return self.bits, self.bases

class Bob:
    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.bases = np.random.randint(2, size=n_bits)

    def measure(self, qubits, channel_bases):
        """
        Bob measures the incoming qubits using his chosen bases.
        If bases match Alice's (or Eve's disturbance), he gets the bit.
        If not, 50% chance of 0 or 1.
        """
        results = []
        for i in range(len(qubits)):
            if self.bases[i] == channel_bases[i]:
                results.append(qubits[i])
            else:
                results.append(np.random.randint(2))
        return np.array(results)

class Eve:
    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.bases = np.random.randint(2, size=n_bits)

    def intercept(self, bits, bases):
        """Eve intercepts Alice's transmission and measures it."""
        intercepted_bits = []
        for i in range(len(bits)):
            if self.bases[i] == bases[i]:
                intercepted_bits.append(bits[i]) # Correctly measured
            else:
                intercepted_bits.append(np.random.randint(2)) # Disturbed
        return np.array(intercepted_bits), self.bases # Re-sending her measurements in her bases

class QuantumChannel:
    def __init__(self, noise_level=0.0):
        self.noise_level = noise_level

    def transmit(self, bits):
        """Simulate channel noise: random bit flips."""
        noisy_bits = np.copy(bits)
        for i in range(len(noisy_bits)):
            if np.random.random() < self.noise_level:
                noisy_bits[i] = 1 - noisy_bits[i]
        return noisy_bits
