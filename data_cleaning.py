import pandas as pd

# Asegúrate de que los nombres de los archivos sean correctos
books_file = 'bookList.csv'
reviews_file = 'bookReview.csv'

# Cargar datasets
try:
    books = pd.read_csv(books_file, encoding='latin1')
    reviews = pd.read_csv(reviews_file, encoding='latin1')
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Asegúrate de que los archivos CSV estén en la misma ruta que este script.")
    exit(1)

# Limpiar caracteres extraños en columnas de texto
books['title'] = books['title'].str.encode('latin1').str.decode('utf-8')
books['subtitle'] = books['subtitle'].str.encode('latin1').str.decode('utf-8')
books['authors'] = books['authors'].str.encode('latin1').str.decode('utf-8')

# Limpiar la columna 'published_date'
# Primero aseguramos que los datos estén en formato de texto para poder manipularlos
books['published_date'] = books['published_date'].astype(str)

# Función para limpiar la fecha
def clean_date(date):
    # Intenta encontrar solo el año
    year_part = date.split('-')[0]  # Divide la fecha por el guion y toma el primer elemento
    return year_part

# Aplicar la función de limpieza a la columna 'published_date'
books['published_date'] = books['published_date'].apply(clean_date)

# Revisar los datos
print("Primeras filas de books:")
print(books.head())
print("\nPrimeras filas de reviews:")
print(reviews.head())

# Guardar los datos limpios para su uso posterior
clean_books_file = 'clean_books.csv'
clean_reviews_file = 'clean_reviews.csv'

books.to_csv(clean_books_file, index=False)
reviews.to_csv(clean_reviews_file, index=False)

print(f"Datos limpios guardados en {clean_books_file} y {clean_reviews_file}")
