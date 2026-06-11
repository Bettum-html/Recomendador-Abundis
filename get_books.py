import os
import requests
from bs4 import BeautifulSoup

def get_links(n: int | list[int] = -1) -> tuple[ list[str], list[str] ]:
    """Obtiene los urls y los nombres de los libros del proyecto de Gutenberg
    deseados.

    Los libros se encuentran en formato txt bajo la sección descargados
    frecuentemente en:
        https://www.gutenberg.org/browse/scores/top.

    Los números `n` deben corresponder a los números en esta lista (empezando
    con uno).

    Parameters
    ----------
    n : int | list[int], optional
        Un entero o lista de enteros con los números de libros deseados.
        Escoge -1 (default) si se desean todos los libros.

    Returns
    -------
    links : list[str]
        Ligas a los archivos txt de los libros.
    titles : list[str]
        Títulos de los libros.
    """
    # URL para conseguir los libros
    url = "https://www.gutenberg.org/browse/scores/top"
    # los vinculos y los titulos deben ser inicializados (empiezan como listas vacias)
    links = [] 
    titles = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status()
        parser = BeautifulSoup(response.text, 'html.parser')
        # para procurar las etiquetas "a" del html
        etiquetas = parser.find_all("a")
        libros_validados = 0
        if isinstance(n, (list, range)):
            n = set(n)
        ids_repetidos = set()
        for link in etiquetas:
            direccion_libro = link.get("href", "")
            # Filtrador de contenido
            if direccion_libro.startswith("/ebooks/"):
                book_id = direccion_libro.split("/")[-1]
                # contamos unicamente un libro si confirmamos que tiene un ID numerico y no se ha erpetido
                if book_id.isdigit() and book_id not in ids_repetidos:
                    ids_repetidos.add(book_id)  # se le implementa una ID aparte para evitar repeticiones
                    libros_validados += 1
                    # con esto se sabe cuantos libros van a ser descargados, depende del numero que quiera usted agregar 
                    #(siendo en este ejemplo 50, va a descargar 50)
                    if n == -1 or (isinstance(n, int) and libros_validados <= n) or (isinstance(n, set) and libros_validados in n):   
                        # Generamos el URL necesario para la descarga
                        txt_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
                        titulo_libro = link.get_text(strip = True)
                        # filtro de caracteres especiales en los titulos
                        titulo_filtrado = "".join(caracter for caracter in titulo_libro if caracter.isalnum() or caracter in "._- ").rstrip()
                        titulo_libro = f"{titulo_filtrado[:50]}.txt"  #son convertidos en formato texto
                        """
                        en este caso los links y los titulos ya estarian completamente filtrados en las variables, siendo estos agregados
                        al final de su lista
                        """
                        links.append(txt_url)
                        titles.append(titulo_libro)

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")
        
    return links, titles

def download_file(url, name, directory):
    """Guarda un archivo que se encuentra en un `url` bajo el nombre que demos
    en `name` en el directorio deseado.
    """
    # Crear el directorio si no existe
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    ruta_exitosa = os.path.join(directory, name)
    
    try:
        # Direccion principal
        response = requests.get(url, stream=True)
        if response.status_code == 404:
            #Obtenemos el ID del libro directamente desde nuestro URL
            book_id = url.split("/")[-2] 
            
            # Creamos un link extra
            url_extra = f"https://gutenberg.org{book_id}/{book_id}-0.txt"
            
            # Reintentamos la petición con la nueva dirección
            response = requests.get(url_extra, stream=True)
            
        # en caso de que haya de nuevo error pasamos directamente a except
        response.raise_for_status() 
        
        # el archivo se guardaria en fragmentos
        with open(ruta_exitosa, mode='wb') as file:
            for chunk in response.iter_content(chunk_size=20 * 1024):  # 20kb de chunks
                file.write(chunk)
        print(f"archivo descargado exitosamente!!!: {ruta_exitosa}")
        
    except requests.exceptions.RequestException:
        print(f"La descarga fue un fracaso!!! :( : {name}")

def store_files(links, names, directory='./'):
    """Guarda cada liga de la lista de ligas `links` en la computadora
    utilizando el directorio deseado y cada uno de los nombres en names.
    """
    for url, name in zip(links, names):
        download_file(url, name, directory)

def main(n = -1, directory='./'):
    links, titles = get_links(n)
    store_files(links, titles, directory)
    print("Done")

if __name__ == '__main__':
    directory = 'Books/'
    n = range(1) # es la cantidad de libros que se van a descargar
    main(n, directory)
