import numpy as np
import scipy.misc as smp

XYZ_WHITE_REFERENCE_X = 95.047
XYZ_WHITE_REFERENCE_Y = 100.0
XYZ_WHITE_REFERENCE_Z = 108.883
XYZ_EPSILON = 0.008856
XYZ_KAPPA = 903.3


def xyz2rgb(x, y, z):

    sr = (x * 3.2406 + y * -1.5372 + z * -0.4986) / 100.0
    sg = (x * -0.9689 + y * 1.8758 + z * 0.0415) / 100.0
    sb = (x * 0.0557 + y * -0.2040 + z * 1.0570) / 100.0

    r = 1.055 * (sr ** (1./2.4)) - 0.055 if sr > 0.0031308 else 12.92 * sr
    g = 1.055 * (sg ** (1./2.4)) - 0.055 if sg > 0.0031308 else 12.92 * sg
    b = 1.055 * (sb ** (1./2.4)) - 0.055 if sb > 0.0031308 else 12.92 * sb

    return r, g, b


def lab2xyz(l, a, b):
    fy = (l + 16.0) / 116.0
    fx = a / 500.0 + fy
    fz = fy - b / 200

    tmp = fx ** 3

    xr = tmp if tmp > XYZ_EPSILON else (116.0 * fx - 16.0) / XYZ_KAPPA
    yr = fy ** 3 if l > XYZ_KAPPA * XYZ_EPSILON else l / XYZ_KAPPA

    tmp = fz ** 3
    zr = tmp if tmp > XYZ_EPSILON else (116 * fz - 16) / XYZ_KAPPA

    x = xr * XYZ_WHITE_REFERENCE_X
    y = yr * XYZ_WHITE_REFERENCE_Y
    z = zr * XYZ_WHITE_REFERENCE_Z
    return x, y, z


def main():
    data = np.zeros((4096, 4096, 3), dtype=np.uint8)

    r_min = 1000
    r_max = -1000
    g_min = 1000
    g_max = -1000
    b_min = 1000
    b_max = -1000

    for l in range(0, 256):
        for a in range(0, 256):
            for cb in range(0, 256):

                lf = l / 255. * 99.65492608793288
                af = a / 255. * (85.92633935711818 + 97.9420836379023) - 85.92633935711818
                bf = cb / 255. * (107.53929844560237 + 94.19692118570444) - 107.53929844560237

                #lf = l / 255.0 * 100.
                #af = (a - 128) / 100.
                #bf = (cb - 128) / 100.

                x, y, z = lab2xyz(lf, af, bf)
                r, g, b = xyz2rgb(x, y, z)

                if r_max < r:
                    r_max = r
                if r_min > r:
                    r_min = r

                if g_max < g:
                    g_max = g
                if g_min > g:
                    g_min = g

                if b_max < b:
                    b_max = b
                if b_min > b:
                    b_min = b

                #print("for L*a*b* ({}, {}, {}) RGB is ({}, {}, {})".format(lf, af, bf, int(r*255.), int(g*255.),

                r_int = int(r*255)
                g_int = int(g*255)
                b_int = int(b*255)
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

                data[l + 256 * (cb // 16), a + 256 * (cb % 16)] = [r_int, g_int, b_int]

    img = smp.toimage(data)
    img.save("lab2rgb.png", "png")

    print("r_min {}".format(r_min))
    print("r_max {}".format(r_max))
    print("g_min {}".format(g_min))
    print("g_max {}".format(g_max))
    print("b_min {}".format(b_min))
    print("b_max {}".format(b_max))


if __name__ == '__main__':
    main()
