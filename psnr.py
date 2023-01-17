import cv2

img1 = cv2.imread("Digite o nome da img original:")
img2 = cv2.imread("Digite o nome da img nova:")
psnr = cv2.PSNR(img1, img2)
print("PSNR entre as imagens é: %f" % psnr)
