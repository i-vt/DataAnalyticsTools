"""Generate sub-package: statistical summaries and synthetic data."""

from .distributions import bootstrap, generate_normal
from .summary import summary, summary_with_correlation

__all__ = [
    "bootstrap",
    "generate_normal",
    "summary",
    "summary_with_correlation",
]
