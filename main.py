## debut du code partie principale intégrant la POO
## les fonctions appelés ci-dessous sont importées du fichier main.py
## cette partie du programme n'intègre pas de fonctionnalités graphique

## Dans un premier temps, nous importons les fonctions programmées dans main.py
## afin de les intégrer dans la classe Action
## puis nous importons le module logging afin de générer des fichiers de logs

from setting import *

## definition de la classe action
class Action:

    def __init__(self):
        self.nettoyagebureau = DesktopCleaner()
        self.corporatebg = wallpaper_update()

if __name__ == '__main__':
    Action()
    logger.info(chemindetoile)
