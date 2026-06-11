import math
"""
    en este apartado ya tendriamos que calcular el peso para conseguir el TF-IDF que necesitamos en
    el código.
"""
class Recomendador:
    def __init__(self, libros) -> None:
        """
        libros: lista con instancias de tipo `Libro`
        """
        self.libros = libros
        self._pesos = None  # Se calcularan con un setter (ver `set_pesos`)

    def set_pesos(self) -> None:
        """Calcula los pesos del algorítmo TF-IDF requeridos para las
        recomendaciones y los guarda en `self._pesos`

        """
        """
            En base a TODAS las frecuencias que tienen las palabras de cada uno de los libro 
            procesados durante todo lo que se realizó con el codigo de ahi realizariamos el
            Preproceso de todos los libros para que vaya a regresar una lista de diccionarios con sus 
            respectivas frecuencias
        """
        frecuencia_libros = [libro.preprocesar_libro() for libro in self.libros]
        cantidad_documentos = len(self.libros) #esto servirá para ver cuantos libros tendriamos en total
        """
            Ahora tomariamos en cuenta la frecuencia de cada palabra en los libros
            (o como nuestro maestro nos mencionó en su clase: "el Document Frequency")
            iniciando ya el conteo dentro del diccionario vacio:
            1 -   En el primer "for" interno al diccionario se cuenta cuantas veces 
                aparece una palabra en distintos libros.
            2 -   Despues de realizar el conteo se calcula la matriz de pesos finales (TF-IDF)
                como lista vacia, inicializando de igual forma como lista vacia el peso de los libros.
            3 -   Con eso ya calculariamos el TF normalizado (qué tan frecuente es una palabra 
                en un documento) y su IDF (que tan rara o comun es la palabra en toda la biblioteca de palabras
                en nuestra lista)
            4 - al terminar los pasos ya se realiza la formula para calcular el peso final, que justamente es eñ
            producto de los componentes "tf" e "idf"
        """
        conteo_por_palabra = {}
        for diccionario in frecuencia_libros:
            for palabra in diccionario.keys():
                conteo_por_palabra[palabra] = (conteo_por_palabra.get(palabra, 0) + 1)

        self._pesos = []
        for diccionario in frecuencia_libros:
            pesos_libro = {} 
            maximo_tf = max(diccionario.values()) if diccionario else 1
            for palabra, tf in diccionario.items():
                tf_normalizado = tf / maximo_tf
                df = conteo_por_palabra[palabra]
                idf = math.log10(cantidad_documentos / df)
                pesos_libro[palabra] = tf_normalizado * idf
            """
                Al finalizar toda la operación se terminaria ya añadiendo los pesos a su
                lista designada
            """
            self._pesos.append(pesos_libro)

    def get_pesos(self):
        """Regresa los pesos calculados"""
        return self._pesos

    def _producto_punto(self, idx_1:int, idx_2:int) -> float:
        """Producto punto entre los libros con índices idx_1 y idx_2."""
        # los productos son los mismos diccionarios de pesos que se usaran para los dos libros
        # que vamos a comparar.
        pesos_libro1 = self._pesos[idx_1] #ingresamos el primer libro
        pesos_libro2 = self._pesos[idx_2] #aqui viene el segundo a comparar con el primero
        # para esto necesitamos un contador,que justamente es el resultado
        resultado = 0.0
        # recorremos sobre las palabras del primer libro
        for palabra, peso1 in pesos_libro1.items():
            # multiplicamos los pesos de la palabra en caso de que sea existente en los dos libros
            if palabra in pesos_libro2:
                peso2 = pesos_libro2[palabra]
                resultado += peso1 * peso2
        # con eso ya tendriamos el resultado, el cual será enviado con un "return"
        return resultado

    def _similitud(self, idx_1, idx_2) -> float:
        """Similitud entre los libros con índices idx_1 y idx_2 de acuerdo al
        coseno del ángulo que forman sus vectores.

        """
        # cuando solicites dos libros con una similitud exacta (o en un caso más creible: comparas 
        # el libros consigo mismo) te regresa un 1.0 (similitud del 100%)
        if idx_1 == idx_2:
            return 1.0
        """
            ya en otro caso se realiza lo siguiente:
            - obtenemos su producto punto (la relación matemática que hay entre los libros)
            - calculamos la magnitus del vector que tiene el libro numero 1
            - se hace la suma de los cuadrados de todos los pesos que tiene para poder realizar la raiz cuadrada
            - ahora entonces conseguimos la norma del vector que tiene el libro 2
        """
        producto_punto = self._producto_punto(idx_1, idx_2)
        norma_libro_uno = math.sqrt(sum(peso**2 for peso in self._pesos[idx_1].values()))
        norma_libro_dos = math.sqrt(sum(peso**2 for peso in self._pesos[idx_2].values()))
        # En este caso es importante evitar que alguna de las normas genere un error por ser de valor 
        # nulo (0), asi que optamos por condicionarlo para que simplemente de 0
        if norma_libro_uno == 0 or norma_libro_dos == 0:
            return 0.0
        
        #  Pasamos a hacer la formula del coseno 
        """ 
        Cos(producto_punto) = Cateto Adyacente(norma_libro_uno) \ Hipotenusa(norma_libro_dos)
        """
        return producto_punto / (norma_libro_uno * norma_libro_dos)

    def mostrar_libros(self):
        """Mostrarle al usuario el índice y nombre para cada libro de acuerdo a
        nuestra lista de libros `self.libros`.

        """
        print("\n-|-|- CATELOGO DE LIBROS-|-|-")
        for idx, libro in enumerate(self.libros):
            # gracias a ese "enumerate" podriamos ya mostrar el índice y el nombre del libro
            print(f" Indice [{idx}]: {libro.name}")
        print(".- " * 40) #separacion

    def resumen(self, idx_libro, num_palabras) -> list[str]:
        """Regresa una lista con las palabras más representativas de un libro
        de acuerdo a los pesos.

        idx_libro: índice del libro cuyo resumen deseamos.
        num_palabras: número de palabras en el resumen.

        """
        # Realizamos ya la extracción el diccionario de pesos TF-IDF para el libro solicitado
        pesos_libro = self._pesos[idx_libro]
        """
            Ordenamos las palabras de mayor a menor basandonos en su peso
            x[1] representa el peso TF-IDF en la tupla (palabra, peso)
            Por ejemplo: [('teeth', 0.39)] el [1] seria 0.39 por ser el peso del indice 1
            (hago uso de "key=lambda" como forma de atajo para menor complejidad dentro del código)
        """
        palabras_organizadas = sorted(pesos_libro.items(), key=lambda x: x[1], reverse=True)

        # Guardamos las palabras del top, ignorando el peso debido a que es solamente un auxiliar 
        # para desempacar.
        top_palabras = [palabra for palabra, peso in palabras_organizadas[:num_palabras]]

        return top_palabras

    def libros_similares(self, idx_libro, num_libros) -> list[str]:
        """Regresa una lista con los libros más parecidos a un libro dado.

        idx_libro: índice del libro a partir del cual quiero recomendaciones.
        num_libros: número de libros en mi recomendación.


        """
        lista_similitud = []
        """
            para finalizar, en esta lista de similitudes calculamos dicha similitud del 
            libro que queremos usar de referencia para recibir recomendaciones 
            para ya juntarlo con los otros de la biblioteca (ignorando o saltando los libros que tengan el 
            mismo valor. queremos libros semejantes, NO IGUALES) y, en base al metodo de similitud de coseno 
            (mencionado en clase) se guarda la información de el dato 
            (de tipo TUPLA, con el nombre del libro y su valor matematico) para ya tenerlo en la lista.

        """
        for idx_mas, libro_mas in enumerate(self.libros):
            # Saltamos la comparacion si es el mismo libro
            if idx_mas == idx_libro:
                continue
            valor_similitud = self._similitud(idx_libro, idx_mas)
            lista_similitud.append((libro_mas.name, valor_similitud))

        # la lista estará ordenada de mayor a menor basandonos en que tan similar es el
        # valor de similitud (el indice 1 de la tupla)
        lista_Descendiente = sorted(
            lista_similitud, key=lambda x: x[1], reverse=True
        )

        # Recortamos la lista para regresar solo el número de recomendaciones solicitado
        # Extraemos únicamente el nombre del libro (el indice 0 de la tupla)
        # num_libros es la cantidad de libros a tomar
        mas_recomendaciones_libro = [nombre for nombre, similitud in lista_Descendiente[:num_libros]]

        return mas_recomendaciones_libro