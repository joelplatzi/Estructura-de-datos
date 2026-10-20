class Nodo:
    def __init__(self,nombre,telefono):
        self.nombre=nombre
        self.telefono=telefono
        self.siguiente=None
        
class ListaEnlazadaAgenda:
    def __init__(self):
        self.cabeza=None
        
    def insertar_ordenado(self,nombre,telefono):
        nuevo=Nodo(nombre,telefono)
        #si la lista esta vacia o el nuevo va antes que la cabeza (alfabeticamente)
        if self.cabeza is None or nombre.lower() < self.cabeza.nombre.lower():
            nuevo.siguiente=self.cabeza
            self.cabeza=nuevo
            return
        
        #buscar la posicion correcta
        actual=self.cabeza
        while actual.siguiente and actual.siguiente.nombre.lower()<nombre.lower():
            actual=actual.siguiente
            
        nuevo.siguiente=actual.siguiente
        actual.siguiente=nuevo
        
    def buscar(self,nombre):
        actual=self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return actual
            actual=actual.siguiente
        return None
    
    def buscar_parcial(self,texto):
        resultados=[]
        actual=self.cabeza
        while actual:
            if texto.lower() in actual.nombre.lower():
                resultados.append(actual)
            actual=actual.siguiente
            
        return resultados
    
    def eliminar(self,nombre):
        if not self.cabeza:
            return False
        
        # si es la cabeza
        if self.cabeza.nombre.lower() == nombre.lower():
            self.cabeza=self.cabeza.siguiente
            return True
        
        actual=self.cabeza
        while actual.siguiente and actual.siguiente.nombre.lower() != nombre.lower():
            actual=actual.siguiente
            
        if actual.siguiente:
            actual.siguiente=actual.siguiente.siguiente
            return True
        return False
    
    def mostrar(self):
        elementos=[]
        actual=self.cabeza
        while actual:
            #elementos.append(f"(actual.nombre)+(actual.telefono)")
            elementos.append(f"{actual.nombre} - {actual.telefono}")
            actual=actual.siguiente
        return elementos