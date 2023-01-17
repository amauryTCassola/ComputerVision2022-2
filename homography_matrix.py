import numpy as np

def homography_matrix(src_points, dst_points):
#dados pontos correspondentes pi e p'i, queremos encontrar
#matrix de homografia H tal que
# p' = H * p
# p' = [x' y' 1] (em coordenadas homogêneas)
# p = [x y 1]
# H = alfa[[h1,h2,h3][h4,h5,h6][h7,h8,h9]] (alfa é algum escalar, já que estamos em homogêneas)
# p' = Hp
#   x' = alfa(h1x + h2y + h3)
#   y' = alfa(h4x + h5y + h6)
#   1  = alfa(h7x + h8y + h9)
#dividimos pela última equação pra retirar o escalar alfa
#e passamos o (h7x + h8y + h9) pro outro lado multiplicando

#   x'(h7x + h8y + h9) = (h1x + h2y + h3)
#   y'(h7x + h8y + h9) = (h4x + h5y + h6)

#reorganizamos os termos pra ter um sistema linear do tipo
# Ab = [0]

#   x'(h7x + h8y + h9) - (h1x + h2y + h3) = 0 
#   y'(h7x + h8y + h9) - (h4x + h5y + h6) = 0

#reorganizando de novo

#   - h1x - h2y - h3 + h7xx' + h8yx' + h9x' = 0 
#   -h4x - h5y - h6 + h7xy' + h8yy' + h9y' = 0

#em forma de sistema linear:
# b = [h1 h2 h3 h4 h5 h6 h7 h8 h9]
# A = [-x -y -1  0  0  0 xx' yx' x']
#     [ 0  0  0  -x  -y  -1 xy' yy' y']

#fazendo isso para vários pares de pontos correspondentes, vamos
#ter Ah = 0
#We can’t use least square since it’s a homogeneous linear equations (the other side of equation is 0 therfore we can’t just multyly it by the psudo inverse). To solve this problem we use Singular-value Decomposition (SVD).
#H is the last row of V

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

if __name__ == "__main__":
    source_points = np.array([
        [200, 541],
        [1216, 413],
        [1373, 993],
        [267, 1208]
    ])
    destination_points = np.array([
        [0, 0],
        [300, 0],
        [300, 300],
        [0, 300],
    ])

    h = homography_matrix(source_points, destination_points)

    source = np.array([267, 1208, 1])
    transformed = h @ source

    print([int(transformed[0]/transformed[2]), int(transformed[1]/transformed[2])])