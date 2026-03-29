FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Ensure output prints immediately (useful for docker logs / subprocess piping)
ENV PYTHONUNBUFFERED=1

# Install required system dependencies (if any are needed for building Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all scripts into the container
COPY scripts/ /app/scripts/

# Define mount points for runtime overrides
VOLUME ["/registry", "/output"]

# Set the generic agent runner as the entrypoint
ENTRYPOINT ["python", "/app/scripts/run_agent.py"]
