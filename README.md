# Gotta Scan 'Em All

<span>
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</span>
<span>
<img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
</span>
<span>
<img alt="MySQL" src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white">
</span>
<span>
<img alt="MariaDB" src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white">
</span>
 
Goot San 'Em All est une application web qui permet d'organiser des chasses au QR codes thématisée. Elle a été créée en 2022 par le pôle web du BDA du campus TSP/IMTBS.

## Installation

Pour déployer l'application, vous avez deux choix :

- Déployer dans une [machine virtuelle](#déploiement-dans-une-vm) (VM)
- Déployer dans un [cluster Kubernetes](#déploiement-dans-un-cluster-kubernetes)

### Déploiement dans une VM

Il vous faut installer `docker compose` dans votre VM. Vous pouvez utiliser les commandes suivantes pour le faire ou suivre d'autres méthodes.

```bash
 curl -fsSL https://get.docker.com -o get-docker.sh
 sudo sh get-docker.sh
```

Ensuite, clonez le repository où vous le souhaitez dans la machine. Déplacez vous dans le dossier racine du projet puis lancez selon votre installation :

```bash
docker compose up
```

ou

```bash
docker-compose up
```

L'application est exposée sur le port **5000** de votre VM.

### Déploiement dans un cluster Kubernetes

TODO: À détailler. Contacter Julien Ribiollet si jamais il y en a besoin.

Dans l'idée, on déploie une MariaDB avec Helm et on fait un déploiement à partir de l'image docker générée par gitlab.

---

## Utiliser l'application

### Étape 1 : Customiser les items

Dans cette chasse aux QR Code, un code correspond à un item. Cet item peut être n'importe quoi. Pour définir les différents items de votre chasse, il vous faut modifier à la main le fichier `./app/items.json`.

```json
{
  "items": [
    {
      "id": 1,
      "title": "Le Billard",
      "subtitle": "",
      "hasImage": true,
      "imagePath": ["1.png"],
      "hasQuestion": false,
      "question": "",
      "answers": [],
      "correctAnswer": 1,
      "pointsMax": 10,
      "pointsMin": 10,
      "slug": ""
    }
  ]
}
```

- `id` : identifiant unique de l'item
- `title` : titre de l'objet, s'affiche une fois scanné
- `subtitle` : sous-titre de l'objet [non implémenté]
- `hasImage` : boolean caractérisant la présence d'une illustration
- `imagePath` : tableau vers une liste de chemins relatifs vers les images qui doivent s'afficher lors d'un scan. Pour changer la base du chemin relatif, il suffit de la modifier dans le fichier `./app/templates/item.html` :
  ```jinja
  ...
  <figure>                                      BASE     imagePath
    <img src="{{url_for('static', filename='cards/apero/' + src)}}" />
  </figure>
  ...
  ```
- `hasQuestion`: [non implémenté]
- `question` : [non implémenté]
- `answers` : [non implémenté]
- `correctAnswer` : [non implémenté]
- `pointsMax` : [non implémenté]
- `pointsMin` : [non implémenté]
- `slug` : morceau de l'URL d'un item généré aléatoirement. Chaque item a sa propre page web vers laquelle mène son qr code. La page aura la forme _votre-domaine.com/`slug`_. Lors de l'édition à la main du fichier `items.json`, laisser cette valeur à une string vide.

### Générer les slugs

Il est important que les URLs des pages de vos items soient complexes pour que personne ne puisse deviner sans avoir à scanner le qr code correspondant.

Pour générer automatiquement les slugs de vos items, vous pouvez lancer le script python : `./utils/generateSlugs.py`.

```bash
python3 ./utils/generateSlugs.py
```

Le fichier `./app/items.json` devrait être modifié en conséquence.

### Générer les QR codes

Pour générer les QR codes de chacun de vos items, ainsi qu'un QR code de base que les joueurs pourrant scanner simplement pour se créer un compte au début du jeu, vous pouvez utiliser le script python : `./utils/generateQRCodes.py`.

D'abord, modifiez la ligne suivante en y mettant l'URL à laquelle la page d'accueil de la plateforme sera accessible (sans oublie le / à la fin).

```python
DEFAULT_URL = "https://qrcodes.bda-tmsp.fr/"
```

Puis lancez le script.

```bash
pip install PyQRCode
python3 ./utils/generateQRCodes.py
```
