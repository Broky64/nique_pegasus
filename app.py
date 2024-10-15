from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv('PEGASUS_PASSWORD')

# Configurer les options de Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Définir le chemin vers le ChromeDriver
service = Service('C:\\WORKSPACE\\niquepegasus\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

# Initialiser le WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 40)  # Augmenter le temps d'attente

try:
    # Ouvrir le site web Pegasus
    driver.get("https://learning.estia.fr/pegasus/index.php")

    # Attendre que la page charge complètement
    time.sleep(5)

    # Clic sur le bouton de connexion Microsoft
    microsoft_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='authlink' and contains(@href, 'o365Auth.php')]"))
    )
    microsoft_login_button.click()

    # Attendre la redirection vers la page Microsoft
    time.sleep(5)

    # Entrer l'email Microsoft
    email_input = wait.until(EC.visibility_of_element_located((By.NAME, 'loginfmt')))
    email_input.send_keys("paul.brocvielle@etu.estia.fr")
    email_input.send_keys(Keys.RETURN)

    # Attendre que le champ de mot de passe soit visible
    time.sleep(5)

    # Entrer le mot de passe directement dans le script
    password_input = wait.until(EC.visibility_of_element_located((By.NAME, 'passwd')))
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # Attendre que la demande "Rester connecté" s'affiche
    time.sleep(5)

    # Gestion de la demande "Rester connecté"
    stay_signed_in_button = wait.until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
    stay_signed_in_button.click()

    # Attendre la redirection après connexion
    time.sleep(5)

    # Clic sur le **deuxième** menu "Vie Académique"
    vie_academique_toggle = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@class='km-menus-toggle'])[2]"))
    )
    vie_academique_toggle.click()

    # Attendre que les options du menu soient visibles
    time.sleep(2)

    # Clic sur "Consulter mes émargements"
    consulter_emargements_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='https://learning.estia.fr/pegasus/index.php?com=emergement&job=load-cours-programmes-apprenant']"))
    )
    consulter_emargements_link.click()

    # Attendre que la page des émargements charge
    time.sleep(8)  # Délai supplémentaire pour s'assurer que tout est bien chargé

    # Basculer vers l'iframe pour accéder au contenu interne
    iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@name='pegasus_contenu']")))
    driver.switch_to.frame(iframe)

    # Chercher tous les divs avec la classe "wc-cal-event"
    try:
        all_events = driver.find_elements(By.XPATH, "//div[contains(@class, 'wc-cal-event')]")
        for event in all_events:
            # Vérifier la couleur de fond de chaque élément
            background_color = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", event)
            if background_color == "rgb(245, 161, 62)":
                # Faire défiler jusqu'à l'élément et le cliquer
                driver.execute_script("arguments[0].scrollIntoView(true);", event)
                time.sleep(1)  # Pause pour s'assurer que l'élément est visible
                event.click()
                print("Élément avec la couleur d'arrière-plan spécifique trouvé et cliqué.")
                break
        else:
            print("L'élément avec la couleur d'arrière-plan spécifique n'a pas été trouvé.")
        
        # Attendre 2 secondes, puis dessiner sur le <canvas>
        time.sleep(2)
        canvas_element = driver.find_element(By.TAG_NAME, 'canvas')

        # Utiliser JavaScript pour simuler un dessin sur le canvas via des événements souris
        driver.execute_script("""
            function triggerMouseEvent(node, eventType, coordX, coordY) {
                const mouseEvent = new MouseEvent(eventType, {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: coordX,
                    clientY: coordY,
                    buttons: 1
                });
                node.dispatchEvent(mouseEvent);
            }

            const canvas = arguments[0];
            const rect = canvas.getBoundingClientRect();

            // Simuler un clic en maintenant, puis déplacer pour dessiner
            triggerMouseEvent(canvas, 'mousedown', rect.left + 10, rect.top + 10);
            triggerMouseEvent(canvas, 'mousemove', rect.left + 100, rect.top + 100);
            triggerMouseEvent(canvas, 'mouseup', rect.left + 100, rect.top + 100);
        """, canvas_element)
        print("Dessiné sur l'élément <canvas> avec des événements souris simulés en JavaScript.")

        # Attendre 1 seconde, puis cliquer sur le bouton "Valider"
        time.sleep(1)
        valider_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(@class, 'button-action')]")))
        
        # Faire défiler jusqu'au bouton et le cliquer via JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", valider_button)
        time.sleep(1)  # Pause pour s'assurer que le bouton est bien visible
        
        driver.execute_script("arguments[0].click();", valider_button)
        print("Bouton 'Valider' trouvé et cliqué via JavaScript.")

    except (NoSuchElementException, ElementNotInteractableException, TimeoutException) as e:
        print(f"Une erreur est survenue lors de l'interaction avec un élément. Erreur : {e}")

finally:
    time.sleep(5)
    # Fermer le navigateur
    driver.quit()