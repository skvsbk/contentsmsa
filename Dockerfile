# Pull base image
FROM python:3.10

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# or update pip if needed
#RUN pip3 install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt --default-timeout=100 --no-cache-dir

# Copy project to WORKDIR
COPY . .

# Run project
CMD ["python", "run.py"]