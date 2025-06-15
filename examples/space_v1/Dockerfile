FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

RUN useradd -m -u 1000 user

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use system Python environment (recommended for containers)
ENV UV_SYSTEM_PYTHON=1

COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

COPY . .

# Setup user
RUN chown -R user:user /app
USER user
ENV HOME=/app

EXPOSE 7860
CMD ["uv", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]