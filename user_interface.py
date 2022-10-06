'''
PUC Minas - Campus Coração Eucarístico
Processamento e Análise de Imagens - Trabalho prático pt. 1
    Arthur Vinícius - #666455
    Gabriel Costa - #665131
O trabalho prático consiste em uma interface gráfica via terminal para processamento de operações
referentes a imagens via interface gráfica.
'''

import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import os.path

sg.theme('BlueMono')
x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False
def img_crop(event, x, y, flags, param):
    '''Função para corte de imagens.

    :param event: Evento referente ao clique do mouse
    :param x: Posição x do mouse
    :param y: Posição y do mouse
    :param flags: Argumento base do método setMouseCallback
    :param param: Argumento base do método setMouseCallback
    '''
    global x_start, y_start, x_end, y_end, cropping
    
    if event == cv.EVENT_LBUTTONDOWN: # caso o botão esquerdo do mouse esteja clicado
        x_start, y_start, x_end, y_end = x, y, x, y # define as variáveis com as coordenadas passadas pelo evento
        cropping = True # defino cropping como true
    
    elif event == cv.EVENT_MOUSEMOVE: # caso o mouse esteja se movendo
        if cropping == True: # enquanto cropping estiver como verdadeiro
            x_end, y_end = x, y # as coordenadas do fim vão se alterando com a posição atual do mouse
   
    elif event == cv.EVENT_LBUTTONUP: # caso o botão esquerdo do mouse esteja "levantado"
        x_end, y_end = x, y # as coordenadas do fim fixam na posição final do mouse
        cropping = False # defino cropping como false
        refPoint = [(x_start, y_start), (x_end, y_end)] # defino refPoint como uma lista de duas tuplas, contendo as coordenadas do começo e do final
        if len(refPoint) == 2: # caso refPoint tenha as duas coordenadas definidas
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]] # defino roi como o corte na imagem original, passando as coordenadas de refPoint para definir um retângulo
            cv.imshow("corte", roi) # mostro a imagem cortada 
            cv.imwrite(f'photos/cropped_image.jpg', roi) # salvo na pasta photos, com o nome de cropped_image

def img_read(img_name):
    '''Função para ler uma imagem de acordo com o nome dado pelo usuário.

    :param img_name: Nome e extensão de imagem.
    :returns: Uma imagem.
    '''
    img = cv.imread(img_name)
    return img

def img_show(img_name):
    '''Função para mostrar uma imagem de acordo com o nome dado pelo usuário.
    
    :param img_name: Nome e extensão de imagem.
    '''
    img = img_read(img_name)
    cv.imshow(img_name, img)

def menu_window():
    '''Função que define a janela de menu do programa.'''
    # o PySimpleGUI utiliza de listas aninhadas para definir o layout do menu
    # aqui defino um título, um separador e dois botões, apresentados na tela inicial
    menu_layout = [
        [sg.Text('Diagnóstico de Osteoartrite Femorotibial', font=('Cambria', 16), text_color='#ffffff')],
        [sg.Text('_'*30, text_color='#ffffff')],
        [sg.Button('Visualizar imagem', font=('Corbel', 12))],
        [sg.Button('Sair', font=('Corbel', 12), button_color='#eb4034')]
    ]
    # para inicializar a janela, uso do método Window() e passo o layout acima como parâmetro
    menu_window = sg.Window('Menu', menu_layout, element_justification='c')
    # o loop abaixo é necessário para fazer com que a janela fique aberta "rodando"
    while True:
        event, values = menu_window.read() # event e values são sempre passados pra definir ações e valores (respectivamente) do usuário na interface gráfica
        if event == 'Sair' or event == sg.WIN_CLOSED: # caso o usuário clique em "Sair" ou feche a janela, sai do loop
            break 
        elif event == 'Visualizar imagem': # caso o usuário clique em "Visualizar imagem", fecha a atual janela e chama a função view_img_window()
            menu_window.close()
            view_img_window()
    menu_window.close()

