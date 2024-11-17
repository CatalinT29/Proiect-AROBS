from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from youtube_navigation import navigate_youtube
from screen_recording import record_combined
from audio_analysis import analyze_audio

# Configureaza serviciul Chrome cu WebDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Pasul 1: Navigheaza pe YouTube si gestioneaza reclamele
    print("Navigam pe YouTube...")
    navigate_youtube(driver)
    print("Navigarea pe YouTube a fost finalizata.")

    # Pasul 2: Inregistreaza ecranul si sunetul timp de 2 minute
    print("Începem înregistrarea ecranului...")
    record_combined(audio_file="final_audio.wav", video_file="final_video.avi", duration=120)
    print("Înregistrarea s-a terminat.")

    # Pasul 3: Analizeaza fișierul audio
    print("Analizam Inregistrarea audio...")
    analyze_audio(audio_file="final_audio.wav", output_file="audio_analysis.txt")
    print("Analiza audio s-a terminat.")

finally:
    # inchide browserul
    driver.quit()
    print("Programul s-a terminat.")

