"""
modelos.py
Define las estructuras de datos más básicas del proyecto:
    - Cancion: los datos "reales" de una canción (nombre, artista, duración).
    - NodoCancion: el nodo del árbol. Guarda una Cancion y dos punteros
    (izquierda / derecha). El árbol NUNCA se representa con listas: la
    única forma de "recorrer" o "guardar" canciones es a través de estos
    punteros, tal como pide la actividad.
"""

class Cancion:
    """
    Representa una canción de la plataforma.
    La 'duracion' (en segundos, entero) es la CLAVE que usa el Árbol de
    Búsqueda Binaria para decidir en qué rama colocar la canción:
        - Si es más corta que el nodo actual -> rama izquierda.
        - Si es más larga que el nodo actual -> rama derecha.
    """

    def __init__(self, nombre: str, artista: str, duracion: int):
        self.nombre = nombre
        self.artista = artista
        self.duracion = duracion  # clave del BST (en segundos)

    def duracion_formateada(self) -> str:
        """Convierte los segundos a un formato mm:ss, solo para mostrarlo bonito."""
        minutos = self.duracion // 60
        segundos = self.duracion % 60
        return f"{minutos}:{segundos:02d}"

    def __str__(self):
        return (f"'{self.nombre}' de {self.artista} "
                f"({self.duracion_formateada()} min | {self.duracion}s)")

class NodoCancion:
    """
    Nodo del Árbol de Búsqueda Binaria.
    Atributos:
        cancion    -> objeto Cancion almacenado en este nodo.
        izquierda  -> puntero (referencia) al subárbol de canciones más cortas.
        derecha    -> puntero (referencia) al subárbol de canciones más largas.
    No existen campos de tipo lista aquí: la estructura completa del árbol
    vive exclusivamente en estos punteros encadenados nodo -> nodo.
    """

    def __init__(self, cancion: Cancion):
        self.cancion = cancion
        self.izquierda = None
        self.derecha = None