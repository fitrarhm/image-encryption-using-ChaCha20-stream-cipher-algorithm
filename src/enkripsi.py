from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QFileInfo
from PyQt5 import uic
from timeit import default_timer as timer
from datetime import timedelta
import sys
import os
import cv2
import imghdr
from Crypto.Cipher import ChaCha20
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import numpy as np
from .histogram import histo
from .format.data_sizes import approximate_size
from .dialog.dialog import successDialog, invalidCipherDialog, failPlaintextDialog, errorWhileSavingDialog

# Get path Location


def getLoc(f):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, f)


# Enkripsi UI
class EnkripsiUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(getLoc("ui/wgtEnkripsi.ui"), self)

        # Define Widget
        self.pixPlaintext = self.findChild(QLabel, "label")
        self.pixCipher = self.findChild(QLabel, "label_2")
        self.labelKeyorPass = self.findChild(QLabel, "label_5")

        self.browseBtn = self.findChild(QPushButton, "pushButton")
        self.enkripsiBtn = self.findChild(QPushButton, "pushButton_2")
        self.saveCipherBtn = self.findChild(QPushButton, "pushButton_3")
        self.btnHistogram = self.findChild(QPushButton, "btnHistogram")

        self.txtPassword = self.findChild(QLineEdit, "lineEdit")
        self.txtNonceInput = self.findChild(QLineEdit, "txtNonceInput")
        self.txtNonce = self.findChild(QLineEdit, "lineEdit_2")
        self.txtPerforma = self.findChild(QLineEdit, "txtPerforma")

        self.cbxManual = self.findChild(QCheckBox, "cbManual")

        self.path = None
        self.cipherImage = None
        self.nonce_rfc7539 = None
        self.imgFileName = None
        self.getFileExtention = None
        self.getFileSize = None
        self.typeImages = None
        self.qpixmap = None
        self.speedPerformance = None

        # Do Something
        self.txtPassword.mousePressEvent = lambda _: self.txtPassword.selectAll()
        self.txtNonce.mousePressEvent = lambda _: self.txtNonce.selectAll()
        self.browseBtn.clicked.connect(self.openImage)
        self.enkripsiBtn.clicked.connect(self.doEncryption)
        self.saveCipherBtn.clicked.connect(self.saveCipher)
        self.btnHistogram.clicked.connect(self.openHistogram)
        self.cbxManual.clicked.connect(self.changeKeyorPass)

    def changeKeyorPass(self):
        if self.cbxManual.isChecked():
            self.labelKeyorPass.setText(str('Key'))
            self.txtNonceInput.setEnabled(True)
        else:
            self.labelKeyorPass.setText(str('Kata Sandi'))
            self.txtNonceInput.setEnabled(False)

    def openHistogram(self):
        type = True
        histo(self, type)

    def openImage(self):
        openDialog = QFileDialog.getOpenFileName(
            self, "Open Image", "c:\\", "Image File(*.bmp *.png *.jpg *.jpeg)")

        # Error handling when "Cancel" OpenDialog
        if openDialog[0] != "":
            self.pixmap = QPixmap(openDialog[0])
            self.pixPlaintext.setPixmap(self.pixmap)

            # Get PlainText path
            self.path = openDialog[0]

            # Get filename, extention, size
            self.imgFileName = QFileInfo(openDialog[0]).baseName()
            self.getFileExtention = QFileInfo(openDialog[0]).suffix()
            self.getFileSize = QFileInfo(openDialog[0]).size()

            # Detect images types based on binnary
            self.typeImages = imghdr.what(self.path)

            # Invalid image format "BMP" or "PNG" or "PJG/JPEG"
            if self.typeImages != "bmp" and self.typeImages != "png" and self.typeImages != "jpeg":
                invalidCipherDialog(self)
            else:
                pass
        else:
            pass

    def isEncNotEmty(self):
        # Make sure if cipherImage is None or not
        if self.cipherImage is None:
            self.btnHistogram.setEnabled(False)
        else:
            self.btnHistogram.setEnabled(True)

    def doEncryption(self):
        # Do encryption based on BMP FILES
        if self.typeImages == "bmp":

            try:
                # Define PlainText, Key, Nonce
                img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
                img_bytes = img.tobytes()

                if self.cbxManual.isChecked():
                    # Manual key & nonce
                    plaintext = img_bytes

                    key = bytes.fromhex(str(self.txtPassword.text()))

                    nonceInput = bytes.fromhex(
                        str(self.txtNonceInput.text()))  # If cb Checked
                    self.nonce_rfc7539 = nonceInput

                else:
                    # Automatic password/key & nonce
                    plaintext = img_bytes

                    bytes_key = self.txtPassword.text().encode("utf-8")
                    key = SHA256.new(data=bytes_key).digest()

                    self.nonce_rfc7539 = get_random_bytes(12)

                # Do encryption
                start = timer()
                cipher = ChaCha20.new(key=key, nonce=self.nonce_rfc7539)
                enc_img_bytes = cipher.encrypt(plaintext)
                end = timer()

                self.cipherImage = np.frombuffer(
                    enc_img_bytes, np.uint8).reshape(img.shape)

                # Do some change
                self.txtNonce.setText(cipher.nonce.hex())  # Nonce

                if len(img.shape) == 3:
                    height, width, channel = img.shape
                    if channel == 3:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGB888).rgbSwapped()
                    elif channel == 4:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGBA8888).rgbSwapped()
                    else:
                        bytesPerLine = 2 * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_MonoLSB).rgbSwapped()
                else:
                    height, width = img.shape
                    bytesPerLine = 1 * width
                    qImg = QImage(self.cipherImage, width, height,
                                  QImage.Format_Indexed8).rgbSwapped()

                qpixmap = QPixmap(qImg)
                self.pixCipher.setPixmap(qpixmap)

                # Save speed performance & sizes as variable
                self.speedPerformance = timedelta(seconds=end-start)
                file_sizes = approximate_size(self.getFileSize, True)
                strPerformace = str(
                    f'Waktu : {self.speedPerformance} | Ukuran : {file_sizes}')
                self.txtPerforma.setText(strPerformace)

            except Exception as error:
                failPlaintextDialog(self, error)

        # Do encryption based on JPG/JPEG FILES
        elif self.typeImages == "jpeg":
            try:
                # Define PlainText, Key, Nonce
                img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
                img_bytes = img.tobytes()

                if self.cbxManual.isChecked():
                    # Manual key & nonce
                    plaintext = img_bytes

                    key = bytes.fromhex(str(self.txtPassword.text()))

                    nonceInput = bytes.fromhex(
                        str(self.txtNonceInput.text()))  # If cb Checked
                    self.nonce_rfc7539 = nonceInput

                else:
                    # Automatic password/key & nonce
                    plaintext = img_bytes

                    bytes_key = self.txtPassword.text().encode("utf-8")
                    key = SHA256.new(data=bytes_key).digest()

                    self.nonce_rfc7539 = get_random_bytes(12)

                # Do encryption
                start = timer()
                cipher = ChaCha20.new(key=key, nonce=self.nonce_rfc7539)
                enc_img_bytes = cipher.encrypt(plaintext)
                end = timer()

                self.cipherImage = np.frombuffer(
                    enc_img_bytes, np.uint8).reshape(img.shape)

                # Do some change
                self.txtNonce.setText(cipher.nonce.hex())  # Nonce

                if len(img.shape) == 3:
                    height, width, channel = img.shape
                    if channel == 3:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGB888).rgbSwapped()
                    elif channel == 4:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGBA8888).rgbSwapped()
                    else:
                        bytesPerLine = 2 * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_MonoLSB).rgbSwapped()
                else:
                    height, width = img.shape
                    bytesPerLine = 1 * width
                    qImg = QImage(self.cipherImage, width, height,
                                  QImage.Format_Indexed8).rgbSwapped()

                qpixmap = QPixmap(qImg)
                self.pixCipher.setPixmap(qpixmap)

                # Save speed performance & sizes as variable
                self.speedPerformance = timedelta(seconds=end-start)
                file_sizes = approximate_size(self.getFileSize, True)
                strPerformace = str(
                    f'Waktu : {self.speedPerformance} | Ukuran : {file_sizes}')
                self.txtPerforma.setText(strPerformace)

            except Exception as error:
                failPlaintextDialog(self, error)

        # Do encryption based on PNG FILES
        elif self.typeImages == "png":
            try:
                # Define PlainText, Key, Nonce
                img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
                img_bytes = img.tobytes()

                if self.cbxManual.isChecked():
                    # Manual key & nonce
                    plaintext = img_bytes

                    key = bytes.fromhex(str(self.txtPassword.text()))

                    nonceInput = bytes.fromhex(
                        str(self.txtNonceInput.text()))  # If cb Checked
                    self.nonce_rfc7539 = nonceInput

                else:
                    # Automatic password/key & nonce
                    plaintext = img_bytes

                    bytes_key = self.txtPassword.text().encode("utf-8")
                    key = SHA256.new(data=bytes_key).digest()

                    self.nonce_rfc7539 = get_random_bytes(12)

                # Do encryption
                start = timer()
                cipher = ChaCha20.new(key=key, nonce=self.nonce_rfc7539)
                enc_img_bytes = cipher.encrypt(plaintext)
                end = timer()

                self.cipherImage = np.frombuffer(
                    enc_img_bytes, np.uint8).reshape(img.shape)

                # Do some change
                self.txtNonce.setText(cipher.nonce.hex())  # Nonce

                if len(img.shape) == 3:
                    height, width, channel = img.shape
                    if channel == 3:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGB888).rgbSwapped()
                    elif channel == 4:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGBA8888).rgbSwapped()
                    else:
                        bytesPerLine = 2 * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_MonoLSB).rgbSwapped()
                else:
                    height, width = img.shape
                    bytesPerLine = 1 * width
                    qImg = QImage(self.cipherImage, width, height,
                                  QImage.Format_Indexed8).rgbSwapped()

                qpixmap = QPixmap(qImg)
                self.pixCipher.setPixmap(qpixmap)

                # Save speed performance & sizes as variable
                self.speedPerformance = timedelta(seconds=end-start)
                file_sizes = approximate_size(self.getFileSize, True)
                strPerformace = str(
                    f'Waktu : {self.speedPerformance} | Ukuran : {file_sizes}')
                self.txtPerforma.setText(strPerformace)

            except Exception as error:
                failPlaintextDialog(self, error)
        else:
            pass
        self.isEncNotEmty()

    def saveCipher(self):
        try:
            # Determine which file format use when Saving based on PlainText
            fExt = None
            if self.getFileExtention == 'bmp':
                fExt = '*.bmp'
            elif self.getFileExtention == 'jpg':
                fExt = '*.png'
            else:
                fExt = '*.png'

            # SaveDialog
            saveDialog = QFileDialog.getSaveFileName(
                self, 'Save Image', f'/{self.imgFileName}_cipher', f'{fExt}')

            # print(saveDialog[0])

            # Save if BMP File
            if self.typeImages == "bmp":
                # Error handling when "Cancel" SaveDialog
                if saveDialog[0] != "":
                    cv2.imwrite(saveDialog[0], self.cipherImage)

                    # Append nonce into EOF
                    with open(saveDialog[0], "ab") as img:
                        img.write(self.nonce_rfc7539)
                        successDialog(self)
                else:
                    pass

            # Save if JPG File
            elif self.typeImages == "jpeg":
                # Error handling when "Cancel" SaveDialog
                if saveDialog[0] != "":
                    cv2.imwrite(saveDialog[0], self.cipherImage)

                    # Append nonce into EOF
                    with open(saveDialog[0], "ab") as img:
                        img.write(self.nonce_rfc7539)
                        successDialog(self)
                else:
                    pass

            # Save if PNG File
            elif self.typeImages == "png":
                # Error handling when "Cancel" SaveDialog
                if saveDialog[0] != "":
                    cv2.imwrite(saveDialog[0], self.cipherImage)

                    # Append nonce into EOF
                    with open(saveDialog[0], "ab") as img:
                        img.write(self.nonce_rfc7539)
                        successDialog(self)
                else:
                    pass
            else:
                pass
        except Exception as error:
            errorWhileSavingDialog(self, error)
