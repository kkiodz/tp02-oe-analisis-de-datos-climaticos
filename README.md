# Trabajo Práctico: Gestión Colaborativa, Control de Versiones y Organización Empresarial (Git, GitHub y Jira)

## Equipo:
### - Hugo (Lider)
### - Paco (Desarrollador)
### - Luis (QA)


## Escenario elegido: A - Analisis de Datos Climaticos

Este proyecto procesa un archivo CSV con datos historicos de temperatura global.
El archivo contiene registros anuales de anomalias termicas desde 1850 hasta la actualidad.
El script lee esos datos, calcula indicadores importantes y guarda los resultados
en la carpeta resultados.

### Como funciona el codigo:
1. Carga el archivo temperaturasanuales.csv que tiene que estar en la carpeta datos
2. Lee linea por linea y guarda los valores de año y anomalia
3. Calcula el promedio de todas las anomalias
4. Busca el año mas calido y el año mas frio
5. Calcula la tendencia total comparando el primer registro con el ultimo
6. Calcula cuanto aumento la temperatura por decada
7. Hace una media movil de 5 años para suavizar la curva

### Resultados que genera:
- resultados_analisis.txt: contiene todos los indicadores calculados
- top_anios_temperatura.txt: lista los 10 años mas calidos y los 10 mas frios
- grafico_evolucion.txt: un grafico de texto que muestra la tendencia
- datos_procesados.csv: los datos originales con la columna de media movil

Ejecución programa:
python scripts/analisis_climatico.py

#### El programa automaticamente:
- busca el archivo en datos/temperaturasanuales.csv
- crea la carpeta resultados si no existe
- escribe todos los archivos de salida ahi

### Que significa cada indicador

**Anomalia promedio**: es el valor medio de todas las anomalias registradas.
Si es positivo significa que en promedio el planeta estuvo mas caliente
que la linea base establecida.

**Anomalia maxima**: el año con la temperatura mas alta registrada.

**Anomalia minima**: el año con la temperatura mas baja registrada.

**Tendencia por decada**: cuanto cambio la temperatura cada 10 años. Un valor
positivo indica calentamiento, negativo indica enfriamiento.

**Media movil 5 años**: promedio de los ultimos 5 años. Sirve para ver la
tendencia sin que los años particulares generen mucho ruido.

### Formato del archivo de entrada

**El archivo CSV tiene que tener este formato exacto:**

Source,Year,Mean
GCAG,1850,-0.4265
GCAG,1851,-0.2635

La primera linea es el encabezado. Despues cada linea tiene tres valores:
la fuente de datos, el año y la anomalia termica.

El script esta preparado para encontrar las columnas aunque los nombres
esten escritos en mayuscula o minuscula. Si los nombres son diferentes
igualmente funciona porque asigna por posicion.

## Consideraciones tecnicas 

El codigo precisa contar con Python 3.6 o superior 
que ya viene con todas las librerias necesarias, y la librería **matplotlib**. 

Los graficos se generan con la librería con matplotlib.

El manejo de errores esta contemplado. Si el archivo no existe o tiene
un formato incorrecto el programa muestra un mensaje y termina sin romperse.

Guardado archivos:

Los datos originales se guardan en la carpeta datos. El script asume
que el archivo se llama temperaturasanuales.csv.

Los resultados se guardan en la carpeta resultados. Si la carpeta no
existe el programa la crea automaticamente.

El script debe ejecutarse desde la carpeta raiz del proyecto porque usa
rutas relativas. Si se mueve a otro lado no va a encontrar los archivos.

Link al repositorio

[ [link github](https://github.com/kkiodz/tp02-oe-analisis-de-datos-climaticos) ]

Link al tablero de Jira

[ [link de Jira](https://juancruzdelapena.atlassian.net/?continue=https%3A%2F%2Fjuancruzdelapena.atlassian.net%2Fwelcome%2Fsoftware%3FprojectId%3D10000&atlOrigin=eyJpIjoiMmMyNDdjNTU2YWFkNGM4NDkxMzcwYWQzNGNkMmM3OWQiLCJwIjoiamlyYS1zb2Z0d2FyZSJ9) ]
