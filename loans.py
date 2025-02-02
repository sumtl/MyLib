



from users import *

from datetime import datetime

def get_valid_books(books):
    if not books:
        print("La bibliothèque est vide.")
        return False
    for book in books:
        if books[book]["Exemplaires"] > 0:
            return True
    print("Erreur: Aucun livre disponible dans la bibliothèque pour emprunter.")
    return False

def emprunts_livres(books, users, loans):
    print (books)
    if not get_valid_books(books):  # Check for available books before any action
        return books, users, loans

    # Demander l'ID de l'utilisateur à emprunter un livre
    while True:
        #Vérifier si dictionnaire vide ou aucun exemplaire disponible  avant chaque emprunt.
        #if not books or all(book.get("Exemplaires", 0) == 0 for book in books.values()):
            #print("Aucun livre disponible dans la bibliothèque pour emprunter.")
            #return books, users, loans

        user_id = get_valid_user_id(users)
        # Annuler si l'utilisateur choisit d'annuler
        if user_id is None:
            return books, users, loans

        # Boucle pour permettre d'emprunter plusieurs livres
        while True:
        # Demander le titre du livre à emprunter
            nom_emprunts = input("Entrez le nom du livre à emprunter: ").strip().title()
        # Vérifier si le livre existe dans la bibliothèque
            if nom_emprunts not in books:
                print(f"Erreur :Ce livre '{nom_emprunts}' n'est pas disponible dans la bibliothèque.")
                continue
        # Vérifier si le livre est disponible
            if books[nom_emprunts]["Exemplaires"] <= 0:
                print(f"Erreur:Ce livre '{nom_emprunts}' n'est pas disponible actuellement.")
                continue
            if nom_emprunts in users[user_id]["ListeLivreLu"]:
                print(f"Erreur : L'utilisateur avec l'ID {user_id} a déjà emprunté le livre '{nom_emprunts}'.")
                continue
            # Enregistrer l'emprunt (date d'emprunt)
            date_emprunt = datetime.now().strftime("%Y-%m-%d")
            emprunt = {
                "Utilisateur_ID": user_id,
                "Livre": nom_emprunts,
                "Date_Emprunt": date_emprunt,
                "Date_Retour": None  # Pas de date de retour au moment de l'emprunt
        }
            # Ajouter l'emprunt à la liste des emprunts
            loans.append(emprunt)
            # Réduire le nombre d'exemplaires du livre dans le stock
            books[nom_emprunts]["Exemplaires"] -= 1
            books[nom_emprunts]["Emprunts"] += 1
            # Ajouter ce livre à la liste des livres empruntés de l'utilisateur,sans répétition
            if nom_emprunts not in users[user_id]["ListeLivreLu"]:
                users[user_id]["ListeLivreLu"].append(nom_emprunts)
            # Mettre à jour le nombre d'emprunts de l'utilisateur
            users[user_id]["Emprunts"] += 1
            # Afficher un message de confirmation
            print(f"L'emprunt du livre '{nom_emprunts}' par l'utilisateur avec ID {user_id} a été effectué avec succès.")
            print(loans)
            return books, users, loans

"""
            #Vérifier si dictionnaire vide ou aucun exemplaire disponible  avant/après chaque emprunt.
            if not books or all(book.get("Exemplaires", 0) == 0 for book in books.values()):
                print("Aucun livre disponible dans la bibliothèque pour emprunter.")
                return books,users,loans  # Exit the function if no books are left

            # Demander à l'utilisateur s'il souhaite emprunter un autre livre pour ce même ID
            if not demander_confirmation(f"Voulez-vous emprunter un autre livre pour l'utilisateur avec ID {user_id} -- {users[user_id]['Nom']} {users[user_id]['Prénom']} ? (o/n): "):
                break  # Quitter la boucle des livres si l'utilisateur ne veut pas en emprunter un autre

        if not books or all(book["Exemplaires"] == 0 for book in books.values()):
            print("Aucun livre disponible dans la bibliothèque pour emprunter.")
            return books,users,loans

        

"""


def retour_livres(books, users, loans):
    user_id = get_valid_user_id(users)
    if user_id is None:
        return books, users, loans

    # Get books borrowed by this user
    user_loans = []
    for loan in loans:
        if "Utilisateur_ID" not in loan or "Date_Retour" not in loan:
            print(f"Erreur: Données manquantes dans l'emprunt: {loan}")
            continue

        if loan["Utilisateur_ID"] == user_id and loan["Date_Retour"] is None:
            user_loans.append(loan)

    if not user_loans:
        print(f"L'utilisateur avec l'ID {user_id} n'a aucun livre à retourner.")
        return loans, books, users

    print(f"Livres empruntés par {users[user_id]['Nom']} {users[user_id]['Prénom']} :")
    for loan in user_loans:
        print(f"- {loan['Livre']} (Emprunté le {loan['Date_Emprunt']})")

    while True:
        book_to_return = input("Entrez le nom du livre à retourner : ").strip().title()

        # Find the matching loan manually
        matching_loan = None
        for loan in user_loans:
            if loan["Livre"] == book_to_return:
                matching_loan = loan
                break  # Stop searching once we find it

        if not matching_loan:
            print(f"Erreur: Ce livre '{book_to_return}' n'a pas été emprunté par cet utilisateur.")
            continue  # Ask again if the book is incorrect

        # Register the return
        matching_loan["Date_Retour"] = datetime.now().strftime("%Y-%m-%d")

        # Update book inventory
        books[book_to_return]["Exemplaires"] += 1

        # Remove the book from the user's borrowed list
        users[user_id]["ListeLivreLu"].remove(book_to_return)

        # Update the user's borrow count
        users[user_id]["Emprunts"] -= 1

        print(f"Le livre '{book_to_return}' a été retourné avec succès.")

        # Ask if they want to return another book
        if not demander_confirmation("Voulez-vous retourner un autre livre ? (o/n): "):
            break  # Stop if they don't want to return more

    return books, users, loans

