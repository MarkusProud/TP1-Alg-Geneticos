
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
# ══════════════════════════════════════════════════════
#  PARÁMETROS FIJOS (enunciado)
# ══════════════════════════════════════════════════════
CANT_POBLACION = 10
CANT_GENES = 30
PROB_CROSSOVER = 0.75
PROB_MUTACION = 0.05
TORNEO_TAM = 3  # Tamaño del torneo para la selección por torneo (Opción B)
ELITISMO_TAM = 2 # Cantidad de individuos a conservar en elitismo (Opción C)

# ══════════════════════════════════════════════════════
#  MÉTODOS DE SELECCIÓN
RULETA = "Ruleta"
TORNEO = "Torneo"
ELITISMO = "Elitismo"

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
def obtener_elites(poblacion, cantidad=ELITISMO_TAM):
    # Ordena la población de mayor a menor fitness
    poblacion_ordenada = sorted(
        poblacion,
        key=funcion_fitness,
        reverse=True
    )

    elites = []

    for i in range(cantidad):
        elites.append(poblacion_ordenada[i].copy())

    return elites

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
        gen_pos = random.randint(0, len(cromosoma) - 1)
        cromosoma[gen_pos] = 1 - cromosoma[gen_pos]

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

def algoritmo_genetico(poblacion, metodo):  
    nueva_poblacion = []

    # Si el método es elitismo, guardamos directamente los 2 mejores
    if metodo == ELITISMO:
        elites = obtener_elites(poblacion, ELITISMO_TAM)

        for elite in elites:
            nueva_poblacion.append(elite.copy())

    # Completamos el resto de la población con selección, crossover y mutación
    while len(nueva_poblacion) < len(poblacion):
        if metodo == RULETA:
            padre1 = ruleta(poblacion)
            padre2 = ruleta(poblacion)

        elif metodo == TORNEO:
            padre1 = torneo(poblacion)
            padre2 = torneo(poblacion)

        elif metodo == ELITISMO:
            # En elitismo usamos ruleta para generar el resto de la población
            padre1 = ruleta(poblacion)
            padre2 = ruleta(poblacion)

        hijos = crossover(padre1, padre2)

        hijo1 = mutacion(hijos[0])
        hijo2 = mutacion(hijos[1])

        if len(nueva_poblacion) < len(poblacion):
            nueva_poblacion.append(hijo1)

        if len(nueva_poblacion) < len(poblacion):
            nueva_poblacion.append(hijo2)

    return nueva_poblacion

# Función para imprimir el historial de cada ciclo por consola
def imprimir_historial(historial):
    print("\n")
    print("HISTORIAL POR CONSOLA")
    print("Ciclo | Min | Max | Promedio | Desvio | Mejor Fitness | Tiempo(ms)")
    print("----------------------------------------------------------------------------")

    tiempo_total = 0

    for fila in historial:
        tiempo_ms = fila["tiempo"] * 1000
        tiempo_total += tiempo_ms

        print(
            fila["ciclo"], "\t",
            round(fila["min"], 3), "\t",
            round(fila["max"], 3), "\t",
            round(fila["promedio"], 3), "\t",
            round(fila["desvio"], 3), "\t",
            round(fila["mejor_fitness"], 3), "\t\t",
            round(tiempo_ms, 3)
        )

    print("\nRESUMEN")

    mejor_final = historial[-1]

    print("Mejor cromosoma final:", mejor_final["mejor_cromosoma"])
    print("Mejor fitness final:", round(mejor_final["mejor_fitness"], 6))
    print("Tiempo total:", round(tiempo_total, 4), "ms")
    print("Tiempo promedio:", round(tiempo_total / len(historial), 4), "ms")

def ejecutar_ciclos(poblacion_inicial, ciclos, metodo):
    historial = []

    # Copiamos la población inicial para no modificarla directamente
    poblacion = []

    for cromosoma in poblacion_inicial:
        poblacion.append(cromosoma.copy())

    # Se ejecutan los ciclos del algoritmo genético
    for ciclo in range(1, ciclos + 1):
        inicio = time.perf_counter()

        # Aplicamos selección, crossover, mutación y elitismo si corresponde
        poblacion = algoritmo_genetico(poblacion, metodo)

        fin = time.perf_counter()

        # Evaluamos la población resultante
        fitness = evaluar_poblacion(poblacion)

        mejor_cromosoma = poblacion[fitness.index(max(fitness))]
        mejor_fitness = funcion_fitness(mejor_cromosoma)

        historial.append({
            "ciclo": ciclo,
            "min": min(fitness),
            "max": max(fitness),
            "promedio": numpy.mean(fitness),
            "desvio": numpy.std(fitness),
            "mejor_cromosoma": mejor_cromosoma,
            "mejor_fitness": mejor_fitness,
            "tiempo": fin - inicio
        })

    return historial

