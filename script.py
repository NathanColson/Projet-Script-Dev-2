import csv
import os
import argparse
import cmd


class GestionCSV:
    """
    Cette classe gère la création, la modification, la recherche, et la fusion
    de fichiers CSV dans des répertoires spécifiques.
    """
    LISTE_CSV_DIR = "liste_csv"
    RECAP_CSV_DIR = "recap_csv"

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """
        Crée les répertoires nécessaires s'ils n'existent pas déjà.
        """
        os.makedirs(self.LISTE_CSV_DIR, exist_ok=True)
        os.makedirs(self.RECAP_CSV_DIR, exist_ok=True)

    def get_file_path(self, file_name, is_recap):
        """
        Renvoie le chemin complet du fichier CSV, en fonction du fait qu'il s'agit
        d'un fichier récapitulatif ou non.
        """
        directory = self.RECAP_CSV_DIR if is_recap else self.LISTE_CSV_DIR
        return os.path.join(directory, file_name)

    def create_csv(self, file_name):
        """
        Crée un fichier CSV avec des entêtes prédéfinies s'il n'existe pas déjà.
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
        Ajoute un produit (ligne) dans le fichier CSV spécifié.
        product_info est une liste au format [nom, quantite, prix, categorie].
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
        Supprime toutes les occurrences (toutes les lignes) du produit spécifié par son nom.
        """
        file_path = self.get_file_path(file_name, is_recap)

        if not os.path.exists(file_path):
            print(f"Le fichier '{file_path}' n'existe pas.")
            return

        temp_file = file_path + '.tmp'
        lines_deleted = 0

        with open(file_path, mode='r', encoding='utf-8') as infile, open(temp_file, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            headers = next(reader)
            writer.writerow(headers)

            for row in reader:
                if row[0] == product_name:
                    lines_deleted += 1
                else:
                    writer.writerow(row)

        os.replace(temp_file, file_path)

        if lines_deleted > 0:
            print(f"{lines_deleted} occurrence(s) du produit '{product_name}' ont été supprimées du fichier '{file_path}'.")
        else:
            print(f"Produit '{product_name}' non trouvé dans le fichier '{file_path}'.")

    def merge_csv(self, input_files, output_file):
        """
        Fusionne plusieurs fichiers CSV individuels en un seul fichier récapitulatif.
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
        Recherche des produits dans un fichier CSV en fonction de différents critères.
        Affiche toutes les lignes correspondant à ces critères.
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
                if ((product_name and row[0] == product_name) or
                    (product_categ and row[3] == product_categ) or
                    (product_prize and row[2] == product_prize) or
                    (product_quantity and row[1] == product_quantity)):

                    if not found:
                        print(f"Produits trouvés dans {'recapitulatif' if is_recap else 'fichier individuel'} '{file_name}':")
                        found = True
                    for header, value in zip(headers, row):
                        print(f"{header}: {value}")
                    print("-" * 30)

            if not found:
                print(f"Aucun produit trouvé correspondant aux critères dans le fichier '{file_name}'.")


class InterfaceInteractif(cmd.Cmd):
    """
    Classe fournissant une interface en ligne de commande interactive
    pour utiliser les fonctionnalités de GestionCSV.
    """
    intro = (
        "Bienvenue dans le gestionnaire CSV interactif.\n"
        "Tapez 'help' pour voir les commandes disponibles.\n"
    )
    prompt = "(csv) "

    def __init__(self, gestion_csv):
        super().__init__()
        self.gestion_csv = gestion_csv

    def do_create(self, arg):
        """
        Créer un fichier CSV.
        Usage: create nom_fichier.csv
        """
        args = arg.strip().split()
        if len(args) != 1:
            print("Usage: create nom_fichier.csv")
            return
        file_name = args[0]
        self.gestion_csv.create_csv(file_name)

    def do_add(self, arg):
        """
        Ajouter un produit au fichier CSV.
        Usage: add nom_fichier.csv nom_produit quantite prix categorie
        """
        args = arg.strip().split()
        if len(args) != 5:
            print("Usage: add nom_fichier.csv nom_produit quantite prix categorie")
            return

        file_name, nom, quantite, prix, categorie = args
        product_info = [nom, quantite, prix, categorie]
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

    def do_delete(self, arg):
        """
        Supprimer un produit (toutes les occurrences) du fichier CSV.
        Usage: delete nom_fichier.csv nom_produit
        """
        args = arg.strip().split()
        if len(args) != 2:
            print("Usage: delete nom_fichier.csv nom_produit")
            return

        file_name, product_name = args
        self.gestion_csv.delete_product(file_name, product_name, is_recap=False)

    def do_merge(self, arg):
        """
        Fusionner plusieurs fichiers CSV individuels en un fichier récapitulatif.
        Usage: merge nom_recap.csv fichier1.csv fichier2.csv ...
        """
        args = arg.strip().split()
        if len(args) < 2:
            print("Usage: merge nom_recap.csv fichier1.csv fichier2.csv ...")
            return

        output_file = args[0]
        input_files = args[1:]
        self.gestion_csv.merge_csv(input_files, output_file)

    def do_search(self, arg):
        """
        Rechercher un produit selon différents critères.
        Usage: search nom_fichier.csv [--product_name "X"] [--product_categ "X"] [--product_prize "X"] [--product_quantity "X"]
        Exemple: search voiture.csv --product_name "Tesla"
        """
        args = arg.strip().split()
        if len(args) < 1:
            print("Usage: search nom_fichier.csv [options]")
            return

        file_name = args[0]
        # Extraction des options
        product_name = None
        product_categ = None
        product_prize = None
        product_quantity = None

        # Parse simple des arguments restants
        for i in range(1, len(args)):
            if args[i] == "--product_name" and i+1 < len(args):
                product_name = args[i+1]
            elif args[i] == "--product_categ" and i+1 < len(args):
                product_categ = args[i+1]
            elif args[i] == "--product_prize" and i+1 < len(args):
                product_prize = args[i+1]
            elif args[i] == "--product_quantity" and i+1 < len(args):
                product_quantity = args[i+1]

        self.gestion_csv.search_product(
            file_name,
            product_name=product_name,
            product_categ=product_categ,
            product_prize=product_prize,
            product_quantity=product_quantity,
            is_recap=False
        )

    def do_exit(self, arg):
        """Quitter le shell interactif."""
        print("Au revoir !")
        return True

    def do_quit(self, arg):
        """Quitter le shell interactif."""
        return self.do_exit(arg)


def main():
    parser = argparse.ArgumentParser(description="Gérer les fichiers CSV (création, ajout, suppression, fusion, recherche).")
    parser.add_argument("action", nargs="?", choices=['create', 'add', 'delete', 'merge', 'search'], help="Action à réaliser")
    parser.add_argument("file_name", nargs="?", help="Nom du fichier CSV")
    parser.add_argument("--product_info", nargs=4, metavar=('NOM', 'QUANTITÉ', 'PRIX', 'CATÉGORIE'),
                        help="Informations du produit à ajouter : nom, quantité, prix unitaire, catégorie.")
    parser.add_argument("--product_name", help="Nom du produit à supprimer ou rechercher.")
    parser.add_argument("--product_categ", help="Catégorie du produit à rechercher.")
    parser.add_argument("--product_prize", help="Prix du produit à rechercher.")
    parser.add_argument("--product_quantity", help="Quantité du produit à rechercher.")
    parser.add_argument("--input_files", nargs='+', help="Liste des fichiers CSV à fusionner (pour 'merge').")
    parser.add_argument("--output_file", help="Nom du fichier récapitulatif (pour 'merge').")
    parser.add_argument("--is_recap", action="store_true",
                        help="Indique si l'opération concerne un fichier récapitulatif.")
    parser.add_argument("--interactive", action="store_true", help="Lancer le programme en mode interactif")

    args = parser.parse_args()
    gestionnaire = GestionCSV()

    # Si mode interactif, on lance le shell
    if args.interactive:
        InterfaceInteractif(gestionnaire).cmdloop()
        return

    # Mode non-interactif (ligne de commande classique)
    if args.action == 'create':
        if args.file_name:
            gestionnaire.create_csv(args.file_name)
        else:
            print("Veuillez fournir le nom du fichier à créer.")

    elif args.action == 'add':
        if args.file_name and args.product_info:
            gestionnaire.add_product(args.file_name, args.product_info, args.is_recap)
        else:
            print("Veuillez fournir le nom du fichier et les informations du produit '--product_info'.")

    elif args.action == 'delete':
        if args.file_name and args.product_name:
            gestionnaire.delete_product(args.file_name, args.product_name, args.is_recap)
        else:
            print("Veuillez fournir le nom du fichier et le nom du produit à supprimer '--product_name'.")

    elif args.action == 'merge':
        if args.input_files and args.output_file:
            gestionnaire.merge_csv(args.input_files, args.output_file)
        else:
            print("Veuillez fournir les fichiers d'entrée avec '--input_files' et le fichier de sortie avec '--output_file'.")

    elif args.action == 'search':
        if args.file_name and (args.product_name or args.product_categ or args.product_prize or args.product_quantity):
            gestionnaire.search_product(
                args.file_name,
                product_name=args.product_name,
                product_categ=args.product_categ,
                product_prize=args.product_prize,
                product_quantity=args.product_quantity,
                is_recap=args.is_recap
            )
        else:
            print("Veuillez fournir le nom du fichier et au moins un critère de recherche (--product_name, --product_categ, --product_prize, --product_quantity).")

    else:
        print("Aucune action spécifiée. Utilisez '--interactive' pour lancer le mode interactif ou précisez une action.") 


if __name__ == "__main__":
    main()
