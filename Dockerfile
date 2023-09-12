FROM python:3.9.18-bullseye

# Make /data, /videos, and port configurable with environment variables
ARG CONFIG_DIR=/data
ARG DOWNLOAD_DIR=/videos
ARG PORT=8000
ARG HOST=0.0.0.0

VOLUME [ "$CONFIG_DIR" ]
VOLUME [ "$DOWNLOAD_DIR" ]

WORKDIR $CONFIG_DIR

# Copy your application code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables
ENV CONFIG_DIR=$CONFIG_DIR
ENV DOWNLOAD_DIR=$DOWNLOAD_DIR
ENV PORT=$PORT
ENV HOST=$HOST

# Expose the specified port
EXPOSE $PORT

# Start the application
CMD ["python3", "app/tubular.py"]
