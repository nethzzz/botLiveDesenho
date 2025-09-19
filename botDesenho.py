import cv2

import pyautogui

import time

import numpy as np


# --- Configurações do tamanho da tela ---

OFFSET_X = 1032

OFFSET_Y = 206

CANVAS_WIDTH = 600

CANVAS_HEIGHT = 663


# --- Parâmetros de Otimização (Ajuste estes valores!) ---

# 1. Simplificação: Menor valor = mais detalhes, mais lento. Maior valor = menos detalhes, mais rápido.

#    Comece com 0.005 e aumente para ver o efeito.

EPSILON_FACTOR = 0.005


# 2. Filtro de Ruído: Contornos com área menor que este valor serão ignorados.

MIN_CONTOUR_AREA = 20

# 3. Velocidade do Mouse: A duração de cada movimento. Valores muito baixos podem perder precisão.

DRAW_DURATION = 0



time.sleep(1)


# --- Processamento da Imagem ---

image = cv2.imread('./fotos_inscritos/ultimoinscrito.png')

img_height, img_width, _ = image.shape


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

edged_image = cv2.Canny(blurred_image, 50, 150)


contours, _ = cv2.findContours(edged_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# --- OTIMIZAÇÕES ---

simplified_contours = []

for contour in contours:

    # Otimização 2: Ignorar contornos muito pequenos

    if cv2.contourArea(contour) > MIN_CONTOUR_AREA:

        # Otimização 1: Simplificar o contorno

        perimeter = cv2.arcLength(contour, True)

        epsilon = perimeter * EPSILON_FACTOR

        approx = cv2.approxPolyDP(contour, epsilon, True)

        simplified_contours.append(approx)


print(f"Otimização: De {len(contours)} contornos para {len(simplified_contours)} contornos significantes.")


# Otimização 3: Ordenar contornos por proximidade para minimizar o movimento do mouse

current_pos = np.array([0, 0])

sorted_contours = []

remaining_contours = simplified_contours.copy()


while remaining_contours:

    closest_contour_index = -1

    min_dist = float('inf')

   

    # Encontra o ÍNDICE do contorno mais próximo da posição atual

    for i, contour in enumerate(remaining_contours):

        start_point = contour[0][0]

        dist = np.linalg.norm(start_point - current_pos)

        if dist < min_dist:

            min_dist = dist

            closest_contour_index = i

           

    # Pega o contorno mais próximo usando o índice que encontramos

    closest_contour = remaining_contours[closest_contour_index]

   

    # Adiciona o contorno mais próximo à lista ordenada

    sorted_contours.append(closest_contour)

   

    # Remove o contorno da lista de restantes usando seu índice (pop)

    remaining_contours.pop(closest_contour_index)

   

    # Atualiza a posição atual para o final do contorno que acabamos de adicionar

    current_pos = closest_contour[-1][0]


# --- Desenho Automatizado e Otimizado ---

for contour in sorted_contours:

    first_point = True

    for point in contour:

        x_img, y_img = point[0]


        # Mapeamento de Coordenadas

        x_screen = int((x_img / img_width) * CANVAS_WIDTH) + OFFSET_X

        y_screen = int((y_img / img_height) * CANVAS_HEIGHT) + OFFSET_Y

       

        if first_point:

            pyautogui.moveTo(x_screen, y_screen)

            pyautogui.mouseDown()

            first_point = False

        else:

            pyautogui.dragTo(x_screen, y_screen, duration=DRAW_DURATION)


    pyautogui.mouseUp()


print("Desenho otimizado concluído!") 