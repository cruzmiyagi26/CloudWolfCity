FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Set Python path for module resolution
ENV PYTHONPATH="/app"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r multi_tool_agent/requirements.txt

# Expose port for Cloud Run
EXPOSE 8080

# Default command for Cloud Run
CMD ["uvicorn", "multi_tool_agent.main:app", "--host", "0.0.0.0", "--port", "8080"]
