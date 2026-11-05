# INTENTIONALLY INSECURE. See examples/secure-app/Dockerfile for the fixed version.

# BUG: Python 3.7 is end-of-life, so the base image no longer gets security fixes.
FROM python:3.7-slim

# BUG: ADD can fetch remote URLs and unpack archives; COPY is the safe default.
ADD . /app
WORKDIR /app

# BUG: package lists left in the image, extra tools nobody needs at runtime.
RUN apt-get update && apt-get install -y curl openssh-server

RUN pip install -r requirements.txt

# BUG: SSH port exposed from an application container.
EXPOSE 5000 22

# BUG: no USER instruction, so the app runs as root.
# BUG: no HEALTHCHECK.
CMD ["python", "app.py"]
