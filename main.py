"""
main.py
Se abre la interfaz grafica (Tkinter). Si el entorno no tiene Tkinter
instalado, el programa caera automaticamente a la interfaz de consola para
que siempre pueda ejecutarse sin dependencias externas
"""

def main():
    try:
        from interfaz_gui import AplicacionMusical
        app = AplicacionMusical()
        app.mainloop()
    except ImportError:
        print("⚠️  Tkinter no está disponible en este entorno "
              "(instálalo con: sudo apt install python3-tk).")
        print("    Iniciando la interfaz de consola como alternativa...\n")
        from interfaz_consola import main as main_consola
        main_consola()

if __name__ == "__main__":
    main()