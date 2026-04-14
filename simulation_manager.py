import os

import matplotlib.pyplot as plt
import numpy as np

import protocols


def compare_protocols(protocol_list=['bb84'], n_bits=5000, noise_levels=[0.0, 0.05, 0.10, 0.15], n_sim=5, output_dir='.', output_prefix='full_protocol_analysis'):
    """
    Compares specified protocols for QBER and final key yield.
    Writes results to an output directory and returns the averaged data.
    """
    os.makedirs(output_dir, exist_ok=True)

    results = {'noise': noise_levels}
    for proto in protocol_list:
        results[f'{proto}_qber_no_eve'] = []
        results[f'{proto}_qber_with_eve'] = []
        results[f'{proto}_key_final_no_eve'] = []
        results[f'{proto}_key_final_with_eve'] = []

    for noise in noise_levels:
        for proto in protocol_list:
            q_0, q_1 = [], []
            kf_0, kf_1 = [], []

            for _ in range(n_sim):
                protocol_func = getattr(protocols, f'{proto}_protocol')
                q, sifted, final = protocol_func(n_bits, False, noise)
                q_0.append(q)
                kf_0.append(final)

                q, sifted, final = protocol_func(n_bits, True, noise)
                q_1.append(q)
                kf_1.append(final)

            results[f'{proto}_qber_no_eve'].append(np.mean(q_0))
            results[f'{proto}_qber_with_eve'].append(np.mean(q_1))
            results[f'{proto}_key_final_no_eve'].append(np.mean(kf_0))
            results[f'{proto}_key_final_with_eve'].append(np.mean(kf_1))

    # Visualization: Compare QBER and Final Key for each protocol
    n_protocols = len(protocol_list)
    plt.figure(figsize=(14, 7 * n_protocols))
    x = np.array([n * 100 for n in noise_levels])

    for idx, proto in enumerate(protocol_list):
        plt.subplot(n_protocols, 2, 2 * idx + 1)
        plt.plot(x, results[f'{proto}_qber_no_eve'], 'o-', label='QBER No Eve', color='#3498db', linewidth=2)
        plt.plot(x, results[f'{proto}_qber_with_eve'], 's--', label='QBER With Eve', color='#e67e22', linewidth=2)
        plt.xlabel('Noise Level (%)')
        plt.ylabel('Average QBER (%)')
        plt.title(f'{proto.upper()}: QBER vs Noise')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)

        plt.subplot(n_protocols, 2, 2 * idx + 2)
        plt.bar(x - 2, results[f'{proto}_key_final_no_eve'], 4, label='Final Key (No Eve)', color='#2ecc71')
        plt.bar(x + 2, results[f'{proto}_key_final_with_eve'], 4, label='Final Key (With Eve)', color='#c0392b')
        plt.xlabel('Noise Level (%)')
        plt.ylabel('Final Secret Key Length (Bits)')
        plt.title(f'{proto.upper()}: Final Secure Key Yield')
        plt.legend()
        plt.grid(True, axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    image_path = os.path.join(output_dir, f'{output_prefix}.png')
    plt.savefig(image_path)
    print(f"Full analysis plot saved as {image_path}")

    summary_path = os.path.join(output_dir, f'{output_prefix}.txt')
    with open(summary_path, 'w') as f:
        f.write("Full QKD Simulation Summary (Post-Processing Included)\n")
        f.write("=" * 60 + "\n")
        for proto in protocol_list:
            f.write(f"\n{proto.upper()} Protocol:\n")
            f.write("Noise % | QBER (No Eve) | Final Key (No Eve) | QBER (With Eve) | Final Key (With Eve)\n")
            f.write("-" * 80 + "\n")
            for i, nl in enumerate(noise_levels):
                f.write(
                    f"{nl*100:6.1f}% | {results[f'{proto}_qber_no_eve'][i]:13.2f}% | {results[f'{proto}_key_final_no_eve'][i]:18.1f} | {results[f'{proto}_qber_with_eve'][i]:13.2f}% | {results[f'{proto}_key_final_with_eve'][i]:19.1f}\n"
                )

    return results


if __name__ == "__main__":
    compare_protocols()
