import csv
import os
import argparse


class GestionCSV:
    LISTE_CSV_DIR = "liste_csv"
    RECAP_CSV_DIR = "recap_csv"

    def __init__(self):
        """
        Description :
         Initialise la classe et crée les répertoires nécessaires.

        PRE :
        - Aucun prérequis.

         POST :
        - Les répertoires `LISTE_CSV_DIR` et `RECAP_CSV_DIR` existent.

        RAISES :
        - OSError si un problème survient lors de la création des répertoires.
        """
        self.ensure_directories()

    def ensure_directories(self):
        """
        Description :
        Crée les dossiers nécessaires pour les fichiers CSV.

        PRE :
        - Aucun prérequis.

        POST :
        - Les répertoires `LISTE_CSV_DIR` et `RECAP_CSV_DIR` existent (créés s'ils n'existent pas déjà).

        RAISES :
        - OSError si un problème survient lors de la création des répertoires.
        """
        os.makedirs(self.LISTE_CSV_DIR, exist_ok=True)
        os.makedirs(self.RECAP_CSV_DIR, exist_ok=True)

    def get_file_path(self, file_name, is_recap):
        """
        Description :
        Renvoie le chemin complet d'un fichier (liste ou récapitulatif).

        PRE :
        - `file_name` est une chaîne valide représentant un nom de fichier.
        - `is_recap` est un booléen indiquant si le fichier est un fichier récapitulatif.

        POST :
        - Retourne un chemin valide sous forme de chaîne.

        RAISES :
        - Aucun.
        """
        directory = self.RECAP_CSV_DIR if is_recap else self.LISTE_CSV_DIR
        return os.path.join(directory, file_name)

    def create_csv(self, file_name):
        """
        Description :
        Crée un fichier CSV avec des colonnes prédéfinies dans le dossier liste_csv.

        PRE :
        - `file_name` est une chaîne valide représentant un nom de fichier.

        POST :
        - Un fichier CSV est créé dans le répertoire `LISTE_CSV_DIR` avec les colonnes 
          ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'].
        - Si le fichier existe déjà, aucune action n'est effectuée.

        RAISES :
        - OSError si un problème survient lors de la création ou de l'écriture du fichier.
    """
        file_path = self.get_file_path(file_name, is_recap=False)

        if os.path.exists(file_path):
            print(f"Le fichier '{file_path}' existe déjà.")
            return

        headers = ['nom du produit', 'quantité', 'prix unitaire', 'catégorie']
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

        print(f"Fichier '{file_path}' créé avec les colonnes : {', '.join(headers)}.")

    def add_product(self, file_name, product_info, is_recap):
        """
        Description :
        Ajoute un produit dans un fichier CSV existant (liste ou récapitulatif).

        PRE :
        - `is_recap` est un booléen indiquant si l'opération concerne un fichier récapitulatif.

        POST :
        - Une nouvelle ligne représentant le produit est ajoutée au fichier spécifié.

        RAISES :
        - FileNotFoundError si le fichier spécifié n'existe pas.
        - ValueError si `product_info` ne contient pas exactement 4 éléments.
        - OSError si un problème survient lors de l'ouverture ou de l'écriture du fichier.
        """
        file_path = self.get_file_path(file_name, is_recap)

        if not os.path.exists(file_path):
            print(f"Le fichier '{file_path}' n'existe pas. Veuillez le créer d'abord.")
            return

        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(product_info)

        print(f"Produit ajouté au fichier '{file_path}'.")

    def delete_product(self, file_name, product_name, is_recap):
        """
        Description :
        Supprime une ligne d'un fichier CSV en fonction du nom du produit.

        PRE :
        - `product_name` est une chaîne représentant le nom du produit à supprimer.
        - `is_recap` est un booléen indiquant si l'opération concerne un fichier récapitulatif.

        POST :
        - Le fichier CSV est mis à jour avec le produit correspondant à `product_name` supprimé.
        - Si le produit n'existe pas, le fichier reste inchangé.

        RAISES :
        - FileNotFoundError si le fichier spécifié n'existe pas.
        - OSError si un problème survient lors de la manipulation des fichiers temporaires.
        """
        file_path = self.get_file_path(file_name, is_recap)

        if not os.path.exists(file_path):
            print(f"Le fichier '{file_path}' n'existe pas.")
            return

        temp_file = file_path + '.tmp'
        with open(file_path, mode='r', encoding='utf-8') as infile, open(temp_file, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            headers = next(reader)
            writer.writerow(headers)

            line_deleted = False
            for row in reader:
                if row[0] != product_name:
                    writer.writerow(row)
                else:
                    line_deleted = True

        os.replace(temp_file, file_path)

        if line_deleted:
            print(f"Produit '{product_name}' supprimé du fichier '{file_path}'.")
        else:
            print(f"Produit '{product_name}' non trouvé dans le fichier '{file_path}'.")

    def merge_csv(self, input_files, output_file):
        """
        Description :
        Fusionne plusieurs fichiers CSV de `LISTE_CSV_DIR` et enregistre le résultat 
        dans un fichier récapitulatif dans `RECAP_CSV_DIR`.

        PRE :
        - `input_files` est une liste de noms de fichiers existants dans `LISTE_CSV_DIR`.
        - `output_file` est une chaîne valide représentant le nom du fichier récapitulatif.

        POST :
        - Un fichier récapitulatif est créé dans `RECAP_CSV_DIR`, contenant les données fusionnées
          de tous les fichiers spécifiés dans `input_files`.
        - Si un fichier d'entrée est introuvable, il est ignoré avec un message d'erreur.

        RAISES :
        - FileNotFoundError si aucun des fichiers spécifiés n'existe.
        - OSError si un problème survient lors de la lecture ou de l'écriture des fichiers.
        """
        input_paths = [self.get_file_path(file, is_recap=False) for file in input_files]
        output_path = self.get_file_path(output_file, is_recap=True)

        header_written = False

        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = None

            for file_path in input_paths:
                if not os.path.exists(file_path):
                    print(f"Erreur : Le fichier '{file_path}' n'existe pas.")
                    continue

                with open(file_path, mode='r', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    header = next(reader)

                    if not header_written:
                        writer = csv.writer(outfile)
                        writer.writerow(header)
                        header_written = True

                    for row in reader:
                        writer.writerow(row)

        print(f"Fichier récapitulatif créé : {output_path}")

    def search_product(self, file_name, product_name=None, product_categ=None, product_prize=None, product_quantity=None, is_recap=False):
        """
        Description :
        Recherche un produit dans un fichier CSV par nom, catégorie, prix ou quantité et affiche ses informations.

        PRE :
        - `file_name` est une chaîne valide représentant un fichier existant.
        - `product_name`, `product_categ`, `product_prize`, ou `product_quantity` peuvent être spécifiés 
          pour définir le critère de recherche.
        - `is_recap` est un booléen indiquant si la recherche doit se faire dans un fichier récapitulatif.

        POST :
        - Les produits correspondant aux critères sont affichés dans la console.
        - Si aucun produit ne correspond, un message d'information est affiché.

        RAISES :
        - FileNotFoundError si le fichier spécifié n'existe pas.
        - OSError si un problème survient lors de la lecture du fichier.
        """
        file_path = self.get_file_path(file_name, is_recap)

        if not os.path.exists(file_path):
            print(f"Le fichier '{file_path}' n'existe pas.")
            return

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)

            found = False
            for row in reader:
                if (product_name and row[0] == product_name) or \
                    (product_categ and row[3] == product_categ) or \
                    (product_prize and row[2] == product_prize) or \
                    (product_quantity and row[1] == product_quantity):
                    if not found:
                        print(f"Produits trouvés dans {'recapitulatif' if is_recap else 'fichier individuel'} '{file_name}':")
                        found = True
                    for header, value in zip(headers, row):
                        print(f"{header}: {value}")
                    print("-" * 30)

            if not found:
                print(f"Aucun produit trouvé correspondant aux critères dans le fichier '{file_name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gérer les fichiers CSV (création, ajout, suppression, fusion, recherche).")
    parser.add_argument("action", choices=['create', 'add', 'delete', 'merge', 'search'],
                        help="Action à réaliser : 'create', 'add', 'delete', 'merge', 'search'.")
    parser.add_argument("file_name", help="Nom du fichier CSV pour 'create', 'add', 'delete' ou 'search'.")
    parser.add_argument("--product_info", nargs=4, metavar=('NOM', 'QUANTITÉ', 'PRIX', 'CATÉGORIE'),
                        help="Informations du produit à ajouter : nom, quantité, prix unitaire, catégorie.")

    parser.add_argument("--product_name", help="Nom du produit à supprimer ou rechercher.")
    parser.add_argument("--product_categ", help="Catégorie du produit à rechercher.")
    parser.add_argument("--product_prize", help="Prix du produit à rechercher")
    parser.add_argument("--product_quantity", help="Quantité du produit à rechercher")

    parser.add_argument("--input_files", nargs='+', help="Liste des fichiers CSV à fusionner (pour 'merge').")
    parser.add_argument("--output_file", help="Nom du fichier récapitulatif (pour 'merge').")
    parser.add_argument("--is_recap", action="store_true",
                        help="Indique si l'opération concerne un fichier récapitulatif.")

    args = parser.parse_args()
    gestionnaire = GestionCSV()

    if args.action == 'create':
        gestionnaire.create_csv(args.file_name)
    elif args.action == 'add':
        if args.product_info:
            gestionnaire.add_product(args.file_name, args.product_info, args.is_recap)
        else:
            print("Veuillez fournir les informations du produit avec l'option '--product_info'.")
    elif args.action == 'delete':
        if args.product_name:
            gestionnaire.delete_product(args.file_name, args.product_name, args.is_recap)
        else:
            print("Veuillez fournir le nom du produit à supprimer avec l'option '--product_name'.")
    elif args.action == 'merge':
        if args.input_files and args.output_file:
            gestionnaire.merge_csv(args.input_files, args.output_file)
        else:
            print("Veuillez fournir les fichiers d'entrée avec '--input_files' et le fichier de sortie avec '--output_file'.")
    elif args.action == 'search':
        if args.product_name or args.product_categ or args.product_prize or args.product_quantity:
            gestionnaire.search_product(args.file_name, product_name=args.product_name, product_categ=args.product_categ, product_prize=args.product_prize, product_quantity=args.product_quantity, is_recap=args.is_recap)
        else:
            print("Veuillez fournir le nom du produit à rechercher avec l'option '--product_name' ou '--product_categ' ou '--product_prize' ou '--product_quantity'.")
