FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Create a non-root user
RUN useradd -m -u 1000 user

# Install git and clean up
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with proper cache directory
ENV UV_CACHE_DIR=/tmp/uv-cache
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to user
RUN chown -R user:user /app

# Switch to non-root user
USER user

# Set environment variables for runtime
ENV HOME=/app
ENV UV_CACHE_DIR=/tmp/uv-cache

EXPOSE 7860
CMD ["uv", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]