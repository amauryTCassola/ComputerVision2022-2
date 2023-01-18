#sudo pip install opencv-python
#sudo apt install qtwayland5 ACHO Q N PRECISA
import cv2
import numpy as np
import sys

pontosOriginal = []
pontosNova = np.array([])
imgO = None #Imagem Original
imgN = None #Imagem Nova
altura = 0
largura = 0

def abrirImg(nome):
    return cv2.imread(nome)

def homography_matrix(src_points, dst_points):
    A = []
    b = []
    for i in range(len(src_points)):
        src_x, src_y = src_points[i]
        dst_x, dst_y = dst_points[i]
        A.append([-src_x, -src_y, -1, 0, 0, 0, src_x*dst_x, src_y*dst_x, dst_x])
        A.append([0, 0, 0, -src_x, -src_y, -1, src_x*dst_y, src_y*dst_y, dst_y])
    A = np.array(A)

    u,s,Vt = np.linalg.svd(A)
    homography = Vt[-1].reshape(3, 3)
    return homography



def clicar(event, x, y, flags, params):
    global pontosOriginal, altura, largura
    if event == cv2.EVENT_LBUTTONDOWN:
        if(len(pontosOriginal) < 4):
            if(len(pontosOriginal) == 0):
                cv2.setWindowTitle("Original", "Clique no canto superior direito")
            if(len(pontosOriginal) == 1):
                cv2.setWindowTitle("Original", "Clique no canto inferior esquerdo")
            if(len(pontosOriginal) == 2):
                cv2.setWindowTitle("Original", "Clique no canto inferior direito")
            if(len(pontosOriginal) == 3):
                cv2.setWindowTitle("Original", "Clique em qualquer lugar para confirmar")
            print("Adicionando ponto:")
            print(x, ' ', y)
            pontosOriginal.append([x,y])
        else:
            cv2.setWindowTitle("Original", "Aguarde")
            pontosOriginal = np.array(pontosOriginal)
            print("Pontos Original")
            for ponto in pontosOriginal:
                print(ponto[0], ' ', ponto[1])
            coletarPontosNovos()
            print(pontosOriginal)
            print(pontosNova)
            matriz = homography_matrix(pontosOriginal, pontosNova)
            print(matriz)
            print(altura)
            print(largura)
            imgN = correct_perspective(imgO, matriz, largura, altura)
            cv2.imwrite("ImagemNova.jpg",imgN)
            cv2.namedWindow("Imagem Nova - Aperte qualquer tecla para fechar", cv2.WINDOW_NORMAL)
            cv2.imshow("Imagem Nova - Aperte qualquer tecla para fechar", imgN)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            sys.exit(0)
            

        
            
def coletarPontosNovos():
    global pontosNova, altura, largura
    #altura = int(input("Digite a altura da img:"))
    #largura = int(input("Digite a largura da img:"))
    x0 = 0
    y0 = 0
    x1 = largura
    y1 = 0
    x2 = 0
    y2 = altura
    x3 = largura
    y3 = altura
    pontosNova = np.array([
        [x0, y0],
        [x1, y1],
        [x2, y2],
        [x3, y3],
    ])

    print("Pontos Nova Imagem")
    for ponto in pontosNova:
                print(ponto[0], ' ', ponto[1])

def correct_perspective(original_img, homography_matrix, destiny_width, destiny_height):
    destiny_image = original_img.copy()
    destiny_image = destiny_image[0:destiny_height, 0:destiny_width]
    destiny_image[:] = [0,0,0]
    inverse_h_matrix = np.linalg.inv(homography_matrix)

    for destiny_y in range(destiny_height):
        for destiny_x in range(destiny_width):
            destiny_coords = np.array([destiny_x, destiny_y, 1])
            transformed = inverse_h_matrix @ destiny_coords
            origin_point = [int(transformed[0]/transformed[2]), int(transformed[1]/transformed[2])]
            origin_x = origin_point[0]
            origin_y = origin_point[1]
            destiny_image[destiny_y, destiny_x] = original_img[origin_y, origin_x]
            
    return destiny_image

def main():
    global imgO, altura, largura
    print(len(sys.argv))
    if(len(sys.argv) < 4 or len(sys.argv) > 4):
        print("Primeiro argumento, nome do arquivo original\n Segundo argumento altura\n teceiro argumento largura")
        sys.exit(0)
    #path = input("Digite o nome do arquivo:\n")
    path = sys.argv[1]
    altura = int(sys.argv[2])
    largura = int(sys.argv[3])
    imgO = abrirImg(path)
    nomeOriginal = "Original"
    cv2.namedWindow(nomeOriginal, cv2.WINDOW_NORMAL)
    cv2.setWindowTitle(nomeOriginal, "Clique no canto superior esquerdo")
    cv2.imshow(nomeOriginal, imgO)
    cv2.setMouseCallback(nomeOriginal, clicar)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit(0)

if __name__ == "__main__":
    main()

