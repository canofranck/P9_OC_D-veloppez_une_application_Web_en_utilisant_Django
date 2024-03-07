import os
import tokenize


def get_comments_from_module(module_path):
    comments = []
    with open(module_path, "rb") as file:
        tokens = tokenize.tokenize(file.readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment_line = token.start[0]
                comment_text = token.string.strip()
                comments.append((comment_line, comment_text))
    return comments


def list_files_in_current_directory():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    return [
        file for file in files if os.path.isfile(os.path.join(current_directory, file))
    ]


files_in_current_directory = list_files_in_current_directory()

print("Liste des fichiers dans le répertoire actuel:")
for i, file in enumerate(files_in_current_directory):
    print(f"{i+1}. {file}")

# Demander à l'utilisateur de choisir le fichier à contrôler
selected_file_index = (
    int(input("Veuillez choisir le numéro du fichier à contrôler: ")) - 1
)
selected_file = files_in_current_directory[selected_file_index]

module_path = os.path.abspath(selected_file)
comments = get_comments_from_module(module_path)

# Afficher les commentaires avec les lignes correspondantes
print("Commentaires dans le fichier sélectionné:")
for line_number, comment_text in comments:
    print(f"Ligne {line_number}: {comment_text}")
