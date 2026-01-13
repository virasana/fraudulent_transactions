FROM python:3.10.12-slim

WORKDIR /app

# Install bash (slim images don't always include it)
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the script is executable
RUN chmod +x ./hello.sh

# Run hello.sh, then start bash
CMD ["bash", "-c", "./hello.sh && exec bash"]
