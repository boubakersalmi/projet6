## ce programme est réalisé sur python 3.7, certains points doivent être adaptés aux versions antérieures de pytho##

##

## DEBUT DU PROGRAMME


## Import des modules nécessaires à l'execution du programme
import os
import json
import glob
import ctypes
import time
import logging
import sys
import csv
import socket



############ Premièren partie du code : la journalisation ########################

## lors de la génération du log, l'heure et la date d'éxecution apparaitront dans le modèle jj/mm/aaaa hh:mm:ss
## le logger a été définit afin de pouvoir faire apparaitre les éléments voulu dans le fichier de log. celui-ci peut etre adapté
logging.basicConfig(
    filename=r'S:\Booba\configfiles\logfile.log',
    format="%(asctime)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level=logging.INFO
)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

##configuration des messages de début et de fin de session
chemindetoileend = "**************** FIN DE SESSION *******************"
chemindetoilestart = "**************** DEBUT DE SESSION *******************"



############ Troisieme partie du code : Définition du fond d'écran adaptatif ########################

## le fichier config_data définit l'emplacement des liens des fonds d'écran en cas d'utilisation d'un fond d'écran non adaptatif.
## celui-ci peut etre modifié pour pointer sur une autre source
## config_data = r'C:\Users\booba\Desktop\filerepo\fond_ecran.txt'
## définition d'une fonction permettant de définir le service dans lequel une personne travaille
## pour cela, la fonction fait appel auu fichier usersandservices dans lequel nous retrouvons la relation entre utilisateur et service concerné.
## le nom de l'utilisateur est celui du hostname windows afin de permettre a la fonction gethostname de la récupérer.
## un logger.info a été rajouté afin de faire apparaitre la relation entre utilisateur et service dans le fichier de log

fichierutilisateurservices = r'S:\Booba\configfiles\usersandservices.csv'

def get_hostname_service():
    # Traitement du csv
    with open(fichierutilisateurservices, "r") as f:
        csvreader = csv.reader(f, delimiter=',')
        next(csvreader)  # skip header
        us_data = [row for row in csvreader]

    current_hostname = socket.gethostname()
    # On cherche a quel service il appartient
    for hostname, service in us_data:
        if hostname == current_hostname:
            break
    else:
        raise Exception(
            f"Impossible de trouver le service auquel '{hostname}' appartient.")

    return service


## par l'intermédiaire de if, nous avons la possbilité de conditionner le chemin de la bibliothèque de fond d'écra
## a utiliser.
## selon la valeur de service nous pourrons définir l'emplacement du dossier dans lequel rechercher les liens de BG

servicesconcerne = get_hostname_service()

if servicesconcerne == "Technique":
    config_data = r'S:\Booba\configfiles\fond_ecran_technique.txt'
elif servicesconcerne == "RH":
    config_data = r'S:\Booba\configfiles\fond_ecran_rh.txt'
elif servicesconcerne == "Commercial":
    config_data = r'S:\Booba\configfiles\fond_ecran_commerciaux.txt'
else:
    print("Impossible de definir le service de l'utilisateur")


## definition de la fonction change_wallpaper
## les prints ci-dessous permettent de définir les messages à afficher. si l'etape ctypes... se déroule bien, nous aurons les deux messages
## suivants qui s'afficheront
def change_wallpaper(wallpaper_path):
    """On change le fond d'ecran"""
    print("Actualisation du fond d'écran")
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper_path.encode("us-ascii"), 3)
    logger.info("Actualisation du fond d'écran réalisée")

## on lit le fichiers fond_ecran contenant les 7 liens pour chacune des images disponibles sur le réseaux interne disque B
with open(config_data, "r") as f:
    mesfonddecrans = f.readlines()
    # On retire le '\n' (retour à la ligne)
    mesfonddecrans = [p[:-1] for p in mesfonddecrans]

## definition des parametres de temps permettant de modifier chaque fond d'écran par rapport au jour d'apparition
localtime = time.localtime(time.time())
jdls = localtime[6]
image_du_jour = mesfonddecrans[jdls]

## si ecran noir apparait en fond d'écran, vérifier les liens
def wallpaper_update():
    change_wallpaper(image_du_jour)




############ Troisieme partie du code : Nettoyage du bureau ########################




## definition de l'adresse du desktop intégrant la variable nomutilisateur
CHEMIN_BUREAU = r'C:\Users\booba\Desktop'

## définition du droit donné sur les dossiers contenant les fichiers nettoyés
permission_octal = 777

## fichier dans lequel nous retrouverons les éléments concernés par le tri
typeelementsconfig = r'S:\Booba\configfiles\type_fichier.json'

## creation du dossier si non existant
def creer_dossier(chemin_dossier):
    # Si le dossier n'existe pas déjà, on le créer
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier, permission_octal)

## définition de la règle de gestion de doublon
def creer_version(nouveau_chemin):
    ## Si le fichier dans le dossier de destination existe déjà, on rajoute une version
    ## example test.txt existe, on renomme en test-v(1, 2, 3, ...).txt
    ## cette partie permet de ne jamais écraser un fichier si deux fichiers ont le même nom
    version = 0
    while os.path.isfile(nouveau_chemin):
        version += 1
        nom_fichier_liste = nom_fichier_liste.split(".")
        nom_fichier_avec_version = "{}-v{}.{}".format(
            nom_fichier_liste[0],
            version,
            nom_fichier_liste[1]
        )
        nouveau_chemin = os.path.join(
            CHEMIN_BUREAU,
            chemin_dossier,
            nom_fichier_avec_version
        )
    return nouveau_chemin

## definition de la fonction de nettoyage du bureau
def DesktopCleaner ():

    with open(typeelementsconfig, "r") as f:
        ## recherche dans le dictionnaire
        dossier_et_extensions = json.load(f)

    for dossier in dossier_et_extensions.keys():
        ## Liste des fichiers qui vont dans le dossier 'dossier'
        ## Si dossier = 'TEXTE'
        ## 'fichiers_dossier' ressemble à ça ['monfichiertxt.txt', 'blabla.txt', ...])
        fichiers_dossier = []
        for extension in dossier_et_extensions[dossier]:
            for fichier in glob.glob(os.path.join(CHEMIN_BUREAU, "*%s" % extension)):
                fichiers_dossier.append(fichier)

        ## Si on a trouvé un fichier alors on le met dans le dossier
        if len(fichiers_dossier) > 0:

            ## Si le dossier n'existe pas déjà, on le créer
            creer_dossier(os.path.join(CHEMIN_BUREAU, dossier))

            ## On met chaque fichier dans le (nouveau) dossier
            for chemin_original in fichiers_dossier:
                nom_fichier = os.path.basename(chemin_original)
                ## message de confirmation
                print("On met le fichier '%s' dans le dossier '%s'" % (nom_fichier, dossier))
                logger.info("Le fichier nommé '%s' a été déplacé dans le dossier '%s'" % (nom_fichier, dossier))

                nouveau_chemin = os.path.join(
                    CHEMIN_BUREAU,
                    dossier,
                    nom_fichier
                )
                ## On ajoute une version -v* si un fichier avec le même nom existe déjà
                nouveau_chemin = creer_version(nouveau_chemin)

                ## on déplace effectivement le fichier dans le dossier
                os.rename(chemin_original, nouveau_chemin)

        ## definition d'un else permettant d'informer du non déplacement de fichier
        else:
            print("Pas de fichiers a ranger pour le dossier %s." % dossier)
            logger.info("Aucune modification n'a été apportée au dossier %s" % dossier)
