# 1. Use official lightweight Python image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system-level dependencies (for PyAudio, ffmpeg, etc.)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy only requirements to leverage Docker cache
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the project files
COPY . .

# 7. Expose Streamlit's port
EXPOSE 8501

# 8. Set environment variables for development and hot reload
ENV STREAMLIT_SERVER_RUN_ON_SAVE=true \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 9. Run Streamlit with hot reloading
CMD ["streamlit", "run", "app.py"]