def imprimir_tablas_min_prom_max(historiales):
    ciclos = len(historiales[RULETA])

    print("\n")
    print("==============================================================")
    print("TABLAS DE MÍNIMOS, PROMEDIOS Y MÁXIMOS -", ciclos, "ITERACIONES")
    print("==============================================================")

    metricas = [
        ("min", "MÍNIMOS"),
        ("promedio", "PROMEDIOS"),
        ("max", "MÁXIMOS")
    ]

    for clave, titulo in metricas:
        print("\nTABLA DE", titulo)
        print("Ciclo | Ruleta | Torneo | Elitismo")
        print("-----------------------------------")

        for i in range(ciclos):
            ciclo = historiales[RULETA][i]["ciclo"]

            valor_ruleta = historiales[RULETA][i][clave]
            valor_torneo = historiales[TORNEO][i][clave]
            valor_elitismo = historiales[ELITISMO][i][clave]

            print(
                ciclo, "\t",
                round(valor_ruleta, 3), "\t",
                round(valor_torneo, 3), "\t",
                round(valor_elitismo, 3)
            )

def graficar_comparacion_por_iteraciones(historiales):
    ciclos = len(historiales[RULETA])

    generaciones = []

    for fila in historiales[RULETA]:
        generaciones.append(fila["ciclo"])

    metricas = [
        ("max", "Valores Máximos"),
        ("promedio", "Valores Promedios"),
        ("min", "Valores Mínimos")
    ]

    for clave, titulo in metricas:
        plt.figure()

        valores_ruleta = []
        valores_torneo = []
        valores_elitismo = []

        for fila in historiales[RULETA]:
            valores_ruleta.append(fila[clave])

        for fila in historiales[TORNEO]:
            valores_torneo.append(fila[clave])

        for fila in historiales[ELITISMO]:
            valores_elitismo.append(fila[clave])

        plt.plot(generaciones, valores_ruleta, label="Ruleta")
        plt.plot(generaciones, valores_torneo, label="Torneo")
        plt.plot(generaciones, valores_elitismo, label="Elitismo")

        plt.title(titulo + " - " + str(ciclos) + " iteraciones")
        plt.xlabel("Generación / Ciclo")
        plt.ylabel("Fitness")
        plt.ylim(0, 1.25)  # Ajustamos el límite del eje Y para mejor visualización
        plt.grid(True)
        plt.legend()

        plt.show()

def calcular_tiempo_promedio(historial):
    tiempo_total = 0
    cantidad = 0

    for fila in historial:
        if fila["tiempo"] > 0:
            tiempo_total += fila["tiempo"] * 1000
            cantidad += 1

    if cantidad == 0:
        return 0

    return tiempo_total / cantidad

def graficar_tiempo_promedio(historial_ruleta, historial_torneo, historial_elitismo):
    metodos = ["Ruleta", "Torneo", "Elitismo"]

    tiempos_promedio = [
        calcular_tiempo_promedio(historial_ruleta),
        calcular_tiempo_promedio(historial_torneo),
        calcular_tiempo_promedio(historial_elitismo)
    ]

    plt.figure(figsize=(8, 5))

    barras = plt.bar(metodos, tiempos_promedio)

    plt.title(f"Tiempo promedio de ejecución por método - {len(historial_ruleta)} iteraciones", fontsize=13, fontweight="bold")
    plt.xlabel("Método de selección")
    plt.ylabel("Tiempo promedio (ms)")
    plt.grid(axis="y", alpha=0.3)

    # Mostrar el valor encima de cada barra
    for barra in barras:
        altura = barra.get_height()

        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            str(round(altura, 4)) + " ms",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.show()

