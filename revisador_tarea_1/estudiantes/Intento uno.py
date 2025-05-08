def valor_carta(carta, as_vale_11):
    if carta == "A":
        return 11 if as_vale_11 else 1
    return int(carta)

def calcular_puntaje(mano, as_vale_11):
    total = 0
    ases = 0
    for carta in mano:
        if carta == "A":
            ases += 1
            total += 11 if as_vale_11 else 1
        else:
            total += int(carta)
    # Ajustar ases si el total se pasa
    while total > 21 and ases > 0 and as_vale_11:
        total -= 10
        ases -= 1
    return total

# Vidas iniciales: jugador1 y jugador2 comienzan con 5 vidas cada uno.
vidas = [5, 5]
ronda = 1

while vidas[0] > 0 and vidas[1] > 0:
    # Entrada para la ronda actual
    mazo = input("Ingrese las cartas del mazo: ").split(",")
    acciones_j1 = input("Ingrese la jugadas del jugador1: ").split(",")
    acciones_j2 = input("Ingrese la jugadas del jugador2: ").split(",")
    
    manos = [[], []]
    historial = [[], []]
    
    # Repartir dos cartas a cada jugador
    for i in range(2):
        for j in range(2):
            carta = mazo.pop(0)
            manos[j].append(carta)
            historial[j].append(carta)
    
    as_vale_11 = False
    accion_ronda = None
    num_acciones = min(len(acciones_j1), len(acciones_j2))
    accion_encontrada = False

    # Procesar acciones de ambas jugadas hasta encontrar una acción "jugar a..."
    for i in range(num_acciones):
        for jugador in range(2):
            accion = (acciones_j1 if jugador == 0 else acciones_j2)[i].strip()
                
            if accion == "pedir":
                if mazo:
                    carta = mazo.pop(0)
                    manos[jugador].append(carta)
                    historial[jugador].append(carta)
                    
            elif accion.startswith("pedir "):
                carta = accion.split()[1]
                if carta in mazo:
                    mazo.remove(carta)
                    manos[jugador].append(carta)
                    historial[jugador].append(carta)
                    
            elif accion == "devolver mi carta":
                if historial[jugador]:
                    carta = historial[jugador].pop()
                    manos[jugador].remove(carta)
                    mazo.append(carta)
                    
            elif accion == "devolver carta rival":
                rival = 1 - jugador
                if historial[rival]:
                    carta = historial[rival].pop()
                    manos[rival].remove(carta)
                    mazo.append(carta)
                    
            elif accion == "desactivar As":
                as_vale_11 = True
                
            elif accion == "robar carta":
                rival = 1 - jugador
                if historial[rival]:
                    carta = historial[rival].pop()
                    manos[rival].remove(carta)
                    manos[jugador].append(carta)
                    historial[jugador].append(carta)
                    
            elif accion.startswith("jugar a"):
                accion_ronda = accion
                accion_encontrada = True
                break
        if accion_encontrada:
            break

    # Si ninguno indicó "jugar a", se asume el objetivo 17 por defecto.
    if not accion_ronda:
        accion_ronda = "jugar a 17"
    
    objetivo = 17 if accion_ronda == "jugar a 17" else 23
    puntajes = [calcular_puntaje(manos[0], as_vale_11), calcular_puntaje(manos[1], as_vale_11)]
    diferencia = [
        objetivo - puntajes[0] if puntajes[0] <= objetivo else float("inf"),
        objetivo - puntajes[1] if puntajes[1] <= objetivo else float("inf")
    ]
    
    print(f"Total: {puntajes[0]}-{puntajes[1]}")
    # Si ambas diferencias son iguales, la ronda es empatada.
    if diferencia[0] == diferencia[1]:
        print(f"Ronda {ronda} empatada")
    # De lo contrario, el que tenga la diferencia menor gana la ronda y el otro pierde una vida.
    elif diferencia[0] < diferencia[1]:
        vidas[1] -= 1
        print(f"Ronda {ronda} para jugador 1")
    else:
        vidas[0] -= 1
        print(f"Ronda {ronda} para jugador 2")
    print(f"Vidas: {vidas[0]} vs {vidas[1]}\n")
    
    ronda += 1

if vidas[0] == 0:
    print("GANA EL JUGADOR 2!")
else:
    print("GANA EL JUGADOR 1!")
