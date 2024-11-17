from time import sleep
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time

# Functie pentru cautarea reclamei
def is_ad_playing(driver):
    try:
        ad_indicator = driver.find_element(By.CLASS_NAME, 'ytp-ad-pod-index')
        if ad_indicator.is_displayed():
            print("Butonul ad_indicator e prezent si vizibil")
            return True
        else:
            print("Butonul ad_indicator e prezent si invizibil")
            return False
    except NoSuchElementException:
        print("Butonul ad_indicator nu e prezent")
        return False

# Functie pentru cautarea butonului de skip
def handle_skip_ad_button(driver):
    try:
        # Așteapta 5 secunde pentru a verifica daca butonul este prezent
        skip_button = driver.find_element(By.CLASS_NAME, 'ytp-skip-ad-button')
        print("Butonul 'Skip Ad' gasit.")
        time.sleep(5)

        # Verifica daca butonul este vizibil si interactiv
        if skip_button.is_displayed() and skip_button.is_enabled():
            skip_button.click()
            print("Butonul 'Skip Ad' a fost apasat.")
            return True
        else:
            print("Butonul 'Skip Ad' nu este interactiv.")
            return False

    except NoSuchElementException:
        # Daca butonul nu este gasit
        print("Butonul 'Skip Ad' nu a fost găsit.")
        return False


# Functie pentru reclame fara skip button
def handle_ad_with_timer(driver):
    try:
        ad_duration_element = driver.find_element(By.CLASS_NAME, 'ytp-time-duration')
        ad_current_time_element = driver.find_element(By.CLASS_NAME, 'ytp-time-current')

        ad_duration_text = ad_duration_element.text.strip()
        ad_current_time_text = ad_current_time_element.text.strip()

        if ad_duration_text == '' or ':' not in ad_duration_text:
            ad_time_left = 60
        else:
            try:
                minutes_total, seconds_total = map(int, ad_duration_text.split(":"))
                minutes_current, seconds_current = map(int, ad_current_time_text.split(":"))
                ad_duration_seconds = minutes_total * 60 + seconds_total
                ad_current_seconds = minutes_current * 60 + seconds_current
                ad_time_left = ad_duration_seconds - ad_current_seconds
            except ValueError:
                ad_time_left = 60

        if handle_skip_ad_button(driver):
            print("Butonul 'Skip Ad' a fost apasat. Reclama s-a terminat.")
            return

        print("Butonul 'Skip Ad' nu este disponibil. Așteptam pana se termina timerul...")
        start_time = time.time()
        while time.time() - start_time < ad_time_left:
            time.sleep(1)
            print(f"Așteptam... {int(ad_time_left - (time.time() - start_time))} secunde ramase.")

        print("Timerul reclamei s-a terminat. Continuam cu videoclipul principal.")

    except NoSuchElementException:
        print("Elementele pentru durata reclamei nu au fost gasite. Continuam cu videoclipul principal.")

# Navigheaza pe YouTube
def navigate_youtube(driver):
    try:
        driver.get("https://www.youtube.com")
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        try:
            accept_button = driver.find_element(By.XPATH, '//*[@aria-label="Accept the use of cookies and other data for the purposes described"]')
            accept_button.click()
        except NoSuchElementException:
            pass

        time.sleep(2)
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys("4k")
        time.sleep(1)

        actions = ActionChains(driver)
        actions.send_keys("\n").perform()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '(//*[@id="video-title"])[2]'))
        )
        first_result = driver.find_element(By.XPATH, '(//*[@id="video-title"])[2]')
        first_result.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ytp-progress-bar-padding"))
        )

        add_detected = True
        i = 0
        while add_detected:
            sleep(1)
            i = i + 1

            if is_ad_playing(driver):
                print(f"Gestionam reclama {i}...")
                handle_ad_with_timer(driver)
            else:
                print(f"Nu exista nicio reclama {i}. Continuam cu videoclipul principal.")
                add_detected = False
                break

    except Exception as e:
        print(f"A aparut o eroare in timpul navigarii pe YouTube: {e}")