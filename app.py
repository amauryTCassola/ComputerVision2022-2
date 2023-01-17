import cv2
import numpy as np

pontosOriginal = []
pontosNova = []

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
    if event == cv2.EVENT_LBUTTONDOWN:
        if(len(pontosOriginal) < 4):
            print("Adicionando ponto:")
            print(x, ' ', y)
            pontosOriginal.append((x,y))
        else:
            print("Pontos Original")
            for ponto in pontosOriginal:
                print(ponto[0], ' ', ponto[1])
            coletarPontosNovos()
            matriz = homography_matrix(pontosOriginal, pontosNova)
        
            
def coletarPontosNovos():
    for i in range(0,4):
        x = input("x%d: " % i)
        y = input("y%d: " % i)
        pontosNova.append((x,y))
    print("Pontos Nova Imagem")
    for ponto in pontosNova:
                print(ponto[0], ' ', ponto[1])

def correct_perspective(original_img, homography_matrix):
    warped_image = np.copy(original_img)
    warped_image[:] = [0,0,0]
    height = original_img.shape[0]
    width = original_img.shape[1]

    for i in range(height):
        for j in range(width):
            original_x = j
            original_y = i
            original_coords = np.array([original_x, original_y, 1])
            transformed = homography_matrix @ original_coords
            destiny_point = [int(transformed[0]/transformed[2]), int(transformed[1]/transformed[2])]
            destiny_x = destiny_point[0]
            destiny_y = destiny_point[1]
            warped_image[destiny_y, destiny_x] = original_img[original_y, original_x]
            
    return warped_image

def main():
    # path = input("Digite o nome do arquivo:\n")
    # img = abrirImg(path)
    # nomeOriginal = "Imagem Original"
    # cv2.imshow(nomeOriginal, img)
    # cv2.setMouseCallback(nomeOriginal, clicar)

    img = cv2.imread('foto1_cap1.jpg', -1)

    source_points = np.array([
        [840, 1072],
        [2650, 670],
        [802, 2458],
        [2833, 2460]
    ])
    destination_points = np.array([
        [0, 0],
        [1500, 0],
        [0, 1140],
        [1500, 1140],
    ])

    h_matrix = homography_matrix(source_points, destination_points)

    warped_image = correct_perspective(img, h_matrix)

    cropped_image = warped_image[0:1140, 0:1500]
    cv2.imwrite('warped_test1.jpg', cropped_image)


if __name__ == "__main__":
    main()
