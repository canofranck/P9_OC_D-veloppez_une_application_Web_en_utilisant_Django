# OC_P9_LITRevu

Il s'agit d'une application web réalisée avec Django pour une société fictive, LITRevu.  
L'application est un réseau social permettant de demander et poster des critiques de livres.

## Fonctionnalités

Un visiteur non connecté doit pouvoir :

* s’inscrire 
* se connecter

Un utilisateur connecté doit pouvoir :

* consulter son flux contenant les derniers billets et les critiques des
utilisateurs qu’il suit, classés par ordre antichronologique ;
* créer des nouveaux billets pour demander des critiques sur un livre/un
article ;
* créer des nouvelles critiques en réponse à des billets ;
* créer un billet et une critique sur ce même billet en une seule étape, pour
créer des critiques « à partir de zéro »
* voir, modifier et supprimer ses propres billets et critiques ;
* suivre les autres utilisateurs en entrant leur nom d'utilisateur ;
* voir qui il suit et suivre qui il veut ;
* arrêter de suivre ou bloquer un utilisateur.

## Installation & lancement

Commencez tout d'abord par installer Python 

Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/canofranck/P9_OC_D-veloppez_une_application_Web_en_utilisant_Django
```
Placez vous dans le dossier P9_OC_D-veloppez_une_application_Web_en_utilisant_Django, puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
env\scripts\activate.bat
```
Linux:
```
source env/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
```
Ensuite, placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations:
```
python manage.py makemigrations
```
Puis: 
```
python manage.py migrate
```
Il ne vous reste plus qu'à lancer le serveur: 
```
python manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton à l'adresse suivante:
```
http://127.0.0.1:8000
```
Administration du site :
admin /admindjango

Utilisateur de test :
userone/ S3cret!!!
usertwo/ S3cret!!!
usethree/ S3cret!!!
userfour/ S3cret!!!

