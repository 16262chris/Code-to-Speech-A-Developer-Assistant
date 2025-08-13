# Uses Python version 3.9 as the base image
FROM python:3.9-slim

# Set the working directory to app (this is basically asking Docker to start the code from app)
WORKDIR /app

# Copy requirements (which are Streamlit and gTTS - Google text-to-speech) first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
