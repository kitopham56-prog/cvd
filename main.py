import os
import time
import schedule
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import telegram

# ===== Config =====
BOT_TOKEN = "8372904645:AAFso89K2UabIdYZ2HZrRGhV8xD41kmaZWA"
GROUP_ID = -1002845367780
HASHWEI_URL = "https://hashwei.ai/dashboard/cvd"

bot = telegram.Bot(token=BOT_TOKEN)

# ===== Selenium Setup =====
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # chạy ẩn
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# ===== Capture and Send =====
def capture_and_send(coin_symbol):
    driver = init_driver()
    driver.get(HASHWEI_URL)
    time.sleep(5)  # chờ load trang + tự login session

    # Chọn coin
    try:
        driver.find_element(By.XPATH, f"//div[contains(text(), '{coin_symbol}')]").click()
        time.sleep(5)
    except:
        print(f"⚠ Không tìm thấy {coin_symbol}")

    # Chụp ảnh
    screenshot_path = f"{coin_symbol}.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()

    # Gửi ảnh lên Telegram
    now = datetime.now().strftime("%H:%M %d/%m/%Y")
    caption = f"{coin_symbol} | Cập nhật: {now}"
    with open(screenshot_path, "rb") as img:
        bot.send_photo(chat_id=GROUP_ID, photo=img, caption=caption)

# ===== Task =====
def job():
    for coin in ["BTCUSDT", "ETHUSDT"]:
        capture_and_send(coin)

# ===== Lịch =====
schedule.every().hour.at(":00").do(job)  # chạy đúng phút 00 mỗi giờ

if __name__ == "__main__":
    job()  # chạy ngay khi khởi động
    while True:
        schedule.run_pending()
        time.sleep(10)
