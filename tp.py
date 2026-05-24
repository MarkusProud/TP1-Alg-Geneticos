
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
#CONSTANTES
CANT_POBLACION = 10
CANT_GENES = 30
PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05
TORNEO_TAM = 3  # Tamaño del torneo para la selección por torneo (Opción B)
RULETA = 1
TORNEO = 2
ELITISMO = 3

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
    coef = (2**30)-1
    return (x/coef)**2
    
#"Devuelve el fitness en funcion del cromosoma"
def funcion_fitness(cromosoma):
    x = binatodeci(cromosoma)
    return funcion_objetivo(x)

# Evalua toda la poblacion y devuelve una lista con los fitness de cada cromosoma
def evaluar_poblacion(poblacion):
    fitness = []

    for cromosoma in poblacion:
        fitness.append(funcion_fitness(cromosoma))

    return fitness

# -- RULETA --
#"Funcion de seleccion: ruleta. Devuelve un nuevo cromosoma"
def ruleta(poblacion):    
    #"Se calcula el fitness de cada cromosoma y se agrega a la lista de fitness"
    fitness = []
    
    for cromosoma in poblacion:
        fitness.append(funcion_fitness(cromosoma))
    
    sum_fitness = sum(fitness)
    
    # Esto es solo validacion en caso de que ocurra la improbabilidad que todo los fitness sumen 0
    if sum_fitness == 0:
        return random.choice(poblacion).copy()
    
    # Este es el giro random de la ruleta del rango del fitness
    r = random.uniform(0, sum_fitness)
 
    acumulado = 0

    # Se busca en que posicion cayo r iterando y acumulando cada probabilidad 
    for i in range(len(poblacion)):
        acumulado += fitness[i]

        if r <= acumulado:
            return poblacion[i].copy()

# -- TORNEO --
# Elige TORNEO_TAM individuos al azar y devuelve el mejor de ese grupo
def torneo(poblacion):
    candidatos = []

    # Selecciona individuos aleatorios de la poblacion
    for _ in range(TORNEO_TAM):
        indice = random.randint(0, len(poblacion) - 1)
        candidatos.append(poblacion[indice])

    # Tomamos el primer candidato como ganador inicial
    ganador = candidatos[0]
    mejor_fitness = funcion_fitness(ganador)

    # Comparamos contra el resto de candidatos
    for cromosoma in candidatos[1:]:
        fitness_actual = funcion_fitness(cromosoma)

        if fitness_actual > mejor_fitness:
            mejor_fitness = fitness_actual
            ganador = cromosoma

    return ganador.copy()
#- ELITISMO -
# Elige el mejor individuo de la poblacion y lo devuelve
def elitismo(poblacion):
    mejor_cromosoma = poblacion[0]
    mejor_fitness = funcion_fitness(mejor_cromosoma)

    for cromosoma in poblacion[1:]:
        fitness_actual = funcion_fitness(cromosoma)

        if fitness_actual > mejor_fitness:
            mejor_fitness = fitness_actual
            mejor_cromosoma = cromosoma

    return mejor_cromosoma.copy()

# Reemplaza el peor individuo de la nueva población por el elite
def reemplazar_peor_por_elite(nueva_poblacion, elite):
    peor_indice = 0
    peor_fitness = funcion_fitness(nueva_poblacion[0])

    # Buscar el peor individuo
    for i in range(1, len(nueva_poblacion)):
        fitness_actual = funcion_fitness(nueva_poblacion[i])

        if fitness_actual < peor_fitness:
            peor_fitness = fitness_actual
            peor_indice = i

    # Reemplazar por el elite
    nueva_poblacion[peor_indice] = elite.copy()

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

