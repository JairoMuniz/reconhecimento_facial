import cv2
import numpy as np

# Carregar a imagem
imagem = cv2.imread('assets\print_estacionamento.png')

# Verificar se a imagem foi carregada corretamente
if imagem is None:
    print("Erro ao carregar a imagem")
    exit()

# Redimensionar a imagem para caber na tela
largura_maxima = 800
altura_maxima = 600
altura, largura = imagem.shape[:2]

if largura > largura_maxima or altura > altura_maxima:
    fator_redimensionamento = min(largura_maxima/largura, altura_maxima/altura)
    imagem = cv2.resize(imagem, (int(largura * fator_redimensionamento), int(altura * fator_redimensionamento)))

rois = []
while True:
    # Selecionar a ROI
    roi = cv2.selectROI("Selecione a ROI e pressione Enter. Pressione Esc para sair.", imagem, fromCenter=False, showCrosshair=True)
    
    # Verificar se a ROI é válida
    if roi[2] == 0 or roi[3] == 0:
        break
    
    rois.append(roi)
    
    # Desenhar a ROI na imagem
    cv2.rectangle(imagem, (int(roi[0]), int(roi[1])), (int(roi[0] + roi[2]), int(roi[1] + roi[3])), (255, 0, 0), 2)
    cv2.imshow("Imagem com ROIs", imagem)

# Salvar as coordenadas das ROIs em um arquivo de texto
with open('rois.txt', 'w') as file:
    for roi in rois:
        file.write(f"{roi[0]},{roi[1]},{roi[2]},{roi[3]}\n")

# Mostrar mensagem de conclusão
print("Coordenadas das ROIs salvas em rois.txt")

cv2.destroyAllWindows()

