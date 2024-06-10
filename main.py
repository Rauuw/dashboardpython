from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = FastAPI()

# Cargar los datos limpios
books = pd.read_csv('clean_books.csv')
reviews = pd.read_csv('clean_reviews.csv')

# Convertir 'published_date' a tipo fecha, manejando errores y convirtiendo a datetime
books['published_date'] = pd.to_datetime(books['published_date'], errors='coerce')

# Merge de los DataFrames 'books' y 'reviews' por 'id'
merged_data = pd.merge(books, reviews, on='id', how='left')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
def get_books():
    return books.to_dict(orient='records')

@app.get("/reviews")
def get_reviews():
    return reviews.to_dict(orient='records')

@app.get("/books/ratings")
def get_books_by_ratings():
    books_ratings = merged_data.groupby(['id', 'title']).agg({'rating': 'mean', 'text_review': 'count'}).reset_index()
    return books_ratings.to_dict(orient='records')

@app.get("/books/year")
def get_books_by_year():
    # Convertir 'published_date' para asegurarse de que está en un formato datetime adecuado
    books['published_date'] = pd.to_datetime(books['published_date'], errors='coerce')
    # Extraer el año de la fecha publicada
    books['year'] = books['published_date'].dt.year

    books_by_year = books.groupby('year').size().reset_index(name='count')
    return books_by_year.to_dict(orient='records')

@app.get("/books/ratings/plot")
def plot_books_by_ratings():
    # Agrupar por la puntuación media para contar cuántos libros tienen cada puntuación
    books_ratings = merged_data.groupby('rating').size().reset_index(name='book_count')

    # Ordenar por rating para una mejor visualización
    books_ratings = books_ratings.sort_values(by='rating')

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(data=books_ratings, x='rating', y='book_count')
    plt.title('Libros por Puntuación \n (Objetivo, saber segun las reseñas el numero de libros \n con puntuacion mala para poder tener una idea clara de la opinion sobre los libros que se tienen en venta)')
    plt.xlabel('Puntuación')
    plt.ylabel('Número de Libros')

    # Guardar el gráfico como un archivo
    plot_file = 'books_by_ratings.png'
    plt.savefig(plot_file)
    plt.close()

    # Enviar el archivo de imagen como respuesta
    return FileResponse(plot_file, media_type='image/png', filename=plot_file)




@app.get("/books/year/plot")
def plot_books_by_year(start_year: int = Query(None), end_year: int = Query(None)):
    # Convertir 'published_date' para asegurarse de que está en un formato datetime adecuado
    books['published_date'] = pd.to_datetime(books['published_date'], errors='coerce')
    # Extraer el año de la fecha publicada
    books['year'] = books['published_date'].dt.year

    # Filtrar por el rango de años
    if start_year and end_year:
        books_filtered = books[(books['year'] >= start_year) & (books['year'] <= end_year)]
    else:
        books_filtered = books

    books_by_year = books_filtered.groupby('year').size().reset_index(name='count')

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=books_by_year, x='year', y='count', marker='o')
    plt.title('Número de Libros publicados por Año \n (Objetivo: Saber el numero de libros por año que se tiene para comprar licencias de venta de libros actuales)')
    plt.xlabel('Año')
    plt.ylabel('Número de Libros')



    plot_file = 'books_by_year.png'
    plt.savefig(plot_file)
    plt.close()

    return FileResponse(plot_file, media_type='image/png', filename=plot_file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
