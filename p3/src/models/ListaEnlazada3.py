class Nodo:
    def __init__(self, nombre, telefono, prioritario=False):
        self.nombre = nombre
        self.telefono = telefono
        self.prioritario = prioritario
        self.siguiente = None
        
class ListaEnlazadaAgenda:
    def __init__(self):
        self.cabeza = None
        self.pila_deshacer = []
        
    def existe_nombre(self, nombre):
        """Verifica si ya existe un contacto con exactamente el mismo nombre"""
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return True
            actual = actual.siguiente
        return False

    def existe_telefono(self, telefono):
        """Verifica si el número de teléfono ya está registrado en la agenda"""
        actual = self.cabeza
        while actual:
            if actual.telefono == telefono:
                return True
            actual = actual.siguiente
        return False

    def insertar_ordenado(self, nombre, telefono, prioritario=False):
        # Validar duplicados antes de insertar
        if self.existe_nombre(nombre):
            return "duplicado_nombre"
        if self.existe_telefono(telefono):
            return "duplicado_telefono"

        nuevo = Nodo(nombre, telefono, prioritario)
        if self.cabeza is None or nombre.lower() < self.cabeza.nombre.lower():
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            return "ok"
        
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.nombre.lower() < nombre.lower():
            actual = actual.siguiente
            
        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        return "ok"
        
    def buscar(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return actual
            actual = actual.siguiente
        return None
    
    def eliminar_por_referencia(self, nombre, telefono):
        if not self.cabeza:
            return False
        
        if self.cabeza.nombre.lower() == nombre.lower() and self.cabeza.telefono == telefono:
            eliminado = self.cabeza
            self.cabeza = self.cabeza.siguiente
            self.pila_deshacer.append(eliminado)
            return True
        
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.nombre.lower() == nombre.lower() and actual.siguiente.telefono == telefono:
                eliminado = actual.siguiente
                actual.siguiente = actual.siguiente.siguiente
                self.pila_deshacer.append(eliminado)
                return True
            actual = actual.siguiente
        return False

    def actualizar_contacto(self, nombre_viejo, nuevo_nombre, nuevo_telefono, prioritario):
        """Actualiza validando que el nuevo nombre o teléfono no pertenezcan a OTRO contacto"""
        nodo_actual = self.buscar(nombre_viejo)
        if not nodo_actual:
            return "no_encontrado"

        # Si cambió de nombre y el nuevo ya existe en otro lado
        if nuevo_nombre.lower() != nombre_viejo.lower() and self.existe_nombre(nuevo_nombre):
            return "duplicado_nombre"
            
        # Si cambió de teléfono y el nuevo teléfono ya está registrado en otro lado
        if nuevo_telefono != nodo_actual.telefono and self.existe_telefono(nuevo_telefono):
            return "duplicado_telefono"

        es_prio = prioritario if prioritario is not None else nodo_actual.prioritario
        self.eliminar_por_referencia(nombre_viejo, nodo_actual.telefono)
        self.insertar_ordenado(nuevo_nombre, nuevo_telefono, es_prio)
        return "ok"

    def toggle_prioridad(self, nombre, telefono):
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower() and actual.telefono == telefono:
                actual.prioritario = not actual.prioritario
                return True
            actual = actual.siguiente
        return False

    def deshacer_eliminacion(self):
        if not self.pila_deshacer:
            return False
        nodo = self.pila_deshacer.pop()
        self.insertar_ordenado(nodo.nombre, nodo.telefono, nodo.prioritario)
        return True
    
    def obtener_todos(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual)
            actual = actual.siguiente
        return elementos