# QKD (Quantum Key Distribution) Project - Comprehensive Code Analysis

## Project Overview
This is an advanced Quantum Key Distribution (QKD) simulation project that implements and compares cryptographic quantum protocols (BB84 and B92) with security analysis under various noise and eavesdropping scenarios.

---

## 📁 File Structure & Component Analysis

### 1. **qkd_core.py** - Core Quantum Simulation Framework
**Purpose:** Foundation classes for quantum state representation and protocol participants

**Key Classes:**
- **QuantumState**: Enum-like class defining quantum bases
  - `RECTILINEAR (0)`: + basis (0→|0⟩, 1→|90°⟩)
  - `DIAGONAL (1)`: × basis (0→|45°⟩, 1→|135°⟩)

- **Alice**: Sender (n_bits)
  - Generates random bits and bases
  - `prepare_qubits()`: Returns bits and bases for transmission
  - **Role**: Generates the quantum states to send

- **Bob**: Receiver (n_bits)
  - Generates random measurement bases
  - `measure()`: Measures incoming qubits with his bases
  - **Quantum mechanics**: If Bob's basis matches, he gets correct bit; otherwise 50% random
  - **Role**: Measures received qubits and generates received bits

- **Eve**: Eavesdropper (n_bits)
  - Intercepts Alice's transmission
  - `intercept()`: Measures with random bases and re-sends
  - **Impact on security**: Introduces detectable errors (QBER) when detected

- **QuantumChannel**: Network simulation (noise_level parameter)
  - `transmit()`: Simulates bit-flip errors during transmission
  - **Noise model**: Random flips at rate = noise_level
  - **Impact**: Degrades signal quality, increases QBER

**Data Flow:**
```
Alice generates random bits/bases 
  → QuantumChannel transmission (with noise)
  → Optional Eve eavesdropping (with basis mismatch detection)
  → Bob measures with random bases
  → Basis comparison (sifting)
```

---

### 2. **reconciliation.py** - Error Correction Layer
**Purpose:** Reconcile differences between Alice and Bob's keys after eavesdropping/noise detection

**Key Function:** `simple_parity_check(alice_key, bob_key, block_size=10)`
- Divides key into blocks of size 10 bits
- Calculates parity (XOR) of each block
- **Keeps blocks** where parities match (likely error-free)
- **Discards blocks** where parities differ (contain errors)

**Algorithm Details:**
```
For each block:
  parity_alice = (bit0 XOR bit1 XOR ... XOR bit9) mod 2
  parity_bob = (bit0 XOR bit1 XOR ... XOR bit9) mod 2
  
  If parity_alice == parity_bob:
    Keep block (both agree on error check)
  Else:
    Discard block (detected error)
```

**Output Impact:** Reduces key length but ensures better agreement

---

### 3. **privacy_amplification.py** - Cryptographic Key Compression
**Purpose:** Transform sifted key into shorter, more secure final key using cryptographic hashing

**Key Function:** `amplify_privacy(reconciled_key, qber)`

**Algorithm:**
1. Converts bit array to binary string
2. Calculates reduction factor based on QBER:
   - `reduction_factor = max(0, 1.0 - qber/20.0)`
   - Higher QBER → more aggressive reduction
3. Applies SHA-256 hash to key string
4. Extracts hexadecimal hash (each hex char = 4 bits)
5. Keeps only `target_bits/4` hex characters

**Formula:**
```
target_bits = original_key_length × (1 - QBER/20)
final_key_length = target_bits / 4  (in hex chars)
```

**Security Principle:** Even if Eve has partial information, hash provides exponential confusion

---

### 4. **bb84.py** - Basic BB84 Protocol Analysis
**Purpose:** Implements enhanced BB84 simulation with detailed statistics collection

**Key Function:** `simulate_bb84_v2(n_bits=1000, eve_present=False, noise_level=0.02)`

**Protocol Steps:**
1. Alice generates random bits and bases
2. Eve (optional): Intercepts and re-sends in her own bases
3. Channel: Applies noise (bit flips)
4. Bob: Measures in random bases
5. Sifting: Keeps only bits where Alice & Bob used same basis
6. QBER Calculation: Error rate = errors / sifted_key_length × 100%
7. Privacy Amplification: Secure final key based on QBER

**QBER Interpretation:**
- QBER < 1%: Likely no eavesdropping (quantum channel assumed)
- QBER ≈ 25%: Eve definitely present (for each mismatch, 50% error)
- QBER > 10%: Threshold to detect eavesdropping

**Output Metrics:**
- `qber`: Quantum Bit Error Rate (%)
- `len(alice_key_sifted)`: Usable key length after basis sifting
- `final_key_len`: Secure key length after privacy amplification

---

### 5. **protocols.py** - Protocol Implementations
**Purpose:** Full implementations of BB84 and B92 protocols with post-processing

#### **BB84 Protocol** `bb84_protocol(n_bits=100, eve_present, noise_level, apply_processing)`

**Steps:**
1. Alice prepares random bits/bases
2. Eve eavesdropping (optional): Measures and disturbs
3. Channel transmission with noise
4. Bob measures with random bases
5. **Sifting**: Keep indices where `alice_bases == bob.bases`
6. **Reconciliation**: Apply parity check error correction
7. **Privacy Amplification**: Compress key securely
8. Return: (QBER, sifted_key_length, final_key_length)

