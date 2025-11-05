import os
import asyncio
import logging
from threading import Thread
from flask import Flask

# মডিউল ইম্পোর্ট করার চেষ্টা করা হচ্ছে
try:
    from main import main as bot_main
except ImportError:
    logging.error("main.py থেকে main ফাংশনটি import করা যায়নি।")
    # যদি main.py তে main ফাংশন না থাকে, তবে load_and_run_plugins থাকতে পারে
    try:
        from main import load_and_run_plugins as bot_main
    except ImportError:
        logging.critical("main.py ফাইলে 'main' বা 'load_and_run_plugins' ফাংশনটি খুঁজে পাওয়া যায়নি!")
        exit(1) # ফাংশন না পাওয়া গেলে প্রস্থান করুন

# Flask অ্যাপ সেটআপ
app = Flask(__name__)

@app.route('/')
def home():
    """UptimeRobot-কে জানানোর জন্য যে বটটি সচল আছে।"""
    return "Bot is alive and running!"

def run_bot_loop():
    """বটটিকে একটি আলাদা থ্রেডে চালানোর জন্য ফাংশন।"""
    try:
        logging.info("বট থ্রেডের জন্য নতুন asyncio লুপ সেট করা হচ্ছে।")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        logging.info("বট main() ফাংশনটি চালানো হচ্ছে...")
        loop.run_until_complete(bot_main())
    except Exception as e:
        logging.error(f"বট লুপে একটি ত্রুটি ঘটেছে: {e}", exc_info=True)

def run_web_server():
    """Flask ওয়েব সার্ভারটি মূল থ্রেডে চালানো।"""
    port = int(os.environ.get('PORT', 8080))
    logging.info(f"Flask ওয়েব সার্ভার 0.0.0.0:{port} এ চালু হচ্ছে...")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # ১. বটটিকে একটি আলাদা থ্রেডে (Thread) চালু করুন
    logging.info("বট থ্রেড চালু করা হচ্ছে...")
    bot_thread = Thread(target=run_bot_loop, name="BotThread")
    bot_thread.daemon = True
    bot_thread.start()
    
    # ২. মূল থ্রেডে Flask ওয়েব সার্ভারটি চালু করুন
    logging.info("মূল থ্রেডে ওয়েব সার্ভার চালু করা হচ্ছে...")
    run_web_server()
