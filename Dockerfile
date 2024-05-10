FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the container
COPY . .

# Expose the port 5000
EXPOSE 5000

# Set the entry point for the container
CMD [ "sh", "-c", "python ./app.py" ]