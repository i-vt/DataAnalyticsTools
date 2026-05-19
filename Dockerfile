# ============================================
# DataAnalyticsTools — multi-stage Docker build
# ============================================

# ---------- Stage 1: build ----------
FROM python:3.12-slim AS builder

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir build \
    && python -m build --wheel --outdir /dist

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim AS runtime

LABEL maintainer="DataAnalyticsTools Contributors"
LABEL description="Data cleanup, generation & visualization toolkit"

# Non-interactive matplotlib backend
ENV MPLBACKEND=Agg
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN groupadd --gid 1000 dat \
    && useradd --uid 1000 --gid dat --create-home dat

WORKDIR /app

# Install the wheel from builder stage
COPY --from=builder /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

# Default data mount point
VOLUME ["/data"]

USER dat

ENTRYPOINT ["dat"]
CMD ["--help"]
