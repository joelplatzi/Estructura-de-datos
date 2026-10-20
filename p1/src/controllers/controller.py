import csv

def exportar_csv(lista, archivo='agenda.csv'):
    try:
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            actual = lista.cabeza
            while actual:
                writer.writerow([actual.nombre, actual.telefono])
                actual = actual.siguiente
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False
            
def importar_csv(lista, archivo='agenda.csv'):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for fila in reader:
                if len(fila) >= 2:
                    nombre, tel = fila[0], fila[1]
                    lista.insertar_ordenado(nombre, tel)
        return True
    except Exception:
        return False