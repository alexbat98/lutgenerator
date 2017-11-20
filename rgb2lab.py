import numpy as np
import scipy.misc as smp

XYZ_WHITE_REFERENCE_X = 95.047
XYZ_WHITE_REFERENCE_Y = 100.0
XYZ_WHITE_REFERENCE_Z = 108.883
XYZ_EPSILON = 0.008856
XYZ_KAPPA = 903.3


def rgb2xyz(r, g, b):
    sr = r / 12.92 if r < 0.04045 else ((r + 0.055) / 1.055) ** 2.4
    sg = g / 12.92 if g < 0.04045 else ((g + 0.055) / 1.055) ** 2.4
    sb = b / 12.92 if b < 0.04045 else ((b + 0.055) / 1.055) ** 2.4

    x = 100 * (0.4124564 * sr + 0.3575761 * sg + 0.1804375 * sb)
    y = 100 * (0.2126729 * sr + 0.7151522 * sg + 0.0721750 * sb)
    z = 100 * (0.0193339 * sr + 0.1191920 * sg + 0.9503041 * sb)

    return x, y, z


def pivot(component):
    return component ** (1. / 3.) if component > XYZ_EPSILON else (XYZ_KAPPA * component + 16.0) / 116.0


def xyz2lab(x, y, z):
    sx = pivot(x / XYZ_WHITE_REFERENCE_X)
    sy = pivot(y / XYZ_WHITE_REFERENCE_Y)
    sz = pivot(z / XYZ_WHITE_REFERENCE_Z)

    light = max(0, 116.0 * sy - 16.0)
    a = 500.0 * (sx - sy)
    b = 200.0 * (sy - sz)
    return light, a, b


def main():
    data = np.zeros((4096, 4096, 3), dtype=np.uint8)
    data2 = np.zeros((4096, 4096, 3), dtype=np.uint8)

    l_min = 1000
    l_max = -100
    a_min = 1000
    a_max = -1000
    b_min = 1000
    b_max = -1000

    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):

                rf = r / 255.0
                gf = g / 255.0
                bf = b / 255.0

                x, y, z = rgb2xyz(rf, gf, bf)
                l, a, cb = xyz2lab(x, y, z)

                if l_min > l:
                    l_min = l
                if l_max < l:
                    l_max = l
                if a_min > a:
                    a_min = a
                if a_max < a:
                    a_max = a
                if b_min > cb:
                    b_min = cb
                if b_max < cb:
                    b_max = cb

                l_int = int(l / 100.00000386666655 * 255)
                a_int = int((a + 86.1827164205346) / (86.1827164205346 + 98.23431188800402) * 255)
                b_int = int((cb + 107.8601617541481) / (107.53929844560237 + 94.47797505367028) * 255)

                data[int(r + 256 * (b // 16)), int(g + 256 * (b % 16))] = [l_int, a_int, b_int]
                #data2[int(l_int + 256 * (b_int // 16)), int(a_int + 256 * (b_int % 16))] = [r, g, b]

    img = smp.toimage(data)
    img.save("rgb2lab.png", "png")
    print("min ({}, {}, {})".format(l_min, a_min, b_min))
    print("max ({}, {}, {})".format(l_max, a_max, b_max))
    #img2 = smp.toimage(data2)
    #img2.save("lab2rgb.png", "png")


if __name__ == '__main__':
    main()
