# main_ci.py
import os, time, random, logging, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import chromedriver_autoinstaller

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

chromedriver_autoinstaller.install()

def create_options(headless=True, proxy=None):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,800')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    return options

def human_random_wait(base=5, jitter=3):
    t = base + random.uniform(0, jitter)
    logging.info(f"sleep {t:.1f}s")
    time.sleep(t)

def random_mouse_activity(driver):
    try:
        # scroll a bit and move
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(random.uniform(0.3, 1.0))
        # small mouse move via JS (selenium cannot truly move OS mouse in headless)
        driver.execute_script("window.scrollBy(0, -100);")
    except Exception as e:
        logging.debug("mouse act error: %s", e)

def safe_click_play(driver):
    try:
        play_button_xpath = "//button[@title='Play Video']"
        WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
        el = driver.find_element(By.XPATH, play_button_xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", el)
        el.click()
        return True
    except Exception as e:
        logging.debug("click play error: %s", e)
        # fallback: click vplayer
        try:
            driver.execute_script("document.getElementById('vplayer') && document.getElementById('vplayer').click();")
            return True
        except Exception as e2:
            logging.debug("fallback click error: %s", e2)
            return False

def run_worker(links, headless=True, proxy=None, screenshots_dir="screens"):
    driver = None
    tries = 0
    while tries < 3:
        try:
            options = create_options(headless=headless, proxy=proxy)
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            break
        except Exception as e:
            logging.warning("Failed to start Chrome, retrying... %s", e)
            tries += 1
            time.sleep(3)
    if not driver:
        logging.error("Cannot start driver.")
        return

    for idx, link in enumerate(links):
        try:
            logging.info("Opening %s", link)
            driver.get(link)
            human_random_wait(base=3, jitter=4)
            random_mouse_activity(driver)
            ok = safe_click_play(driver)
            if ok:
                human_random_wait(base=30, jitter=10)  # watch some time
            # screenshot
            os.makedirs(screenshots_dir, exist_ok=True)
            fn = f"{screenshots_dir}/shot_{idx}_{int(time.time())}.png"
            driver.save_screenshot(fn)
            logging.info("Saved %s", fn)
            # small random extra interactions
            if random.random() < 0.4:
                driver.execute_script("window.scrollBy(0, 200);")
            human_random_wait(base=5, jitter=5)
        except Exception as e:
            logging.exception("Error processing link %s: %s", link, e)

    try:
        driver.quit()
    except Exception:
        pass

def fetch_links(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return [l.strip() for l in r.text.splitlines() if l.strip()]

if __name__ == "__main__":
    LINKS_URL = os.environ.get("LINKS_URL", "https://raw.githubusercontent.com/anisidina29/earn/refs/heads/main/videzzz_link.2txt")
    HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
    PROXY = os.environ.get("PROXY")  # optional
    # If CI parallel node index provided, split list:
    NODE_INDEX = int(os.environ.get("CIRCLE_NODE_INDEX", "0"))
    NODES_TOTAL = int(os.environ.get("CIRCLE_NODE_TOTAL", "1"))

    try:
        links = fetch_links(LINKS_URL)
    except Exception as e:
        logging.error("Cannot fetch links: %s", e)
        links = []

    # split links by node
    if links:
        per = max(1, len(links)//NODES_TOTAL)
        start = NODE_INDEX*per
        end = start+per if NODE_INDEX < NODES_TOTAL-1 else len(links)
        mylinks = links[start:end]
        logging.info("Node %d/%d handling %d links", NODE_INDEX, NODES_TOTAL, len(mylinks))
        run_worker(mylinks, headless=HEADLESS, proxy=PROXY)
    else:
        logging.warning("No links to process.")
