# DataAnalyticsTools

A production-grade Python toolkit for **data cleanup**, **synthetic data generation**, and **visualization** — packaged with a CLI, full test suite, and Docker support.

## Quick Start

```bash
# Install locally
pip install -e ".[dev]"

# Run the CLI
dat summary data/GraphFromCSV_TestData.csv --sep " "
dat histogram-dates data/mod_dates.txt --save chart.png
dat bootstrap '[1,2,3,4,5]' --n 500 --seed 42
dat normal --mean 10 --std 2 --n 200
dat tokenize '["alice","bob","carol"]' --method token
```

## Project Structure

```
DataAnalyticsTools/
├── src/data_analytics_tools/
│   ├── cleanup/          # Tokenisation, file-rename & organisation utils
│   │   ├── tokenizer.py
│   │   └── formatting.py
│   ├── generate/         # Statistical summaries & synthetic data
│   │   ├── summary.py
│   │   └── distributions.py
│   ├── visualize/        # Matplotlib charts & sklearn decision-tree plots
│   │   ├── histograms.py
│   │   ├── graphs.py
│   │   └── decision_tree.py
│   └── cli.py            # Unified CLI entry point (`dat`)
├── tests/                # 50+ pytest unit tests (>90% coverage)
├── data/                 # Sample data files
├── Dockerfile            # Multi-stage production image
├── Dockerfile.dev        # Dev/test image
├── docker-compose.yml    # Orchestration for app + test services
├── Makefile              # Common dev tasks
└── pyproject.toml        # PEP 621 metadata & tool config
```

## Docker

```bash
# Build production image
docker build -t data-analytics-tools .

# Run a CLI command
docker run --rm -v $(pwd)/data:/data data-analytics-tools summary /data/GraphFromCSV_TestData.csv --sep " "

# Run the test suite in a container
docker compose run --rm test
```

## Development

```bash
# Install in editable mode with dev extras
make dev

# Run tests
make test

# Run tests with coverage
make coverage

# Lint
make lint

# Type-check
make typecheck
```

## Python API

```python
from data_analytics_tools.generate import summary, bootstrap, generate_normal
from data_analytics_tools.cleanup import tokenize_array, str_to_sha512
from data_analytics_tools.visualize import plot_date_histogram, plot_xy, train_trees

# Six-number summary
summary([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# {'min': 1.0, 'q1': 3.25, 'median': 5.5, 'mean': 5.5, 'q3': 7.75, 'max': 10.0}

# Bootstrap resampling
samples = bootstrap([10, 20, 30, 40], n_samples=1000, seed=42)

# Normal distribution generation
data = generate_normal(mean=100, std=15, n_samples=5000, seed=0)

# Tokenize a list of strings
tokenize_array(["alice", "bob", "carol"], method="token")
# [('alice', 'a'), ('bob', 'b'), ('carol', 'c')]

# Plot and save
fig = plot_xy([1,2,3], [10,20,30], title="Revenue", save_path="revenue.png")
```

## What Changed from the Original

| Area | Before | After |
|---|---|---|
| **Structure** | Flat scripts with inline execution | PEP 621 package with `src/` layout |
| **Code quality** | Global state, mixed tabs/spaces, bare excepts, bugs | Type-hinted functions, dataclass results, proper error handling |
| **Testing** | Commented-out manual tests | 50+ pytest cases, >90% coverage |
| **CLI** | None | Unified `dat` command with sub-commands |
| **Docker** | None | Multi-stage prod image + dev/test image + Compose |
| **CI-ready** | No | Makefile targets for lint, typecheck, coverage |
| **Bug fixes** | `DecisionTreeClassifier` called instead of `plot_tree` | Fixed; proper `sklearn.tree.plot_tree` |

## License

MIT
