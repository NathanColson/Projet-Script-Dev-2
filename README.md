# Gestionnaire de fichiers CSV en ligne de commande

Ce projet est une application Python permettant de gérer des fichiers CSV à l'aide de commandes en ligne. 
Vous pouvez créer, ajouter, supprimer, fusionner et rechercher des produits dans des fichiers CSV.

---

## Table des matières
1. [Fonctionnalités](#fonctionnalités)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
    - [Création de fichiers CSV](#création-de-fichiers-csv)
    - [Ajout de produits](#ajout-de-produits)
    - [Suppression de produits](#suppression-de-produits)
    - [Fusion de fichiers CSV](#fusion-de-fichiers-csv)
    - [Recherche de produits](#recherche-de-produits)
5. [Structure des dossiers](#structure-des-dossiers)
6. [Exemples](#exemples)
7. [Auteurs](#auteurs)

---

## Fonctionnalités

- **Création** : Créer des fichiers CSV avec des colonnes prédéfinies (nom du produit, quantité, prix et catégorie).
- **Ajout** : Ajouter des produits dans un fichier CSV.
- **Suppression** : Supprimer des produits d'un fichier CSV en fonction de leur nom.
- **Fusion** : Fusionner plusieurs fichiers CSV en un seul fichier récapitulatif.
- **Recherche** : Rechercher des produits dans un fichier CSV en fonction de différents critères (nom, catégorie, prix, quantité).

---

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.12** ou une version ultérieure.
- Le module `argparse` (inclus par défaut avec Python).
- Accès en lecture/écriture à votre système de fichiers.

---

## Installation

1. **Clonez le projet :**

    ```bash
    git clone https://github.com/votre-repo/gestionnaire-csv.git
    cd projet-script-dev-2/
    ```

2. **Installez les dépendances (si nécessaire) :**

    Aucune dépendance externe n'est requise pour ce projet. Tout est inclus avec Python standard.

3. **Vérifiez l'installation :**

    Lancez la commande suivante pour vérifier que le script est fonctionnel :

    ```bash
    python gestion_csv.py -h
    ```

    Vous devriez voir le guide d'utilisation de l'application.

---

## Utilisation

Le programme peut être exécuté à l'aide de la commande suivante :

```bash
python script.py <action> <file_name> [options]
```

**1. Création de fichiers CSV**

Pour créer un fichier CSV :
```bash
Copier le code
python script.py create produits.csv
```

**2. Ajout de produits**

Pour ajouter un produit dans un fichier CSV existant :
```bash
Copier le code
python script.py add produits.csv --product_info "Banane" 10 1.5 "Fruits"
```

**3. Suppression de produits**

Pour supprimer un produit d'un fichier CSV existant :
```bash
python script.py delete produits.csv --product_name "Banane"
```

**4. Fusion de fichiers CSV**

Pour fusionner plusieurs fichiers CSV dans un fichier récapitulatif :
```bash
python script.py merge recapitulatif.csv --input_files produits1.csv produits2.csv
```

**5. Recherche de produits**

Pour rechercher un produit dans un fichier CSV :

Par nom :
```bash
python script.py search produits.csv --product_name "Banane"
```
Par catégorie :
```bash
python script.py search produits.csv --product_categ "Fruits"
```

Par prix :
```bash
python script.py search produits.csv --product_prize 1.5
```
---
## Structure des dossiers
Le programme crée automatiquement deux dossiers :

liste_csv : Contient les fichiers CSV individuels.
recap_csv : Contient les fichiers récapitulatifs après fusion.

---

## Exemples

**1. Exemple complet d'ajout et de recherche**

Création du fichier CSV :
```bash
python script.py create produits.csv
```

Ajout de produits :
```bash
python script.py add produits.csv --product_info "Pomme" 50 0.5 "Fruits"
python script.py add produits.csv --product_info "Carotte" 30 0.2 "Légumes"
```

Recherche d'un produit par catégorie :
```bash
python script.py search produits.csv --product_categ "Fruits"
```

**2. Fusion de fichiers**

Fichiers source :

produits1.csv contient des fruits.
produits2.csv contient des légumes.

Fusion :
```bash
python script.py merge recapitulatif.csv --input_files produits1.csv produits2.csv
```

---

## Auteurs

**Nathan Colson**

Avec l'aide de CHATGPT (plus d'info dans mon analyse utilisation de IA)


PS : Pour toute question ou amélioration, n'hésitez pas à ouvrir une issue ou soumettre une PR sur GitHub !