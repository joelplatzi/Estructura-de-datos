class Nodo:
    def __init__(self, nombre, telefono, prioritario=False):
        self.nombre = nombre
        self.telefono = telefono
        self.prioritario = prioritario
        self.siguiente = None
        
class ListaEnlazadaAgenda:
    def __init__(self):
        self.cabeza = None
        self.pila_deshacer = [] # Pila (Stack) LIFO para la función Deshacer
        
    def insertar_ordenado(self, nombre, telefono, prioritario=False):
        nuevo = Nodo(nombre, telefono, prioritario)
        if self.cabeza is None or nombre.lower() < self.cabeza.nombre.lower():
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            return
        
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.nombre.lower() < nombre.lower():
            actual = actual.siguiente
            
        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        
    def buscar(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return actual
            actual = actual.siguiente
        return None
    
    def actualizar(self, nombre, nuevo_telefono):
        nodo = self.buscar(nombre)
        if nodo:
            nodo.telefono = nuevo_telefono
            return True
        return False
    
    def eliminar_por_referencia(self, nombre, telefono):
        """Elimina un contacto exacto y lo guarda temporalmente en la Pila"""
        if not self.cabeza:
            return False
        
        if self.cabeza.nombre.lower() == nombre.lower() and self.cabeza.telefono == telefono:
            eliminado = self.cabeza
            self.cabeza = self.cabeza.siguiente
            self.pila_deshacer.append(eliminado) # Se guarda en la pila
            return True
        
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.nombre.lower() == nombre.lower() and actual.siguiente.telefono == telefono:
                eliminado = actual.siguiente
                actual.siguiente = actual.siguiente.siguiente
                self.pila_deshacer.append(eliminado) # Se guarda en la pila
                return True
            actual = actual.siguiente
        return False

    def toggle_prioridad(self, nombre, telefono):
        """Cambia el estado de prioridad de un contacto específico"""
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower() and actual.telefono == telefono:
                actual.prioritario = not actual.prioritario
                return True
            actual = actual.siguiente
        return False

    def deshacer_eliminacion(self):
        """Restaura el último elemento eliminado de la Pila (LIFO)"""
        if not self.pila_deshacer:
            return False
        nodo = self.pila_deshacer.pop()
        self.insertar_ordenado(nodo.nombre, nodo.telefono, nodo.prioritario)
        return True
    
    def obtener_todos(self):
        """Devuelve una lista con todos los objetos Nodo para pintarlos en la interfaz"""
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual)
            actual = actual.siguiente
        return elementos