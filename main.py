import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
from fake_useragent import UserAgent
import pickle
import re
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
os.environ["CHROME_PATH"] = "/usr/bin/google-chrome"
chromedriver_autoinstaller.install()

def create_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options



# Di chuyển chuột ngẫu nhiên
def random_mouse_move(driver):
    try:
        # Lấy kích thước cửa sổ hiện tại
        window_width = driver.execute_script("return window.innerWidth;")
        window_height = driver.execute_script("return window.innerHeight;")

        # Di chuyển chuột trong phạm vi cửa sổ trình duyệt
        action = ActionChains(driver)
        x_offset = random.randint(-window_width//2, window_width//2)
        y_offset = random.randint(-window_height//2, window_height//2)

        # Di chuyển chuột ngẫu nhiên trong phạm vi này
        action.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.5, 1.5))  # Đảm bảo thời gian di chuyển không quá nhanh

    except Exception as e:
        # Kiểm tra và xử lý lỗi liên quan đến di chuyển chuột
        print(f"Error: {e}")

        # Cuộn trang để phần tử có thể nằm trong tầm nhìn
        driver.execute_script("window.scrollBy(0, 250);")  # Cuộn trang xuống
        time.sleep(1)  # Thời gian nghỉ ngắn sau khi cuộn


def run_main_selenium():
    import requests

    # URL chứa file .txt
    url = "https://raw.githubusercontent.com/anisidina29/earn/refs/heads/main/videzzz_link.2txt"

    # Tải nội dung từ URL
    response = requests.get(url)
    response.raise_for_status()  # Gây lỗi nếu tải thất bại

    # Chuyển mỗi dòng thành một phần tử trong list
    link_list = response.text.strip().splitlines()

    # Chọn ngẫu nhiên 2 link
    selected_links = random.sample(link_list, 2)

    # Nhân đôi danh sách đã chọn
    selected_links = selected_links + selected_links

    print(selected_links)

    for link in selected_links:
      for i in ["1", "2", "2"]:
        driver = webdriver.Chrome(options=create_chrome_options())
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get("https://www.dailymotion.com/playlist/x9dd5m")
        time.sleep(random.uniform(5, 10))

        driver.get(link)
        time.sleep(random.uniform(3, 5))
        random_mouse_move(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='vplayer']")))

        for i in range(5):
            try:
                play_button_xpath = "//button[@title='Play Video']"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
                play_button = driver.find_element(By.XPATH, play_button_xpath)
                driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
                # driver.save_screenshot("screenshot_{}.png".format(time.time()))
                play_button.click()

                # Click Play
                driver.execute_script("""
                    var playButton = document.evaluate("//div[@id='vplayer']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (playButton) {
                        playButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(function() { playButton.click(); }, 500);
                    }""")
                time.sleep(5)
                driver.save_screenshot(f"screenshot_{i}.png")
                random_mouse_move(driver)
                random_mouse_move(driver)

            except Exception as e:
                    print(f"Error: {e}")
                    try:
                        driver.execute_script("""
                                    var element = document.getElementById('vplayer');
                                  var clickEvent = new MouseEvent('click', {
                                    bubbles: true,
                                    cancelable: true,
                                    view: window
                                  });
                                  element.dispatchEvent(clickEvent); """)


                        try:
                                element = driver.find_element(By.XPATH, play_button_xpath)
                                actions = ActionChains(driver)

                                # Click tại tọa độ (x_offset, y_offset) so với phần tử
                                actions.move_to_element_with_offset(element, 5, 5).click().perform()
                                time.sleep(30)
                                driver.save_screenshot("screenshot_{}.png".format(i))
                        except Exception as e:
                                print(f"PyAutoGUI click failed: {e}")

                    except Exception as click_error:
                        print(f"Khong the click toa do: {click_error}")
        time.sleep(150)
        driver.save_screenshot("screenshot_final.png")


      # Tải video
      download_button_xpath = "//a[@class='btn btn-success btn-lg btn-download btn-download-n']"
      for i in range(5):
          try:
                  # Find and click the download button
                  download_button = driver.find_element(By.XPATH, download_button_xpath)
                  download_button.click()
                  time.sleep(random.uniform(1, 3))
                  random_mouse_move()
                  driver.save_screenshot(f"screenshot_{i}.png")

                  # Handle captcha if present
                  try:
                      captcha_iframe = WebDriverWait(driver, 10).until(
                          ec.presence_of_element_located((By.TAG_NAME, 'iframe'))
                      )
                      ActionChains(driver).move_to_element(captcha_iframe).click().perform()

                      captcha_box = WebDriverWait(driver, 10).until(
                          ec.presence_of_element_located((By.ID, 'g-recaptcha-response'))
                      )
                      driver.execute_script("arguments[0].click()", captcha_box)
                      time.sleep(10)
                  except Exception:
                      print("Captcha not found")
          except Exception as e:
                  print(f"Error: {e}")


      # driver.save_screenshot("screenshot_{}.png".format(time.time()))
      # time.sleep(150)
      driver.quit()

# run_main_selenium()
import multiprocessing

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    print(f"Detected {num_cores} CPU cores.")

    # Giới hạn số process tùy theo máy
    num_processes = min(5, num_cores)  # an toàn trên máy yếu

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=run_main_selenium)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
