import numpy as np
import scipy.misc as smp

XYZ_WHITE_REFERENCE_X = 95.047
XYZ_WHITE_REFERENCE_Y = 100.0
XYZ_WHITE_REFERENCE_Z = 108.883
XYZ_EPSILON = 0.008856
XYZ_KAPPA = 903.3


def xyz2rgb(X, Y, Z):
    var_X = X / 100
    var_Y = Y / 100
    var_Z = Z / 100

    var_R = var_X * 3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y * 1.8758 + var_Z * 0.0415
    var_B = var_X * 0.0557 + var_Y * -0.2040 + var_Z * 1.0570

    if (var_R > 0.0031308):
        var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_R = 12.92 * var_R
    if (var_G > 0.0031308):
        var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_G = 12.92 * var_G
    if (var_B > 0.0031308):
        var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_B = 12.92 * var_B

    sR = var_R * 255
    sG = var_G * 255
    sB = var_B * 255
    return sR, sG, sB


def lab2xyz(CIE_L, CIE_a, CIE_b):
    var_Y = (CIE_L + 16) / 116
    var_X = CIE_a / 500 + var_Y
    var_Z = var_Y - CIE_b / 200

    if (var_Y ** 3 > 0.008856):
        var_Y = var_Y ** 3
    else:
        var_Y = ( var_Y - 16 / 116 ) / 7.787
    if (var_X ** 3 > 0.008856):
        var_X = var_X ** 3
    else:
        var_X = ( var_X - 16 / 116 ) / 7.787
    if (var_Z ** 3 > 0.008856):
        var_Z = var_Z ** 3
    else:
        var_Z = ( var_Z - 16 / 116 ) / 7.787

    X = var_X * XYZ_WHITE_REFERENCE_X
    Y = var_Y * XYZ_WHITE_REFERENCE_Y
    Z = var_Z * XYZ_WHITE_REFERENCE_Z
    return X, Y, Z


def main():
    data = np.zeros((4096, 4096, 3), dtype=np.uint8)

    l_min = 1000
    l_max = -100
    a_min = 1000
    a_max = -1000
    b_min = 1000
    b_max = -1000

    for l in range(0, 256):
        for a in range(0, 256):
            for cb in range(0, 256):

                lf = l / 255. * 100.00000386666655
                af = a / 255. * (86.1827164205346 + 98.23431188800402) - 86.1827164205346
                bf = cb / 255. * (107.8601617541481 + 94.47797505367028) - 107.8601617541481

                if l_min > lf:
                    l_min = lf
                if l_max < lf:
                    l_max = lf
                if a_min > af:
                    a_min = af
                if a_max < af:
                    a_max = af
                if b_min > bf:
                    b_min = bf
                if b_max < bf:
                    b_max = bf

                x, y, z = lab2xyz(lf, af, bf)
                r, g, b = xyz2rgb(x, y, z)

                #print("lab is ({}, {}, {}) rgb is ({}, {}, {})".format(lf, af, bf, r, g, b))

                r_int = int(r)
                g_int = int(g)
                b_int = int(b)

                if r_int < 0:
                    r_int = 0
                if r_int > 255:
                    r_int = 255
                if g_int < 0:
                    g_int = 0
                if g_int > 255:
                    g_int = 255
                if b_int < 0:
                    b_int = 0
                if b_int > 255:
                    b_int = 255

                data[a + 256 * (l // 16), cb + 256 * (l % 16)] = [r_int, g_int, b_int]

    img = smp.toimage(data)
    img.save("lab2rgb.png", "png")
    print("min ({}, {}, {})".format(l_min, a_min, b_min))
    print("max ({}, {}, {})".format(l_max, a_max, b_max))


if __name__ == '__main__':
    # main()
    x, y, z = lab2xyz(0, 0, 0)
    r, g, b = xyz2rgb(x, y, z)
    print("x, y, z - {}, {}, {}".format(x, y, z))
    print("rgb - {}, {}, {}".format(r, g, b))
