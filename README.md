# P2_mignon_helene
**Livrable du Projet 2 du parcours D-A Python d'OpenClassrooms :**
Scraping de books.toscrape.com avec BeautifulSoup4 ; exportation des infos dans fichiers .csv et des images de couverture dans dossier 'exports'.

_Notes : Ce programme invite l'utilisateur à copier l'url du site (https://books.toscrape.com/index.html) ou de la catégorie qu'il souhaite exporter. Testé sous Windows 10, Python 3.9.5._

----------------------------------------------
## Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
### Récupération du projet

    $ git clone https://github.com/hmignon/P2_mignon_helene.git

### Activer l'environnement virtuel
    $ cd P2_mignon_helene 
    $ python -m venv env 
    $ ~env\scripts\activate
    
### Installer les paquets requis
    $ pip install -r requirements.txt

### Lancer le programme
    $ python main.py
    
----------------------------------------------
## MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
### Récupération du projet

    $ git clone https://github.com/hmignon/P2_mignon_helene.git

### Activer l'environnement virtuel
    $ cd P2_mignon_helene 
    $ python3 -m venv env 
    $ source env/bin/activate
    
### Installer les paquets requis
    $ pip install -r requirements.txt

### Lancer le programme
    $ python3 main.py
