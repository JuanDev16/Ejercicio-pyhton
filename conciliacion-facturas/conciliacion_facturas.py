from collections import defaultdict
 

erp = [
    {"numero": "F01", "proveedor": "ProveedorA", "valor": 1000},
    {"numero": "F02", "proveedor": "ProveedorB", "valor": 2000},
    {"numero": "F03", "proveedor": "ProveedorC", "valor": 1500},
    {"numero": "F04", "proveedor": "ProveedorD", "valor": 3000},
    {"numero": "F05", "proveedor": "ProveedorE", "valor": 2500},
    {"numero": "F06", "proveedor": "ProveedorF", "valor": 1800},
    {"numero": "F02", "proveedor": "ProveedorB", "valor": 2000},  # duplicada
    {"numero": "F07", "proveedor": "ProveedorG", "valor": 2200},
]
 
portal = [
    {"numero": "F01", "proveedor": "ProveedorA", "valor": 1000},  # conciliada
    {"numero": "F02", "proveedor": "ProveedorB", "valor": 2500},  # diferencia
    {"numero": "F03", "proveedor": "ProveedorC", "valor": 1500},  # conciliada
    {"numero": "F08", "proveedor": "ProveedorH", "valor": 4000},  # faltante en ERP
    {"numero": "F09", "proveedor": "ProveedorI", "valor": 500},
    {"numero": "F05", "proveedor": "ProveedorE", "valor": 2600},  # diferencia
    {"numero": "F09", "proveedor": "ProveedorI", "valor": 500},   # duplicada
    {"numero": "F10", "proveedor": "ProveedorJ", "valor": 700},
]

 
# Funciones

def detectar_duplicados(lista, nombre_lista):
    duplicados = []
    conteo = defaultdict(int)
    for factura in lista:
        numero = factura.get("numero")
        if numero:
            conteo[numero] += 1
    for numero, cantidad in conteo.items():
        if cantidad > 1:
            duplicados.append({"numero": numero, "lista": nombre_lista, "cantidad": cantidad})
    return duplicados
 
def conciliar_facturas(erp, portal):
    conciliadas = []
    diferencias = []
    faltantes_portal = []
    faltantes_erp = []
 
    # Crear índices por número
    index_erp = {f["numero"]: f for f in erp if f.get("numero")}
    index_portal = {f["numero"]: f for f in portal if f.get("numero")}
 
    
    for numero, factura in index_erp.items():
        if numero in index_portal:
            valor_erp = factura.get("valor", 0)
            valor_portal = index_portal[numero].get("valor", 0)
            if valor_erp == valor_portal:
                conciliadas.append(factura)
            else:
                diferencias.append({
                    "numero": numero,
                    "valor_erp": valor_erp,
                    "valor_portal": valor_portal,
                    "diferencia": abs(valor_erp - valor_portal)
                })
        else:
            faltantes_portal.append(factura)
 
    # Revisar Portal contra ERP
    for numero, factura in index_portal.items():
        if numero not in index_erp:
            faltantes_erp.append(factura)
 
    return conciliadas, diferencias, faltantes_portal, faltantes_erp
 
def generar_reporte(erp, portal):
    conciliadas, diferencias, faltantes_portal, faltantes_erp = conciliar_facturas(erp, portal)
    duplicados = detectar_duplicados(erp, "ERP") + detectar_duplicados(portal, "Portal")
 
    # Reporte por categoría
    print("REPORTE DE CONCILIACIÓN \n")
 
    print("1. Conciliadas:")
    for f in conciliadas:
        print(f"   Factura {f['numero']} - Proveedor {f['proveedor']} - Valor {f['valor']}")
 
    print("\n2. Diferencias de valor:")
    for f in diferencias:
        print(f"   Factura {f['numero']} - ERP: {f['valor_erp']} | Portal: {f['valor_portal']} | Dif: {f['diferencia']}")
 
    print("\n3. Faltantes en Portal:")
    for f in faltantes_portal:
        print(f"   Factura {f['numero']} - Proveedor {f['proveedor']} - Valor {f['valor']}")
 
    print("\n4. Faltantes en ERP:")
    for f in faltantes_erp:
        print(f"   Factura {f['numero']} - Proveedor {f['proveedor']} - Valor {f['valor']}")
 
    print("\n5. Duplicadas:")
    for f in duplicados:
        print(f"   Factura {f['numero']} duplicada en {f['lista']} ({f['cantidad']} veces)")
 
    # Totales
    total_conciliadas = sum(f["valor"] for f in conciliadas)
    total_diferencias = sum(f["diferencia"] for f in diferencias)
 
    print("\nTOTALES ")
    print(f"Conciliadas: {len(conciliadas)} | Valor total conciliado: {total_conciliadas}")
    print(f"Diferencias: {len(diferencias)} | Valor total en diferencia: {total_diferencias}")
    print(f"Faltantes en Portal: {len(faltantes_portal)}")
    print(f"Faltantes en ERP: {len(faltantes_erp)}")
    print(f"Duplicadas: {len(duplicados)}")
 

# Ejecución

if __name__ == "__main__":
    generar_reporte(erp, portal)