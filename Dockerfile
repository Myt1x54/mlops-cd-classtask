FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so this layer is cached across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application and the version marker.
COPY app.py .
COPY VERSION .

# Build-time metadata, baked into the image and exposed via /health.
# These are overridden by the CD pipeline with the real tag and git commit.
ARG APP_VERSION=0.0.0
ARG GIT_COMMIT=unknown
ENV APP_VERSION=${APP_VERSION}
ENV GIT_COMMIT=${GIT_COMMIT}

EXPOSE 5000

CMD ["python", "app.py"]
