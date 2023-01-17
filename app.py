#sudo pip install opencv-python
#sudo apt install qtwayland5 ACHO Q N PRECISA
import cv2

pontosOriginal = []
pontosNova = []

def abrirImg(nome):
    return cv2.imread(nome)

def homography_matrix(src_points, dst_points):
    pass

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



def main():
    path = input("Digite o nome do arquivo:\n")
    img = abrirImg(path)
    nomeOriginal = "Imagem Original"
    cv2.imshow(nomeOriginal, img)
    cv2.setMouseCallback(nomeOriginal, clicar)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