def calculate_average_loan_duration_by_genre(books,loans):
    #print(type(books))----test
    #print(books)-----test
    genre_durations = {}
    for loan in loans:
        if loan["Date_Retour"] is None:
            continue
        book_title = loan["Livre"]
        print(book_title)
        genre = books[book_title]["Genre"]

        date_emprunt = datetime.strptime(loan["Date_Emprunt"], "%Y-%m-%d")
        date_retour = datetime.strptime(loan["Date_Retour"], "%Y-%m-%d")
        duration = (date_retour - date_emprunt).days
        if genre in genre_durations:
            genre_durations[genre]["total_duration"] += duration
            genre_durations[genre]["count"] += 1
        else:
            genre_durations[genre] = {"total_duration":duration, "count": 1}

    print("\nDurée moyenne des emprunts par genre:\n")
    for genre in genre_durations:
        if genre_durations[genre]["count"] > 0:
            average_duration = genre_durations[genre]["total_duration"] / genre_durations[genre]["count"]
        else:
            average_duration = 0
        print(f"Genre: {genre}, Durée moyenne: {average_duration} jours\n")

    return genre_durations

def list_most_borrowed_books(books):
    if books is None:
        print("Error: La bibliothèque est vide.")
        return []
    count = []
    for nom_item in books:
        count.append((nom_item,books[nom_item]["Emprunts"]))
    for i in range(len(count)):
        for j in range(i + 1, len(count)):
            if count[i][1]< count[j][1]:
                count[i], count[j] = count[j], count[i]

    print("\nLes 5 livres ayant le plus grand nombre d’emprunts:\n")
    for book,emprunts in count[:5]:
        print(f"Titre: {book}, Nombre d'emprunts: {emprunts}\n")
    print(count)
    return count


def list_most_active_users(users):
    if users is None:
        print("Error: Utilisateurs vides.")
        return []

    count = []
    for user_id, user_info in users.items():
        count.append((user_id,user_info["Nom"],user_info["Prénom"],user_info["Emprunts"]))

    for i in range(len(count)):
        for j in range(i + 1, len(count)):
            if count[i][3] < count[j][3]:
                count[i], count[j] = count[j], count[i]

    print("Les 3 utilisateurs ayant emprunté le plus de livres:")
    for user in count[:3]:  #same as "for i in range(min(3, len(utilisateurs_actifs))):"
        user_id, nom, prenom, emprunts_count = user
        print(f"ID: {user_id}, Nom: {nom}, Prénom: {prenom}, Nombre de livres empruntés: {emprunts_count}")
    print(count)
    return count


def afficher_statistiques (books, users, loans):
    # 1. Nombre total de livres
    total_livres = len(books)

    # 2. Nombre total d’exemplaires empruntés
    total_empruntes = 0
    for book in books:
        total_empruntes += books[book]["Emprunts"]

    # 3. Pourcentage d’exemplaires actuellement disponibles
    total_exemplaires = 0
    total_empruntes = 0
    for book in books:
        total_empruntes += books[book]["Emprunts"]
        total_exemplaires += books[book]["Exemplaires"]

        if total_exemplaires == 0:
            print("La bibliothèque est vide. Impossible de calculer le pourcentage d'exemplaires actuellement disponibles.")
            return
    pourcentage_exemplaires_disponibles =  (total_exemplaires / total_livres) * 100

    # 4. Nombre moyen de livres empruntés par utilisateur
    total_users = len(users)
    if total_users == 0:
        print("La bibliothèque est vide. Impossible de calculer le nombre moyen de livres empruntés par utilisateur.")
        return
    moyenne_emprunts_utilisateur = total_empruntes / total_users

    # Affichage des résultats
    print(f"Statistiques de la bibliothèque:")
    print(f"Nombre total de livres: {total_livres}")
    print(f"Nombre total d'exemplaires empruntés: {total_empruntes}")
    print(f"Pourcentage d'exemplaires actuellement disponibles: {pourcentage_exemplaires_disponibles:.2f}%")
    print(f"Nombre moyen de livres empruntés par utilisateur: {moyenne_emprunts_utilisateur:.2f}")
    return books, users,loans

def sauvegarder_loans(loans,fichier="loans.json"):
    with open(fichier,"w") as file:
        json.dump(loans,file,indent=4)
    print("Les emprunts ont bien été sauvegardés.")
"""
def charger_loans(fichier="loans.json"):
    global loans
    with open(fichier, "r") as file:
        loans = json.load(file)
    print("Les emprunts ont bien été chargés.")
    print(loans)
"""
def charger_loans(fichier="loans.json"):
    try:
        with open(fichier, "r") as file:
            loans = json.load(file)
            if loans is None:  # Check if the file is empty or invalid
                raise ValueError("Le fichier loans.json est vide ou invalide.")
            print("Les emprunts ont bien été chargés.")
            print(loans)
            return loans
    except FileNotFoundError:
        print(f"Erreur: Le fichier {fichier} n'a pas été trouvé.")
        loans = []  # Set loans to an empty list to avoid errors in the program
    except json.JSONDecodeError:
        print("Erreur: Le fichier loans.json est mal formaté.")
        loans = []  # Set loans to an empty list
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        loans = []  # Set loans to an empty list





