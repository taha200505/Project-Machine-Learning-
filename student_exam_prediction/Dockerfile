# ============================================================================
# Dockerfile for Student Exam Score Prediction System
# Multi-stage build for optimized production image
# ============================================================================

# Stage 1: Base image with system dependencies
FROM python:3.11-slim AS base

# Metadata
LABEL maintainer="your.email@example.com"
LABEL description="Student Exam Score Prediction System - ML-powered Streamlit application"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# ============================================================================
# Stage 2: Python dependencies installation
# ============================================================================
FROM base AS dependencies

# Copy only requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================================
# Stage 3: Final production image
# ============================================================================
FROM base AS production

# Copy Python packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p .streamlit

# Create Streamlit configuration file
RUN echo '\
[server]\n\
port = 8501\n\
address = "0.0.0.0"\n\
headless = true\n\
runOnSave = false\n\
fileWatcherType = "none"\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "0.0.0.0"\n\
serverPort = 8501\n\
\n\
[theme]\n\
primaryColor = "#1f77b4"\n\
backgroundColor = "#ffffff"\n\
secondaryBackgroundColor = "#f0f2f6"\n\
textColor = "#262730"\n\
font = "sans serif"\n\
\n\
[client]\n\
showErrorDetails = false\n\
toolbarMode = "minimal"\n\
' > .streamlit/config.toml

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash streamlit && \
    chown -R streamlit:streamlit /app

# Switch to non-root user
USER streamlit

# Expose Streamlit default port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Set the entrypoint
ENTRYPOINT ["streamlit", "run"]

# Default command
CMD ["app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.fileWatcherType=none", \
     "--browser.gatherUsageStats=false"]


# docker run -d \
#   --name student-exam-predictor \
#   -p 8501:8501 \
#   -v $(pwd)/cleaned_data.csv:/app/cleaned_data.csv:ro \
#   student-exam-predictor:latest

# docker run -d --name student-exam-predictor -p 8501:8501 -v "$PWD/cleaned_data.csv:/app/cleaned_data.csv:ro" student-exam-predictor:latest