def view_img_window():
    '''Função que define a janela de visualizar imagens'''
    # o PySimpleGUI utiliza de listas aninhadas para definir o layout do menu
    # aqui defino um título, o input de arquivo, o botão de pesquisar nos diretórios e a lista de arquivos
    file_list_column = [[
        sg.Text("Buscar arquivo"),
        sg.In(size=(40, 1), enable_events=True, key="folder"),
        sg.FolderBrowse()],
        [sg.Listbox(values=[], size=(61, 20), key="file_list")]
    ]
    # aqui defino o layout acima como uma coluna e quatro botões
    layout = [
        [sg.Column(file_list_column)],
        [sg.Button('Abrir imagem', font=('Corbel', 12)),
        sg.Button('Cortar imagem', font=('Corbel', 12)), 
        sg.Button('Detectar imagem', font=('Corbel', 12)), 
        sg.Button('Voltar', font=('Corbel', 12), button_color='#ed7b09')]
    ]
     # para inicializar a janela, uso do método Window() e passo o layout acima como parâmetro
    img_view_window = sg.Window("Visualizador de imagens", layout)
    # o loop abaixo é necessário para fazer com que a janela fique aberta "rodando"
    while True:
        event, values = img_view_window.read() # event e values são sempre passados pra definir ações e valores (respectivamente) do usuário na interface gráfica
        if event == "Voltar": # caso o usuário clique em "Voltar", fecha a atual janela e chama a função menu_window()
            img_view_window.close()
            menu_window()
            break
        elif event == sg.WIN_CLOSED: # caso o usuário feche a janela, sai do loop
            break
        if event == "folder": # se o usuário clica no botão de selecionar diretório
            folder = values["folder"] 
            try: # pega a lista dos arquivos na pasta
                file_list = os.listdir(folder)
            except: 
                file_list = []
            # lista o nome dos arquivos por meio de compreensão de lista
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f)) # se é um arquivo
                and f.lower().endswith((".png", ".jpg")) # e termina nas extensões .png ou .jpg
            ]
            img_view_window["file_list"].update(fnames) # atualiza os valores do elemento 'file_list' com a lista acima
        elif event == 'Abrir imagem': # caso o usuário clique em "Abrir imagem"
            try:
                filename = os.path.join(
                    values["folder"], values["file_list"][0]
                )
                img_show(filename) # pego o nome completo do diretório aonde a imagem selecionada está e chamo a função img_show() pra ela
            except:
                pass
        elif event == 'Cortar imagem': # caso o usuário clique em "Cortar imagem"
            try:
                filename = os.path.join(
                    values["folder"], values["file_list"][0]
                ) # pego o nome completo do diretório aonde a imagem selecionada está
                img = img_read(filename) # chamo a função img_read() para o filename definido acima

                global oriImage # defino oriImage como variável global, aonde ela é uma cópia da imagem original
                oriImage = img.copy()

                cv.namedWindow(filename) # chamo a função namedWindow() e passo filename como nome desta. namedWindow é basicamente um placeholder pra imagens
                cv.setMouseCallback(filename, img_crop) # chamo a função setMouseCallback(), passo a janela acima e função img_crop() como parâmetros para definir um "evento personalizado"
                i = img.copy() # copio a imagem original

                if not cropping: # se não está cortando (variável definida globalmente, controlada por img_crop)
                    cv.imshow(filename, img) # apenas mostro a imagem original (o primeiro parâmetro é o nome da janela)
                elif cropping: # caso esteja cortando
                    cv.rectangle(img, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2) # desenha um retângulo na imagem original com base nas coordenadas
            except:
                pass
        elif event == 'Detectar imagem': # caso o usuário clique em "Detectar imagem"
            try:
                filename = os.path.join(
                    values["folder"], values["file_list"][0]
                ) # pego o nome completo do diretório aonde a imagem selecionada está
                img = cv.imread(filename, 0) # img recebe o retorno da função imread(), que lê a imagem no diretório selecionado 
                img2 = img.copy() # copio img
                template = cv.imread('photos/cropped_image.jpg', 0) # e defino o template (imagem previamente cortada)
                
                w, h = template.shape[::-1] # w (width) e h (height) defino como as medidas da imagem template usando o atributo shape
                
                img = img2.copy() # copio img2 e retono como img

                res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED) # defino res como a função matchTemplate(), que faz o cálculo da correlação cruzada
                                                                           # a função leva como parâmetro a imagem original, a imagem cortada e o método
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res) # defino as variáveis como valores e localidades extremas (mínimas e máximas) da imagem res

                top_left = max_loc # defino top_left como a localidade máxima da imagem res
                bottom_right = (top_left[0] + w, top_left[1] + h) # bottom_right defino como uma tupla carregando os pontos máximos da imagem res

                cv.rectangle(img, top_left, bottom_right, 255, 2) # "ploto" um retângulo na imagem original

                plt.subplot(111),plt.imshow(img,cmap = 'gray') # uso imshow para mostrar o resultado na imagem original
                plt.title('Imagem detectada'), plt.xticks([]), plt.yticks([])
                plt.show()

            except:
                pass
    img_view_window.close()

def main():
    menu_window()
    
if __name__ == '__main__':
    main()