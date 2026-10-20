import tkinter as tk
from tkinter import messagebox
from p3.src.models.ListaEnlazada3 import ListaEnlazadaAgenda
from p3.src.controllers.controller import exportar_ambas_agendas, importar_agenda

class VistaAgenda:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Agenda Completa - MVC")
        self.root.geometry("540x720")
        
        self.agenda = ListaEnlazadaAgenda()
        importar_agenda(self.agenda)

        # --- SECCIÓN DE ENTRADA DE DATOS ---
        frame_inputs = tk.LabelFrame(root, text=" Datos del Contacto ", padx=10, pady=10)
        frame_inputs.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nombre = tk.Entry(frame_inputs, width=34)
        self.txt_nombre.grid(row=0, column=1, pady=5)

        tk.Label(frame_inputs, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_tel = tk.Entry(frame_inputs, width=34)
        self.txt_tel.grid(row=1, column=1, pady=5)

        self.var_prioritario = tk.BooleanVar()
        self.chk_prioridad = tk.Checkbutton(frame_inputs, text="Marcar como Contacto Prioritario ⭐", variable=self.var_prioritario)
        self.chk_prioridad.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        self.txt_tel.bind("<Return>", lambda event: self.accion_insertar())

        # --- SECCIÓN DE BOTONES ---
        frame_botones = tk.Frame(root, pady=5)
        frame_botones.pack(fill="x", padx=10)

        tk.Button(frame_botones, text="Insertar", bg="#4CAF50", fg="white", width=12, command=self.accion_insertar).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Actualizar", bg="#FF9800", fg="white", width=12, command=self.accion_actualizar).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="↩️ Deshacer", bg="#673AB7", fg="white", width=12, command=self.accion_deshacer).grid(row=0, column=2, padx=2, pady=2)

        tk.Button(frame_botones, text="Buscar Exacto", width=12, command=self.accion_buscar_exacto).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="Buscar Parcial", width=12, command=self.accion_buscar_parcial).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="Limpiar Vista", bg="#9E9E9E", fg="white", width=12, command=self.accion_mostrar_todos).grid(row=1, column=2, padx=2, pady=2)

        tk.Button(frame_botones, text="Mostrar Todos", bg="#008CBA", fg="white", width=18, command=self.accion_mostrar_todos).grid(row=2, column=0, padx=2, pady=4)
        tk.Button(frame_botones, text="⭐ Solo Prioritarios", bg="#FFC107", fg="black", width=18, command=self.accion_mostrar_prioritarios).grid(row=2, column=1, columnspan=2, padx=2, pady=4)

        # --- SECCIÓN DE RESULTADOS INTERACTIVOS (CON SCROLL) ---
        frame_output = tk.LabelFrame(root, text=" Lista de Contactos (Doble clic para editar) ", padx=5, pady=5)
        frame_output.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(frame_output, bg="white")
        self.scrollbar = tk.Scrollbar(frame_output, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.accion_mostrar_todos()

    def guardar_cambios(self):
        exportar_ambas_agendas(self.agenda)
    """
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
        nuevo_nombre = self.txt_nombre.get().strip()
        nuevo_tel = self.txt_tel.get().strip()
        es_prio = self.var_prioritario.get()
        
        nombre_viejo = getattr(self, 'nombre_en_edicion', nuevo_nombre)

        if nuevo_nombre and nuevo_tel:
            if self.agenda.actualizar_contacto(nombre_viejo, nuevo_nombre, nuevo_tel, es_prio):
                self.guardar_cambios()
                self.limpiar_campos()
                if hasattr(self, 'nombre_en_edicion'):
                    del self.nombre_en_edicion
                messagebox.showinfo("Éxito", "Contacto actualizado correctamente.")
                self.accion_mostrar_todos()
            else:
                messagebox.showerror("Error", f"No se pudo actualizar el contacto.")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa el nombre y el teléfono.")
    """
    def accion_insertar(self):
        nombre = self.txt_nombre.get().strip()
        tel = self.txt_tel.get().strip()
        es_prio = self.var_prioritario.get()
        
        if nombre and tel:
            resultado = self.agenda.insertar_ordenado(nombre, tel, es_prio)
            if resultado == "duplicado_nombre":
                messagebox.showerror("Error de Duplicidad", f"Ya existe un contacto registrado con el nombre '{nombre}'.")
            elif resultado == "duplicado_telefono":
                messagebox.showerror("Error de Duplicidad", f"El número de teléfono '{tel}' ya pertenece a otro contacto.")
            else:
                self.guardar_cambios()
                self.limpiar_campos()
                self.accion_mostrar_todos()
        else:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")

    def accion_actualizar(self):
        nuevo_nombre = self.txt_nombre.get().strip()
        nuevo_tel = self.txt_tel.get().strip()
        es_prio = self.var_prioritario.get()
        
        nombre_viejo = getattr(self, 'nombre_en_edicion', nuevo_nombre)

        if nuevo_nombre and nuevo_tel:
            resultado = self.agenda.actualizar_contacto(nombre_viejo, nuevo_nombre, nuevo_tel, es_prio)
            if resultado == "duplicado_nombre":
                messagebox.showerror("Error", f"El nombre '{nuevo_nombre}' ya está en uso por otro contacto.")
            elif resultado == "duplicado_telefono":
                messagebox.showerror("Error", f"El teléfono '{nuevo_tel}' ya se encuentra registrado.")
            elif resultado == "ok":
                self.guardar_cambios()
                self.limpiar_campos()
                if hasattr(self, 'nombre_en_edicion'):
                    del self.nombre_en_edicion
                messagebox.showinfo("Éxito", "Contacto actualizado correctamente.")
                self.accion_mostrar_todos()
            else:
                messagebox.showerror("Error", "No se pudo encontrar el contacto a actualizar.")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa el nombre y el teléfono.") 
    def accion_deshacer(self):
        if self.agenda.deshacer_eliminacion():
            self.guardar_cambios()
            messagebox.showinfo("Deshacer", "Se ha restaurado el último contacto eliminado.")
            self.accion_mostrar_todos()
        else:
            messagebox.showwarning("Atención", "No hay acciones pendientes para deshacer.")

    def renderizar_lista(self, filtrar_solo_prioritarios=False, filtro_texto=""):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        nodos = self.agenda.obtener_todos()
        contador = 0

        for nodo in nodos:
            if filtrar_solo_prioritarios and not nodo.prioritario:
                continue
            if filtro_texto and filtro_texto.lower() not in nodo.nombre.lower():
                continue

            contador += 1
            fila_frame = tk.Frame(self.scrollable_frame, bg="white", pady=3)
            fila_frame.pack(fill="x", anchor="w", padx=5)

            var_chk = tk.BooleanVar()
            chk = tk.Checkbutton(fila_frame, variable=var_chk, bg="white")
            chk.pack(side="left", padx=2)

            estado_estrella = "⭐" if nodo.prioritario else "  "
            texto_info = f"{estado_estrella} {nodo.nombre} - Tel: {nodo.telefono}"
            
            lbl = tk.Label(fila_frame, text=texto_info, bg="white", anchor="w", width=32, font=("Arial", 10), fg="blue" if nodo.prioritario else "black")
            lbl.pack(side="left", padx=5)
            
            # Doble clic para cargar datos y editar
            lbl.bind("<Double-Button-1>", lambda e, n=nodo.nombre, t=nodo.telefono, p=nodo.prioritario: self.cargar_para_editar(n, t, p))

            btn_prio = tk.Button(
                fila_frame, text="⭐", bg="#FFC107", width=3,
                command=lambda n=nodo.nombre, t=nodo.telefono: self.accion_toggle_prio(n, t)
            )
            btn_prio.pack(side="left", padx=2)

            btn_eliminar = tk.Button(
                fila_frame, text="🗑️", bg="#F44336", fg="white", width=3,
                command=lambda n=nodo.nombre, t=nodo.telefono: self.accion_eliminar_individual(n, t)
            )
            btn_eliminar.pack(side="left", padx=2)

        if contador == 0:
            lbl_vacio = tk.Label(self.scrollable_frame, text="No se encontraron contactos.", bg="white", fg="gray")
            lbl_vacio.pack(padx=10, pady=10)

    def cargar_para_editar(self, nombre, telefono, prioritario):
        self.nombre_en_edicion = nombre
        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, nombre)
        self.txt_tel.delete(0, tk.END)
        self.txt_tel.insert(0, telefono)
        self.var_prioritario.set(prioritario)
        self.txt_nombre.focus()

    def accion_buscar_exacto(self):
        texto = self.txt_nombre.get().strip()
        if texto:
            self.renderizar_lista(filtro_texto=texto)
        else:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para buscar.")

    def accion_buscar_parcial(self):
        texto = self.txt_nombre.get().strip()
        if texto:
            self.renderizar_lista(filtro_texto=texto)
        else:
            messagebox.showwarning("Advertencia", "Ingresa texto para la búsqueda parcial.")

    def accion_eliminar_individual(self, nombre, telefono):
        if self.agenda.eliminar_por_referencia(nombre, telefono):
            self.guardar_cambios()
            self.accion_mostrar_todos()

    def accion_toggle_prio(self, nombre, telefono):
        if self.agenda.toggle_prioridad(nombre, telefono):
            self.guardar_cambios()
            self.accion_mostrar_todos()

    def accion_mostrar_todos(self):
        self.txt_nombre.delete(0, tk.END)
        if hasattr(self, 'nombre_en_edicion'):
            del self.nombre_en_edicion
        self.renderizar_lista(filtrar_solo_prioritarios=False)

    def accion_mostrar_prioritarios(self):
        self.renderizar_lista(filtrar_solo_prioritarios=True)

    def limpiar_campos(self):
        self.txt_nombre.delete(0, tk.END)
        self.txt_tel.delete(0, tk.END)
        self.var_prioritario.set(False)
        self.txt_nombre.focus()

def iniciar_interfaz():
    root = tk.Tk()
    app = VistaAgenda(root)
    root.mainloop()