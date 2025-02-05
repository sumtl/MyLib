import csv

def initialiser_csv():

    with open('livres.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Titre', 'Auteur', 'Genre', 'Exemplaires', 'Emprunts'])


    with open('utilisateurs.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Emprunts'])


    with open('emprunts.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Utilisateur_ID', 'Livre', 'Date Emprunt', 'Date Retour'])

    print("Les fichiers CSV ont bien été initialisés.")

def sauvegarder_csv(books, users, loans):

    with open('livres.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Titre', 'Auteur', 'Genre', 'Exemplaires', 'Emprunts'])
        for livre, details in books.items():
            writer.writerow([livre, details['Auteur'], details['Genre'], details['Exemplaires'], details['Emprunts']])


    with open('utilisateurs.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Emprunts' ])
        for user_id, user_info in users.items():
            writer.writerow([user_id, user_info['Nom'], user_info['Prénom'], user_info['Email'], user_info['Téléphone'], user_info['Emprunts']])

    if loans:
        with open('emprunts.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Utilisateur_ID', 'Livre', 'Date Emprunt', 'Date Retour'])
            for emprunt in loans:
                writer.writerow([emprunt['Utilisateur_ID'], emprunt['Livre'], emprunt['Date_Emprunt'], emprunt['Date_Retour']])

    print(" Données sauvegardées avec succès dans les fichiers CSV !")


def charger_csv():
    books = {}
    users = {}
    loans = []


    with open('livres.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            titre, auteur, genre, exemplaires, emprunts = row
            books[titre] = {
                'Auteur': auteur,
                'Genre': genre,
                'Exemplaires': int(exemplaires),
                'Emprunts': int(emprunts)
            }


    with open('utilisateurs.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            user_id, nom, prenom, email, telephone, emprunts  = row
            users[int(user_id)] = {
                    "Nom": nom,
                    "Prénom": prenom,
                    "Email": email,
                    "Téléphone": telephone,
                    "Emprunts": int(emprunts)
                }


    with open('emprunts.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            utilisateur, livre, date_emprunt, date_retour = row
            loans.append({
                'Utilisateur': utilisateur,
                'Livre': livre,
                'Date_Emprunt': date_emprunt,
                'Date_Retour': date_retour
            })

    print("Les données ont été chargées depuis les fichiers CSV.")
    return books, users, loans