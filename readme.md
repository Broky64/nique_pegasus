# Projet Nique Pegasus

Ce projet automatise des interactions sur le site Pegasus (connexion via Microsoft, consultation des émargements, etc.) à l'aide de Selenium et webdriver_manager. L'application est containerisée avec Docker et l'image est prête à être utilisée directement, sans avoir besoin d'être reconstruite.

## Prérequis

- **Docker** doit être installé sur votre machine.
- **Accès Internet** pour télécharger les dépendances nécessaires (Google Chrome, etc.) lors de la première exécution.

## Configuration

L'application utilise des variables d'environnement pour récupérer vos identifiants. Vous devez fournir les deux variables suivantes :

- `PEGASUS_EMAIL` : Votre adresse e-mail pour la connexion Pegasus.
- `PEGASUS_PASSWORD` : Votre mot de passe associé.

## Lancement de l'application

Exécutez la commande suivante en remplaçant les valeurs par vos identifiants :

```bash
docker run -e PEGASUS_EMAIL="votre.email@example.com" -e PEGASUS_PASSWORD="votreMotDePasse" nique_pegasus
```

## Structure du projet
- **app.py** : Script principal qui automatise la connexion et les interactions sur Pegasus via Selenium.

- **DockerFile** : Fichier de configuration pour containeriser l'application.

- **entrypoint.sh** : Script d'initialisation qui lance l'application dès le démarrage du conteneur et configure éventuellement cron pour des exécutions périodiques.

- **requirements.txt** : Liste des dépendances Python (par exemple, selenium, webdriver_manager, etc.).

## Remarques

- **Aucune reconstruction nécessaire :**
L'image Docker est conçue pour être utilisée telle quelle. Vous n'avez qu'à la lancer avec les bonnes variables d'environnement pour personnaliser vos identifiants.

- **Sécurité :**
L'image ne contient aucune donnée sensible. Vos identifiants sont fournis lors du lancement et ne sont pas intégrés dans l'image.

- **Débogage :**
En cas d'erreur, consultez les logs générés par le conteneur. Si l'application prend des captures d'écran (exemple : ```driver.save_screenshot("/app/debug/debug.png"```), utilisez l'option de montage de volume pour y accéder.