#### **B92 Protocol** `b92_protocol(n_bits=100, eve_present, noise_level)`

**Differences from BB84:**
- Alice always sends "0" state of her chosen basis
- Bob detection: Success only when he gets a "1" (unexpected result)
- Fewer bits pass through to sifting
- More robust to certain eavesdropping patterns

---

### 6. **simulation_manager.py** - Comparative Analysis Runner
**Purpose:** Execute comprehensive simulations comparing protocols over multiple scenarios

**Key Function:** `compare_protocols(n_bits=5000, noise_levels=[0.0, 0.05, 0.10, 0.15])`

**Simulation Parameters:**
- **n_bits**: 5000 bits per run
- **n_sim**: 50 simulations per noise level for averaging
- **noise_levels**: [0%, 5%, 10%, 15%]
- **Eve scenarios**: Present vs. Absent

**Analysis Metrics Collected:**
```
For each noise level:
  - BB84 QBER (no eavesdropping)
  - BB84 QBER (with eavesdropping)
  - BB84 Final Key Length (no eavesdropping)
  - BB84 Final Key Length (with eavesdropping)
```

**Outputs Generated:**
1. **full_protocol_analysis.png**: Visualization with 2 subplots
   - Left: QBER vs Noise Level (line plot)
   - Right: Final Key Length vs Noise Level (bar chart)
2. **full_analysis_summary.txt**: Tabular statistics

---

### 7. **main.py** - Entry Point
**Purpose:** Execute full analysis and display results

**Execution Flow:**
```python
run_project()
  ├─ Call simulation_manager.compare_protocols()
  │  ├─ Run 50 simulations × 4 noise levels
  │  ├─ Generate visualization png
  │  └─ Write summary txt
  └─ Read and print full_analysis_summary.txt
```

---

## 📊 Expected Output Analytics

### Quantitative Metrics

#### **QBER Analysis**
| Scenario | Expected QBER | Interpretation |
|----------|---------------|-----------------|
| No Eve, 0% Noise | 0.0-0.5% | Quantum channel working perfectly |
| No Eve, 5% Noise | 4.5-5.5% | Noise rate dominates |
| With Eve, 0% Noise | 20-25% | Eve introduces detectable errors |
| With Eve, 5% Noise | 23-27% | Combined Eve + noise |

#### **Key Length Impact**
- **Sifted Key**: ~50% of original (only matching bases kept)
- **Reconciled Key**: ~90% of sifted (parity check removes ~10%)
- **Final Key**: ~30-50% of reconciled (privacy amplification compression)

**Example:**
```
n_bits = 5000
Sifted (50% same bases) ≈ 2500 bits
Reconciled (90% parity pass) ≈ 2250 bits
Final (privacy amplication, QBER=5%) ≈ 1000-1500 bits (after compression)
```

#### **Privacy Amplification Formula**
```
For QBER = 5%:
  reduction_factor = 1 - 5/20 = 0.75
  target_bits = 2250 × 0.75 = 1687.5
  final_key_chars = 1687.5 / 4 ≈ 421 hex chars = 1684 bits
```

---

## 🔐 Security Analysis

### Detection Capabilities
1. **Eavesdropping Detection**: QBER threshold = 11% (tunable)
   - If QBER > threshold → Assume Eve present → Abort protocol
   - If QBER < threshold → Proceed with key generation

2. **Privacy Level**: 
   - After amplification, Eve's information → < 2^(-k) for k-bit key
   - Shannon entropy ≈ log₂(final_key_length) bits of security

### Threat Model Covered
- ✅ Passive eavesdropping (Eve measures and re-sends)
- ✅ Channel noise (realistic quantum channels)
- ✅ Basis mismatch detection
- ✅ Error reconciliation
- ✅ Privacy amplification

---

## 📈 Code Quality Metrics

### Modularity
- **5 core modules**: qkd_core, protocols, reconciliation, privacy_amplification, simulation_manager
- **Clear separation of concerns**: Physics simulation, protocol logic, post-processing
- **Reusability**: Functions easily configurable with parameters

### Computational Complexity
- **Per run**: O(n) where n = number of bits (linear in each component)
- **Total simulation**: O(n × n_sim × len(noise_levels)) = O(5000 × 50 × 4) = 1M operations

### Dependencies
- **numpy**: Array operations and random number generation
- **matplotlib**: Visualization of results
- **hashlib**: Cryptographic hashing (SHA-256)

---

## 🎯 Key Findings from Analysis

1. **Noise Dominates QBER**: Channel noise is the primary source of errors
2. **Eve Detection Effective**: Eavesdropping introduces ≈20-25% QBER, easily detected
3. **Key Yield Trade-off**: Better privacy (more amplification) = shorter final key
4. **Protocol Robustness**: BB84 stable across noise levels; effectiveness depends on threshold tuning

---

## Summary

This QKD project is a **production-quality educational simulator** that:
- ✅ Implements real quantum cryptography protocols
- ✅ Analyzes security under realistic attack scenarios
- ✅ Provides statistical evidence of protocol effectiveness
- ✅ Generates visual comparisons and detailed reports
- ✅ Shows practical key generation rates and security bounds
