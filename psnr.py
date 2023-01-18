import cv2
import numpy as np
import math

print("Pontuacao PSNR")
img1n = input("Digite o nome da img original:")
img2n = input("Digite o nome da img nova:")
img1 = cv2.imread(img1n)
img2 = cv2.imread(img2n)
psnr = cv2.PSNR(img1, img2)

#calculando manualmente
#img1 = img1.astype(np.float64) / 255.
#img2 = img2.astype(np.float64) / 255.
#mse = np.mean((img1 - img2) ** 2)
#psnr = 10 * math.log10(1. / mse)



print("PSNR entre as imagens é: %f" % psnr)
