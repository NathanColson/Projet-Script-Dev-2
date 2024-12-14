import csv
import os
import argparse


class GestionCSV:
    LISTE_CSV_DIR = "liste_csv"
    RECAP_CSV_DIR = "recap_csv"

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """Crée les dossiers nécessaires s'ils n'existent pas."""
        os.makedirs(self.LISTE_CSV_DIR, exist_ok=True)
        os.makedirs(self.RECAP_CSV_DIR, exist_ok=True)

    def get_file_path(self, file_name, is_recap):
        """Renvoie le chemin complet du fichier selon qu'il s'agit d'un fichier récapitulatif ou non."""
        directory = self.RECAP_CSV_DIR if is_recap else self.LISTE_CSV_DIR
        return os.path.join(directory, file_name)

    def create_csv(self, file_name):
        """Crée un fichier CSV dans le dossier liste_csv avec des colonnes prédéfinies."""
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
        """Ajoute une ligne au fichier CSV existant (liste ou récapitulatif)."""
        file_path = self.get_file_path(file_name, is_recap)

        if not os.path.exists(file_path):
            print(f"Le fichier '{file_path}' n'existe pas. Veuillez le créer d'abord.")
            return

        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(product_info)

        print(f"Produit ajouté au fichier '{file_path}'.")

    def delete_product(self, file_name, product_name, is_recap):
        """Supprime une ligne d'un fichier CSV en fonction du nom du produit."""
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
        """Fusionne plusieurs fichiers CSV depuis liste_csv et sauvegarde le fichier récapitulatif dans recap_csv."""
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
        """Recherche un produit dans un fichier CSV par nom ou par catégorie et affiche ses informations."""
        file_path = self.get_file_path(file_name, is_recap)

        if not os.path.exists(file_path):
            print(f"Le fichier '{file_path}' n'existe pas.")
            return

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)

            found = False
            for row in reader:
                if (product_name and row[0] == product_name) or (product_categ and row[3] == product_categ) or (product_prize and row[2] == product_prize) or (product_quantity and row[1] == product_quantity):
                    if not found:
                        print(f"Produits trouvés dans {'recapitulatif' if is_recap else 'fichier individuel'} '{file_name}':")
                        found = True
                    for header, value in zip(headers, row):
                        print(f"{header}: {value}")
                    print("-" * 30)

            if not found:
                if product_name:
                    print(f"Produit '{product_name}' non trouvé dans le fichier '{file_name}'.")
                elif product_categ:
                    print(f"Aucun produit trouvé dans la catégorie '{product_categ}' dans le fichier '{file_name}'.")
                elif product_prize:
                    print(f"Aucun produit trouvé avec le prix '{product_prize}' dans le fichier '{file_name}'")
                elif product_quantity:
                    print(f"Aucun produit trouvé avec cette quantité '{product_quantity}' dans le fichier '{file_name}'")


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
