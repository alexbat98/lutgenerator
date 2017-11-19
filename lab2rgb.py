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
    fy = (l + 16) / 116.0
    fx = a / 500 + fy
    fz = fy - b / 200

    tmp = fx ** 3

    xr = tmp if tmp > XYZ_EPSILON else (116 * fx - 16) / XYZ_KAPPA
    yr = fy ** 3 if l > XYZ_KAPPA * XYZ_EPSILON else l / XYZ_KAPPA

    tmp = fz ** 3
    zr = tmp if tmp > XYZ_EPSILON else (116 * fz - 16) / XYZ_KAPPA

    x = xr * XYZ_WHITE_REFERENCE_X
    y = yr * XYZ_WHITE_REFERENCE_Y
    z = zr * XYZ_WHITE_REFERENCE_Z
    return x, y, z


def main():
    data = np.zeros((4096, 4096, 3), dtype=np.uint8)

    for l in range(0, 256):
        for a in range(0, 256):
            for cb in range(0, 256):

                lf = l / 255. * 99.65492608793288
                af = a / 255. * (85.92633935711818 + 97.9420836379023) - 85.92633935711818
                bf = cb / 255. * (107.53929844560237 + 94.19692118570444) - 107.53929844560237

                x, y, z = lab2xyz(lf, af, bf)
                r, g, b = xyz2rgb(x, y, z)

                data[l + 256 * (cb // 16), a + 256 * (cb % 16)] = [int(r*255.), int(g*255.), int(b*255.)]

    img = smp.toimage(data)
    img.save("lab2rgb.png", "png")


if __name__ == '__main__':
    main()
