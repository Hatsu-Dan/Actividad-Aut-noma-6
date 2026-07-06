# Nombre: Christian Correa
# Fecha: 5/7/2026
# Carrera: Ciencia de Datos e Inteligencia Atificial

# 🎧 Motor de Recomendación Musical con Árbol de Búsqueda Binaria (BST)

Proyecto para la actividad autónoma **Unidad 3 - Tema 2: Árboles Binarios**
(Estructuras de Datos, UNACH). Simula el motor de recomendación de una
plataforma de música organizando las canciones en un **Árbol de Búsqueda
Binaria (BST)**, usando como clave la **duración de la canción en segundos**.

## ¿Por qué un BST y no una lista?

En una lista buscar la canción más parecida a una duración pedida obliga a
revisar canción por canción: **O(n)**. En un BST balanceado, cada
comparación descarta la mitad del árbol restante, así que la misma búsqueda
cuesta apenas **O(log n)**. Esa es la ventaja que se está demostrando aquí:
si el usuario quiere una canción más corta, el sistema baja a la izquierda,
si la quiere más larga, baja a la derecha — nunca revisa el árbol completo.

## Estructura del proyecto

```
bst_musica/
├── modelos.py          # Clases Cancion y NodoCancion (nodo con punteros)
├── arbol.py            # Clase ArbolCancionesBST: toda la lógica del árbol
├── interfaz_consola.py # Menú de texto para usar el programa en terminal
├── interfaz_gui.py     # Interfaz gráfica (Tkinter)
├── main.py             # Punto de entrada: abre la GUI o la consola si Tkinter no está instalado
└── README.md
```

## Reglas de diseño respetadas

- El árbol se maneja **exclusivamente con nodos y punteros** (`izquierda`,
  `derecha`). En ningún punto se usa una lista, tupla o diccionario para
  almacenar las canciones o resolver un recorrido.
- **Todas** las operaciones (inserción, búsqueda, eliminación, cálculo de
  tiempo total, recomendación, filtrado, verificación de balance) están
  implementadas de forma **recursiva**, con un caso base claro (`nodo is
  None`).
- La eliminación contempla los 3 casos clásicos de un BST: nodo hoja, nodo
  con un solo hijo, y nodo con dos hijos (usando el sucesor inorden).

## Operaciones implementadas

| Función | Qué hace |
|---|---|
| `insertar(cancion)` | Inserta una canción según su duración (clave del BST). |
| `buscar(duracion)` | Busca una canción por duración exacta. |
| `eliminar(duracion)` | Elimina una canción y reestructura los punteros. |
| `calcular_tiempo_total(nodo)` | Suma recursivamente la duración de todas las canciones del árbol (o subárbol). |
| `recomendar_cancion_perfecta(segundos)` | Baja por el BST guardando la menor diferencia absoluta encontrada; retorna la canción exacta o la más cercana en O(log n). |
| `filtrar_canciones_cortas(minimo)` | Reconstruye el árbol de abajo hacia arriba eliminando toda canción por debajo del mínimo, reutilizando la lógica de eliminación para fusionar correctamente los subárboles restantes. |
| `verificar_balance(nodo)` **(funcionalidad propia)** | Calcula la altura y el factor de balance (estilo AVL) de cada nodo, para saber si el árbol sigue garantizando búsquedas en O(log n) o si conviene reconstruirlo/balancearlo. |

## Cómo ejecutar

```bash
# Interfaz gráfica (si tienes Tkinter instalado; en Windows/Mac ya viene incluido)
python main.py

# Si tu Linux no tiene Tkinter, instálalo con:
sudo apt install python3-tk

# O usa directamente la interfaz de consola (sin dependencias):
python interfaz_consola.py
```

## Complejidad

Con el árbol balanceado, `buscar`, `eliminar` y `recomendar_cancion_perfecta`
cuestan **O(log n)**. `calcular_tiempo_total`, `filtrar_canciones_cortas` y
`verificar_balance` recorren el árbol completo, por lo que cuestan **O(n)**
(no pueden ser más rápidas, porque necesitan visitar cada canción al menos una vez).
