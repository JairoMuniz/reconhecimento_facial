import cv2
import numpy as np

vaga1 = [11, 58, 57, 87]
vaga2 = [103, 61, 67, 89]
vaga3 = [194, 66, 75, 81]
vaga4 = [287, 70, 81, 78]
vaga5 = [384, 74, 80, 79]
vaga6 = [478, 77, 77, 80]
vaga7 = [567, 79, 78, 73]
vaga8 = [662, 78, 77, 74]

vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]

video = cv2.VideoCapture('assets\carro_estacionando.mp4')

# Definir as dimensões para redimensionar
largura_maxima = 800
altura_maxima = 600

while True:
    check, img = video.read()
    
    if not check:
        break

    # Redimensionar o frame do vídeo
    altura, largura = img.shape[:2]
    fator_redimensionamento = min(largura_maxima/largura, altura_maxima/altura)
    img = cv2.resize(img, (int(largura * fator_redimensionamento), int(altura * fator_redimensionamento)))

    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, -5)
    imgBlur = cv2.medianBlur(imgTh, 7)
    kernel = np.ones((3, 3), np.int8)
    imgDil = cv2.dilate(imgBlur, kernel)

    qtVagasAbertas = 0

    for x, y, w, h in vagas:
        recorte = imgDil[y:y+h, x:x+w]
        qtPxBranco = cv2.countNonZero(recorte)
        cv2.putText(img, str(qtPxBranco), (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        if qtPxBranco > 820:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            qtVagasAbertas += 1
    cv2.rectangle(img, (90, 0), (330, 30), (255, 0, 0), -1)
    cv2.putText(img, f"Vagas abertas: {qtVagasAbertas}/8", (95, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow('Video', img)
    cv2.imshow('Video TH', imgDil)
    if cv2.waitKey(10) & 0xFF == 27:  # Pressione Esc para sair
        break

video.release()
cv2.destroyAllWindows()