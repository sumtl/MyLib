
from books import *

from loans import *

"""
def main():
    books = charger_books("books.json")
    users = charger_users("users.json")
    print("Books loaded:", books)
    print("Users loaded:", users)
    loans = []
    loans, books, users = emprunts_livres(books, users, loans)
    sauvegarder_loans(loans)

""" 
def main():
    #books = {}
    #loans = []
    users = {}
    id_users = 0
    books=charger_books()
    users=charger_users()
    loans=charger_loans()

    while True:
        print("\n--- Menu Principal ---")
        print("1. Ajouter ou supprimer un livre")
        print("2. Ajouter ou supprimer un utilisateur")
        print("3. Enregistrer un emprunt ou un retour")
        print("4. Lister les livres les plus empruntés")
        print("5. Calculer la durée moyenne des emprunts par genre")
        print("6. Identifier les utilisateurs les plus actifs")
        print("7. Afficher le statut de la bibliothèque")
        print("8. Visualisation: Diagramme circulaire des emprunts par genre")
        print("9. Visualisation: Évolution mensuelle des emprunts")
        print("10. Quitter")
        choix = input("Choisissez une option: ")

        if not choix.isdigit() or int(choix) not in range(1,11):
            print("\nChoix invalide. Veuillez entrer un numéro valide entre 1 et 10.\n")
            continue

        choix = int(choix)

        if choix == 1:
            while True:
                print("Option 1\n ---Menu des livres---\n1: Ajouter. \n2: Supprimer. \n3. Revenir au menu principal.")
                sous_choix = input("\nEntrez votre choix ：\n")
                if sous_choix == "1":
                    books =ajouter_livres(books)
                    sauvegarder_books(books)
                elif sous_choix == "2":
                    books,loans = supprimer_livres(books,loans)
                    sauvegarder_books(books)
                elif sous_choix == "3":  
                    break
                else:   
                    print("\nChoix invalide. Veuillez entrer l'un des numéros suivants :1, 2 ou 3.\n")
                    continue
                sauvegarder_books(books)

        elif choix == 2:
            while True:  
                print(
                    "\nOption 2 \n--- Menu des utilisateur ---\n1: Ajouter. \n2: Supprimer. \n3. Revenir au menu principal.")
                sous_choix = input("\nEntrez votre choix : \n")
                if sous_choix == "1":
                    users, id_users = ajouter_users(users, id_users)
                    sauvegarder_users(users)
                elif sous_choix == "2":
                    users,loans = supprimer_users(users,loans)
                    sauvegarder_users(users)
                elif sous_choix == "3":
                    break
                else:
                    print("\nChoix invalide. Veuillez entrer l'un des numéros suivants :1, 2 ou 3.")
                    continue


        elif choix == 3:
            while True:
                print(
                    "\nOption 3 \nMenu de Enregistrer un emprunt ou un retour.\n1.Enregistrer un emprunt.\n2.Enregistrer un retour.\n3.Revenir au menu principal.")
                sous_choix = input("\nEntrez votre choix : \n")
                if sous_choix == "1":
                    books, users, loans = emprunts_livres(books, users, loans)
                    sauvegarder_loans(loans)
                    sauvegarder_users(users)
                    sauvegarder_books(books)
                elif sous_choix == "2":
                    books, users, loans = retour_livres(books, users, loans)
                    sauvegarder_loans(loans)
                    sauvegarder_users(users)
                    sauvegarder_books(books)
                elif sous_choix == "3":
                    break
                else:
                    print("\nChoix invalide. Veuillez entrer l'un des numéros suivants :1, 2 ou 3.\n")
                    continue


        elif choix == 4:
            borrowed_books =list_most_borrowed_books(books)

        elif choix == 5:
            genre_durations = calculate_average_loan_duration_by_genre(books,loans)

        elif choix == 6:
            active_users =list_most_active_users(users)

        elif choix == 7:
            books, users, loans = afficher_statistiques(books, users, loans)

        elif choix == 8:
            pass#visualize_loans_by_genre(library)

        elif choix == 9:
            pass#visualize_monthly_loans(library)


        elif choix == 10:
            pass#save_data(library)
            print("Données sauvegardées. Au revoir!")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()