
# Use the latest Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment
RUN venv/bin/python -m pip install --upgrade pip

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code files to the container
COPY . .

# Run the desired command to execute your code
CMD [ "python3", "main.py" ]
