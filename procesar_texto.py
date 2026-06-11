import preprocesado
import nltk #recomendacion que se nos dió
from nltk.corpus import stopwords #recomendacion que se nos dió

def main(filename: str) -> dict[str, int]:
    # Definir lista con caracteres especiales.
    # Utilizar los caracteres dados por `punctuation` en la librería `string`
    from string import punctuation
    caracteres_especiales = punctuation
    # Definir lista con stopwords
    # Utilizar los stopword en inglés dados en la librería nltk (como vimos en
    # clase).
    # stopwords = ...
    # Descargar los stopwords
    try:
        nltk.data.find('corpora/stopwords') #para procurar que está descargado
    except LookupError:
        nltk.download('stopwords') #se es instalado en caso de no estar descargado
    stopwords_english = set(stopwords.words('english'))
    stopwords_spanish = set(stopwords.words('spanish'))
    """
        se unen para poder ingresar ambas stopwords, haciendo su filtracion aun más efectiva
    """ 
    stopwords_adjuntas = stopwords_english | stopwords_spanish 
    

    # Leer el libro utilizando función correspondiente del módulo `preprocesado`
    libro_lineas = preprocesado.leer_libro(filename)

    # Preprocesar el libro obteniendo un diccionario de palabras relevantes y
    # sus frecuencias y retornar este resultado.
    # Debes utilizar el método correspondiente en `preprocesado`.
    frecuencia = preprocesado.preprocesar_libro(libro_lineas, caracteres_especiales, stopwords_adjuntas)
    return frecuencia

if __name__ == '__main__':
    # Definir a continuación `filename`
    # filename = ...
    filename = "Dracula by Bram Stoker 2471.txt"
    # Ahora descomenta la línea de abajo
    frecuencia = main(filename)
    """
        en base a las primeras 300 palabras en la lista veremos la frecuencia de cada una
    """
    print("Palabras cargadas con exito!!!")
    for palabra in list(frecuencia.keys())[:300]:
        print(f"{palabra}: {frecuencia[palabra]}") 
    # Una vez llenado el módulo preprocesado y este script, puedes ejecutarlo
    # escribiendo en la terminal
    # python procesar_texto 