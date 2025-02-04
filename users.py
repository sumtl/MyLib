import books
from loans import *
import json


users = {}
id_users = 0
def get_valid_email():

    while True:
        # Demande à l'utilisateur d'entrer son adresse courriel et la convertit en minuscules
        email_user = input("Entrez l'adresse courriel de l'utilisateur (doit se terminer par @gmail.com): ").strip().lower()

        # Validate email ending with "@gmail.com"
        if not email_user.endswith("@gmail.com")or email_user == "@gmail.com":
            print("\nErreur: L'adresse courriel doit avoir au moins un caractère avant @gmail.com .\n")
        else:
            return email_user

# Function to get a valid phone number.Enter only 10 digits, then I willl format the numbers afterward.
def get_valid_phone():

    while True:
        phone_user = input("Entrez le numéro de téléphone de l'utilisateur (10 chiffres seulement): ")
        # Vérifie si le numéro a bien 10 chiffres et si ce sont des chiffres
        if len(phone_user) != 10 or not phone_user.isdigit():
            print("Erreur: Le numéro de téléphone doit contenir exactement 10 chiffres.")
        else:
            # Si le numéro est valide, le formatte en "xxx-xxx-xxxx" et le retourne
            phone_user = f"{phone_user[:3]}-{phone_user[3:6]}-{phone_user[6:]}"
            return phone_user



# Fonction pour ajouter des utilisateurs
def ajouter_users(users, id_users):

    while True:
        nom_user = input("Entrez le nom de famille de l'utilisateur: ").capitalize()
        prenom_user = input("Entrez le prénom de l'utilisateur: ").capitalize()
        email_user = get_valid_email()
        phone_user = get_valid_phone()


        if books.demander_confirmation(f"Voulez-vous ajouter l'utilisateur {nom_user} ? (o/n): "):
            emprunts_user = 0  #  no emprunts pour le moment
            listelivrelu = []  # Initialize ListeLivreLu as an empty list


        #Ici l'information des users est stockees dans un sous-dictionnaire!
            user_info = {
                "Nom": nom_user,
                "Prénom": prenom_user,
                "Email": email_user,
                "Téléphone": phone_user,
                "Emprunts": emprunts_user,
                "ListeLivreLu": listelivrelu
            }
        #Dans cette partie on cree une cle (ID) unique a chaque users et ensuite on l'associe au user_info !
            id_users += 1
            users[id_users] = user_info


            # Affiche un message confirmant l'ajout de l'utilisateur
            print(f"\nL'utilisateur avec l'ID {id_users}, {nom_user} {prenom_user} a été ajouté avec succès.")
        else:
            print(f"Utilisateur {nom_user} non ajouté.")
        print(users)
        return users, id_users

#Fonction pour valider un ID utilisateur
def get_valid_user_id(users):

    while True:
        # Demande à l'utilisateur d'entrer l'ID
        user_id_input = input("\nEntrez l'ID de l'utilisateur(ou appuyez sur Entrée pour annuler): ")

        # Si l'utilisateur appuie sur Entrée sans rien taper, on annule l'opération
        if user_id_input == "":
            print("\nOpération annulée.")
            return None

        # Vérifie si l'ID entré est un nombre (valide)
        if user_id_input.isdigit():
            user_id = int(user_id_input)

            # Vérifie si l'ID existe dans la liste des utilisateurs
            if user_id in users:
                return user_id
            # Si l'ID n'existe pas dans la bibliothèque, affiche un message d'erreur
            else:
                print(f"Erreur : Aucun utilisateur trouvé avec l'ID {user_id_input}. Veuillez entrer un numéro valide.")

        # Si l'ID entré n'est pas un nombre, affiche un message d'erreur
        else:
            print(f"Erreur : ID {user_id_input} invalide. Veuillez entrer un ID valide (numérique).")



# Fonction pour supprimer un utilisateur par son ID unique
def supprimer_users(users,loans):
    # Vérifie si la bibliothèque d'utilisateurs est vide
    if users == {}:
        print("\nAucun utilisateur dans la bibliothèque.")
        return users,loans

    while True:
            # Utilise une fonction auxiliaire pour obtenir un ID utilisateur valide
        user_id_supprimer = get_valid_user_id(users)
        if user_id_supprimer is None:
            break

        # Récupère les informations de l'utilisateur à supprimer
        user_info = users[user_id_supprimer]

        # Vérifie si l'utilisateur a des livres non retournés
        livres_empruntes = []
        for loan in loans:
            if loan["Utilisateur_ID"] == user_id_supprimer and loan["Date_Retour"] is None:
                livres_empruntes.append(loan["Livre"])  # Ajoute les livres non retournés

        if livres_empruntes:
            print("\nErreur : Impossible de supprimer cet utilisateur tant qu'il a des livres empruntés.")
            print(f"L'utilisateur avec l'ID {user_id_supprimer} a encore des livres empruntés:")
            for livre in livres_empruntes:
                print(f"- {livre}")
            continue  # Retourne à la demande d'un autre utilisateur à supprimer


        # Affiche un message de confirmation avec les informations de l'utilisateur à supprimer
        confirmation_message = (
                    f"\nVoulez-vous vraiment supprimer l'utilisateur suivant ?\n"
                    f"ID: {user_id_supprimer}\n"
                    f"Nom: {user_info['Nom']}\n"
                    f"Prénom: {user_info['Prénom']}\n"
                    f"Email: {user_info['Email']}\n"
                    f"Téléphone: {user_info['Téléphone']}\n"
                    "(o/n): "
                )

        # Demande confirmation pour supprimer l'utilisateur
        if books.demander_confirmation(confirmation_message):
            # Supprime l'utilisateur de la bibliothèque
            del users[user_id_supprimer]
            print(f"\nL'utilisateur avec l'ID {user_id_supprimer} a été supprimé avec succès.\n")
        else:
            # Si l'utilisateur annule
            print(f"\nLa suppression du l'utilisateur avec l'ID {user_id_supprimer} a été annulée.\n")  # Si l'utilisateur annule
    print(users)
    return users,loans


def sauvegarder_users(users,fichier ="users.json"):
    with open(fichier,"w") as f:
        json.dump(users,f,indent=4)
    print("Les utilisateurs ont bien été sauvegardés.")
"""
def charger_users(fichier ="users.json"):
    global users
    with open(fichier,"r") as f:
        users=json.load(f)
    print("Les utilisateurs ont bien été chargés.")
"""
def charger_users(fichier="users.json"):
    try:
        with open(fichier, "r") as file:
            users = json.load(file)
            users = {int(key): value for key, value in users.items()}
        print("Les utilisateurs ont bien été chargés.")
        print(users)  # Debugging: Afficher les utilisateurs chargés
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier} n'a pas été trouvé.")
        users = {}  # Si le fichier n'existe pas, on initialise users comme un dictionnaire vide
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {fichier} n'est pas un fichier JSON valide.")
        users = {}  # Si le fichier n'est pas un JSON valide, on initialise users comme un dictionnaire vide
    except Exception as e:
        print(f"Erreur inconnue lors du chargement de {fichier}: {e}")
        users = {}
    return users

