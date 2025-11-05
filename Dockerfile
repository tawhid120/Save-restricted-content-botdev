# Python 3.10-slim বেস ইমেজ ব্যবহার করুন
FROM python:3.10-slim

# ffmpeg এবং অন্যান্য প্রয়োজনীয় সিস্টেম লাইব্রেরি ইন্সটল করুন
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ওয়ার্কিং ডিরেক্টরি সেট করুন
WORKDIR /app

# প্রথমে requirements.txt কপি করুন এবং লাইব্রেরিগুলো ইন্সটল করুন
COPY requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

# আপনার প্রোজেক্টের বাকি সব ফাইল কপি করুন
COPY . .

# Render এই কমান্ডটি চালাবে। আমরা আমাদের নতুন app.py ফাইলটি চালাবো
CMD ["python3", "app.py"]
