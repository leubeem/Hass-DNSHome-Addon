# ARG BUILD_FROM
# FROM $BUILD_FROM
FROM python:slim

# Copy requirements.txt first for better cache
COPY requirements.txt /opt/

RUN apk add --no-cache python3 py3-pip

# Install requirements using their Python
RUN pip install -r /opt/requirements.txt

# Copy your script
COPY run.py /opt/
RUN chmod a+x /opt/run.py

# Set workdir
WORKDIR /opt

# Run script
CMD [ "python", "run.py" ]
