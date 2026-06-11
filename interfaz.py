import get_books
import libros
import recomendaciones
from string import punctuation

carpeta_destino = "Books/"


def descargar_libros():
    """Opción 1: Descargar libros de Gutenberg"""
    print("--- Bienvenido al panel de descarga de libros ---")

    while True:
        try:
            cantidad_libros = int(
                input("Cantidad de libros a descargar: ").strip()
            )
            if cantidad_libros <= 0:
                print("Por favor introduzca un número mayor a cero.")
                continue
            break
        except ValueError:
            print("Entrada inválida, por favor introduzca un número entero.")

    print(f"\nIniciando la descarga de {cantidad_libros} libros...")

    rango_libro = range(1, cantidad_libros + 1)
    get_books.main(
        n=rango_libro,
        directory=carpeta_destino
    )
    print("\n" + ".-" * 25)
    print(" Descarga finalizada con éxito ")
    print(f" {cantidad_libros} libros descargados ")
    print(".-" * 25)
    input("\nPresione ENTER para regresar al menú principal...")


def actualizar_motor():
    """Carga libros y calcula TF-IDF"""

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
            input("\nIntroduzca el índice del libro: ").strip()
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
        print("Entrada inválida. Ingrese un número entero.")
        input("\nPresione ENTER para continuar...")
        return None


def solicitar_resumen(motor, lista_libros):
    """Opción 2: palabras clave"""

    idx = capturar_indice_valido(lista_libros)
    if idx is None:
        return
    print(f"\nLibro seleccionado: {lista_libros[idx].name}")

    try:
        cantidad_palabras = int(
            input(
                "Cantidad de palabras que desea ver: "
            ).strip()
        )
        if cantidad_palabras <= 0:
            print("La cantidad debe ser mayor a cero.")
            input("\nPresione ENTER para continuar...")
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
    input("\nENTER para regresar al menú...")

def solicitar_recomendaciones(motor, lista_libros):
    """Opción 3: Recomendar libros similares"""

    if len(lista_libros) < 2:
        print(
            "Se necesitan al menos 2 libros para "
            "generar recomendaciones."
        )
        input("\nPresione ENTER para continuar...")
        return

    idx = capturar_indice_valido(lista_libros)
    if idx is None:
        return
    print(f"\nLibro seleccionado: {lista_libros[idx].name}")
    try:
        limite = len(lista_libros) - 1
        cantidad_sugerencias = int(
            input(
                f"¿Cuántos libros desea? "
                f"(Máximo {limite}): "
            ).strip()
        )
        if cantidad_sugerencias <= 0:
            print("La cantidad debe ser mayor a cero.")
            input("\nENTER para continuar...")
            return
        if cantidad_sugerencias > limite:
            print(
                f"Solo existen {limite} libros "
                f"para comparar."
            )
            input("\nPresione ENTER para continuar...")
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
    print("\n" + ".-" * 30)
    print(" SISTEMA RECOMENDADOR DE LIBROS ")
    print("-." * 30)
    print(
        "\nEste programa analiza libros de "
        "Project Gutenberg utilizando TF-IDF"
    )
    print(
        "para encontrar palabras importantes "
        "y recomendar libros similares.\n"
    )


def menu():
    opcion = "0"

    motor, lista_libros = actualizar_motor()

    while opcion != "4":
        print("\n" + ".-" * 30)
        print(" MENU PRINCIPAL ")
        print("-." * 30)

        if lista_libros:
            motor.mostrar_libros()
        else:
            print(
                "No hay libros descargados.\n"
                "Utilice la opción 1 para poder descargarlos."
            )
        print("\nOpciones!!!:")
        print("- 1 Descargar libros -.-.-")
        print("- 2 Resumen en palabras clave-.-.-.-.-.")
        print("- 3 Recomendaciones.-.-.-.-.-.-.-.")
        print("- 4 Salir del codigo.-.-.-.-.-.-......")

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()

        if opcion == "1":
            descargar_libros()
            print(
                "\nProcesando textos y "
                "calculando TF-IDF..."
            )
            motor, lista_libros = actualizar_motor()

            if lista_libros:
                print("Motor actualizado correctamente.")
        elif opcion == "2":
            if not lista_libros:
                print(
                    "Debe descargar libros primero."
                )
                input("\nENTER para regresar...")
            else:
                motor.mostrar_libros()
                solicitar_resumen(
                    motor,
                    lista_libros
                )

        elif opcion == "3":

            if not lista_libros:
                print(
                    "Debes descargar por lo menos unos cuantos libros primero."
                )
                input("\nENTER para regresar...")
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

            
        else:

            print("Opción inválida.")
            input("\nPresione ENTER...")


if __name__ == "__main__":
    bienvenida()
    menu()
