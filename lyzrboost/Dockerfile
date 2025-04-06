FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_demo.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_demo.txt

# Copy the package and demo files
COPY . .

# Install the package in development mode
RUN pip install -e .

# Expose the Streamlit port
EXPOSE 8501

# Set the API key as an environment variable (replace with your actual key or use docker run -e)
ENV LYZR_API_KEY="sk-default-9wdTatnu1figlN2UilBoBW0yz58wNokO"

# Start the Streamlit app
CMD ["streamlit", "run", "demo_app.py", "--server.address=0.0.0.0"] 