import matplotlib.pyplot as plt
from datetime import datetime


def visualize_loans_by_genre(books, loans):
    genre_counts = {}

    # pulling data from loans and books
    for loan in loans:
        book_title = loan['Livre']
        genre = books[book_title]['Genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Sorting
    genres = list(genre_counts.keys())
    counts = list(genre_counts.values())

    # Pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(counts, labels=genres, autopct='%1.1f%%')
    plt.title('Répartition des Emprunts par Genre')

    # Legend
    plt.legend(genres, title="Genres", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))

    plt.axis('equal')
    plt.show()


def visualize_monthly_loans(loans):
    # Current year
    current_year = datetime.now().year

    # Number of month
    monthly_loans = {month: 0 for month in range(1, 13)}

    # Loan data per month
    for loan in loans:
        loan_date = datetime.strptime(loan['Date_Emprunt'], '%Y-%m-%d')
        if loan_date.year == current_year:
            monthly_loans[loan_date.month] += 1

    # Data
    months = range(1, 13)
    loan_counts = [monthly_loans[month] for month in months]
    month_names = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']

    # Chart
    plt.figure(figsize=(12, 6))
    plt.plot(months, loan_counts, marker='o', linewidth=2, markersize=8)

    # Customizing the chart
    plt.title(f'Évolution des Emprunts Mensuels {current_year}')
    plt.xlabel('Mois')
    plt.ylabel('Nombre d\'Emprunts')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(months, month_names, rotation=45)

    # Add labels
    for i, count in enumerate(loan_counts, 1):
        plt.annotate(str(count), (i, count), textcoords="offset points",
                     xytext=(0, 10), ha='center')

    plt.tight_layout()
    plt.show()
