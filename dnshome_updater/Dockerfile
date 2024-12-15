ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install build dependencies based on the available package manager
RUN if command -v apk > /dev/null; then \
        apk add --no-cache \
            gcc \
            musl-dev \
            python3-dev \
            libffi-dev \
            miniupnpc-dev; \
    elif command -v apt-get > /dev/null; then \
        apt-get update && \
        apt-get install -y \
            python3-dev \
            gcc \
            libminiupnpc-dev \
            && rm -rf /var/lib/apt/lists/*; \
    elif command -v dnf > /dev/null; then \
        dnf install -y \
            gcc \
            python3-devel \
            miniupnpc-devel \
            && dnf clean all; \
    fi

# Copy requirements.txt first for better cache
COPY requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt

# Copy your script
COPY run.py /opt/
RUN chmod a+x /opt/run.py

# Set workdir
WORKDIR /opt

# Run script
CMD [ "python3", "run.py" ]