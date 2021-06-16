# P2_mignon_helene
Livrable du Projet 2 de la formation OpenClassrooms D-A Python ; scraping de books.toscrape.com via BeautifulSoup4 ; exportation des infos dans fichiers .csv et des images de couverture dans dossier 'exports'.

## Récupération du projet
Dans Windows Powershell, naviguer vers le dossier souhaité.

    $ git clone https://github.com/hmignon/P2_mignon_helene.git

## Activer l'environnement virtuel
    $ cd P2_mignon_helene 
    $ python3 -m venv env 
    $ source env/bin/activate

## Installer les paquets requis
    $ pip install -r requirements.txt

## Lancer le script
    $ python3 getBookInfo.py