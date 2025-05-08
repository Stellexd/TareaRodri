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
    # ajustar ases si el total se pasa
    while total > 21 and ases > 0 and as_vale_11:
        total -= 10
        ases -= 1
    return total

def ejecutar_acciones(mazo, acciones1, acciones2):
    vidas = [5, 5]
    turno = 0
    as_vale_11 = False
    manos = [[], []]
    historial = [[], []]
    juego_terminado = False 


    for i in range(2):
        for j in range(2):
            carta = mazo.pop(0)
            manos[j].append(carta)
            historial[j].append(carta)

    acciones = [acciones1.split(","), acciones2.split(",")]
    ronda = 0
    
    while vidas[0] > 0 and vidas[1] > 0 and not juego_terminado:
        for i in range(min(len(acciones[0]), len(acciones[1]))):
            if juego_terminado:  # pruiebna
                continue
                
            for jugador in range(2):
                if juego_terminado:  # f
                    continue
                    
                accion = acciones[jugador][i].strip()
                rival = 1 - jugador

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
                    if historial[rival]:
                        carta = historial[rival].pop()
                        manos[rival].remove(carta)
                        mazo.append(carta)

                elif accion == "desactivar As":
                    as_vale_11 = True

                elif accion == "robar carta":
                    if historial[rival]:
                        carta = historial[rival].pop()
                        manos[rival].remove(carta)
                        manos[jugador].append(carta)
                        historial[jugador].append(carta)

                elif accion == "jugar a 17" or accion == "jugar a 23":
                    objetivo = 17 if accion == "jugar a 17" else 23
                    puntajes = [calcular_puntaje(manos[0], as_vale_11), calcular_puntaje(manos[1], as_vale_11)]
                    diferencia = [objetivo - puntajes[0] if puntajes[0] <= objetivo else float("inf"),
                                objetivo - puntajes[1] if puntajes[1] <= objetivo else float("inf")]

                    if diferencia[0] == diferencia[1]:
                        mensaje = f"Empate: {puntajes[0]}-{puntajes[1]}"
                    elif diferencia[0] < diferencia[1]:
                        vidas[1] -= 1
                        mensaje = f"Total: {puntajes[0]}-{puntajes[1]} -> Gana Jugador 1"
                    else:
                        vidas[0] -= 1
                        mensaje = f"Total: {puntajes[0]}-{puntajes[1]} -> Gana Jugador 2"
                    print(mensaje)
                    print(f"Vidas: J1={vidas[0]} | J2={vidas[1]}")
                    ronda += 1
                    if vidas[0] == 0 or vidas[1] == 0:
                        juego_terminado = True 

    ganador = "Jugador 1" if vidas[1] == 0 else "Jugador 2"
    print(f"\nGanador final: {ganador}")

# variables globales
mazo = input("Ingrese el orden de las cartas del mazo (ej: 6,9,2,4,A,5,10,8,7,3): ").split(",")
acciones_j1 = input("Ingrese las acciones del Jugador 1 separadas por coma: ")
acciones_j2 = input("Ingrese las acciones del Jugador 2 separadas por coma: ")

ejecutar_acciones(mazo, acciones_j1, acciones_j2)
