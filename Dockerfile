FROM  python:3.11-slim

WORKDIR /app

# Set environment variables to prevent prompts during installations
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg	git --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable --no-install-recommends \
    && apt-get purge --auto-remove -y curl gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD python -m overleaf_backup
