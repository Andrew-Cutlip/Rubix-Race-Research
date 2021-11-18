import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np


def detect_edges(img, filename):
    edges = cv.Canny(img, 100, 300)
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original Image")
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap="gray")
    plt.title("Edges Image")
    plt.xticks([])
    plt.yticks([])
    name = filename.split(".")
    plt.savefig(f"./{name[1]}-Edges.{name[2]}")
    plt.show()

    return img, edges


def detect_lines(img, edges, filename):
    lines = cv.HoughLinesP(edges, 1, np.pi/180, 80, 30, 10)

    # need to check if there are even any lines
    if lines is not None:
        for line in lines:
            rho = line[0][0]
            theta = line[0][1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 100 * (-b))
            y2 = int(y0 - 1000 * a)

            cv.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

    name = filename.split('.')
    cv.imwrite(f"./{name[1]}-Lines.{name[2]}", img)


def blur_image(filename):

    img = cv.imread(filename)

    blur = cv.GaussianBlur(img, (3, 3), 0)
    plt.imshow(blur)

    plt.show()

    return img


if __name__ == '__main__':

    file1 = "./images/Photo-1.jpeg"
    blur1 = blur_image(file1)
    i1, e1 = detect_edges(blur1, file1)
    detect_lines(i1, e1, file1)

    file2 = "./images/Photo-2.jpeg"
    blur2 = blur_image(file2)
    i2, e2 = detect_edges(blur2, file2)
    detect_lines(i2, e2, file2)

    file3 = "./images/Photo-3.jpeg"
    blur3 = blur_image(file3)
    i3, e3 = detect_edges(blur3, file3)
    detect_lines(i3, e3, file3)

    file4 = "./images/Photo-4.jpeg"
    blur4 = blur_image(file4)
    i4, e4 = detect_edges(blur4, file4)
    detect_lines(i4, e4, file4)

    file5 = "./images/Photo-5.jpeg"
    blur5 = blur_image(file5)
    i5, e5 = detect_edges(blur5, file5)
    detect_lines(i5, e5, file5)
