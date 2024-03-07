import os
import ast


def extract_functions_and_docstrings(file_path):
    functions = {}
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            docstring = ast.get_docstring(node)
            functions[function_name] = docstring
    return functions


def list_files_in_directory(directory):
    files = os.listdir(directory)
    return [file for file in files if file.endswith(".py")]


# Obtenir le répertoire où le code est lancé
current_directory = os.getcwd()

# Liste des fichiers dans le répertoire actuel
files_in_directory = list_files_in_directory(current_directory)

print("Liste des fichiers dans le répertoire:")
for i, file in enumerate(files_in_directory):
    print(f"{i+1}. {file}")

# Demander à l'utilisateur de choisir le fichier à contrôler
selected_file_index = (
    int(input("Veuillez choisir le numéro du fichier à contrôler: ")) - 1
)
selected_file = files_in_directory[selected_file_index]

file_path = os.path.join(current_directory, selected_file)
functions_and_docstrings = extract_functions_and_docstrings(file_path)

# Afficher les résultats
missing_docstrings_count = 0
for function_name, docstring in functions_and_docstrings.items():
    print(f"Function: {function_name}")
    print(f"Docstring:\n{docstring}\n{'-'*30}")
    if docstring is None:
        missing_docstrings_count += 1

print(f"Nombre de docstrings manquants : {missing_docstrings_count}")
