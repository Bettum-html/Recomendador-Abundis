import get_books
import libros
import recomendaciones
from string import punctuation

carpeta_destino = "Books/"


def descargar_libros():
    """Opción numero 1: hay que descargar libros de Gutenberg"""
    print("°.-|.°-|°.-|°.- Bienvenido al panel de descarga de libros, usuario!!! :) °.-|.°-|°.-|°.-")

    while True:
        try:
            cantidad_libros = int(
                input("cual es la cantidad de libros que gusta descargar?: ").strip()
            )
            if cantidad_libros <= 0:
                print("Por favor ingrese un número mayor a cero, solo acepto numeros positivos y enteros :(")
                continue
            break
        except ValueError:
            print("Entrada inválida, por favor introduzca un número entero, solo puedo aceptar esos!!! :(")

    print(f"\nEmpezando la descarga de {cantidad_libros} libros [...]")

    rango_libro = range(1, cantidad_libros + 1)
    get_books.main(
        n=rango_libro,
        directory=carpeta_destino
    )
    print("\n" + ".-" * 20)
    print(" Descarga finalizada con éxito!!! ")
    print(f" el numero de libros descargados es el siguiente: {cantidad_libros}!!!"
           "espero sean más proximamente!! :) ")
    print(".-" * 20)
    input("\npress 'enter' para regresar al menú principal. :)")


def actualizar_motor():
    """se encargará de cargar libros y calcula TF-IDF"""

    lista_libros = libros.crear_lista_libros_ingles(
        directory=carpeta_destino,
        caract_especiales=punctuation
    )
    if not lista_libros:
        return None, []
    motor = recomendaciones.Recomendador(lista_libros)
    motor.set_pesos()
    return motor, lista_libros

def capturar_indice_valido(lista_libros):
    """Valida el índice ingresado"""
    try:
        idx = int(
            input("\nIngrese el índice del libro, por favor! "
            "(el indice es el numero que se muestra antes del nombre): ").strip()
        )
        if idx < 0 or idx >= len(lista_libros):
            print(
                f"Índice fuera de rango. Debe estar entre "
                f"0 y {len(lista_libros)-1}"
            )
            input("\nPresione ENTER para continuar...")
            return None
        return idx
    except ValueError:
        print("Lo siento, la entrada es inválida!!! debes de ingresar un número entero.")
        input("\npress 'enter' para continuar")
        return None


def solicitar_resumen(motor, lista_libros):
    """Opción numero 2: captura de palabras clave"""

    idx = capturar_indice_valido(lista_libros)
    if idx is None:
        return
    print(f"\nLibro indicado: {lista_libros[idx].name}")

    try:
        cantidad_palabras = int(
            input(
                "cual es la cantidad de palabras que desearias ver, usuario? :) : "
            ).strip()
        )
        if cantidad_palabras <= 0:
            print("La cantidad ingresada debe ser mayor a cero!!! >_<")
            input("\npress 'enter' para continuar...")
            return
        top_palabras = motor.resumen(
            idx_libro=idx,
            num_palabras=cantidad_palabras
        )
        print("\n" + ".-" * 30)
        print(f" Nombre del libro: {lista_libros[idx].name}")
        print(".-" * 30)
        print(
            f" Palabras clave: {', '.join(top_palabras)}"
        )
        print("=" * 50)
    except ValueError:
        print("Por favor ingrese un número entero.")
    input("\npress 'enter' para regresar al menú...")

