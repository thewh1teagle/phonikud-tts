FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["uv", "run", "app.py", '--host', '0.0.0.0', '--port', '7860']