def graficar_un_metodo(historial, metodo):
    gens = []
    valores_max = []
    valores_prom = []
    valores_min = []

    COLORES = {
        RULETA: "blue",
        TORNEO: "orange",
        ELITISMO: "green"
    }
    
    for fila in historial:
        gens.append(fila["ciclo"])
        valores_max.append(fila["max"])
        valores_prom.append(fila["promedio"])
        valores_min.append(fila["min"])

    color = COLORES[metodo]

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(gens, valores_max, label="Máximo", color=color, linewidth=2, linestyle="-")
    ax.plot(gens, valores_prom, label="Promedio", color=color, linewidth=2, linestyle="--")
    ax.plot(gens, valores_min, label="Mínimo", color=color, linewidth=2, linestyle=":")
    ax.fill_between(gens, valores_min, valores_max, color=color, alpha=0.08)

    ax.set_title(
        f"Fitness por generación — {metodo.upper()} | {len(historial)} iteraciones",
        fontsize=13,
        fontweight="bold"
    )
    ax.set_xlabel("Generación")
    ax.set_ylabel("f(x)")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def obtener_tabla_comparativa(historiales):
    tabla_comp = {}

    for metodo in historiales:
        historial = historiales[metodo]

        # Mejor fitness alcanzado
        mejor_fitness = historial[0]["max"]
        generacion_mejor = historial[0]["ciclo"]

        for fila in historial:
            if fila["max"] > mejor_fitness:
                mejor_fitness = fila["max"]
                generacion_mejor = fila["ciclo"]

        # Estabilidad: promedio del desvío estándar de la población
        desvios = []

        for fila in historial:
            desvios.append(fila["desvio"])

        desv_std = numpy.mean(desvios)

        # Tiempo promedio en milisegundos
        tiempo_total = 0
        cantidad = 0

        for fila in historial:
            if fila["tiempo"] > 0:
                tiempo_total += fila["tiempo"] * 1000
                cantidad += 1

        if cantidad > 0:
            tiempo_ms = tiempo_total / cantidad
        else:
            tiempo_ms = 0

        tabla_comp[metodo] = {
            "mejor_f": mejor_fitness,
            "desv_std": desv_std,
            "tiempo_ms": tiempo_ms,
            "gen_media": generacion_mejor
        }

    return tabla_comp

def graficar_tabla_comparativa(tabla_comp):
    """
    Barra agrupada: mejor fitness, desviación estándar,
    tiempo promedio y generación media del mejor para los 3 métodos.
    No guarda archivo, solo muestra la gráfica.
    """
    
    COLORES = {
        RULETA: "blue",
        TORNEO: "orange",
        ELITISMO: "green"
    }
    
    metodos = list(tabla_comp.keys())

    mejor_f = []
    desv_st = []
    tiempos = []
    gen_med = []
    colores = []

    for metodo in metodos:
        mejor_f.append(tabla_comp[metodo]["mejor_f"])
        desv_st.append(tabla_comp[metodo]["desv_std"])
        tiempos.append(tabla_comp[metodo]["tiempo_ms"])
        gen_med.append(tabla_comp[metodo]["gen_media"])
        colores.append(COLORES[metodo])

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    fig.suptitle(
        "Comparación de métodos de selección",
        fontsize=13,
        fontweight="bold"
    )

    datos = [mejor_f, desv_st, tiempos, gen_med]

    titulos = [
        "Mejor fitness promedio",
        "Desv. estándar (Estabilidad)",
        "Tiempo promedio (ms)",
        "Generación media del mejor"
    ]

    formatos = [".4f", ".4f", ".3f", ".1f"]

    for ax, valores, titulo, formato in zip(axes, datos, titulos, formatos):
        barras = ax.bar(
            metodos,
            valores,
            color=colores,
            edgecolor="white",
            width=0.5
        )

        ax.set_title(titulo, fontsize=10)

        maximo = max(valores)

        if maximo > 0:
            ax.set_ylim(0, maximo * 1.25)
        else:
            ax.set_ylim(0, 1)

        ax.grid(axis="y", alpha=0.3)

        for barra, valor in zip(barras, valores):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + maximo * 0.02,
                f"{valor:{formato}}",
                ha="center",
                va="bottom",
                fontsize=9
            )

    plt.tight_layout()
    plt.show()

poblacion_inicial = init_poblacion(CANT_POBLACION, CANT_GENES)

for generaciones in [20, 100, 200]:
    historial_ruleta = ejecutar_ciclos(poblacion_inicial, generaciones, RULETA)
    historial_torneo = ejecutar_ciclos(poblacion_inicial, generaciones, TORNEO)
    historial_elitismo = ejecutar_ciclos(poblacion_inicial, generaciones, ELITISMO)
    
    imprimir_historial(historial_ruleta)
    imprimir_historial(historial_torneo)
    imprimir_historial(historial_elitismo)
    
    historiales = {
        RULETA: historial_ruleta,
        TORNEO: historial_torneo,
        ELITISMO: historial_elitismo
    }
    imprimir_tablas_min_prom_max(historiales)
    
    tabla_comparativa = obtener_tabla_comparativa(historiales)
    graficar_tabla_comparativa(tabla_comparativa)
    
    graficar_un_metodo(historial_ruleta, RULETA)
    graficar_un_metodo(historial_torneo, TORNEO)
    graficar_un_metodo(historial_elitismo, ELITISMO)
    
    graficar_tiempo_promedio(historial_ruleta, historial_torneo, historial_elitismo)





