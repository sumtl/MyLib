

#import json
from loans import *
#from datetime import datetime


def demander_confirmation(message):
    # Boucle infinie pour demander une réponse valide
    while True:
        # Demande une réponse à l'utilisateur et la convertit en minuscule
        response = input(message).lower()

        # Si l'utilisateur répond "o", retourner True
        if response == "o":
            return True
        # Si l'utilisateur répond "n", retourner False
        elif response == "n":
            return False
        # Si la réponse est invalide, afficher un message d'erreur
        else:
            print("Entrée invalide, veuillez répondre par 'o' ou 'n'.")



#Voici la fonction pour ajouter un livre!
def ajouter_livres(books):
    while True:

        # On demande d'entrer le nom du livre
        nom_item = input("Entrez le nom du livre (ou appuyez sur Entrée pour annuler): ").strip().title()

        # Si l'utilisateur ne veux plus ajouter de livre, il n'a qu'à écrire 'quitter'
        if nom_item =="":
            print("\nOpération annulée.")
            return books

        # Ici on collecte les informations du livre dans plusieurs variables
        auteur = input("Entrez le nom de l'auteur du livre: ").strip().title()
        genre = input("Entrez le genre du livre: ").strip().capitalize()

 #  Vérifie si le nombre d'exemplaires est un entier valide
        while True:
            exemplaires = input("Entrez le nombre d'exemplaires: ").strip()
            if exemplaires.isdigit():
                exemplaires = int(exemplaires)
                break
            else:
                print("\nErreur: Veuillez entrer un nombre entier pour le nombre d'exemplaires.\n")

        # Dans la variable item, on crée un dictionnaire pour associer pass les valeurs précédemment collectées à leurs clés!
        item = {
            "Auteur": auteur,
            "Genre": genre,
            "Exemplaires": exemplaires,
            "Emprunts": 0
        }

        # Vérifie si l'auteur n'est pas déjà dans le dictionnaire books
        if nom_item not in books:
          # Demande une confirmation pour ajouter le livre
            if demander_confirmation (f"Voulez-vous ajouter le livre <{nom_item}> à la bibliothèque? (o/n): "):
              # Dans cette ligne de code on associe la clé nom_item avec la valeur item et on l'ajoute au dictionnaire de books !
                books[nom_item] = item
                print(f"\nLe livre <{nom_item}> a été ajouté à la bibliothèque.\n")

            else:
                # Annule l'ajout du livre
                print(f"\nl'ajout du livre <{nom_item}> a été annulée.\n")

        else:
            #Indique que le livre existe déjà
            print(f"\nLe livre <{nom_item}> existe déjà dans la bibliothèque.")
        print(books)
        return books


#Voici la fonction pour supprimer un livre de l'inventaire!
def supprimer_livres(books,loans):
 #(Wansu)
    # Vérifie si la bibliothèque est vide
    if books == {}:
        print("\nAucun livre dans la bibliothèque.")
        return books

    while True:

        livre_supprimer = input("Quel est le nom du livre a supprimer?: ").strip().title()
        #On verifi pour voir si le livre est dans l'inventaire ou non
        if livre_supprimer not in books:
            print("Ce livre ne figure pas dans la liste")
        else:
            #Si oui alors le delete et on update l'inventaire
            # Vérifier si le livre est actuellement emprunté
            livre_emprunté = False
            for loan in loans:
                if loan["Livre"] == livre_supprimer and loan["Date_Retour"] is None:
                    livre_emprunté = True
                    break  # Le livre est emprunté, on sort de la boucle

            if livre_emprunté:
                print(f"Ce livre '{livre_supprimer}' est actuellement emprunté et ne peut pas être supprimé.")

            else:
                # Demande une confirmation avant de supprimer le livre
                if demander_confirmation(f"\nVoulez-vous vraiment supprimer <{livre_supprimer}> ? (o/n):"):
                    del books[livre_supprimer]
                    print(f"\nLe livre {livre_supprimer} a ete supprime avec succes\n")

                else:
                    # Annule la suppression si l'utilisateur change d'avis
                    print(f"\nLa suppression du <{livre_supprimer}> a été annulée.\n")

        print(books)
        return books,loans


def sauvegarder_books(books,fichier ="books.json"):
    with open(fichier,"w") as f:
        json.dump(books,f,indent=4)
    print("Les livres ont bien été sauvegardés.")

"""
def charger_books(fichier="books.json"):
    global books
    with open(fichier,"r")as f:
        books = json.load(f)
    print("Les livres ont bien été chargés.")

"""
def charger_books(fichier="books.json"):
    try:
        with open(fichier, "r") as file:
            books = json.load(file)
        print("Les livres ont bien été chargés.")
        print(books)# Debugging: Afficher les livres chargés
        print(type(books))
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier} n'a pas été trouvé.")
        books = {}  # Si le fichier n'existe pas, on initialise books comme un dictionnaire vide
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {fichier} n'est pas un fichier JSON valide.")
        books = {}  # Si le fichier n'est pas un JSON valide, on initialise books comme un dictionnaire vide
    except Exception as e:
        print(f"Erreur inconnue lors du chargement de {fichier}: {e}")
        books = {}
    return books


