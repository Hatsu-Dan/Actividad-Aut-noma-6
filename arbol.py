"""
arbol.py
Motor de recomendación musical implementado como un Árbol de Búsqueda
Binaria (BST) donde la clave de cada nodo es la duración de la canción
en segundos.

Reglas de diseño que sigue TODO este archivo:
    1. El árbol se maneja solo con nodos y punteros (izquierda/derecha).
    2. Todas las operaciones de recorrido/cálculo son recursivas.
    3. No se usan listas, tuplas ni diccionarios para almacenar canciones
    o para resolver los recorridos; cuando se necesita "mostrar" datos
    en pantalla se imprime directamente durante la recursión.
"""

from modelos import Cancion, NodoCancion

class ArbolCancionesBST:
    """Árbol de Búsqueda Binaria especializado en canciones."""

    def __init__(self):
        self.raiz = None

    # 1) INSERCIÓN
    def insertar(self, cancion: Cancion):
        """Punto de entrada público: inserta una canción a partir de la raíz."""
        self.raiz = self._insertar_recursivo(self.raiz, cancion)

    def _insertar_recursivo(self, nodo: NodoCancion, cancion: Cancion):
        """
        Caso base: si llegamos a un puntero nulo, ahí va el nuevo nodo.
        Caso recursivo: bajamos a la izquierda o a la derecha según la
        duración, exactamente como un BST clásico.
        """
        if nodo is None:
            return NodoCancion(cancion)

        if cancion.duracion < nodo.cancion.duracion:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, cancion)
        elif cancion.duracion > nodo.cancion.duracion:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, cancion)
        else:
            """
            Política simple para claves duplicadas: como la duración es la
            clave única del árbol, si ya existe una canción con esa misma
            duración exacta, avisamos y no la insertamos (evita ambigüedad
            en las comparaciones izquierda/derecha).
            """
            print(f"⚠️  Ya existe una canción con {cancion.duracion}s "
                  f"('{nodo.cancion.nombre}'). No se insertó '{cancion.nombre}'.")
        return nodo

    # 2) BÚSQUEDA
    def buscar(self, duracion: int) -> Cancion:
        """Punto de entrada público."""
        return self._buscar_recursivo(self.raiz, duracion)

    def _buscar_recursivo(self, nodo: NodoCancion, duracion: int):
        if nodo is None:
            return None
        if duracion == nodo.cancion.duracion:
            return nodo.cancion
        elif duracion < nodo.cancion.duracion:
            return self._buscar_recursivo(nodo.izquierda, duracion)
        else:
            return self._buscar_recursivo(nodo.derecha, duracion)

    # 3) ELIMINACIÓN GENERAL (una sola canción por duración exacta)
    """
    Maneja los 3 casos clásicos: nodo hoja, un hijo, dos hijos.
    Esta función se reutiliza más abajo dentro de filtrar_canciones_cortas().
    """
    def eliminar(self, duracion: int):
        """Punto de entrada público."""
        self.raiz = self._eliminar_nodo(self.raiz, duracion)

    def _eliminar_nodo(self, nodo: NodoCancion, duracion: int):
        if nodo is None:
            return None  # la canción no existe, no hay nada que borrar
        if duracion < nodo.cancion.duracion:
            nodo.izquierda = self._eliminar_nodo(nodo.izquierda, duracion)
        elif duracion > nodo.cancion.duracion:
            nodo.derecha = self._eliminar_nodo(nodo.derecha, duracion)
        else:
            """
            Encontramos el nodo a eliminar.
            Caso 1: nodo hoja (sin hijos) -> simplemente se corta el puntero.
            Caso 2: un solo hijo -> el hijo "sube" y ocupa el lugar del nodo.
            """
            if nodo.izquierda is None:
                return nodo.derecha
            if nodo.derecha is None:
                return nodo.izquierda

            """
            Caso 3: dos hijos -> se busca el sucesor (el valor más pequeño
            del subárbol derecho), se copia su canción a este nodo y luego
            se elimina el sucesor de su posición original. Así el árbol
            sigue cumpliendo la propiedad de orden del BST.
            """
            sucesor = self._encontrar_minimo(nodo.derecha)
            nodo.cancion = sucesor.cancion
            nodo.derecha = self._eliminar_nodo(nodo.derecha, sucesor.cancion.duracion)
        return nodo

    def _encontrar_minimo(self, nodo: NodoCancion) -> NodoCancion:
        """Baja siempre a la izquierda: el mínimo de un BST está en el extremo izquierdo."""
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    # OPERACIÓN 1: calcular_tiempo_total
    def calcular_tiempo_total(self, nodo: NodoCancion = "__raiz__") -> int:
        """
        Suma recursivamente la duración de TODAS las canciones del árbol
        (o de un subárbol específico si se pasa un nodo distinto a la raíz).
        Fórmula recursiva:
            tiempo(nodo) = duracion(nodo) + tiempo(izquierda) + tiempo(derecha)
            tiempo(None) = 0   <- caso base
        """
        if nodo == "__raiz__":       # si no se especifica nodo, se usa la raíz
            nodo = self.raiz

        if nodo is None:
            return 0  # caso base: árbol/subárbol vacío no aporta tiempo

        return (nodo.cancion.duracion
                + self.calcular_tiempo_total(nodo.izquierda)
                + self.calcular_tiempo_total(nodo.derecha))

    # OPERACIÓN 2: recomendar_cancion_perfecta
    def recomendar_cancion_perfecta(self, segundos_disponibles: int):
        """
        Punto de entrada público. Devuelve una tupla:
            (cancion_recomendada, diferencia_en_segundos)
        """
        return self._recomendar_recursivo(self.raiz, segundos_disponibles,
                                           mejor=None, menor_diferencia=float("inf"))

    def _recomendar_recursivo(self, nodo: NodoCancion, objetivo: int,
                               mejor: Cancion, menor_diferencia: float):
        """
        Baja por el árbol aprovechando la propiedad de orden del BST
        (por eso NO hace falta revisar todos los nodos): en cada paso
        decide un único camino (izquierda o derecha), lo que da una
        complejidad O(log n) en un árbol balanceado, en vez de O(n).

        En cada nodo visitado se compara su diferencia absoluta contra el
        objetivo y, si es menor que la mejor encontrada hasta el momento,
        se actualiza el "mejor candidato".
        """
        if nodo is None:
            return mejor, menor_diferencia  # caso base: ya no hay más ramas

        diferencia = abs(nodo.cancion.duracion - objetivo)
        if diferencia < menor_diferencia:
            mejor = nodo.cancion
            menor_diferencia = diferencia

        if diferencia == 0:
            # Coincidencia exacta: no hace falta seguir bajando.
            return mejor, menor_diferencia

        if objetivo < nodo.cancion.duracion:
            return self._recomendar_recursivo(nodo.izquierda, objetivo, mejor, menor_diferencia)
        else:
            return self._recomendar_recursivo(nodo.derecha, objetivo, mejor, menor_diferencia)

    # OPERACIÓN 3: filtrar_canciones_cortas
    def filtrar_canciones_cortas(self, duracion_minima: int):
        """Punto de entrada público."""
        self.raiz = self._filtrar_recursivo(self.raiz, duracion_minima)

    def _filtrar_recursivo(self, nodo: NodoCancion, duracion_minima: int):
        """
        Reconstruye el árbol de abajo hacia arriba (post-order):
        1) Primero filtra el subárbol izquierdo.
        2) Luego filtra el subárbol derecho.
        3) Recién ahí decide qué hacer con el nodo actual.

        Como el filtrado nunca cambia el ORDEN relativo de las canciones que
        sobreviven, si el nodo actual no cumple con la duración mínima se lo
        puede eliminar reutilizando exactamente la misma lógica de
        _eliminar_nodo (buscar sucesor cuando hay dos hijos, o "ascender" al
        único hijo si sólo tiene uno), garantizando que los punteros queden
        correctamente reestructurados y la propiedad de BST se mantenga.
        """
        if nodo is None:
            return None  # caso base

        nodo.izquierda = self._filtrar_recursivo(nodo.izquierda, duracion_minima)
        nodo.derecha = self._filtrar_recursivo(nodo.derecha, duracion_minima)

        if nodo.cancion.duracion < duracion_minima:
            # Esta canción es "audio basura": hay que sacarla del árbol.
            if nodo.izquierda is None:
                return nodo.derecha
            if nodo.derecha is None:
                return nodo.izquierda

            sucesor = self._encontrar_minimo(nodo.derecha)
            nodo.cancion = sucesor.cancion
            nodo.derecha = self._eliminar_nodo(nodo.derecha, sucesor.cancion.duracion)

        return nodo

    # OPERACIÓN 4: funcionalidad_propia
    def verificar_balance(self, nodo: NodoCancion = "__raiz__"):
        """
        FUNCIONALIDAD PROPIA: "Auditor de Balance del Árbol".

        ¿Qué hace?
            Recorre el árbol de forma recursiva (post-order) calculando,
            para cada nodo, su ALTURA y su FACTOR DE BALANCE
            (altura del subárbol izquierdo - altura del subárbol derecho),
            igual que se hace para mantener un árbol AVL.

        ¿Para qué sirve en el contexto musical?
            El motor de recomendación depende de que las búsquedas
            (recomendar_cancion_perfecta, buscar) se resuelvan en O(log n).
            Si la app inserta canciones en un orden desafortunado (por
            ejemplo, siempre canciones cada vez más largas), el árbol se
            "estira" y se parece a una lista enlazada, degradando las
            búsquedas a O(n). Esta función le permite a la aplicación
            preguntar periódicamente "¿sigo siendo eficiente?" y decidir
            si conviene reconstruir/balancear el árbol.

        Retorna una tupla (altura_del_arbol, esta_balanceado: bool).
        Un árbol está balanceado si TODOS sus nodos tienen un factor de
        balance entre -1 y 1 (criterio de balance estilo AVL).
        """
        if nodo == "__raiz__":
            nodo = self.raiz

        if nodo is None:
            return -1, True  # caso base: árbol vacío, altura -1, balanceado

        altura_izq, balanceado_izq = self.verificar_balance(nodo.izquierda)
        altura_der, balanceado_der = self.verificar_balance(nodo.derecha)

        factor_balance = altura_izq - altura_der
        altura_actual = 1 + max(altura_izq, altura_der)
        esta_balanceado = (balanceado_izq and balanceado_der
                            and abs(factor_balance) <= 1)

        return altura_actual, esta_balanceado

    # UTILIDAD DE VISUALIZACIÓN
    def mostrar_inorden(self, nodo: NodoCancion = "__raiz__"):
        """
        Recorrido in-order: imprime las canciones ordenadas de menor a
        mayor duración. Se imprime directamente durante la recursión, sin
        acumular resultados en ninguna lista.
        """
        if nodo == "__raiz__":
            nodo = self.raiz
        if nodo is None:
            return
        self.mostrar_inorden(nodo.izquierda)
        print(f"   🎵 {nodo.cancion}")
        self.mostrar_inorden(nodo.derecha)

    def esta_vacio(self) -> bool:
        return self.raiz is None