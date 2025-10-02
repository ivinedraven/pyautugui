FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libxshmfence1 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Cài Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Cài Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

ENV DISPLAY=:99
# Thiết lập biến môi trường để Chrome nằm trong PATH
ENV CHROME_PATH=/usr/bin/google-chrome

CMD ["python", "main.py"]
