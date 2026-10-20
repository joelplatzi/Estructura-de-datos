import tkinter as tk
from tkinter import messagebox
from p1.src.models.ListaEnlazada import ListaEnlazadaAgenda
from p1.src.controllers.controller import exportar_csv, importar_csv

class VistaAgenda:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contactos - MVC")
        self.root.geometry("450x580")
        
        self.agenda = ListaEnlazadaAgenda()

        # Carga automática al iniciar
        importar_csv(self.agenda)

        # --- SECCIÓN DE ENTRADA DE DATOS ---
        frame_inputs = tk.LabelFrame(root, text=" Datos del Contacto ", padx=10, pady=10)
        frame_inputs.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nombre = tk.Entry(frame_inputs, width=30)
        self.txt_nombre.grid(row=0, column=1, pady=5)

        tk.Label(frame_inputs, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_tel = tk.Entry(frame_inputs, width=30)
        self.txt_tel.grid(row=1, column=1, pady=5)

        # Atajo con la tecla Enter para insertar
        self.txt_tel.bind("<Return>", lambda event: self.accion_insertar())

        # --- SECCIÓN DE BOTONES ---
        frame_botones = tk.Frame(root, pady=5)
        frame_botones.pack(fill="x", padx=10)

        tk.Button(frame_botones, text="Insertar", bg="#4CAF50", fg="white", width=14, command=self.accion_insertar).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Actualizar", bg="#FF9800", fg="white", width=14, command=self.accion_actualizar).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="Eliminar", bg="#F44336", fg="white", width=14, command=self.accion_eliminar).grid(row=0, column=2, padx=2, pady=2)

        tk.Button(frame_botones, text="Buscar Exacto", width=14, command=self.accion_buscar).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Buscar Parcial", width=14, command=self.accion_buscar_parcial).grid(row=1, column=1, padx=2, pady=2)
        
        # NUEVOS BOTONES: Limpiar Vista y Mostrar Todos separados
        tk.Button(frame_botones, text="Limpiar Vista", bg="#9E9E9E", fg="white", width=14, command=self.accion_limpiar_vista).grid(row=1, column=2, padx=2, pady=2)

        tk.Button(frame_botones, text="Mostrar Todos", bg="#008CBA", fg="white", width=44, command=self.accion_mostrar).grid(row=2, column=0, columnspan=3, padx=2, pady=4)

        # --- SECCIÓN DE RESULTADOS ---
        frame_output = tk.LabelFrame(root, text=" Agenda en Tiempo Real ", padx=10, pady=10)
        frame_output.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_resultado = tk.Text(frame_output, height=10, width=50)
        self.txt_resultado.pack(fill="both", expand=True)

        # Mostrar la agenda al arrancar
        self.accion_mostrar()

    def guardar_automaticamente(self):
        exportar_csv(self.agenda)

    def accion_insertar(self):
        nombre = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        if nombre and tel:
            self.agenda.insertar_ordenado(nombre, tel)
            self.guardar_automaticamente()
            self.limpiar_campos()
            self.accion_mostrar()
        else:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")

    def accion_actualizar(self):
        nombre = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        if nombre and tel:
            if self.agenda.actualizar(nombre, tel):
                self.guardar_automaticamente()
                self.limpiar_campos()
                self.accion_mostrar()
            else:
                messagebox.showerror("Error", "No se encontró el contacto.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa el nombre y el nuevo teléfono.")

    def accion_eliminar(self):
        nombre = self.txt_nombre.get().strip()
        if nombre:
            if self.agenda.eliminar(nombre):
                self.guardar_automaticamente()
                self.limpiar_campos()
                self.accion_mostrar()
            else:
                messagebox.showerror("Error", "Contacto no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa el nombre a eliminar.")

    def accion_buscar(self):
        nombre = self.txt_nombre.get().strip()
        if nombre:
            nodo = self.agenda.buscar(nombre)
            self.txt_resultado.delete("1.0", tk.END)
            if nodo:
                self.txt_resultado.insert(tk.END, f"--- ENCONTRADO ---\n• {nodo.nombre} | Tel: {nodo.telefono}\n")
            else:
                self.txt_resultado.insert(tk.END, "No se encontró el contacto.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para buscar.")

    def accion_buscar_parcial(self):
        texto = self.txt_nombre.get().strip()
        if texto:
            resultados = self.agenda.buscar_parcial(texto)
            self.txt_resultado.delete("1.0", tk.END)
            if resultados:
                self.txt_resultado.insert(tk.END, "--- COINCIDENCIAS ---\n")
                for r in resultados:
                    self.txt_resultado.insert(tk.END, f"• {r.nombre} | Tel: {r.telefono}\n")
            else:
                self.txt_resultado.insert(tk.END, "Sin coincidencias.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa texto para la búsqueda parcial.")

    def accion_mostrar(self):
        elementos = self.agenda.mostrar()
        self.txt_resultado.delete("1.0", tk.END)
        if elementos:
            self.txt_resultado.insert(tk.END, "--- AGENDA ACTUALIZADA ---\n")
            for el in elementos:
                self.txt_resultado.insert(tk.END, f"• {el}\n")
        else:
            self.txt_resultado.insert(tk.END, "La agenda está vacía.")

    def accion_limpiar_vista(self):
        """Borra completamente todo el contenido del cuadro de resultados"""
        self.txt_resultado.delete("1.0", tk.END)

    def limpiar_campos(self):
        self.txt_nombre.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.txt_nombre.focus()

def iniciar_interfaz3():
    root = tk.Tk()
    app = VistaAgenda(root)
    root.mainloop()