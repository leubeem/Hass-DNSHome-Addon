# ARG BUILD_FROM
# FROM $BUILD_FROM
FROM python:slim

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip


WORKDIR /opt

# Copy requirements.txt first for better cache
COPY requirements.txt .

#RUN apk add --no-cache python3 py3-pip

# Install requirements using their Python
RUN pip install -r requirements.txt -vvv

COPY run.py run.py

# Copy your script
RUN chmod a+x /opt/run.py

# Set workdir
WORKDIR /opt

# Run script
CMD [ "python", "run.py" ]
