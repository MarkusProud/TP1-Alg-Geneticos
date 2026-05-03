
from random import *
from numpy import *
import time

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

PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05

tiempos_ejecucion = []

#"Se inicializa la poblacion como una matriz o una lista anidada con valores aleatorios de cada gen en cada cromosoma"
def init_poblacion(cant_cromosomas, cant_genes):
    poblacion = []

    for i in range(cant_cromosomas):
        cromo = []
        
        for j in range(cant_genes):
            gen = randint(0, 1);
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

#"Funcion de seleccion: ruleta. Devuelve un cromosoma"
def ruleta(poblacion):
    cromo = []
    
    # "TODO: Se selecciona el cromosoma de la poblacion usando el metodo de la ruleta"
    
    return cromo;

# Funcion mutacion
def mutacion(cromosoma):
    
    return 0

# Funcion crossover
def crossover(cromo_p, cromo_m):
    
    return 0

# Funcion recursiva. Aca se ejecutan los ciclos del programa y se aplicaran el crossover, el metodo de seleccion y la mutacion.
def ciclo(poblacion, ciclos):  
    start_time = time.perf_counter() # "Se obtiene el tiempo de ejecucion actual"
    
    fitness = []

    for cromosoma in poblacion:
        fitness.append(funcion_fitness(cromosoma)) #"Se calcula el fitness de cada cromosoma y se agrega a la lista de fitness"
    
    print("")
    print(fitness)
    print(max(fitness))     #"Devuelve el maximo de la poblacion"
    print(min(fitness))     #"Devuelve el minimo de la poblacion"
    print(mean(fitness))    #"Devuelve el promedio de la poblacion"
    print(std(fitness))     #"Devuelve el el desvio estandar de la poblacion"
    
    #"TODO: Aca se hace el metodo de seleccion el crossover y la mutacion"
    
    end_time = time.perf_counter()  # "Se obtiene el tiempo de ejecucion cuando finaliza un ciclo"

    tiempos_ejecucion.append(end_time - start_time)
    
    if ciclos <= 1:
        # "Finaliza todos los ciclos y muestra las estadisticas, graficos, etc"
        print("Tiempo Promedio de Ejecucion: ", mean(tiempos_ejecucion))
    else:
        ciclo(poblacion, ciclos-1)
    

poblacion = init_poblacion(10, 30)  #"Se inicializaa la poblacion Inicial"

nro_ciclos = int(input("Seleccione la cantidad de ciclos: "))

ciclo(poblacion, nro_ciclos) #"Se ejecuta el ciclo del programa de forma recursiva"

time.sleep(1)

input("Press to exit...")









