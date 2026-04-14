import argparse
import os
import simulation_manager


def run_project(protocols, n_bits, noise_levels, n_sim, output_dir='.', output_prefix='full_protocol_analysis', display_summary=True):
    print("=" * 60)
    print("Welcome to the QKD Simulation Project (Advanced Analysis)")
    print("=" * 60)
    print(f"\nStarting comprehensive protocol comparison: {', '.join(protocols).upper()}...")

    results = simulation_manager.compare_protocols(
        protocols,
        n_bits,
        noise_levels,
        n_sim,
        output_dir=output_dir,
        output_prefix=output_prefix,
    )

    summary_path = os.path.join(output_dir, f"{output_prefix}.txt")
    image_path = os.path.join(output_dir, f"{output_prefix}.png")

    print("\nDONE: Full QKD analysis completed.")
    print(f"- Analysis graph: {image_path}")
    print(f"- Detailed stats: {summary_path}")

    if display_summary and os.path.exists(summary_path):
        with open(summary_path, 'r') as f:
            print("\n" + f.read())

    return results


def parse_args():
    parser = argparse.ArgumentParser(description="QKD Simulation Project")
    parser.add_argument('--protocols', nargs='+', default=['bb84'], choices=['bb84', 'b92', 'six_state'], help='Protocols to simulate')
    parser.add_argument('--n_bits', type=int, default=100, help='Number of bits per simulation')
    parser.add_argument('--noise_levels', nargs='+', type=float, default=[0.0, 0.1], help='Noise levels to test')
    parser.add_argument('--n_sim', type=int, default=5, help='Number of simulations per condition')
    parser.add_argument('--output-dir', type=str, default='.', help='Directory to write output files')
    parser.add_argument('--output-prefix', type=str, default='full_protocol_analysis', help='Filename prefix for output files')
    parser.add_argument('--no-summary', action='store_true', help='Do not print the text summary to the console')
    return parser.parse_args()


def main():
    args = parse_args()
    run_project(
        args.protocols,
        args.n_bits,
        args.noise_levels,
        args.n_sim,
        output_dir=args.output_dir,
        output_prefix=args.output_prefix,
        display_summary=not args.no_summary,
    )
if __name__ == "__main__":
    main()