def solicitar_recomendaciones(motor, lista_libros):
    """Opción numero 3: se deben recomendar libros similares"""

    if len(lista_libros) < 2:
        print(
            "Se necesitan al menos 2 libros para "
            "generar recomendaciones... vamos, intenta unos más! :)"
        )
        input("\npress 'enter' para continuar el código!...")
        return

    idx = capturar_indice_valido(lista_libros)
    if idx is None:
        return
    print(f"\nLibro indicado: {lista_libros[idx].name} :O")
    try:
        limite = len(lista_libros) - 1
        cantidad_sugerencias = int(
            input(
                f"Cuántos libros desearias descargar, usuario? :) "
                f"(CANTIDAD MÁXIMA! {limite}): "
            ).strip()
        )
        if cantidad_sugerencias <= 0:
            print("La cantidad debe ser mayor a cero.")
            input("\npress 'enter' para continuar...")
            return
        if cantidad_sugerencias > limite:
            print(
                f"Solo existen {limite} libros "
                f"para comparar."
            )
            input("\npress 'enter' para continuar...")
            return
        sugerencias = motor.libros_similares(
            idx_libro=idx,
            num_libros=cantidad_sugerencias
        )
        print("\n" + ".-" * 30)
        print(
            f" RECOMENDACIONES PARA: "
            f"{lista_libros[idx].name}"
        )
        print("-" * 50)
        for i, libro in enumerate(
            sugerencias,
            start=1
        ):
            print(f"{i}. {libro}")
        print("-." * 30)
    except ValueError:
        print("Por favor ingrese un número entero.")
    input("\nPresione ENTER para regresar al menú...")

def bienvenida():
    print("\n" + ".-°-." * 15)
    print("                     SISTEMA RECOMENDADOR DE LIBROS ")
    print("-|-°-|-" * 15)
    print(
        "\nUn gusto conocerlo, usuario!!!, yo como programa me encargo"
         "de analizar los libros de la pagina "
        "Project Gutenberg utilizando TF-IDF para recomendarte los"
        "libros que puede que te gusten en base al libro que mas te gusto. :)"
    )
    print(
        "yo encontrar palabras importantes "
        "para de nuevo, recomendarte un libro similar a ello.\n"
    )

"""
    esta seria el switch que ya, en base a la opcion elegida entre uno y cuatro, hará lo pedido.
"""
def menu():
    opcion = "0"

    motor, lista_libros = actualizar_motor()

    while opcion != "4":
        print("\n" + ".-~`~-." * 12)
        print("          ||  MENU  || ")
        print("-.`.-" * 12)

        if lista_libros:
            motor.mostrar_libros()
        else:
            print(
                "por el momento no hay libros descargados...\n"
                "Para alegrar nuestra lista agrega"
                "libros con la opcion 1 para poder descargarlos!!! :)"
            )
        print("\n-.-.-.-.-.-.-Opciones disponibles!!!:")
        print("_- I Descargar libros!  -.°-.°-")
        print("°- II palabras claves! -.-°.-.°-.°-.")
        print("_- III Recomendaciones :)-°-.-°-.-.-.-.")
        print("°- IV Salir del codigo.-.-.°-°.-.-°.-......")

        opcion = input(
            "\nSeleccione una opción (1,2,3,4): "
        ).strip()

        if opcion == "1":
            descargar_libros()
            print(
                "\nProcesando los textos para "
                "calcular su TF-IDF..."
            )
            motor, lista_libros = actualizar_motor()

            if lista_libros:
                print("Motor actualizado correctamente!!!")
        elif opcion == "2":
            if not lista_libros:
                print(
                    "Ups!, Debes de descargar libros primero!, procura " \
                    "darle a la opción 1 para descargar los libros."

                )
                input("\npress 'enter' para regresar...")
            else:
                motor.mostrar_libros()
                solicitar_resumen(
                    motor,
                    lista_libros
                )

        elif opcion == "3":

            if not lista_libros:
                print(
                    "Debes descargar por lo menos unos cuantos libros primero para desbloquear esta opción! :("
                )
                input("\npress 'enter' para regresar...")
            else:
                motor.mostrar_libros()
                solicitar_recomendaciones(
                    motor,
                    lista_libros
                )

        elif opcion == "4":

            print("\n¡Muchas gracias por usar este sistema!")
            print("-.-.-.- este recomendador fue hecho en el grupo 2-3 por: -.-.-.-")
            print("- Leon Favela Dagoberto")
            print("- Chavez Ramirez David Uriel")
            print("- Espero volvernos a ver  pronto !!! :3 ")
            

            
        else:

            print("Opción inválida.")
            input("\nPresione ENTER...")

#prueba de interfaz
if __name__ == "__main__":
    bienvenida()
    menu()
