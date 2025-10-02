FROM python:3.10-bullseye

# Cài dependencies hệ thống cho Chrome & Selenium
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

# Cài Google Chrome stable (từ .deb chính thức)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && google-chrome --version

WORKDIR /app

# Cài Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Thiết lập biến môi trường cho Chrome
ENV DISPLAY=:99
ENV CHROME_PATH=/usr/bin/google-chrome

CMD ["python", "main.py"]
