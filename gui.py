import tkinter as tk
from tkinter import ttk, messagebox
from books import *
from users import *
from loans import *
from data import *
from visualizations import *
from datetime import datetime


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bibliotheque - Système de Gestion de Bibliothèque")
        self.root.geometry("800x600")

        self.books, self.users, self.loans = charger_csv()
        self.id_users = 0

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(self.main_frame, text="Biblio", font=('Helvetica', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.create_main_buttons()

    def create_main_buttons(self):
        buttons = [
            ("Gérer les Livres", self.show_books_menu),
            ("Gérer les Utilisateurs", self.show_users_menu),
            ("Gérer les Emprunts", self.show_loans_menu),
            ("Livres les Plus Empruntés", self.show_most_borrowed),
            ("Durée Moyenne par Genre", self.show_duration_by_genre),
            ("Utilisateurs les Plus Actifs", self.show_active_users),
            ("Statistiques Bibliothèque", self.show_statistics),
            ("Visualisation par Genre", self.show_genre_visualization),
            ("Évolution Mensuelle", self.show_monthly_visualization)
        ]

        for idx, (text, command) in enumerate(buttons, 1):
            btn = ttk.Button(self.main_frame, text=text, command=command)
            btn.grid(row=idx, column=0, columnspan=2, pady=5, padx=20, sticky="ew")

    def show_books_menu(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Gestion des Livres")
        dialog.geometry("400x300")

        ttk.Button(dialog, text="Ajouter un Livre",
                   command=lambda: self.show_add_book_form(dialog)).pack(pady=10)
        ttk.Button(dialog, text="Supprimer un Livre",
                   command=lambda: self.show_delete_book_form(dialog)).pack(pady=10)

    def show_add_book_form(self, parent):
        form = tk.Toplevel(parent)
        form.title("Ajouter un Livre")

        fields = {'Titre': '', 'Auteur': '', 'Genre': '', 'Exemplaires': ''}
        entries = {}

        for i, (field, default) in enumerate(fields.items()):
            ttk.Label(form, text=field).grid(row=i, column=0, pady=5, padx=5)
            entries[field] = ttk.Entry(form)
            entries[field].insert(0, default)
            entries[field].grid(row=i, column=1, pady=5, padx=5)

        def submit():
            book_data = {
                'Titre': entries['Titre'].get(),
                'Auteur': entries['Auteur'].get(),
                'Genre': entries['Genre'].get(),
                'Exemplaires': int(entries['Exemplaires'].get()),
                'Emprunts': 0
            }
            self.books[book_data['Titre']] = book_data
            sauvegarder_csv(self.books, self.users, self.loans)
            messagebox.showinfo("Succès", "Livre ajouté avec succès!")
            form.destroy()

        ttk.Button(form, text="Ajouter", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def show_delete_book_form(self, parent):
        form = tk.Toplevel(parent)
        form.title("Supprimer un Livre")

        ttk.Label(form, text="Titre du livre:").pack(pady=5)
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(form, textvariable=book_var)
        book_combo['values'] = list(self.books.keys())
        book_combo.pack(pady=5)

        def delete():
            title = book_var.get()
            if title in self.books:
                del self.books[title]
                self.loans = [loan for loan in self.loans if loan['Livre'] != title]
                sauvegarder_csv(self.books, self.users, self.loans)
                messagebox.showinfo("Succès", "Livre supprimé avec succès!")
                form.destroy()

        ttk.Button(form, text="Supprimer", command=delete).pack(pady=10)

    def show_delete_user_form(self, parent):
        form = tk.Toplevel(parent)
        form.title("Supprimer un Utilisateur")

        # Ajout d'un case de recherche
        search_frame = ttk.Frame(form)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Rechercher par nom ou ID:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Selection d'utilisateur
        ttk.Label(form, text="Sélectionner l'utilisateur:").pack(pady=5)
        user_var = tk.StringVar()
        user_combo = ttk.Combobox(form, textvariable=user_var, width=50)

        # Limiter la selection a 20, pour pas depasser la limite de l'ecran
        initial_values = [f"{user['Nom']} {user['Prénom']} (ID: {user_id})"
                          for user_id, user in list(self.users.items())[:20]]
        user_combo['values'] = initial_values
        user_combo.pack(pady=5)

        def search_user(*args):
            search_term = search_var.get().lower()
            filtered_users = [
                f"{user['Nom']} {user['Prénom']} (ID: {user_id})"
                for user_id, user in self.users.items()
                if search_term in user['Nom'].lower() or
                   search_term in user['Prénom'].lower() or
                   search_term in str(user_id).lower()
            ]
            # Limit de 20, pour pas depasser la limite de l'ecran
            user_combo['values'] = filtered_users[:20]

            if filtered_users:
                user_combo.set(filtered_users[0])

        search_var.trace('w', search_user)

        def delete():
            selected = user_var.get()
            if selected:
                user_id = selected.split("(ID: ")[1].rstrip(")")
                if user_id in self.users:
                    del self.users[user_id]
                    self.loans = [loan for loan in self.loans if loan['Utilisateur_ID'] != user_id]
                    sauvegarder_csv(self.books, self.users, self.loans)
                    messagebox.showinfo("Succès", "Utilisateur supprimé avec succès!")
                    form.destroy()

        ttk.Button(form, text="Supprimer", command=delete).pack(pady=10)

    def show_users_menu(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Gestion des Utilisateurs")
        dialog.geometry("400x300")

        ttk.Button(dialog, text="Ajouter un Utilisateur",
                   command=lambda: self.show_add_user_form(dialog)).pack(pady=10)
        ttk.Button(dialog, text="Supprimer un Utilisateur",
                   command=lambda: self.show_delete_user_form(dialog)).pack(pady=10)

    def show_add_user_form(self, parent):
        form = tk.Toplevel(parent)
        form.title("Ajouter un Utilisateur")

        fields = {'Nom': '', 'Prénom': '', 'Email': '', 'Téléphone': ''}
        entries = {}

        for i, (field, default) in enumerate(fields.items()):
            ttk.Label(form, text=field).grid(row=i, column=0, pady=5, padx=5)
            entries[field] = ttk.Entry(form)
            entries[field].insert(0, default)
            entries[field].grid(row=i, column=1, pady=5, padx=5)

        def submit():
            user_data = {
                'Nom': entries['Nom'].get(),
                'Prénom': entries['Prénom'].get(),
                'Email': entries['Email'].get(),
                'Téléphone': entries['Téléphone'].get(),
                'Emprunts': 0,
                'ListeLivreLu': []
            }
            self.id_users += 1
            self.users[str(self.id_users)] = user_data
            sauvegarder_csv(self.books, self.users, self.loans)
            messagebox.showinfo("Succès", "Utilisateur ajouté avec succès!")
            form.destroy()

        ttk.Button(form, text="Ajouter", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def show_loans_menu(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Gestion des Emprunts")
        dialog.geometry("400x300")

        ttk.Button(dialog, text="Enregistrer un Emprunt",
                   command=lambda: self.show_loan_form(dialog)).pack(pady=10)
        ttk.Button(dialog, text="Enregistrer un Retour",
                   command=lambda: self.show_return_form(dialog)).pack(pady=10)

    def show_loan_form(self, parent):
        form = tk.Toplevel(parent)
        form.title("Enregistrer un Emprunt")

        ttk.Label(form, text="Utilisateur:").grid(row=0, column=0, pady=5)
        user_var = tk.StringVar()
        user_combo = ttk.Combobox(form, textvariable=user_var)
        user_combo['values'] = [f"{user['Nom']} {user['Prénom']} (ID: {user_id})"
                                for user_id, user in self.users.items()]
        user_combo.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Livre:").grid(row=1, column=0, pady=5)
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(form, textvariable=book_var)
        book_combo['values'] = [title for title, book in self.books.items()
                                if book['Exemplaires'] > 0]
        book_combo.grid(row=1, column=1, pady=5)

        def submit():
            selected_user = user_var.get()
            book_title = book_var.get()

            if selected_user and book_title:
                user_id = selected_user.split("(ID: ")[1].rstrip(")")

                if book_title in self.books and self.books[book_title]['Exemplaires'] > 0:
                    # Initialize Emprunts if not present
                    if 'Emprunts' not in self.users[user_id]:
                        self.users[user_id]['Emprunts'] = 0

                    loan = {
                        'Utilisateur_ID': user_id,
                        'Livre': book_title,
                        'Date_Emprunt': datetime.now().strftime("%Y-%m-%d"),
                        'Date_Retour': None
                    }
                    self.loans.append(loan)
                    self.books[book_title]['Exemplaires'] -= 1
                    self.books[book_title]['Emprunts'] += 1
                    self.users[user_id]['Emprunts'] += 1
                    sauvegarder_csv(self.books, self.users, self.loans)
                    messagebox.showinfo("Succès", "Emprunt enregistré avec succès!")
                    form.destroy()

        ttk.Button(form, text="Enregistrer", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

    def show_return_form(self, parent):
        form = tk.Toplevel(parent)
        form.title("Enregistrer un Retour")

        active_loans = [loan for loan in self.loans if loan['Date_Retour'] is None]

        ttk.Label(form, text="Sélectionner l'emprunt:").pack(pady=5)
        loan_var = tk.StringVar()
        loan_combo = ttk.Combobox(form, textvariable=loan_var)
        loan_combo['values'] = [f"{loan['Utilisateur_ID']} - {loan['Livre']}" for loan in active_loans]
        loan_combo.pack(pady=5)

        def submit():
            selected = loan_combo.get()
            if selected:
                user_id, book_title = selected.split(" - ")
                for loan in self.loans:
                    if loan['Utilisateur_ID'] == user_id and loan['Livre'] == book_title and loan[
                        'Date_Retour'] is None:
                        loan['Date_Retour'] = datetime.now().strftime("%Y-%m-%d")
                        self.books[book_title]['Exemplaires'] += 1
                        sauvegarder_csv(self.books, self.users, self.loans)
                        messagebox.showinfo("Succès", "Retour enregistré avec succès!")
                        form.destroy()
                        break

        ttk.Button(form, text="Enregistrer", command=submit).pack(pady=10)

    def show_most_borrowed(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Livres les Plus Empruntés")

        borrowed_books = list_most_borrowed_books(self.books)
        for book, count in borrowed_books:
            ttk.Label(dialog, text=f"{book}: {count} emprunts").pack(pady=5)

    def show_duration_by_genre(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Durée Moyenne des Emprunts par Genre")

        genre_durations = calculate_average_loan_duration_by_genre(self.books, self.loans)

        # Display results in the dialog window
        for genre, stats in genre_durations.items():
            if stats["count"] > 0:
                avg_duration = stats["total_duration"] / stats["count"]
                ttk.Label(dialog,
                          text=f"Genre {genre}: {avg_duration:.1f} jours").pack(pady=5)

    def show_active_users(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Utilisateurs les Plus Actifs")

        active_users = list_most_active_users(self.users)
        #for user_id, loan_count in active_users:
        for user_id, nom, prenom, loan_count in active_users:  # Update to unpack four values(new modified)
            user_info = self.users[user_id]
            ttk.Label(dialog,
                      text=f"{user_info['Nom']} {user_info['Prénom']}: {loan_count} emprunts").pack(pady=5)

    def show_statistics(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Statistiques de la Bibliothèque")

        stats = afficher_statistiques(self.books, self.users, self.loans)
        books, users, loans = stats

        # Calculate total books and copies
        total_livres = len(books)
        total_empruntes = sum(book["Emprunts"] for book in books.values())

        # Calculate available books percentage
        livres_disponibles = sum(1 for book in books.values() if book["Exemplaires"] > 0)
        pourcentage_exemplaires_disponibles = (livres_disponibles / total_livres) * 100 if total_livres > 0 else 0

        # Calculate average loans per user
        total_users = len(users)
        moyenne_emprunts_utilisateur = total_empruntes / total_users if total_users > 0 else 0

        # Display all statistics
        ttk.Label(dialog, text=f"Nombre total de livres: {total_livres}").pack(pady=5)
        ttk.Label(dialog, text=f"Nombre total d'exemplaires empruntés: {total_empruntes}").pack(pady=5)
        ttk.Label(dialog,
                  text=f"Pourcentage d'exemplaires disponibles: {pourcentage_exemplaires_disponibles:.2f}%").pack(
            pady=5)
        ttk.Label(dialog,
                  text=f"Nombre moyen de livres empruntés par utilisateur: {moyenne_emprunts_utilisateur:.2f}").pack(
            pady=5)

    def show_genre_visualization(self):
        visualize_loans_by_genre(self.books, self.loans)

    def show_monthly_visualization(self):
        visualize_monthly_loans(self.loans)


def main():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()