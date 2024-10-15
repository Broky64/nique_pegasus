from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurer les options de Chrome (sans mode headless pour le débogage)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Définir le chemin vers le ChromeDriver
service = Service('C:\\WORKSPACE\\niquepegasus\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

# Initialiser le WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Ouvrir le site web Pegasus
    driver.get("https://learning.estia.fr/pegasus/index.php")

    # Attendre que la page charge (vous pouvez ajuster le temps selon votre connexion)
    time.sleep(5)

    # Débug : Imprimer l'URL actuelle pour vérifier l'état
    print("URL actuelle:", driver.current_url)

    # Attente explicite pour que le bouton de connexion Microsoft soit cliquable
    wait = WebDriverWait(driver, 20)
    
    # Utiliser le sélecteur XPath pour cibler l'élément <a> avec la classe 'authlink'
    microsoft_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='authlink' and contains(@href, 'o365Auth.php')]"))
    )
    microsoft_login_button.click()

    # Attendre la redirection vers la page Microsoft
    time.sleep(5)

    # Débug : Imprimer l'URL actuelle pour vérifier la redirection
    print("URL actuelle après redirection:", driver.current_url)

    # Entrer l'email Microsoft
    email_input = wait.until(EC.visibility_of_element_located((By.NAME, 'loginfmt')))
    email_input.send_keys("paul.brocvielle@etu.estia.fr")
    email_input.send_keys(Keys.RETURN)

    time.sleep(5)

    # Attendre le chargement du champ de mot de passe
    password_input = wait.until(EC.visibility_of_element_located((By.NAME, 'passwd')))
    password_input.send_keys("S5yL1#5$!#")
    password_input.send_keys(Keys.RETURN)

    # Attendre quelques secondes pour que l'authentification se termine
    time.sleep(5)

    # Gestion de la demande "Rester connecté"
    stay_signed_in_button = wait.until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
    stay_signed_in_button.click()

    # Attendre que la page charge après la réponse à la demande
    time.sleep(5)

    # Débug : Imprimer l'URL après connexion
    print("URL après connexion:", driver.current_url)

    # Clic sur le **deuxième** menu "Vie Académique" (deuxième élément avec la classe 'km-menus-toggle')
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

    # Attendre que la page charge après avoir cliqué sur le lien
    time.sleep(5)

    # Débug : Imprimer l'URL après avoir accédé à la page des émargements
    print("URL après avoir cliqué sur 'Consulter mes émargements':", driver.current_url)

finally:
    # Fermer le navigateur (commentez ceci si vous souhaitez laisser le navigateur ouvert pour l'inspection manuelle)
    driver.quit()
