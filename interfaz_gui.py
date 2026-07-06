"""
interfaz_gui.py
Interfaz gráfica para operar el Árbol de Búsqueda Binaria de canciones.
Permite insertar, buscar, eliminar, mostrar la playlist ordenada,
calcular el tiempo total, pedir una recomendación, filtrar canciones cortas
y verificar el balance del árbol, todo desde botones y campos de texto.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from arbol import ArbolCancionesBST
from modelos import Cancion

CANCIONES_DE_EJEMPLO = [
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

class AplicacionMusical(tk.Tk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.title("🎧 Motor de Recomendación Musical (BST)")
        self.geometry("760x560")
        self.configure(bg="#101418")
        self.arbol = ArbolCancionesBST()
        self._construir_panel_formulario()
        self._construir_panel_acciones()
        self._construir_panel_resultados()
        self._precargar_ejemplos()

    # Construcción de la interfaz
    def _construir_panel_formulario(self):
        panel = tk.Frame(self, bg="#101418", pady=10)
        panel.pack(fill="x", padx=15)

        tk.Label(panel, text="Nombre:", bg="#101418", fg="white").grid(row=0, column=0, sticky="w")
        self.entrada_nombre = tk.Entry(panel, width=22)
        self.entrada_nombre.grid(row=0, column=1, padx=5)

        tk.Label(panel, text="Artista:", bg="#101418", fg="white").grid(row=0, column=2, sticky="w")
        self.entrada_artista = tk.Entry(panel, width=18)
        self.entrada_artista.grid(row=0, column=3, padx=5)

        tk.Label(panel, text="Duración (s):", bg="#101418", fg="white").grid(row=0, column=4, sticky="w")
        self.entrada_duracion = tk.Entry(panel, width=8)
        self.entrada_duracion.grid(row=0, column=5, padx=5)

        tk.Button(panel, text="➕ Insertar", command=self.accion_insertar,
                  bg="#2e7d32", fg="white").grid(row=0, column=6, padx=8)

    def _construir_panel_acciones(self):
        panel = tk.Frame(self, bg="#101418", pady=8)
        panel.pack(fill="x", padx=15)

        tk.Label(panel, text="Segundos:", bg="#101418", fg="white").grid(row=0, column=0, sticky="w")
        self.entrada_segundos = tk.Entry(panel, width=10)
        self.entrada_segundos.grid(row=0, column=1, padx=5)

        botones = [
            ("🔎 Buscar", self.accion_buscar, "#1565c0"),
            ("🗑️ Eliminar", self.accion_eliminar, "#c62828"),
            ("🎯 Recomendar", self.accion_recomendar, "#6a1b9a"),
            ("🧹 Filtrar < seg.", self.accion_filtrar, "#ef6c00"),
        ]
        for i, (texto, comando, color) in enumerate(botones, start=2):
            tk.Button(panel, text=texto, command=comando, bg=color, fg="white").grid(row=0, column=i, padx=5)

        panel2 = tk.Frame(self, bg="#101418", pady=4)
        panel2.pack(fill="x", padx=15)

        tk.Button(panel2, text="📃 Mostrar playlist ordenada", command=self.accion_mostrar_todas,
                  bg="#37474f", fg="white").pack(side="left", padx=4)
        tk.Button(panel2, text="⏱️ Tiempo total", command=self.accion_tiempo_total,
                  bg="#37474f", fg="white").pack(side="left", padx=4)
        tk.Button(panel2, text="⚖️ Verificar balance", command=self.accion_balance,
                  bg="#37474f", fg="white").pack(side="left", padx=4)
        tk.Button(panel2, text="🔄 Cargar ejemplos", command=self._precargar_ejemplos,
                  bg="#37474f", fg="white").pack(side="left", padx=4)

    def _construir_panel_resultados(self):
        panel = tk.Frame(self, bg="#101418")
        panel.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(panel, text="Resultados / Consola:", bg="#101418", fg="#9e9e9e").pack(anchor="w")

        self.texto_resultado = tk.Text(panel, bg="#1b1f24", fg="#e0e0e0",
                                        insertbackground="white", wrap="word")
        self.texto_resultado.pack(fill="both", expand=True)

    # Utilidades internas
    def _log(self, mensaje: str):
        self.texto_resultado.insert("end", mensaje + "\n")
        self.texto_resultado.see("end")

    def _limpiar_log(self):
        self.texto_resultado.delete("1.0", "end")

    def _leer_entero(self, entry_widget, nombre_campo) -> int:
        valor = entry_widget.get().strip()
        try:
            return int(valor)
        except ValueError:
            messagebox.showerror("Dato inválido", f"'{nombre_campo}' debe ser un número entero.")
            return None

    def _precargar_ejemplos(self):
        for nombre, artista, duracion in CANCIONES_DE_EJEMPLO:
            self.arbol.insertar(Cancion(nombre, artista, duracion))
        self._log(f"✅ Se cargaron {len(CANCIONES_DE_EJEMPLO)} canciones de ejemplo.")

    # Acciones ligadas a los botones
    def accion_insertar(self):
        nombre = self.entrada_nombre.get().strip()
        artista = self.entrada_artista.get().strip()
        duracion = self._leer_entero(self.entrada_duracion, "Duración")
        if not nombre or not artista or duracion is None:
            messagebox.showwarning("Faltan datos", "Completa nombre, artista y duración.")
            return
        self.arbol.insertar(Cancion(nombre, artista, duracion))
        self._log(f"➕ Insertada: '{nombre}' - {artista} ({duracion}s)")
        self.entrada_nombre.delete(0, "end")
        self.entrada_artista.delete(0, "end")
        self.entrada_duracion.delete(0, "end")

    def accion_buscar(self):
        duracion = self._leer_entero(self.entrada_segundos, "Segundos")
        if duracion is None:
            return
        resultado = self.arbol.buscar(duracion)
        if resultado:
            self._log(f"🔎 Encontrada: {resultado}")
        else:
            self._log(f"❌ No hay ninguna canción de exactamente {duracion}s.")

    def accion_eliminar(self):
        duracion = self._leer_entero(self.entrada_segundos, "Segundos")
        if duracion is None:
            return
        if self.arbol.buscar(duracion) is None:
            self._log(f"❌ No existe ninguna canción de {duracion}s para eliminar.")
            return
        self.arbol.eliminar(duracion)
        self._log(f"🗑️ Canción de {duracion}s eliminada. Árbol reestructurado.")

    def accion_recomendar(self):
        if self.arbol.esta_vacio():
            self._log("El árbol está vacío, no hay nada que recomendar.")
            return
        segundos = self._leer_entero(self.entrada_segundos, "Segundos")
        if segundos is None:
            return
        cancion, diferencia = self.arbol.recomendar_cancion_perfecta(segundos)
        if diferencia == 0:
            self._log(f"🎯 Coincidencia exacta para {segundos}s: {cancion}")
        else:
            self._log(f"🎯 Más cercana a {segundos}s: {cancion} (se aleja {diferencia}s)")

    def accion_filtrar(self):
        minimo = self._leer_entero(self.entrada_segundos, "Segundos")
        if minimo is None:
            return
        self.arbol.filtrar_canciones_cortas(minimo)
        self._log(f"🧹 Se eliminaron todas las canciones de menos de {minimo}s.")

    def accion_mostrar_todas(self):
        if self.arbol.esta_vacio():
            self._log("El árbol está vacío.")
            return
        self._log("🎼 Playlist ordenada de más corta a más larga:")
        # Recorrido in-order que imprime directamente en el log de la GUI
        self._mostrar_inorden_en_log(self.arbol.raiz)

    def _mostrar_inorden_en_log(self, nodo):
        """Misma lógica recursiva que arbol.mostrar_inorden(), pero enviando
        cada línea al cuadro de texto de la interfaz en vez de a la consola."""
        if nodo is None:
            return
        self._mostrar_inorden_en_log(nodo.izquierda)
        self._log(f"   🎵 {nodo.cancion}")
        self._mostrar_inorden_en_log(nodo.derecha)

    def accion_tiempo_total(self):
        total = self.arbol.calcular_tiempo_total()
        minutos, segundos = divmod(total, 60)
        self._log(f"⏱️ Tiempo total de la playlist: {total}s ({minutos} min {segundos}s)")

    def accion_balance(self):
        altura, balanceado = self.arbol.verificar_balance()
        estado = "SÍ está balanceado ✅" if balanceado else "NO está balanceado ⚠️"
        self._log(f"📏 Altura del árbol: {altura} | ⚖️ {estado}")

if __name__ == "__main__":
    app = AplicacionMusical()
    app.mainloop()