import pygame
import math
import numpy as np

# Ubicando los 49 puntos inciando en (0,0)
def construir_puntos(puntos, x, y):
    for row in range(0, rows):
        for column in range(0, cols):
            puntos.append((x, y))
            y += padding
        x += padding
        y = 0

# Función para dibujar fichas -> al final, luego realizar todas las rotaciones y transformaciones lineales
def dibujar_fichas(puntos, color):
    for punto in puntos:
        pygame.draw.circle(screen, color, punto, radius)


def transformaciones(puntos, M_transf_lineal, M_traslacion_centro, M_traslacion_origen, M_rotacion):
    nuevos_puntos = []

    puntos_trasladados = []
    for punto in puntos:
        combinado = zip(punto, M_traslacion_origen)
        punto = tuple(map(sum, combinado))
        puntos_trasladados.append(punto)

    puntos_transformados_linealmente = []
    for punto in puntos_trasladados:
        p = np.matmul(np.asarray(punto), M_transf_lineal)
        puntos_transformados_linealmente.append(p)
    
    puntos_rotados = []
    for punto in puntos_transformados_linealmente:
        p = np.matmul(np.asarray(punto), M_rotacion)
        puntos_rotados.append(p)

    puntos_trasladados_centro = []
    for punto in puntos_rotados:
        combinado = zip(punto, M_traslacion_centro)
        punto = tuple(map(sum, combinado))
        puntos_trasladados_centro.append(punto)

    nuevos_puntos = puntos_trasladados_centro
    
    return nuevos_puntos


if __name__ == "__main__":
    pygame.init()

    # Tamaño de la ventana
    width, height = 700, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hungry Chinese Checkers")

    # Colores 
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # Parámetros del tablero
    rows = 7
    cols = 7
    radius = 15
    padding = 50

    # Coordenadas iniciales para los puntos 
    x = 0
    y = 0
    puntos = []
    construir_puntos(puntos, x, y)

    # LA TRANSFORMACIONES NO SON LAS ESPERADAS YA QUE EL SISTEMA DE COORDENADAS NO TIENE LA MISMA ORIENTACIÓN QUE EL SISTEMA DE COORDENADAS TRADICIONAL
    # Matrices para realizar las transformaciónes
    # Transformación lineal para obtener los ángulos deseados (60° entre i y j, i y j a 15° de los antiguos vectores canónicos)
    M_transf_lineal = np.array([[math.sin(math.radians(15)), math.cos(math.radians(15))],
                                [-math.cos(math.radians(15)), -math.sin(math.radians(15))]])
    M_traslacion_centro = (350, 350)
    M_traslacion_origen = (-150, -150)
    #Rotación de 45° en sentido horario
    M_rotacion = np.array([[math.cos(-math.pi / 4), -math.sin(-math.pi / 4)],
                        [math.sin(-math.pi / 4), math.cos(-math.pi / 4)]])

    puntos = transformaciones(puntos, M_transf_lineal, M_traslacion_centro, M_traslacion_origen, M_rotacion)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        dibujar_fichas(puntos, WHITE)

        pygame.display.flip()

    print(puntos)
    pygame.quit()
