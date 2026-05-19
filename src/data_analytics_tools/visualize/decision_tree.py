"""Decision-tree trainer and visualiser from CSV data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

matplotlib.use("Agg")


@dataclass
class TreeResult:
    """Result of training a decision tree on one target column."""
    target: str
    accuracy: float
    model: DecisionTreeClassifier
    figure: Optional[plt.Figure] = None


def train_trees(
    csv_path: str | Path,
    *,
    delimiter: str = "|",
    drop_columns: Optional[Sequence[str]] = None,
    test_size: float = 0.2,
    random_state: int = 42,
    save_dir: Optional[str | Path] = None,
    figsize: tuple[int, int] = (20, 12),
    dpi: int = 150,
) -> List[TreeResult]:
    """Train a decision tree for every remaining column as the target.

    Parameters
    ----------
    csv_path:
        Path to a delimited file.
    delimiter:
        Column separator.
    drop_columns:
        Columns to exclude from both features and targets.
    test_size:
        Fraction of data reserved for testing.
    random_state:
        Seed for reproducibility.
    save_dir:
        If set, save each tree visualisation as a PNG in this directory.
    figsize:
        Figure dimensions per tree.
    dpi:
        Image resolution.

    Returns
    -------
    list[TreeResult]
    """
    df = pd.read_csv(csv_path, delimiter=delimiter)
    if drop_columns:
        df = df.drop(columns=[c for c in drop_columns if c in df.columns])

    columns = list(df.columns)
    results: List[TreeResult] = []

    for target in columns:
        features = [c for c in columns if c != target]
        X = df[features]
        y = df[target]
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state,
            )
            clf = DecisionTreeClassifier(random_state=random_state)
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_test, y_test)

            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
            plot_tree(clf, filled=True, feature_names=features, ax=ax)
            ax.set_title(f"Decision Tree: {target!r} (accuracy {accuracy:.2%})")
            fig.tight_layout()

            if save_dir:
                Path(save_dir).mkdir(parents=True, exist_ok=True)
                fig.savefig(str(Path(save_dir) / f"tree_{target}.png"), dpi=dpi)

            results.append(TreeResult(target, accuracy, clf, fig))
        except Exception:
            # Some columns may not be suitable targets — skip them.
            continue

    return results
