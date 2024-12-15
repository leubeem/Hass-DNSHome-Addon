FROM homeassistant/amd64-base-python:3.9
WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy your script
COPY run.py .

# Make script executable
RUN chmod +x run.py

# Run script
CMD [ "./run.py" ]