
import random
import numpy
import time
import matplotlib.pyplot as plt
"""
TP°1 Alg. Geneticos
OBJETIVO: 
Buscar maximo de la funcion f(x) = (x/coef)^2 en el dominio [0 , 2^30 -1], donde coef = 2^30 -1 utilizando conceptos de Alg. Geneticos
Teniendo en cuenta los siguientes parametros:
    Probabilidad de Crossover = 0,75
    Probabilidad de Mutación = 0,05
    Población Inicial: 10 individuos
    Ciclos del programa: 20
    Método de Selección: Ruleta
    Método de Crossover: 1 Punto
    Método de Mutación: invertida
"""

CANT_POBLACION = 10
CANT_GENES = 30
PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05

#"Se inicializa la poblacion como una matriz o una lista anidada con valores aleatorios de cada gen en cada cromosoma"
def init_poblacion(cant_cromosomas, cant_genes):
    poblacion = []

    for _ in range(cant_cromosomas):
        cromo = []
        
        for _ in range(cant_genes):
            gen = random.randint(0, 1);
            cromo.append(gen);
            
        poblacion.append(cromo)
    
    return poblacion

#"Funcion que convierte una lista binaria y devuelve el resultado en decimal"
def binatodeci(binary):    
    resultado = 0

    for idx, val in enumerate(reversed(binary)):
        resultado += val * (2 ** idx)

    return resultado

#"Devuelve el valor de la funcion de x => f(x) = (x/coef)^2"
def funcion_objetivo(x):
    coef = (2**30)-1;
    return (x/coef)**2
    
#"Devuelve el fitness en funcion del cromosoma"
def funcion_fitness(cromosoma):
    x = binatodeci(cromosoma)
    return funcion_objetivo(x)

#"Funcion de seleccion: ruleta. Devuelve un nuevo cromosoma"
def ruleta(poblacion):    
    #"Se calcula el fitness de cada cromosoma y se agrega a la lista de fitness"
    fitness = []
    for cromosoma in poblacion:
        fitness.append(funcion_fitness(cromosoma))
    
    sum_fitness = sum(fitness)
    
    # Este es el giro random de la ruleta del rango del fitness
    r = random.uniform(0, sum_fitness)
 
    acumulado = 0

    # Se busca en que posicion cayo r iterando y acumulando cada probabilidad 
    for i in range(len(poblacion)):
        acumulado += fitness[i]

        if r <= acumulado:
            return poblacion[i].copy()

# Funcion mutacion: La mutacion es una probabilidad que puede ocurrir en algun gen cualquiera del cromosoma
def mutacion(cromosoma):
    if random.random() < PROB_MUTACION:
            gen_pos = random.randint(0, len(cromosoma)-1)
            cromosoma[gen_pos] = 1 - cromosoma[gen_pos] #Se invierte el gen.

    return cromosoma

# Funcion crossover de 1-punto, devuelve dos hijos
def crossover(padre1, padre2):
    if random.random() <= PROB_CROSSOVER:      
        punto = random.randint(1, len(padre1)-1) # Se corta en un punto aleatorio entre 1 y 29
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return [hijo1, hijo2]
    else:
        return [padre1.copy(), padre2.copy()] # Si no ocurre el crossover entonces se devuelven los mismos cromosomas

def aplicar_operadores(poblacion):
    nueva_poblacion = []
    
    for _ in range(len(poblacion)//2):
        padre1 = ruleta(poblacion)
        padre2 = ruleta(poblacion)
        hijos = crossover(padre1, padre2) #Devuelve una lista de dos hijos 
        hijo1 = mutacion(hijos[0])
        hijo2 = mutacion(hijos[1])
        nueva_poblacion.append(hijo1)
        nueva_poblacion.append(hijo2)
        
    return nueva_poblacion

def calcular_stats(poblacion):
    fitness = []

    for cromosoma in poblacion:
        fitness.append(funcion_fitness(cromosoma))

    #Se calculan las stats en forma de un diccionario
    return {
    "min": min(fitness),
    "max": max(fitness),
    "promedio": numpy.mean(fitness),
    "desvio": numpy.std(fitness)
    }

def graficar_ciclo(historial):
    fig, ax = plt.subplots()
    
    ax.set_title(str(len(historial)) + " Iteraciones")
    
    categories = ["Maximo", "Minimo", "Promedio"]
    
    valores = [
        historial[-1]["max"],
        historial[-1]["min"],
        historial[-1]["promedio"]
    ]
    
    bars = ax.bar(categories, valores)
    ax.bar_label(bars)
    ax.set_ylabel("Fitness")
    ax.set_ylim(0, 1)
    fig.show()
        

def imprimir_historial(historial):
    print("\n")
    print("HISTORIAL:")
    print("Gen | Min | Max | Promedio | Desvio | Tiempo(mseg)")
    print("------------------------------------------------")
    tiempo_total = 0
    for fila in historial:
        tiempo = fila["tiempo"]*1000
        tiempo_total += tiempo 
        
        print(
            fila["generacion"],"\t",
            round(fila["min"], 3),"\t",
            round(fila["max"], 3),"\t",
            round(fila["promedio"], 3),"\t",
            round(fila["desvio"], 3),"\t",
            round(tiempo, 3)
        )
    print("\n")
    print("RESUMEN")
    print("Tiempo Total: ", round(tiempo_total, 3),"(mseg)", "Tiempo Promedio: ", round(tiempo_total / len(historial), 3),"(mseg)")
    print("\nGraficar Ciclo? \n 1 - Si \n 2 - No\n")
    ingreso = int(input("Seleccione una opcion"))
    if ingreso == 1:
        graficar_ciclo(historial)

#Esta funcion devolvera un diccionario o historial de stats
def ejecutar_ciclos(nro_ciclos):
    
    if nro_ciclos <= 0: #Validacion
        return 0
    
    historial = [] # Historial de que contiene las stats de cada generacion: nro_gen, minimo, maximo, promedio, desvio, tiempo ejecucion
    
    start_time = time.perf_counter() # "Se obtiene el tiempo de ejecucion inicial"
    poblacion = init_poblacion(CANT_POBLACION, CANT_GENES)  #"Se inicializa la poblacion Inicial"
    stats = calcular_stats(poblacion)   
    end_time = time.perf_counter()
    
    historial.append({
        "generacion": 1,
        "min": stats["min"],
        "promedio": stats["promedio"],
        "max": stats["max"],
        "desvio": stats["desvio"],
        "tiempo": end_time - start_time         
    })
    
    #Aca empieza la generacion pos inicializada la primera.
    for generacion in range(nro_ciclos-1):           
        start_time = time.perf_counter() # "Se obtiene el tiempo de ejecucion actual"
        poblacion = aplicar_operadores(poblacion) #Para la siguiente poblacion 
        stats = calcular_stats(poblacion)   
        end_time = time.perf_counter()
     
        #Se guarda los stats de esta generacion en el historial
        historial.append({
            "generacion": generacion+2,
            "min": stats["min"],
            "promedio": stats["promedio"],
            "max": stats["max"],
            "desvio": stats["desvio"],
            "tiempo": end_time - start_time             
        })
       
    return historial

nro_ciclos = int(input("Seleccione la cantidad de ciclos: "))
historial = ejecutar_ciclos(nro_ciclos)
imprimir_historial(historial)
input("Press to exit...")








