import numpy as np

def warp_perspective(source_image, homography_matrix):
    dest_image = []
    for point in source_image:
        point_homogeneous = np.array([point[0], point[1], 1])
        transformed = homography_matrix @ point_homogeneous
        destiny_point = [int(transformed[0]/transformed[2]), int(transformed[1]/transformed[2])]
        dest_image.append(destiny_point)
    return dest_image