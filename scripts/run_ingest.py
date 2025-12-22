"""Simple CLI to run the ingest pipeline on a CSV file."""
import argparse

from ingest import process_file


def main():
    p = argparse.ArgumentParser(description="Run ingest pipeline for telemetry CSVs")
    p.add_argument("input", help="Input CSV file")
    p.add_argument("--output", "-o", help="Output cleaned CSV path (optional)")
    p.add_argument("--method", "-m", choices=["zscore", "minmax"], default="zscore", help="Normalization method")
    args = p.parse_args()

    out = process_file(args.input, output_path=args.output, normalize_method=args.method)
    print(f"Ingest complete. Output: {out}")


if __name__ == "__main__":
    main()
