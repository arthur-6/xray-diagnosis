'''
PUC Minas - Campus Coração Eucarístico
Processamento e Análise de Imagens - Trabalho prático pt. 2
    Arthur Vinícius - #666455
    Gabriel Costa - #665131
A segunda parte do trabalho prático consiste na leitura dos datasets indicados,
equalização do histograma e espelhamento horizontal para aumentar a quantidade de dados,
especificação e treinamento de classificador raso e de rede neural convulocional,
medição do tempo de execução,
e classificação das imagens.

Neste script, fazemos a equalização do histograma, utilizando OpenCV.
'''
import os

import cv2

directory = r'dataset\train'

for root, dirs, files in os.walk(directory):
    for name in files:
        path = os.path.join(root, name)

        he_img_path = os.path.join(root, 'equalized_' + name)
        hm_img_path = os.path.join(root, 'mirrored_' + name)

        img = cv2.imread(path, 0) 

        # equalização de histograma
        equ = cv2.equalizeHist(img)
        cv2.imwrite(he_img_path, equ)

        # espelhamento horizontal
        mir = cv2.flip(img, 1)
        cv2.imwrite(hm_img_path, mir)


print('done!')