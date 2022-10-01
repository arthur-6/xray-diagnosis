'''
PUC Minas - Campus Coração Eucarístico
Processamento e Análise de Imagens - Trabalho prático pt. 1
    Arthur Vinícius - #666455
    Lucas Baesse
    Gabriel Costa
    Yago Duarte

O trabalho prático consiste em uma interface gráfica via terminal para processamento de operações
referentes a imagens via input do usuário. Estas consistem em:
    1 - Leitura de imagem; 
    2 - Corte de imagem;
    3 - Busca de padrão em imagens.
'''
import os

import cv2 as cv

def get_img_path():
    print('Por favor, coloque o nome e a extensão da imagem.\n')
    img_name = input()
    return img_name

def img_read(img_name):
    img = cv.imread(f'photos/{img_name}')
    return img

def img_show(img_name):
    img = img_read(img_name)
    cv.imshow(img_name, img)

x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False
def img_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
   
    if event == cv.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    
    elif event == cv.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
   
    elif event == cv.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2:
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv.imshow("corte", roi)
            cv.imwrite(f'photos/cropped_{img_name}', roi)

if __name__ == '__main__':

    print("Selecione uma opção\n")
    option_select = int(input("[1] Leitura de imagem\n[2] Corte de imagem\n[3] Busca de padrão em imagem\n"))
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if option_select == 1:
        '''Opção de leitura de imagem.'''
        img_name = get_img_path()
        img_show(img_name)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Pressione qualquer tecla para sair.')
        cv.waitKey(0)

    elif option_select == 2:
        '''Opção de corte de imagem.'''
        img_name = get_img_path()
        img = img_read(img_name)
        oriImage = img.copy()
         
        cv.namedWindow(img_name)
        cv.setMouseCallback(img_name, img_crop)

        i = img.copy()

        if not cropping:
            cv.imshow(img_name, img)
        elif cropping:
            cv.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
            cv.imshow('imagem', i)

        os.system('cls' if os.name == 'nt' else 'clear')
        print('Pressione qualquer tecla para sair.')
        cv.waitKey(0)

        