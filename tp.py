
from random import *
from numpy import *

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

"Se inicializa la poblacion como una matriz o una lista anidada con valores aleatorios de cada gen en cada cromosoma"
def inicializar_poblacion(cant_cromosomas, cant_genes):
    poblacion = []
    
    for i in range(cant_cromosomas):
        cromo = []
        
        for j in range(cant_genes):
            gen = randint(0, 1);
            cromo.append(gen);
            
        poblacion.append(cromo)
    
    return poblacion

"Funcion que convierte una lista binaria y devuelve el resultado en decimal"
def binatodeci(binary):    
    resultado = 0

    for idx, val in enumerate(reversed(binary)):
        resultado += val * (2 ** idx)

    return resultado

"Devuelve el valor de la funcion de x => f(x) = (x/coef)^2"
def funcion_objetivo(x):
    coef = (2**30)-1;
    return (x/coef)**2
    
"Devuelve el fitness en funcion del cromosoma"
def funcion_fitness(cromosoma):
    x = binatodeci(cromosoma)
    return funcion_objetivo(x)
    

"Poblacion Inicial"
poblacion = inicializar_poblacion(10, 30);

fitness = []

for cromosoma in poblacion:
    fitness.append(funcion_fitness(cromosoma))

print(fitness)
print(max(fitness)) ;"Devuelve el maximo de la poblacion"
print(min(fitness)) ;"Devuelve el minimo de la poblacion"
print(mean(fitness)) ;"Devuelve el promedio de la poblacion"
print(std(fitness)) ;"Devuelve el el desvio estandar de la poblacion"

input("Press to exit...")









