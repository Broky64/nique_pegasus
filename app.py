import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
)
from dotenv import load_dotenv

# Importation de webdriver_manager pour gérer ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration des options de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.binary_location = os.getenv("CHROME_BINARY", "/usr/bin/google-chrome")

# Initialisation du WebDriver avec webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
logging.info("WebDriver initialisé avec succès.")

# Chargement des variables d'environnement
load_dotenv()
email = os.getenv("PEGASUS_EMAIL")
if not email:
    logging.warning("La variable PEGASUS_EMAIL n'est pas définie !")
else:
    logging.info("Variable PEGASUS_EMAIL chargée.")

password = os.getenv("PEGASUS_PASSWORD")
if not password:
    logging.warning("La variable PEGASUS_PASSWORD n'est pas définie !")
else:
    logging.info("Variable PEGASUS_PASSWORD chargée.")

# Initialisation du WebDriverWait
wait = WebDriverWait(driver, 40)  # Augmenter le temps d'attente

try:
    # Ouvrir le site web Pegasus
    logging.info("Ouverture du site web Pegasus.")
    driver.get("https://learning.estia.fr/pegasus/index.php")
    time.sleep(5)  # Attendre que la page charge complètement

    # Clic sur le bouton de connexion Microsoft
    logging.info("Recherche et clic sur le bouton de connexion Microsoft.")
    microsoft_login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='authlink' and contains(@href, 'o365Auth.php')]")
        )
    )
    microsoft_login_button.click()
    time.sleep(5)  # Attendre la redirection vers la page Microsoft

    # Entrer l'email Microsoft
    logging.info("Saisie de l'email Microsoft.")
    driver.save_screenshot("/app/debug/mail.png")
    email_input = wait.until(EC.visibility_of_element_located((By.NAME, "loginfmt")))
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)
    time.sleep(10)  # Attendre que le champ de mot de passe soit visible

    # Entrer le mot de passe
    logging.info("Saisie du mot de passe.")
    driver.save_screenshot("/app/debug/mdp.png")
    password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='i0118']")))
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(10)  # Attendre l'affichage de la demande "Rester connecté"

    # Gestion de la demande "Rester connecté"
    logging.info("Gestion de la demande 'Rester connecté'.")
    driver.save_screenshot("/app/debug/connect.png")
    stay_signed_in_button = wait.until(
        EC.element_to_be_clickable((By.ID, "idBtn_Back"))
    )
    stay_signed_in_button.click()
    time.sleep(10)  # Attendre la redirection après connexion

    # Clic sur le deuxième menu "Vie Académique"
    
    driver.save_screenshot("/app/debug/debug.png")

    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/nav/div/div[2]")))
    time.sleep(2)  # délai supplémentaire pour être sûr que l'élément est interactif
    element.click()
    driver.save_screenshot("/app/debug/debug1.png")



    logging.info("Clic sur le deuxième menu 'Vie Académique'.")
    time.sleep(2)  # Attendre que les options du menu soient visibles

    # Clic sur "Consulter mes émargements"
    logging.info("Clic sur 'Consulter mes émargements'.")
    consulter_emargements_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[@href='https://learning.estia.fr/pegasus/index.php?com=emergement&job=load-cours-programmes-apprenant']",
            )
        )
    )
    consulter_emargements_link.click()
    time.sleep(8)  # Attendre que la page des émargements charge

    # Basculer vers l'iframe pour accéder au contenu interne
    logging.info("Basculement vers l'iframe 'pegasus_contenu'.")
    iframe = wait.until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@name='pegasus_contenu']"))
    )
    driver.switch_to.frame(iframe)

    # Chercher tous les divs avec la classe "wc-cal-event"
    logging.info("Recherche des éléments d'évènements.")
    try:
        all_events = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'wc-cal-event')]"
        )
        for event in all_events:
            background_color = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).backgroundColor;", event
            )
            if background_color == "rgb(245, 161, 62)":
                driver.execute_script("arguments[0].scrollIntoView(true);", event)
                time.sleep(1)
                event.click()
                logging.info(
                    "Élément avec la couleur d'arrière-plan spécifique trouvé et cliqué."
                )
                break
        else:
            logging.info(
                "L'élément avec la couleur d'arrière-plan spécifique n'a pas été trouvé."
            )

        # Dessiner sur le <canvas>
        logging.info("Recherche de l'élément <canvas> pour simuler un dessin.")
        time.sleep(2)
        canvas_element = driver.find_element(By.TAG_NAME, "canvas")
        driver.execute_script(
            """
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
            triggerMouseEvent(canvas, 'mousedown', rect.left + 10, rect.top + 10);
            triggerMouseEvent(canvas, 'mousemove', rect.left + 100, rect.top + 100);
            triggerMouseEvent(canvas, 'mouseup', rect.left + 100, rect.top + 100);
        """,
            canvas_element,
        )
        logging.info(
            "Dessiné sur l'élément <canvas> avec des événements souris simulés."
        )

        # Clic sur le bouton "Valider"
        logging.info("Recherche du bouton 'Valider'.")
        time.sleep(1)
        valider_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@type='submit' and contains(@class, 'button-action')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", valider_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", valider_button)
        logging.info("Bouton 'Valider' cliqué avec succès.")

    except (
        NoSuchElementException,
        ElementNotInteractableException,
        TimeoutException,
    ) as e:
        logging.error(f"Erreur lors de l'interaction avec un élément: {e}")

finally:
    time.sleep(5)
    logging.info("Fermeture du navigateur.")
    driver.quit()
