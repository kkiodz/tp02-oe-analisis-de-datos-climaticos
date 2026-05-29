import os
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    TIENE_PLT = True
except ImportError:
    TIENE_PLT = False
    print("Nota: matplotlib no disponible, se usará gráfico ASCII")

# Configuracion de rutas

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATOS_PATH = os.path.join(BASE_DIR, 'datos', 'temperaturasanuales.csv')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'resultados')

os.makedirs(RESULTADOS_DIR, exist_ok=True)

print("\n" + "="*60)
print("ANALISIS DE TEMPERATURA GLOBAL (CSV")
print("="*60 + "\n")

# Verificar que el archivo existe

if not os.path.exists(DATOS_PATH):
    print(f"ERROR: No se encuentra el archivo: {DATOS_PATH}")
    print(f"Nota: Asegurate de tener el archivo 'temperaturasanuales.csv' en la carpeta /datos")
    print(f"Nota: El archivo debe tener el formato: Source,Year,Mean")
    exit()

# Paso 1: cargar datos del csv manualmente

print("Cargando archivo CSV...")
datos = []
fuente = ""

try:
    with open(DATOS_PATH, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
    
    # la primera linea es el encabezado
    if not lineas:
        print("ERROR: El archivo esta vacio")
        exit()
    
    encabezado = lineas[0].strip().split(',')
    print(f"Encabezado encontrado: {encabezado}")
    

    idx_source = -1
    idx_year = -1
    idx_mean = -1
    
    for i, col in enumerate(encabezado):
        col_clean = col.strip().lower()
        if 'source' in col_clean:
            idx_source = i
        elif 'year' in col_clean:
            idx_year = i
        elif 'mean' in col_clean:
            idx_mean = i

    if idx_source == -1:
        idx_source = 0
    if idx_year == -1:
        idx_year = 1
    if idx_mean == -1:
        idx_mean = 2
    
    # Procesar lineas de datos (desde la linea 1 hasta el final)
    for linea in lineas[1:]:
        linea = linea.strip()
        if not linea:
            continue
        
        partes = linea.split(',')
        if len(partes) > max(idx_source, idx_year, idx_mean):
            try:
                fuente = partes[idx_source].strip()
                año = int(partes[idx_year].strip())
                anomalia = float(partes[idx_mean].strip())
                datos.append({
                    'fuente': fuente,
                    'año': año,
                    'anomalia': anomalia
                })
            except ValueError as e:
                print(f"Advertencia: Error al procesar linea: {linea} - {e}")
                continue
    
    print(f"Datos cargados correctamente desde: {DATOS_PATH}")
    print(f"Registros encontrados: {len(datos)} años")
    if datos:
        print(f"Fuente de datos: {fuente}")
        print(f"Periodo: {datos[0]['año']} - {datos[-1]['año']}")
    
except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo: {DATOS_PATH}")
    exit()
except Exception as e:
    print(f"ERROR: Error al cargar el archivo: {e}")
    exit()

if not datos:
    print("ERROR: No se pudieron cargar los datos. Verifica el archivo.")
    exit()

# Paso 2: calcular indicadores climaticos
print("\n" + "="*50)
print("CALCULO DE INDICADORES CLIMATICOS")
print("="*50)

# inicializar acumuladores
suma_anomalias = 0.0
anomalia_max = datos[0]['anomalia']
anomalia_min = datos[0]['anomalia']
año_max = datos[0]['año']
año_min = datos[0]['año']

for registro in datos:
    anomalia = registro['anomalia']
    año = registro['año']
    
    suma_anomalias += anomalia
    
    if anomalia > anomalia_max:
        anomalia_max = anomalia
        año_max = año
    
    if anomalia < anomalia_min:
        anomalia_min = anomalia
        año_min = año

# ---------------- Promedio +  Tendencias ----------------
cantidad = len(datos)
anomalia_promedio = suma_anomalias / cantidad

primera_anomalia = datos[0]['anomalia']
ultima_anomalia = datos[-1]['anomalia']
tendencia_total = ultima_anomalia - primera_anomalia
# ----------------------------------------------------------------

# Calentamiento por decada
años_totales = datos[-1]['año'] - datos[0]['año']
if años_totales > 0:
    calentamiento_por_decada = (tendencia_total / años_totales) * 10
else:
    calentamiento_por_decada = 0

# Paso 3: calcular media movil de 5 años
ventana = 5
media_movil_5 = []
for i in range(len(datos)):
    if i < ventana - 1:
        media_movil_5.append((datos[i]['año'], None))
    else:
        suma = 0.0
        for j in range(i - ventana + 1, i + 1):
            suma += datos[j]['anomalia']
        media = suma / ventana
        media_movil_5.append((datos[i]['año'], media))

# Muestro resultados en pantalla
print(f"\nRESULTADOS (Anomalias de temperatura vs linea base):")
print(f"   • Anomalia promedio: {anomalia_promedio:.4f}°C")
print(f"   • Anomalia maxima: {anomalia_max:.4f}°C (año {año_max})")
print(f"   • Anomalia minima: {anomalia_min:.4f}°C (año {año_min})")
print(f"   • Tendencia general: {tendencia_total:+.4f}°C")
print(f"   • Calentamiento por decada: {calentamiento_por_decada:+.4f}°C/decada")

# Almaceno resultados en un diccionario
resultados = {
    'fuente_datos': datos[0]['fuente'] if datos else "Desconocida",
    'periodo_inicio': datos[0]['año'],
    'periodo_fin': datos[-1]['año'],
    'cantidad_registros': cantidad,
    'anomalia_promedio': anomalia_promedio,
    'anomalia_maxima': anomalia_max,
    'año_anomalia_maxima': año_max,
    'anomalia_minima': anomalia_min,
    'año_anomalia_minima': año_min,
    'tendencia_total': tendencia_total,
    'calentamiento_por_decada': calentamiento_por_decada,
    'media_movil_5': media_movil_5,
    'fecha_analisis': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Paso 4: generar grafico ascii en consola
print("\n" + "="*50)
print("GRAFICO DE EVOLUCION (Vista simplificada)")
print("="*50)

# tomar una muestra para no saturar (maximo 40 años)
paso = max(1, len(datos) // 40)
muestra = datos[::paso]

min_anomalia = resultados['anomalia_minima']
max_anomalia = resultados['anomalia_maxima']
rango = max_anomalia - min_anomalia
if rango == 0:
    rango = 1

escala = 50
linea_cero = int((0 - min_anomalia) / rango * escala)

print(f"\nEscala: {min_anomalia:.2f}°C (izquierda) a {max_anomalia:.2f}°C (derecha)")
print(f"(Cada '=' representa aproximadamente {rango/escala:.2f}°C)")
print("-"*80)

for reg in muestra:
    año = reg['año']
    anomalia = reg['anomalia']
    
    pos = int((anomalia - min_anomalia) / rango * escala)
    
    if anomalia >= 0:
        barra = " " * linea_cero + "█" * max(1, pos - linea_cero)
    else:
        barra = "▒" * max(1, linea_cero - pos) + " " * (escala - linea_cero)
    
    marcador = ""
    if año == resultados['año_anomalia_maxima']:
        marcador = " <- MAXIMO"
    elif año == resultados['año_anomalia_minima']:
        marcador = " <- MINIMO"
    
    print(f"{año:4d} | {barra} {anomalia:6.3f}°C{marcador}")

print("-"*80)

# SE COMENTA GRAFICO EN ASCII YA QUE TENGO EL MATPLOTLIB DISPONIBLE, PERO SE DEJA EL CODIGO COMO REFERENCIA PARA FUTURAS VERSIONES SIN DEPENDENCIAS EXTERNAS
# output_grafico = os.path.join(RESULTADOS_DIR, 'grafico_evolucion.txt')
# with open(output_grafico, 'w', encoding='utf-8') as f:
#     f.write("="*70 + "\n")
#     f.write("GRAFICO DE EVOLUCION DE TEMPERATURA GLOBAL (formato texto)\n")
#     f.write("="*70 + "\n\n")
    
#     f.write(f"Escala: {min_anomalia:.2f}°C a {max_anomalia:.2f}°C\n")
#     f.write(f"Linea 0°C marcada con '|'\n")
#     f.write("-"*80 + "\n")
    
#     for reg in datos:
#         año = reg['año']
#         anomalia = reg['anomalia']
        
#         pos = int((anomalia - min_anomalia) / rango * escala)
        
#         if pos >= linea_cero:
#             barra = " " * linea_cero + "█" * (pos - linea_cero) + "|"
#         else:
#             barra = "▒" * (linea_cero - pos) + "|" + " " * (escala - linea_cero)
        
#         f.write(f"{año:4d} | {barra} {anomalia:6.3f}°C\n")
    
#     f.write("-"*80 + "\n")

# print(f"Grafico guardado en: {output_grafico}")

# paso 6: guardar resultados numericos en archivo de texto
output_resultados = os.path.join(RESULTADOS_DIR, 'resultados_analisis.txt')
with open(output_resultados, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("ANALISIS DE TEMPERATURA GLOBAL - RESULTADOS FINALES\n")
    f.write("="*70 + "\n\n")
    
    f.write(f"Fecha del analisis: {resultados['fecha_analisis']}\n")
    f.write(f"Fuente de datos: {resultados['fuente_datos']}\n")
    f.write(f"Periodo analizado: {resultados['periodo_inicio']} - {resultados['periodo_fin']}\n")
    f.write(f"Cantidad de años registrados: {resultados['cantidad_registros']}\n\n")
    
    f.write("="*70 + "\n")
    f.write("INDICADORES DE TEMPERATURA\n")
    f.write("="*70 + "\n\n")
    
    f.write("ANOMALIA PROMEDIO:\n")
    f.write(f"   • Valor: {resultados['anomalia_promedio']:.6f}°C\n")
    f.write(f"   • Interpretacion: La temperatura global ha sido ")
    if resultados['anomalia_promedio'] > 0:
        f.write("SUPERIOR")
    else:
        f.write("INFERIOR")
    f.write(" a la linea base\n\n")
    
    f.write("ANOMALIA MAXIMA (Año mas calido):\n")
    f.write(f"   • Año: {resultados['año_anomalia_maxima']}\n")
    f.write(f"   • Valor: {resultados['anomalia_maxima']:.6f}°C\n\n")
    
    f.write("ANOMALIA MINIMA (Año mas frio):\n")
    f.write(f"   • Año: {resultados['año_anomalia_minima']}\n")
    f.write(f"   • Valor: {resultados['anomalia_minima']:.6f}°C\n\n")
    
    f.write("TENDENCIAS:\n")
    f.write(f"   • Cambio total del periodo: {resultados['tendencia_total']:+.6f}°C\n")
    f.write(f"   • Calentamiento por decada: {resultados['calentamiento_por_decada']:+.6f}°C/decada\n")
    
    if resultados['calentamiento_por_decada'] > 0:
        f.write(f"   • Conclusion: El planeta se esta CALENTANDO a razon de ")
        f.write(f"{abs(resultados['calentamiento_por_decada']):.4f}°C por decada\n\n")
    else:
        f.write(f"   • Conclusion: El planeta se esta ENFRIANDO a razon de ")
        f.write(f"{abs(resultados['calentamiento_por_decada']):.4f}°C por decada\n\n")

print(f"Resultados guardados en: {output_resultados}")

# paso 7: guardar top 10 años mas calidos y mas frios
output_top = os.path.join(RESULTADOS_DIR, 'top_anios_temperatura.txt')

# copiar listas para ordenar
datos_calidos = datos.copy()
datos_frios = datos.copy()

# ordenar por anomalia descendente (mas calidos primero) con bubble sort
for i in range(len(datos_calidos)):
    for j in range(i + 1, len(datos_calidos)):
        if datos_calidos[i]['anomalia'] < datos_calidos[j]['anomalia']:
            datos_calidos[i], datos_calidos[j] = datos_calidos[j], datos_calidos[i]

# ordenar por anomalia ascendente (mas frios primero) con bubble sort
for i in range(len(datos_frios)):
    for j in range(i + 1, len(datos_frios)):
        if datos_frios[i]['anomalia'] > datos_frios[j]['anomalia']:
            datos_frios[i], datos_frios[j] = datos_frios[j], datos_frios[i]

top_calidos = datos_calidos[:10]
top_frios = datos_frios[:10]

with open(output_top, 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("TOP 10 AÑOS MAS CALIDOS\n")
    f.write("="*60 + "\n")
    for reg in top_calidos:
        f.write(f"   Año {reg['año']:4d}: {reg['anomalia']:.4f}°C\n")
    
    f.write("\n" + "="*60 + "\n")
    f.write("TOP 10 AÑOS MAS FRIOS\n")
    f.write("="*60 + "\n")
    for reg in top_frios:
        f.write(f"   Año {reg['año']:4d}: {reg['anomalia']:.4f}°C\n")

print(f"Top años guardado en: {output_top}")

# paso 8: guardar datos procesados año por año (csv)
output_csv = os.path.join(RESULTADOS_DIR, 'datos_procesados.csv')
with open(output_csv, 'w', encoding='utf-8') as f:
    f.write("Año,Anomalia_C,Media_Movil_5a\n")
    
    for i, reg in enumerate(datos):
        año = reg['año']
        anomalia = reg['anomalia']
        
        media_movil = ""
        if i >= 4:
            mm = media_movil_5[i][1]
            if mm is not None:
                media_movil = f"{mm:.4f}"
        
        f.write(f"{año},{anomalia:.4f},{media_movil}\n")

print(f"Datos procesados guardados en: {output_csv}")

if TIENE_PLT and len(datos) > 10:
    plt.figure(figsize=(10,5))
    plt.plot([d['año'] for d in datos], [d['anomalia'] for d in datos])
    plt.savefig(os.path.join(RESULTADOS_DIR, 'grafico.png'))
    print("Gráfico PNG generado adicionalmente")

# finalizar
print("\n" + "="*60)
print("ANALISIS COMPLETADO CON EXITO")
print(f"Resultados guardados en: {RESULTADOS_DIR}")
print("\nArchivos generados:")
print("   • resultados_analisis.txt - Indicadores principales")
print("   • top_anios_temperatura.txt - Años mas calidos/frios")
print("   • grafico_evolucion.txt - Grafico de evolucion")
print("   • datos_procesados.csv - Datos año por año (CSV)")
print("="*60)