from typing import NamedTuple
from datetime import datetime
from typing import List
import csv
from pathlib import Path

Partida = NamedTuple("Partida", [
    ("pj1", str),
    ("pj2", str),
    ("puntuacion", int),
    ("tiempo", float),
    ("fecha_hora", datetime),
    ("golpes_pj1", List[str]),
    ("golpes_pj2", List[str]),
    ("movimiento_final", str),
    ("combo_finish", bool),
    ("ganador", str),
    ])

def lee_fichero(ruta:str)->List[Partida]:
    """Lee un fichero con partidas guardadas y devuelve una lista de Partida."""
    partidas = []
    with open(ruta, "r", encoding="utf-8") as fichero:
        lector = csv.reader(fichero, delimiter=",")
        next(lector)  # Saltar la cabecera
        for campos in lector:
            pj1 = campos[0]
            pj2 = campos[1]
            puntuacion = int(campos[2])
            tiempo = float(campos[3])
            fecha_hora = datetime.fromisoformat(campos[4])
            golpes_pj1 = campos[5].split(",") if campos[5] else []
            golpes_pj2 = campos[6].split(",") if campos[6] else []
            movimiento_final = campos[7]
            combo_finish = campos[8] == "1"
            ganador = campos[9]
            partida = Partida(
                pj1, pj2, puntuacion, tiempo, fecha_hora,
                golpes_pj1, golpes_pj2, movimiento_final,
                combo_finish, ganador
            )
            partidas.append(partida)
    return partidas

def victora_mas_rapida(partidas:List[Partida]):
    """Devuelve la partida ganada más rápidamente por el jugador dado."""
    partida_rapida = None
    for partida in partidas:
        if partida_rapida is None or partida.tiempo < partida_rapida.tiempo :
            partida_rapida = partida
    return partida_rapida.pj1, partida_rapida.pj2, partida_rapida.tiempo

def top_ratio_medio_personajes(partidas:List[Partida], n:int)->List[str]:
    """Devuelve una lista con los personajes ordenados por su ratio medio de victorias."""
    
    ratio_victorias = {}
    numero_victorias = {}
    for partida in partidas:
        ganador = partida.ganador
        puntacion = partida.puntuacion
        ratio = puntacion / partida.tiempo
        if ganador not in ratio_victorias:
            ratio_victorias[ganador] = ratio
            numero_victorias[ganador] = 1
        ratio_victorias[ganador]= (ratio_victorias[ganador] + ratio) 
        numero_victorias[ganador] = numero_victorias[ganador] + 1

    ratio_victorias_media = {}
    for personaje, ratios in ratio_victorias.items():
        ratio_victorias_media[personaje] = ratios / numero_victorias[personaje]
    
    print(ratio_victorias)

    # Ordenar personajes por su ratio medio de victorias
    # TODO : Implementar sin lambda 
    personajes_ordenados = sorted(ratio_victorias_media.items(), key=lambda x: x[1], reverse=True)
    # Devolver solo los n personajes con mejor ratio
    return [personaje[0] for personaje in personajes_ordenados[:n]]

def enemigos_mas_debiles(partidas: List[Partida], personaje:str): 
    ganadas = {}
    for partida in partidas:
        perdedor = None
        if (personaje == partida.ganador and personaje == partida.pj1):
            perdedor = partida.pj2
        elif (personaje == partida.ganador and personaje == partida.pj2):
            perdedor = partida.pj1
        
        if (perdedor in ganadas) and (not perdedor is None):
            ganadas[perdedor] = ganadas[perdedor] + 1
        elif (not (perdedor in ganadas)) and (not perdedor is None):
            ganadas[perdedor] = 1

    max_derrotas = max(ganadas.values())
    perdedores = []
    for jugador, derrotas in ganadas.items():
        if derrotas==max_derrotas:
            perdedores.append(jugador)
    
    return perdedores, max_derrotas
    
    

if __name__ == "__main__":
    ruta_fichero = Path("data/games.csv")
    if not ruta_fichero.exists():
        print(f"El fichero {ruta_fichero} no existe.")
    partidas = lee_fichero(ruta_fichero)
    print(partidas)
    print("La partida más rápida: ",victora_mas_rapida(partidas))
    print("Los jugadores con menos ratio medio de victorias: ",top_ratio_medio_personajes(partidas, 3))
    
    print(enemigos_mas_debiles(partidas=partidas, personaje="Ken"))