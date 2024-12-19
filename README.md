# Gestionnaire de fichiers CSV en ligne de commande et mode interactif

Ce projet est une application Python permettant de gérer des fichiers CSV à l'aide de commandes en ligne **ou** via un shell interactif. Vous pouvez créer, ajouter, supprimer, fusionner et rechercher des produits dans des fichiers CSV. Le mode interactif offre une expérience plus intuitive grâce à une interface en ligne de commande.

---

## Table des matières

1. [Fonctionnalités](#fonctionnalités)  
2. [Prérequis](#prérequis)  
3. [Installation](#installation)  
4. [Utilisation](#utilisation)  
    - [Mode non-interactif (ligne de commande)](#mode-non-interactif-ligne-de-commande)  
    - [Mode interactif (shell basé sur cmd)](#mode-interactif-shell-basé-sur-cmd)  
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

- **Création** : Créer des fichiers CSV avec des colonnes prédéfinies (nom du produit, quantité, prix, catégorie).
- **Ajout** : Ajouter des produits dans un fichier CSV existant.
- **Suppression** : Supprimer **toutes les occurrences** d'un produit donné dans un fichier CSV sur base de son nom.  
  *Amélioration :* Si plusieurs lignes correspondent au même nom, elles sont toutes supprimées et le nombre total de suppressions est indiqué.
- **Fusion** : Fusionner plusieurs fichiers CSV en un seul fichier récapitulatif.
- **Recherche** : Rechercher des produits dans un fichier CSV selon différents critères (nom, catégorie, prix, quantité).  
  *Amélioration :* Affiche désormais tous les produits correspondant au(x) critère(s).
- **Mode Interactif** : Lancer un shell interactif pour effectuer les opérations sans avoir à relancer le script Python à chaque fois.

---

## Prérequis

- **Python 3.12** ou une version ultérieure.
- Le module `argparse` (inclus avec Python).
- Le module `cmd` (inclus avec Python).
- Accès en lecture/écriture aux fichiers.

---

## Installation

1. Clonez le projet :

    ```bash
    git clone https://github.com/votre-repo/gestionnaire-csv.git
    cd projet-script-dev-2/
    ```

2. Aucune dépendance externe n'est requise.

3. Vérifiez l'installation :

    ```bash
    python script.py -h
    ```
    Vous devriez voir le guide d'utilisation.

---

## Utilisation

L'application propose deux modes d'utilisation :

### Mode non-interactif (ligne de commande)

Exécutez directement une action :

```bash
python script.py <action> <file_name> [options]
```

### Exemple :

```bash
python script.py create produits.csv
```

Mode interactif (shell basé sur cmd)
Pour lancer le mode interactif :

```bash
python script.py --interactive
```

Vous arriverez dans un shell (csv). Vous pouvez y taper directement les commandes (create, add, delete, merge, search) sans relancer Python.

### Exemple d'utilisation interactive :

```bash
(csv) create produits.csv
(csv) add produits.csv Pomme 50 0.5 Fruits
(csv) search produits.csv --product_categ Fruits
(csv) exit
```

**Création de fichiers CSV**

Non-interactif :

```bash
python script.py create produits.csv
```

Interactif :

```bash
(csv) create produits.csv
```

**Ajout de produits**

Non-interactif :

```bash
python script.py add produits.csv --product_info "Banane" 10 1.5 "Fruits"
```

Interactif :

```bash
(csv) add produits.csv Banane 10 1.5 Fruits
```


**Suppression de produits**

Non-interactif :

```bash
python script.py delete produits.csv --product_name "Banane"
```

Interactif :

```bash
(csv) delete produits.csv Banane
```

Amélioration : Toutes les lignes correspondant au nom du produit sont supprimées, et le nombre total est affiché.

### Fusion de fichiers CSV

Non-interactif :

```bash
python script.py merge recapitulatif.csv --input_files produits1.csv produits2.csv
```

Interactif :

```bash
(csv) merge recapitulatif.csv produits1.csv produits2.csv
```

### Recherche de produits

Non-interactif :

Par nom :

```bash
python script.py search produits.csv --product_name "Banane"
```

Par catégorie :

```bash
python script.py search produits.csv --product_categ "Fruits"
```

Par prix :

```bash
python script.py search produits.csv --product_prize 1.5
```

Par quantité :

```bash
python script.py search produits.csv --product_quantity 10
```

Interactif :

```bash
(csv) search produits.csv --product_name "Banane"
```

ou

```bash
(csv) search produits.csv --product_categ "Fruits"
```

### Structure des dossiers

liste_csv/ : Contient les fichiers CSV individuels.
recap_csv/ : Contient les fichiers récapitulatifs après fusion.

### Exemples

Exemple complet en mode non-interactif

```bash
# Création du fichier CSV
python script.py create produits.csv
```

## Ajout de produits
```bash
python script.py add produits.csv --product_info "Pomme" 50 0.5 "Fruits"
python script.py add produits.csv --product_info "Carotte" 30 0.2 "Légumes"
python script.py add produits.csv --product_info "Pomme" 20 0.5 "Fruits"  # Une autre Pomme

# Recherche par catégorie (toutes les pommes s'afficheront)
python script.py search produits.csv --product_categ "Fruits"

# Suppression du produit "Pomme" (toutes les occurrences seront supprimées)
python script.py delete produits.csv --product_name "Pomme"
``` 

**Fusion de fichiers**

```bash
python script.py merge recapitulatif.csv --input_files produits1.csv produits2.csv
```

Exemple en mode interactif

```bash
python script.py --interactive
(csv) create produits.csv
(csv) add produits.csv Pomme 50 0.5 Fruits
(csv) add produits.csv Banane 10 1.5 Fruits
(csv) search produits.csv --product_categ Fruits
(csv) delete produits.csv Pomme
(csv) exit
```

## Auteurs

**Nathan Colson**

PS : Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou une pull request !







