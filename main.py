import os
import datetime
import tkinter as tk
from tkinter import scrolledtext, filedialog

def obtener_nombre_archivo():
    ahora = datetime.datetime.now()
    nombre_archivo = ahora.strftime("%H%M%S%f%d%m%Y")
    return nombre_archivo

def guardar(event=None, guardar_como=False):
    contenido = texto.get("1.0", tk.END)
    if guardar_como:
        archivo_guardado = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    else:
        carpeta_notas = "notas"
        if not os.path.exists(carpeta_notas):
            os.makedirs(carpeta_notas)
        nombre_archivo = obtener_nombre_archivo()
        archivo_guardado = os.path.join(carpeta_notas, nombre_archivo + ".txt")
    if archivo_guardado:
        with open(archivo_guardado, "w") as archivo:
            archivo.write(contenido)
        print("¡Notas guardadas en:", archivo_guardado, "!")
    else:
        print("Guardado fallido.")

def guardar_como(event=None):
    guardar(event, guardar_como=True)

def cargar(event=None):
    archivo_cargado = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivo_cargado:
        try:
            with open(archivo_cargado, "r") as archivo:
                contenido = archivo.read()
            texto.delete("1.0", tk.END)
            texto.insert("1.0", contenido)
            print("Notas cargadas correctamente desde:", archivo_cargado)
        except FileNotFoundError:
            print("No se encontró ningún archivo de notas.")
    else:
        print("Carga cancelada.")

def crear_menu_archivo():
    menu_archivo = tk.Menu(ventana)
    ventana.config(menu=menu_archivo)

    submenu_archivo = tk.Menu(menu_archivo)
    menu_archivo.add_cascade(label="Archivo", menu=submenu_archivo)
    submenu_archivo.add_command(label="Guardar", command=guardar, accelerator="Ctrl+S")
    submenu_archivo.add_command(label="Guardar como...", command=guardar_como, accelerator="Ctrl+Shift+S")
    submenu_archivo.add_command(label="Cargar", command=cargar, accelerator="Ctrl+O")

    ventana.bind_all("<Control-s>", guardar)
    ventana.bind_all("<Control-S>", guardar_como)
    ventana.bind_all("<Control-o>", cargar)

def mostrar_info():
    version = "Versión 1.0.0"
    label_version.config(text=version)

    fila_columna = texto.index(tk.INSERT)
    label_fila_columna.config(text=f"Fila: {fila_columna.split('.')[0]}, Columna: {fila_columna.split('.')[1]}")

    ventana.after(100, mostrar_info)

ventana = tk.Tk()
ventana.title("Bloc de Notas")
ventana.geometry("800x600")
ventana.resizable(False, False)

ruta_icono = os.path.join("images", "icono.ico")
ventana.iconbitmap(ruta_icono)

texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=30)
texto.pack(expand=True, fill='both')

crear_menu_archivo()

label_version = tk.Label(ventana, text="", anchor="e")
label_version.pack(side="right", padx=5, pady=5, anchor="se")

label_fila_columna = tk.Label(ventana, text="", anchor="w")
label_fila_columna.pack(side="left", padx=5, pady=5, anchor="sw")

mostrar_info()

ventana.mainloop()
