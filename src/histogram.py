from ast import Not
import matplotlib.pyplot as plt
import cv2
from .dialog.dialog import generalError


def histo(self, type):
    try:

        # if type = True then title = Plaintext
        titleOne = "Plaintext" if type else "Ciphertext"
        # if type = True then title = Ciphertext
        titleTwo = "Ciphertext" if type else "Plaintext"

        imageOne = self.cipherImage if type else self.plainImage

        # Make sure path file is not empty
        if self.path != None:

            plt.figure(figsize=(10, 5))
            plt.style.use('seaborn')

            # 1. Plaintext if True, Ciphertext if False
            plt.subplot(231)
            image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
            plt.axis('off')
            plt.title(f"{titleOne} Image")
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            blue_histogram = cv2.calcHist(
                [image], [0], None, [256], [0, 256])
            green_histogram = cv2.calcHist(
                [image], [1], None, [256], [0, 256])
            red_histogram = cv2.calcHist(
                [image], [2], None, [256], [0, 256])

            # 2
            plt.subplot(232)
            plt.title("Histogram of All Colors")
            plt.hist(blue_histogram, color="darkblue")
            plt.hist(green_histogram, color="green")
            plt.hist(red_histogram, color="red")

            # 3
            plt.subplot(233)
            plt.title("Line Plots of All Colors")
            plt.plot(blue_histogram, color="darkblue")
            plt.plot(green_histogram, color="green")
            plt.plot(red_histogram, color="red")

            # 4. Ciphertext if True, Plaintext if False
            plt.subplot(234)
            image2 = imageOne
            plt.axis("off")
            plt.title(f"{titleTwo} Image")
            plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))

            blue_histogram = cv2.calcHist(
                [image2], [0], None, [256], [0, 256])
            green_histogram = cv2.calcHist(
                [image2], [1], None, [256], [0, 256])
            red_histogram = cv2.calcHist(
                [image2], [2], None, [256], [0, 256])

            # 5
            plt.subplot(235)
            plt.title("Histogram of All Colors")
            plt.hist(blue_histogram, color="darkblue")
            plt.hist(green_histogram, color="green")
            plt.hist(red_histogram, color="red")

            # 6
            plt.subplot(236)
            plt.title("Line Plots of All Colors")
            plt.plot(blue_histogram, color="darkblue")
            plt.plot(green_histogram, color="green")
            plt.plot(red_histogram, color="red")

            plt.tight_layout()
            plt.show()

    except Exception as error:
        generalError(self, error)
