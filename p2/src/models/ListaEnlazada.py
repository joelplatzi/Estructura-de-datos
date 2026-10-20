class Nodo:
    def __init__(self, nombre, telefono, prioritario=False):
        self.nombre = nombre
        self.telefono = telefono
        self.prioritario = prioritario  # True si es prioritario, False si es normal
        self.siguiente = None
        
class ListaEnlazadaAgenda:
    def __init__(self):
        self.cabeza = None
        
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
    
    def buscar_parcial(self, texto):
        resultados = []
        actual = self.cabeza
        while actual:
            if texto.lower() in actual.nombre.lower():
                resultados.append(actual)
            actual = actual.siguiente
        return resultados
    
    def actualizar(self, nombre, nuevo_telefono):
        nodo = self.buscar(nombre)
        if nodo:
            nodo.telefono = nuevo_telefono
            return True
        return False
    
    def eliminar(self, nombre):
        if not self.cabeza:
            return False
        
        if self.cabeza.nombre.lower() == nombre.lower():
            self.cabeza = self.cabeza.siguiente
            return True
        
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.nombre.lower() != nombre.lower():
            actual = actual.siguiente
            
        if actual.siguiente:
            actual.siguiente = actual.siguiente.siguiente
            return True
        return False
    
    def mostrar(self):
        elementos = []
        actual = self.cabeza
        while actual:
            marca = "⭐ " if actual.prioritario else "• "
            elementos.append(f"{marca}{actual.nombre} - {actual.telefono}")
            actual = actual.siguiente
        return elementos

    def mostrar_prioritarios(self):
        elementos = []
        actual = self.cabeza
        while actual:
            if actual.prioritario:
                elementos.append(f"⭐ {actual.nombre} - {actual.telefono}")
            actual = actual.siguiente
        return elementos