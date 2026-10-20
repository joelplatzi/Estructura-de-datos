import csv

def exportar_ambas_agendas(lista):
    """Guarda todos en agenda1.csv y filtra los prioritarios para agenda2.csv"""
    try:
        # 1. Guardar todos en agenda1.csv
        with open('agenda1.csv', 'w', newline='', encoding='utf-8') as f1:
            writer1 = csv.writer(f1)
            actual = lista.cabeza
            while actual:
                es_prio = '1' if actual.prioritario else '0'
                writer1.writerow([actual.nombre, actual.telefono, es_prio])
                actual = actual.siguiente

        # 2. Guardar únicamente los prioritarios en agenda2.csv
        with open('agenda2.csv', 'w', newline='', encoding='utf-8') as f2:
            writer2 = csv.writer(f2)
            actual = lista.cabeza
            while actual:
                if actual.prioritario:
                    writer2.writerow([actual.nombre, actual.telefono, '1'])
                actual = actual.siguiente

        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False
            
def importar_agenda(lista):
    """Carga los datos iniciales desde agenda1.csv al arrancar"""
    try:
        with open('agenda1.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for fila in reader:
                if len(fila) >= 2:
                    nombre, tel = fila[0], fila[1]
                    prioritario = True if len(fila) >= 3 and fila[2] == '1' else False
                    lista.insertar_ordenado(nombre, tel, prioritario)
        return True
    except Exception:
        # Si agenda1.csv no existe todavía, no pasa nada
        return False