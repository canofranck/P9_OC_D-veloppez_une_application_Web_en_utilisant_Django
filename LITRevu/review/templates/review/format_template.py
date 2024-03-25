import os


def executer_djhtml_sur_fichier(fichier_html):
    # Vérifier si le fichier est un fichier HTML
    if fichier_html.endswith(".html"):
        # Exécuter la commande djhtml sur le fichier
        commande = f"djhtml {fichier_html}"
        resultat = os.system(commande)
        print(f"Résultat de djhtml pour {fichier_html} : {resultat}")


def parcourir_repertoire_et_executer_djhtml(repertoire):
    # Parcourir tous les fichiers dans le répertoire
    for fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, fichier)
        # Vérifier si le chemin est un fichier
        if os.path.isfile(chemin_fichier):
            # Exécuter djhtml sur le fichier
            executer_djhtml_sur_fichier(chemin_fichier)


# Obtenir le répertoire du fichier Python en cours d'exécution
repertoire_courant = os.path.dirname(__file__)

# Appeler la fonction pour parcourir le répertoire et exécuter djhtml sur
# chaque fichier HTML
parcourir_repertoire_et_executer_djhtml(repertoire_courant)
