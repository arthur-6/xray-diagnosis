import PySimpleGUI as sg
import cv2 as cv
import numpy as np

import os.path
import diagnosis as dg

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
            cv.imwrite(f'photos/cropped_image.jpg', roi)

def menu_window():
    menu_layout = [
        [sg.Text('Diagnóstico de Osteoartrite Femorotibial', font=('Cambria', 16), text_color='#ffffff')],
        [sg.Text('_'*30, text_color='#ffffff')],
        [sg.Button('Visualizar imagem', font=('Corbel', 12))],
        [sg.Button('Sair', font=('Corbel', 12), button_color='#eb4034')]
    ]
    menu_window = sg.Window('Menu', menu_layout, element_justification='c')
    while True:
        event, values = menu_window.read()
        if event == 'Sair' or event == sg.WIN_CLOSED:
            break
        elif event == 'Visualizar imagem':
            menu_window.close()
            view_img_window()
    menu_window.close()

def view_img_window():
    file_list_column = [[
        sg.Text("Buscar arquivo"),
        sg.In(size=(40, 1), enable_events=True, key="folder"),
        sg.FolderBrowse()],
        [sg.Listbox(values=[], size=(61, 20), key="file_list")]
    ]
    layout = [
        [sg.Column(file_list_column)],
        [sg.Button('Abrir imagem', font=('Corbel', 12)),
        sg.Button('Cortar imagem', font=('Corbel', 12)), 
        sg.Button('Reconhecer imagem', font=('Corbel', 12)), 
        sg.Button('Voltar', font=('Corbel', 12), button_color='#ed7b09')]
    ]
    img_view_window = sg.Window("Visualizador de imagens", layout)

    while True:
        event, values = img_view_window.read()
        if event == "Voltar":
            img_view_window.close()
            menu_window()
            break
        elif event == sg.WIN_CLOSED:
            break
        if event == "folder":
            folder = values["folder"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg"))
            ]
            img_view_window["file_list"].update(fnames)
        elif event == 'Abrir imagem':
            try:
                filename = os.path.join(
                    values["folder"], values["file_list"][0]
                )
                dg.img_show(filename)
            except:
                pass
        elif event == 'Cortar imagem':
            try:
                filename = os.path.join(
                    values["folder"], values["file_list"][0]
                )
                img = dg.img_read(filename)
                global oriImage
                oriImage = img.copy()

                cv.namedWindow(filename)
                cv.setMouseCallback(filename, img_crop)
                i = img.copy()

                if not cropping:
                    cv.imshow(filename, img)
                elif cropping:
                    cv.rectangle(img, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
                    # cv.imshow('cropped', i)
            except:
                pass
        elif event == 'Reconhecer imagem':
            try:
                filename = os.path.join(
                    values["folder"], values["file_list"][0]
                )
                img = cv.imread(filename)
                template = cv.imread('photos/cropped_image.jpg')
                
                img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
                # cv.imshow('template_cropped', template_gray)
                
                w, h = template.shape[::-1]

                res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
                threshold = 0.3
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                cv.imshow('pic', img)
            except:
                pass
    img_view_window.close()

def save_window(img):
    save_layout = [
        [sg.Text('Nome do arquivo a ser salvo', font=('Corbel', 12))],
        [sg.InputText(key='file_name')],
        [sg.Button('Salvar', font=('Corbel', 12), key='Salvar'), 
        sg.Button('Cancelar', font=('Corbel', 12), button_color='#eb4034', key='Cancelar')]
    ]
    save_window = sg.Window('Salvar', save_layout)

    while True:
        save_event, save_values = save_window.read()
        if save_event == 'Cancelar' or save_event == sg.WIN_CLOSED:
            break
        elif save_event == 'Salvar':
            file_name = save_values['file_name'].strip()
            if file_name:
                cv.imwrite(f'photos/{file_name}.jpg', img)
                break
    save_window.close()

def main():
    menu_window()
    
if __name__ == '__main__':
    main()