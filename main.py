# -*- coding: utf-8 -*-

# import des 3 modules os / struct / ctypes
import os
import struct
import ctypes


# Le fond d'ecran sera change par le background par défaut
IMAGE_PATH = os.path.normpath('image.jpg')

# definition d'execution du changement de fond d'ecran
def changeBG(path):
    ctypes.windll.user32.SystemParametersInfoA(20, 0, path.encode("us-ascii"), 3)
    print("Le fond d'ecran a ete change !")


# démarrage du programme principal
if __name__ == "__main__":
    try:
        # On lit le fichier config.csv
        with open("./config.csv", "r") as f:
            # On recupere les lignes et on cherche a savoir si
            # FOND_ECRAN=KO
            content = f.readlines()
            for c in content:
                left, right = c.split("=")
                if left == "FOND_ECRAN":  # repere de ligne pour orienter la recherche
                    if right == "OK": # si la ligne renvoie OK, pas de changement avec message de confirmation
                        print("On ne change pas le fond d'ecran.")
                    else:
                        changeBG(IMAGE_PATH) #si la ligne renvoie KO, alors on lance changeBG avec IMAGE_PATH
                    break;  # on arrête la boucle for c in content
            else:
                print("Impossible de trouver la ligne FOND_ECRAN=... !")
                #message a afficher en cas de lecture impossible de la ligne

    except Exception as e:
        print("\nIl y a une erreur inattendue !\n")
        print(e.message)
        raise e
