import cv2
import numpy as np
import matplotlib.pyplot as plt
import stroke
from permutohedral import PermutohedralLattice


class Joint_bilateral_filter(object):
    def __init__(self, sigma_s, sigma_r):
        self.sigma_r = sigma_r
        self.sigma_s = sigma_s

    def permutohedralfilter(self, img, ref):

        invSpatialStdev = float(1.0/self.sigma_s)
        invColorStdev = float(1.0/self.sigma_r)

        # Construct the position vectors out of x, y, r, g, and b.
        height = img.shape[0]
        width = img.shape[1]

        eCh = ref.shape[2]
        positions = np.zeros((height, width, 2+eCh), dtype=np.float32)

        # From Mat to Image
        for y in range(height):
            for x in range(width):
                positions[y, x, 0] = invSpatialStdev * x
                positions[y, x, 1] = invSpatialStdev * y
                positions[y, x, 2:-1] = invColorStdev * ref[y, x, :-1]

        out = PermutohedralLattice.filter(img, positions)

        return out * 255


image_dir = "images"
image_name = "scale_aware_b4.png" # testing


origin_img = cv2.imread(f"{image_dir}/{image_name}")

b, g, r = cv2.split(origin_img)
origin_img = cv2.merge([r, g, b])

# iteration_time = 4
# iteration_time = 2
# sigma_s = 3
# sigma_r = 25.5
# filter = Joint_bilateral_filter(sigma_s, sigma_r)

filter_buffer = [0, 0]

# for i in range(iteration_time):
#     if i == 0:
#         temp = cv2.GaussianBlur(origin_img, (0, 0), sigma_s, sigma_s)
#         filter_buffer.append(temp.copy())
#         origin_img = origin_img / 255.
#         origin_img = origin_img.astype(np.float32)
#     else:
#         temp = filter.permutohedralfilter(origin_img, temp)

#         if filter_buffer != []:
#             for j in range(len(filter_buffer)):
#                 print(i, "==", j, ":", (temp == filter_buffer[j]).all())
#         filter_buffer.append(temp.copy())


# fig, ax = plt.subplots(2, 2)
# for i in range(2):
#     for j in range(2):
        # print(filter_buffer[2*i+j].max(), filter_buffer[2*i+j].min())
        # ax[i, j].imshow(filter_buffer[2*i+j] / 255)



filter_buffer[1] = origin_img


# output is now in `filter_buffer[3]`
plt.imshow(filter_buffer[1] / 255)

# permutohedralfilter output `float64`(0-255), cast back to `uint8`
result = (filter_buffer[1]).astype(np.uint8)

# stroke_img = stroke.rolling_edge_detection(result, 0)
# stroke_img = stroke.edge_seperation(stroke_img)

stroke_img = stroke.ditering(result, 0.85)
# result = stroke.ditering(result, 0.001)


# result = cv2.add(result, stroke_img)

# plt.imshow(result)
plt.imshow(stroke_img)
plt.show()
