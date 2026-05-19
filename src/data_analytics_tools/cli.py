"""Command-line interface for DataAnalyticsTools.

Usage examples
--------------
    dat summary data.csv
    dat histogram-dates dates.txt --save chart.png
    dat histogram-weekdays days.txt
    dat graph data.csv --sep " " --title "Revenue"
    dat bootstrap '[1,2,3,4,5]' --n 500
    dat normal --mean 10 --std 2 --n 200
    dat tokenize '["alice","bob","carol"]' --method token
"""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np
import pandas as pd


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dat",
        description="DataAnalyticsTools — data cleanup, generation & visualisation from the CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── summary ─────────────────────────────────
    p = sub.add_parser("summary", help="Print six-number summary of a CSV column")
    p.add_argument("file", help="CSV file path")
    p.add_argument("--col", default=None, help="Column name (default: first numeric)")
    p.add_argument("--sep", default=",", help="Delimiter")

    # ── histogram-dates ─────────────────────────
    p = sub.add_parser("histogram-dates", help="Bar chart of date frequencies")
    p.add_argument("file", help="Text file with one date per line")
    p.add_argument("--fmt", default="%Y%m%d", help="Date format")
    p.add_argument("--save", default=None, help="Save image path")

    # ── histogram-weekdays ──────────────────────
    p = sub.add_parser("histogram-weekdays", help="Bar chart of weekday frequencies")
    p.add_argument("file", help="Text file with one weekday per line")
    p.add_argument("--save", default=None, help="Save image path")

    # ── graph ───────────────────────────────────
    p = sub.add_parser("graph", help="Line chart from a two-column file")
    p.add_argument("file", help="CSV file with X Y columns")
    p.add_argument("--sep", default=" ")
    p.add_argument("--title", default="Graph")
    p.add_argument("--save", default=None, help="Save image path")

    # ── bootstrap ───────────────────────────────
    p = sub.add_parser("bootstrap", help="Bootstrap resample from a JSON array")
    p.add_argument("data", help="JSON array of numbers")
    p.add_argument("--n", type=int, default=1000, help="Number of samples")
    p.add_argument("--seed", type=int, default=None)

    # ── normal ──────────────────────────────────
    p = sub.add_parser("normal", help="Generate normally distributed data")
    p.add_argument("--mean", type=float, default=0.0)
    p.add_argument("--std", type=float, default=1.0)
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--seed", type=int, default=None)

    # ── tokenize ────────────────────────────────
    p = sub.add_parser("tokenize", help="Tokenize a JSON array of strings")
    p.add_argument("data", help="JSON array of unique strings")
    p.add_argument("--method", choices=["token", "hash"], default="token")

    return parser


def main(argv: list[str] | None = None) -> int:  # noqa: C901
    """Entry point. Returns 0 on success, 1 on error."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "summary":
            from data_analytics_tools.generate.summary import summary
            df = pd.read_csv(args.file, sep=args.sep)
            col = args.col or df.select_dtypes("number").columns[0]
            result = summary(df[col])
            for k, v in result.items():
                print(f"{k:>8s}: {v:.4f}")

        elif args.command == "histogram-dates":
            from data_analytics_tools.visualize.histograms import plot_date_histogram
            from pathlib import Path
            lines = Path(args.file).read_text().strip().splitlines()
            fig = plot_date_histogram(lines, args.fmt, save_path=args.save)
            if not args.save:
                import matplotlib.pyplot as plt
                plt.show()

        elif args.command == "histogram-weekdays":
            from data_analytics_tools.visualize.histograms import plot_weekday_histogram
            from pathlib import Path
            lines = Path(args.file).read_text().strip().splitlines()
            fig = plot_weekday_histogram(lines, save_path=args.save)
            if not args.save:
                import matplotlib.pyplot as plt
                plt.show()

        elif args.command == "graph":
            from data_analytics_tools.visualize.graphs import plot_from_csv
            fig = plot_from_csv(args.file, sep=args.sep, title=args.title, save_path=args.save)
            if not args.save:
                import matplotlib.pyplot as plt
                plt.show()

        elif args.command == "bootstrap":
            from data_analytics_tools.generate.distributions import bootstrap
            data = json.loads(args.data)
            result = bootstrap(data, args.n, seed=args.seed)
            print(json.dumps(result.tolist()))

        elif args.command == "normal":
            from data_analytics_tools.generate.distributions import generate_normal
            result = generate_normal(args.mean, args.std, args.n, seed=args.seed)
            print(json.dumps(result.tolist()))

        elif args.command == "tokenize":
            from data_analytics_tools.cleanup.tokenizer import tokenize_array
            data = json.loads(args.data)
            result = tokenize_array(data, args.method)
            print(json.dumps(result))

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
