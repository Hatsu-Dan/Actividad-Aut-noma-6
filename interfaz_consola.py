"""
interfaz_consola.py
Interfaz de texto para operar el arbol de búsqueda binaria de canciones 
desde la terminal. Es la forma más simple y portable de probar todas las 
operaciones pedidas por la actividad sin depender de librerías gráficas.
"""

from arbol import ArbolCancionesBST
from modelos import Cancion

def cargar_canciones_de_ejemplo(arbol: ArbolCancionesBST):
    """Precarga algunas canciones para poder probar el sistema de inmediato."""
    ejemplo = [
        ("Bohemian Rhapsody", "Queen", 355),
        ("Blinding Lights", "The Weeknd", 200),
        ("Hotel California", "Eagles", 391),
        ("Numb", "Linkin Park", 187),
        ("Stairway to Heaven", "Led Zeppelin", 482),
        ("Levitating", "Dua Lipa", 203),
        ("Yesterday", "The Beatles", 125),
        ("Bad Guy", "Billie Eilish", 194),
        ("Wonderwall", "Oasis", 258),
        ("Africa", "Toto", 295),
    ]
    for nombre, artista, duracion in ejemplo:
        arbol.insertar(Cancion(nombre, artista, duracion))
    print(f"✅ Se cargaron {len(ejemplo)} canciones de ejemplo.\n")

def pedir_entero(mensaje: str) -> int:
    """Pide un número entero por teclado y no deja avanzar hasta que sea válido."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("⚠️  Por favor ingresa un número entero válido.")

def mostrar_menu():
    print("\n" + "=" * 55)
    print("   🎧  MOTOR DE RECOMENDACIÓN MUSICAL (BST)  🎧")
    print("=" * 55)
    print("1. Insertar canción")
    print("2. Buscar canción por duración exacta")
    print("3. Eliminar canción por duración")
    print("4. Mostrar todas las canciones (ordenadas por duración)")
    print("5. Calcular tiempo total de la playlist")
    print("6. Recomendar canción perfecta")
    print("7. Filtrar canciones cortas (audios basura)")
    print("8. Verificar balance del árbol (funcionalidad propia)")
    print("9. Cargar canciones de ejemplo")
    print("0. Salir")
    print("=" * 55)

def main():
    arbol = ArbolCancionesBST()
    print("Bienvenido/a al motor de recomendación musical.")

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre de la canción: ").strip()
            artista = input("Artista: ").strip()
            duracion = pedir_entero("Duración en segundos: ")
            arbol.insertar(Cancion(nombre, artista, duracion))
            print(f"✅ '{nombre}' insertada correctamente.")

        elif opcion == "2":
            duracion = pedir_entero("¿Duración exacta a buscar (segundos)?: ")
            resultado = arbol.buscar(duracion)
            if resultado:
                print(f"🔎 Encontrada: {resultado}")
            else:
                print("❌ No existe ninguna canción con esa duración exacta.")

        elif opcion == "3":
            duracion = pedir_entero("Duración de la canción a eliminar: ")
            if arbol.buscar(duracion) is None:
                print("❌ No hay ninguna canción con esa duración.")
            else:
                arbol.eliminar(duracion)
                print("🗑️  Canción eliminada y árbol reestructurado.")

        elif opcion == "4":
            if arbol.esta_vacio():
                print("El árbol está vacío.")
            else:
                print("\n🎼 Playlist ordenada de más corta a más larga:")
                arbol.mostrar_inorden()

        elif opcion == "5":
            total = arbol.calcular_tiempo_total()
            minutos, segundos = divmod(total, 60)
            print(f"⏱️  Tiempo total de la playlist: {total}s "
                  f"({minutos} min {segundos}s)")

        elif opcion == "6":
            if arbol.esta_vacio():
                print("El árbol está vacío, no hay nada que recomendar.")
                continue
            segundos = pedir_entero("¿Cuántos segundos tienes disponibles?: ")
            cancion, diferencia = arbol.recomendar_cancion_perfecta(segundos)
            if diferencia == 0:
                print(f"🎯 Coincidencia exacta: {cancion}")
            else:
                print(f"🎯 La más cercana es: {cancion} "
                      f"(se aleja por {diferencia}s de lo pedido)")

        elif opcion == "7":
            minimo = pedir_entero("Eliminar canciones con menos de cuántos segundos?: ")
            arbol.filtrar_canciones_cortas(minimo)
            print(f"🧹 Se eliminaron todas las canciones de menos de {minimo}s.")

        elif opcion == "8":
            altura, balanceado = arbol.verificar_balance()
            estado = "SÍ está balanceado ✅" if balanceado else "NO está balanceado ⚠️"
            print(f"📏 Altura del árbol: {altura}")
            print(f"⚖️  {estado}")
            if not balanceado:
                print("   Sugerencia: considera reinsertar las canciones en un orden")
                print("   distinto (o implementar rotaciones AVL) para recuperar")
                print("   búsquedas en O(log n).")

        elif opcion == "9":
            cargar_canciones_de_ejemplo(arbol)

        elif opcion == "0":
            print("¡Hasta luego! 🎶")
            break

        else:
            print("⚠️  Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()