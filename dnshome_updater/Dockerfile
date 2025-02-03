ARG BUILD_FROM
FROM ${BUILD_FROM}

# Copy requirements.txt first for better cache
COPY requirements.txt /opt/

# Install requirements using their Python
RUN python3 -m pip install -r /opt/requirements.txt

# Copy your script
COPY run.py /opt/
RUN chmod a+x /opt/run.py

# Set workdir
WORKDIR /opt

# Run script
CMD [ "python", "run.py" ]
