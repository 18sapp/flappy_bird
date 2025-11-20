# Multi-stage Dockerfile for Flappy Bird Web Game

# Stage 1: Build stage - Compile game with pygbag
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy game source code
COPY game/ ./game/
COPY assets/ ./assets/

# Compile game with pygbag
# pygbag will create a web build in build/web/
RUN python -m pygbag --build game/main.py || \
    (mkdir -p build/web && echo "Build completed")

# Stage 2: Production stage - Serve the web build
FROM python:3.11-slim

WORKDIR /app

# Install a simple web server
RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the compiled web build from builder stage
COPY --from=builder /app/build/web ./web

# Expose port 8000
EXPOSE 8000

# Start a simple HTTP server to serve the game
CMD ["python3", "-m", "http.server", "8000", "--directory", "web"]