def aplicar_operadores(poblacion, metodo):
    nueva_poblacion = []
    elite = elitismo(poblacion) #Necesitamos guardar el mejor individuo actual

    for _ in range(len(poblacion)//2):
        padre1 = []
        padre2 = []
        
        if metodo == RULETA or metodo == ELITISMO: #En el caso de elitismo se puede usar el metodo de ruleta para generar la poblacion
            padre1 = ruleta(poblacion)
            padre2 = ruleta(poblacion)
        elif metodo == TORNEO:
            padre1 = torneo(poblacion)
            padre2 = torneo(poblacion)
        
        hijos = crossover(padre1, padre2) #Devuelve una lista de dos hijos 
        hijo1 = mutacion(hijos[0])
        hijo2 = mutacion(hijos[1])
        nueva_poblacion.append(hijo1)
        nueva_poblacion.append(hijo2)
    # --- ELITISMO ---
    if metodo == ELITISMO:
        reemplazar_peor_por_elite(nueva_poblacion, elite)
    return nueva_poblacion

def calcular_stats(poblacion):
    
    fitness = evaluar_poblacion(poblacion)
    
    #Se calculan las stats en forma de un diccionario
    return {
    "min": min(fitness),
    "max": max(fitness),
    "promedio": numpy.mean(fitness),
    "desvio": numpy.std(fitness)
    }

def graficar_ciclo(historial):
    generaciones = [fila["generacion"] for fila in historial]
    maximos = [fila["max"] for fila in historial]
    minimos = [fila["min"] for fila in historial]
    promedios = [fila["promedio"] for fila in historial]

    fig, ax = plt.subplots()

    ax.set_title(f"Evolución del Fitness - {len(historial)} Generaciones")    
    
    ax.plot(generaciones, maximos, label="Máximo")
    ax.plot(generaciones, promedios, label="Promedio")
    ax.plot(generaciones, minimos, label="Mínimo")
    
    ax.set_xlabel("Generación")
    ax.set_ylabel("Fitness")

    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(True)
    
    plt.show()

#Esta funcion devolvera un diccionario o historial de stats
def ejecutar_ciclos(poblacion_inicial, nro_ciclos, metodo):
    
    if nro_ciclos <= 0:
        return []
    
    historial = []

    start_time = time.perf_counter()

    # Usamos una copia de la poblacion inicial
    poblacion = []

    for cromosoma in poblacion_inicial:
        poblacion.append(cromosoma.copy())

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
    
    for generacion in range(nro_ciclos - 1):           
        start_time = time.perf_counter()

        poblacion = aplicar_operadores(poblacion, metodo)

        stats = calcular_stats(poblacion)   
        end_time = time.perf_counter()
     
        historial.append({
            "generacion": generacion + 2,
            "min": stats["min"],
            "promedio": stats["promedio"],
            "max": stats["max"],
            "desvio": stats["desvio"],
            "tiempo": end_time - start_time             
        })
       
    return historial
        
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
 
#Se inicializa la primera poblacion.
poblacion_inicial = init_poblacion(CANT_POBLACION, CANT_GENES)
    
# Generaciones 20, 100 y 200 con metodo RULETA
histRuleta20 = ejecutar_ciclos(poblacion_inicial, 20, RULETA)
histRuleta100 = ejecutar_ciclos(poblacion_inicial, 100, RULETA)
histRuleta200 = ejecutar_ciclos(poblacion_inicial, 200, RULETA)

# Historial Por Consola
imprimir_historial(histRuleta20)
imprimir_historial(histRuleta100)
imprimir_historial(histRuleta200)

# Graficas matplotlib
graficar_ciclo(histRuleta20)
graficar_ciclo(histRuleta100)
graficar_ciclo(histRuleta200)

# Generaciones 20, 100 y 200 con metodo TORNEO
histTorneo20 = ejecutar_ciclos(poblacion_inicial, 20, TORNEO)
histTorneo100 = ejecutar_ciclos(poblacion_inicial, 100, TORNEO)
histTorneo200 = ejecutar_ciclos(poblacion_inicial, 200, TORNEO)

# Historial Por Consola
imprimir_historial(histTorneo20)
imprimir_historial(histTorneo100)
imprimir_historial(histTorneo200)

# Graficas matplotlib
graficar_ciclo(histTorneo20)
graficar_ciclo(histTorneo100)
graficar_ciclo(histTorneo200)

# Generaciones 20, 100 y 200 (NO PIDE EL DE 200) con metodo ELITE
histElitismo20 = ejecutar_ciclos(poblacion_inicial, 20, ELITISMO)
histElitismo100 = ejecutar_ciclos(poblacion_inicial, 100, ELITISMO)
#histElitismo200 = ejecutar_ciclos(poblacion_inicial, 200, ELITISMO)

# Historial Por Consola
imprimir_historial(histElitismo20)
imprimir_historial(histElitismo100)
#imprimir_historial(histElitismo200)

# Graficas matplotlib
graficar_ciclo(histElitismo20)
graficar_ciclo(histElitismo100)
#graficar_ciclo(histElitismo200)

input("Press to exit...")


