import numpy as np
from scipy import misc
from skimage import color

img1 = misc.imread("lab2rgb.png")
#
# l = 100
# l_int = int(l / 100. * 255)

lena = misc.imread("lena.png")

lab = color.rgb2lab(lena.data)

res = np.zeros((512, 512, 3))

for x in range(0, 512):
    for y in range(0, 512):
        l_int = int(lab[x, y, 0] / 100. * 255)
        a_int = int((lab[x, y, 1] + 86.1827164205346) / (86.1827164205346 + 98.23431188800402) * 255)
        b_int = int((lab[x, y, 2] + 107.8601617541481) / (107.53929844560237 + 94.47797505367028) * 255)

        # print("lab {}, {}, {}".format(l_int, a_int, b_int))
        # print("lab {}, {}, {}".format(lab[x, y, 0], lab[x, y, 1], lab[x, y, 2]))

        res[x, y, 0] = img1.data[a_int + 256 * (l_int // 16), b_int + 256 * (l_int % 16), 0]
        res[x, y, 1] = img1.data[a_int + 256 * (l_int // 16), b_int + 256 * (l_int % 16), 1]
        res[x, y, 2] = img1.data[a_int + 256 * (l_int // 16), b_int + 256 * (l_int % 16), 2]

res_img = misc.toimage(res)
res_img.save("lena_2.png", "png")
