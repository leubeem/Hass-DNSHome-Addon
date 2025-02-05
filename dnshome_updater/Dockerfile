# ARG BUILD_FROM
# FROM $BUILD_FROM
FROM python:3.9

# run this before copying requirements for cache efficiency
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    ; \
    rm -rf /var/lib/apt/lists/*; \
    pip3 install --no-cache-dir --upgrade pip



WORKDIR /opt

# Copy requirements.txt first for better cache
COPY requirements.txt .

#RUN apk add --no-cache python3 py3-pip

# Install requirements using their Python
# Explicitly install requests in case requirements.txt fails
RUN pip install -r requirements.txt || pip install requests -vvv
RUN pip3 install -r requirements.txt || pip3 install requests -vvv

COPY run.py run.py

# Copy your script
RUN chmod a+x /opt/run.py

# Set workdir
WORKDIR /opt

# Run script
CMD [ "python", "run.py" ]
