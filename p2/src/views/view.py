import tkinter as tk
from tkinter import messagebox
from p2.src.models.ListaEnlazada import ListaEnlazadaAgenda
from p2.src.controllers.controller import exportar_ambas_agendas, importar_agenda

class VistaAgenda:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Agenda (General y Prioritaria)")
        self.root.geometry("480x640")
        
        self.agenda = ListaEnlazadaAgenda()

        # Carga automática de agenda1.csv al iniciar
        importar_agenda(self.agenda)

        # --- SECCIÓN DE ENTRADA DE DATOS ---
        frame_inputs = tk.LabelFrame(root, text=" Datos del Contacto ", padx=10, pady=10)
        frame_inputs.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nombre = tk.Entry(frame_inputs, width=32)
        self.txt_nombre.grid(row=0, column=1, pady=5)

        tk.Label(frame_inputs, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_tel = tk.Entry(frame_inputs, width=32)
        self.txt_tel.grid(row=1, column=1, pady=5)

        # Casilla para marcar si es prioritario (se guardará en agenda2.csv automáticamente)
        self.var_prioritario = tk.BooleanVar()
        self.chk_prioridad = tk.Checkbutton(frame_inputs, text="Marcar como Contacto Prioritario ⭐", variable=self.var_prioritario)
        self.chk_prioridad.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        self.txt_tel.bind("<Return>", lambda event: self.accion_insertar())

        # --- SECCIÓN DE BOTONES (TODAS LAS OPCIONES ORIGINALES) ---
        """
        frame_botones = tk.Frame(root, pady=5)
        frame_botones.pack(fill="x", padx=10)

        tk.Button(frame_botones, text="Insertar", bg="#4CAF50", fg="white", width=14, command=self.accion_insertar).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Actualizar", bg="#FF9800", fg="white", width=14, command=self.accion_actualizar).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="Eliminar", bg="#F44336", fg="white", width=14, command=self.accion_eliminar).grid(row=0, column=2, padx=2, pady=2)

        tk.Button(frame_botones, text="Buscar Exacto", width=14, command=self.accion_buscar).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Buscar Parcial", width=14, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="Limpiar Vista", bg="#9E9E9E", fg="white", width=14, command=self.accion_limpiar_vista).grid(row=1, column=2, padx=2, pady=2)

        # Botones de visualización separados
        tk.Button(frame_botones, text="Mostrar Todos (Agenda 1)", bg="#008CBA", fg="white", width=21, command=self.accion_mostrar_todos).grid(row=2, column=0, columnspan=1, padx=2, pady=6)
        tk.Button(frame_botones, text="⭐ Mostrar Prioritarios (Agenda 2)", bg="#FFC107", fg="black", width=21, command=self.accion_mostrar_prioritarios).grid(row=2, column=1, columnspan=2, padx=2, pady=6)
        """
        # --- SECCIÓN DE BOTONES (CORREGIDA) ---
        frame_botones = tk.Frame(root, pady=5)
        frame_botones.pack(fill="x", padx=10)

        # Fila 0
        tk.Button(frame_botones, text="Insertar", bg="#4CAF50", fg="white", width=14, command=self.accion_insertar).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Actualizar", bg="#FF9800", fg="white", width=14, command=self.accion_actualizar).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="Eliminar", bg="#F44336", fg="white", width=14, command=self.accion_eliminar).grid(row=0, column=2, padx=2, pady=2)

        # Fila 1
        tk.Button(frame_botones, text="Buscar Exacto", width=14, command=self.accion_buscar).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Buscar Parcial", width=14, command=self.accion_buscar_parcial).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="Limpiar Vista", bg="#9E9E9E", fg="white", width=14, command=self.accion_limpiar_vista).grid(row=1, column=2, padx=2, pady=2)

        # Fila 2: Botones de visualización separados
        tk.Button(frame_botones, text="Mostrar Todos (Agenda 1)", bg="#008CBA", fg="white", width=21, command=self.accion_mostrar_todos).grid(row=2, column=0, columnspan=1, padx=2, pady=6)
        tk.Button(frame_botones, text="⭐ Mostrar Prioritarios (Agenda 2)", bg="#FFC107", fg="black", width=21, command=self.accion_mostrar_prioritarios).grid(row=2, column=1, columnspan=2, padx=2, pady=6)
        # --- SECCIÓN DE RESULTADOS ---
        frame_output = tk.LabelFrame(root, text=" Salida / Resultados ", padx=10, pady=10)
        frame_output.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_resultado = tk.Text(frame_output, height=10, width=52)
        self.txt_resultado.pack(fill="both", expand=True)

        # Mostrar la agenda general al arrancar
        self.accion_mostrar_todos()

    def guardar_cambios(self):
        """Sincroniza y guarda automáticamente en agenda1.csv y agenda2.csv"""
        exportar_ambas_agendas(self.agenda)

    def accion_insertar(self):
        nombre = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        es_prio = self.var_prioritario.get()
        
        if nombre and tel:
            self.agenda.insertar_ordenado(nombre, tel, es_prio)
            self.guardar_cambios()
            self.limpiar_campos()
            self.accion_mostrar_todos()
        else:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")

    def accion_actualizar(self):
        nombre = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        if nombre and tel:
            if self.agenda.actualizar(nombre, tel):
                self.guardar_cambios()
                self.limpiar_campos()
                self.accion_mostrar_todos()
            else:
                messagebox.showerror("Error", "No se encontró el contacto para actualizar.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa el nombre y el nuevo teléfono.")

    def accion_eliminar(self):
        nombre = self.txt_nombre.get().strip()
        if nombre:
            if self.agenda.eliminar(nombre):
                self.guardar_cambios()
                self.limpiar_campos()
                self.accion_mostrar_todos()
            else:
                messagebox.showerror("Error", "No se encontró el contacto a eliminar.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa el nombre del contacto a eliminar.")

    def accion_buscar(self):
        nombre = self.txt_nombre.get().strip()
        if nombre:
            nodo = self.agenda.buscar(nombre)
            self.txt_resultado.delete("1.0", tk.END)
            if nodo:
                estado = "⭐ (Prioritario)" if nodo.prioritario else "(Normal)"
                self.txt_resultado.insert(tk.END, f"--- CONTACTO ENCONTRADO ---\n• {nodo.nombre} | Tel: {nodo.telefono} {estado}\n")
            else:
                self.txt_resultado.insert(tk.END, "No se encontró ningún contacto con ese nombre.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para buscar.")

    def accion_buscar_parcial(self):
        texto = self.txt_nombre.get().strip()
        if texto:
            resultados = self.agenda.buscar_parcial(texto)
            self.txt_resultado.delete("1.0", tk.END)
            if resultados:
                self.txt_resultado.insert(tk.END, "--- COINCIDENCIAS ENCONTRADAS ---\n")
                for r in resultados:
                    est = "⭐" if r.prioritario else ""
                    self.txt_resultado.insert(tk.END, f"• {r.nombre} | Tel: {r.telefono} {est}\n")
            else:
                self.txt_resultado.insert(tk.END, "Sin coincidencias parciales.")
        else:
            messagebox.showwarning("Advertencia", "Ingresa texto para la búsqueda parcial.")

    def accion_mostrar_todos(self):
        """Muestra todos los contactos guardados en agenda1.csv"""
        elementos = self.agenda.mostrar()
        self.txt_resultado.delete("1.0", tk.END)
        if elementos:
            self.txt_resultado.insert(tk.END, "--- AGENDA GENERAL (agenda1.csv) ---\n")
            for el in elementos:
                self.txt_resultado.insert(tk.END, f"{el}\n")
        else:
            self.txt_resultado.insert(tk.END, "La agenda general está vacía.")

    def accion_mostrar_prioritarios(self):
        """Muestra exclusivamente los filtrados de agenda2.csv"""
        elementos = self.agenda.mostrar_prioritarios()
        self.txt_resultado.delete("1.0", tk.END)
        if elementos:
            self.txt_resultado.insert(tk.END, "--- CONTACTOS PRIORITARIOS ⭐ (agenda2.csv) ---\n")
            for el in elementos:
                self.txt_resultado.insert(tk.END, f"{el}\n")
        else:
            self.txt_resultado.insert(tk.END, "No hay contactos marcados como prioritarios en agenda2.csv.")

    def accion_limpiar_vista(self):
        self.txt_resultado.delete("1.0", tk.END)

    def limpiar_campos(self):
        self.txt_nombre.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.var_prioritario.set(False)
        self.txt_nombre.focus()

def iniciar_interfaz7():
    root = tk.Tk()
    app = VistaAgenda(root)
    root.mainloop()