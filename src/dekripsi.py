from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QComboBox, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QFileInfo
from PyQt5 import uic
import sys
import os
from timeit import default_timer as timer
from datetime import timedelta
from Crypto.Cipher import ChaCha20
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import numpy as np
import cv2
import imghdr
from .histogram import histo
from .format.data_sizes import approximate_size
from .dialog.dialog import successDialog, failCipherDialog, invalidCipherDialog, errorWhileSavingDialog


# Get path Location
def getLoc(f):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, f)


# Decryption UI
class DekripsiUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(getLoc("ui/wgtDekripsi.ui"), self)

        # Define Widget
        self.pixCipher = self.findChild(QLabel, "label")
        self.pixPlaintext = self.findChild(QLabel, "label_2")
        self.labelKeyorPass = self.findChild(QLabel, "label_5")

        self.browseBtn = self.findChild(QPushButton, "pushButton")
        self.dekripsiBtn = self.findChild(QPushButton, "pushButton_2")
        self.savePlaintextBtn = self.findChild(QPushButton, "pushButton_3")
        self.btnHistogram = self.findChild(QPushButton, "btnHistogram")

        self.txtPassword = self.findChild(QLineEdit, "lineEdit")
        self.txtNonce = self.findChild(QLineEdit, "lineEdit_2")
        self.txtPerforma = self.findChild(QLineEdit, "txtPerforma")

        self.combo = self.findChild(QComboBox, "comboBox")

        self.cbxManual = self.findChild(QCheckBox, "cbManual")

        self.path = None
        self.plainImage = None
        self.nonce_rfc7539 = None
        self.imgFileName = None

        self.getFileExtention = None
        self.typeImages = None
        self.fExt = None

        self.speedPerformance = None

        self.qpixmap = None
        self.imgtype_list = ["BMP", "PNG", "JPG"]

        # Do Something
        self.txtPassword.mousePressEvent = lambda _: self.txtPassword.selectAll()
        self.txtNonce.mousePressEvent = lambda _: self.txtNonce.selectAll()
        self.browseBtn.clicked.connect(self.openCipher)
        self.dekripsiBtn.clicked.connect(self.doDecryption)
        self.savePlaintextBtn.clicked.connect(self.savePlaintext)
        self.btnHistogram.clicked.connect(self.openHistogram)
        self.cbxManual.clicked.connect(self.changeKeyorPass)

    def changeKeyorPass(self):
        if self.cbxManual.isChecked():
            self.labelKeyorPass.setText(str('Key'))
        else:
            self.labelKeyorPass.setText(str('Kata Sandi'))

    def isImageOpen(self):
        if self.typeImages == "bmp":
            self.combo.clear()
            self.combo.addItems(self.imgtype_list)
            self.combo.setCurrentIndex(0)
        elif self.typeImages == "png":
            self.combo.clear()
            self.combo.addItems(self.imgtype_list)
            self.combo.setCurrentIndex(1)
        else:
            pass

    def openHistogram(self):
        type = False
        histo(self, type)

    def openCipher(self):

        openDialog = QFileDialog.getOpenFileName(
            self, "Open Image", "c:\\", "Image File(*.bmp *.png)")

        # Error handling when "Cancel" OpenDialog
        if openDialog[0] != "":
            self.pixmap = QPixmap(openDialog[0])
            self.pixCipher.setPixmap(self.pixmap)

            # Get CipherText path
            self.path = openDialog[0]

            # Get filename, extention, size
            self.imgFileName = QFileInfo(openDialog[0]).baseName()
            self.getFileExtention = QFileInfo(openDialog[0]).suffix()
            self.getFileSize = QFileInfo(openDialog[0]).size()

            # Detect images types based on binnary
            self.typeImages = imghdr.what(self.path)

            # Calling for change combobox
            self.isImageOpen()

            # Invalid image format "BMP" or "PNG"
            if self.typeImages != "bmp" and self.typeImages != "png":
                invalidCipherDialog(self)
            else:
                pass
        else:
            pass

    def isDecNotEmty(self):
        # Make sure if cipherImage is None or not
        if self.plainImage is None:
            self.btnHistogram.setEnabled(False)
        else:
            self.btnHistogram.setEnabled(True)

    def doDecryption(self):

        # Do encryption based on BMP FILES
        if self.typeImages == "bmp":
            try:
                # Read original ciphertext, separate original png from 12 bytes nonce
                getImgSize = self.getFileSize

                with open(self.path, 'rb') as file:
                    bmp_data = file.read(getImgSize - 12)
                    nonce = file.read()

                # binary > cv np array (skip cv2.imwrite > array. Become direcly byte > array)

                    img = cv2.imdecode(np.frombuffer(bmp_data, np.uint8), -1)
                    img_bytes = img.tobytes()

                # Define CipherText, Key, Nonce
                ciphertext = img_bytes

                if self.cbxManual.isChecked():
                    key = bytes.fromhex(str(self.txtPassword.text()))
                else:
                    bytes_key = self.txtPassword.text().encode("utf-8")
                    key = SHA256.new(data=bytes_key).digest()

                self.nonce_rfc7539 = nonce

                # Do decryption

                start = timer()
                cipher = ChaCha20.new(key=key, nonce=self.nonce_rfc7539)
                dec_img_bytes = cipher.decrypt(ciphertext)
                end = timer()

                dec_img = np.frombuffer(
                    dec_img_bytes, np.uint8).reshape(img.shape)

                # PlainText
                self.plainImage = dec_img

                # Do some change
                self.txtNonce.setText(cipher.nonce.hex())  # Nonce

                if len(img.shape) == 3:
                    height, width, channel = img.shape
                    if channel == 3:
                        bytesPerLine = channel * width
                        qImg = QImage(self.plainImage, width, height, bytesPerLine,
                                      QImage.Format_RGB888).rgbSwapped()
                    elif channel == 4:
                        bytesPerLine = channel * width
                        qImg = QImage(self.cipherImage, width, height, bytesPerLine,
                                      QImage.Format_RGBA8888).rgbSwapped()
                    else:
                        bytesPerLine = 2 * width
                        qImg = QImage(self.plainImage, width, height, bytesPerLine,
                                      QImage.Format_MonoLSB).rgbSwapped()
                else:
                    height, width = img.shape
                    bytesPerLine = 1 * width
                    qImg = QImage(self.plainImage, width, height, bytesPerLine,
                                  QImage.Format_Indexed8).rgbSwapped()

                qpixmap = QPixmap(qImg)
                self.pixPlaintext.setPixmap(qpixmap)

                # Save speed performance & sizes as variable
                self.speedPerformance = timedelta(seconds=end-start)
                file_sizes = approximate_size(getImgSize, True)
                strPerformace = str(
                    f'Waktu : {self.speedPerformance} | Ukuran : {file_sizes}')
                self.txtPerforma.setText(strPerformace)

            except Exception as error:
                failCipherDialog(self, error)

        elif self.typeImages == "png":
            try:
                # Read original ciphertext, separate original png from 12 bytes nonce
                getImgSize = self.getFileSize

                with open(self.path, 'rb') as file:
                    png_data = file.read(getImgSize - 12)
                    nonce = file.read()

                    # binary > cv np array (skip cv2.imwrite > array. Become direcly byte > array)
                    img = cv2.imdecode(np.frombuffer(png_data, np.uint8), -1)
                    img_bytes = img.tobytes()

                # Define CipherText, Key, Nonce
                ciphertext = img_bytes

                if self.cbxManual.isChecked():
                    key = bytes.fromhex(str(self.txtPassword.text()))
                else:
                    bytes_key = self.txtPassword.text().encode("utf-8")
                    key = SHA256.new(data=bytes_key).digest()

                self.nonce_rfc7539 = nonce

                # Do decryption

                start = timer()
                cipher = ChaCha20.new(key=key, nonce=self.nonce_rfc7539)
                dec_img_bytes = cipher.decrypt(ciphertext)
                end = timer()

                dec_img = np.frombuffer(
                    dec_img_bytes, np.uint8).reshape(img.shape)

                # PlainText
                self.plainImage = dec_img

                # Do some change
                self.txtNonce.setText(cipher.nonce.hex())

                if len(img.shape) == 3:
                    height, width, channel = img.shape
                    if channel == 3:
                        bytesPerLine = channel * width
                        qImg = QImage(self.plainImage, width, height, bytesPerLine,
                                      QImage.Format_RGB888).rgbSwapped()
                    elif channel == 4:
                        bytesPerLine = channel * width
                        qImg = QImage(self.plainImage, width, height, bytesPerLine,
                                      QImage.Format_RGBA8888).rgbSwapped()
                    else:
                        bytesPerLine = 2 * width
                        qImg = QImage(self.plainImage, width, height, bytesPerLine,
                                      QImage.Format_MonoLSB).rgbSwapped()
                else:
                    height, width = img.shape
                    bytesPerLine = 1 * width
                    qImg = QImage(self.plainImage, width, height,
                                  QImage.Format_Indexed8).rgbSwapped()

                qpixmap = QPixmap(qImg)
                self.pixPlaintext.setPixmap(qpixmap)

                # Save speed performance & sizes as variable
                self.speedPerformance = timedelta(seconds=end-start)
                file_sizes = approximate_size(getImgSize, True)
                strPerformace = str(
                    f'Waktu : {self.speedPerformance} | Ukuran : {file_sizes}')
                self.txtPerforma.setText(strPerformace)

            except Exception as error:
                failCipherDialog(self, error)

        self.isDecNotEmty()

    def savePlaintext(self):
        try:
            # Determine which file format use when Saving based on CipherText
            if self.combo.currentIndex() == 0:
                self.fExt = '*.bmp'
            elif self.combo.currentIndex() == 1:
                self.fExt = '*.png'
            elif self.combo.currentIndex() == 2:
                self.fExt = '*.jpg'
            else:
                pass

            # SaveDialog
            saveDialog = QFileDialog.getSaveFileName(
                self, 'Save Image', f'/{self.imgFileName}_plaintext', f'{self.fExt}')

            # Save as BMP File
            if self.combo.currentIndex() == 0:
                # Error handling when "Cancel" SaveDialog
                if saveDialog[0] != "":
                    plainFileImg = self.plainImage
                    cv2.imwrite(saveDialog[0], plainFileImg)
                    successDialog(self)
                else:
                    pass

            # Save as PNG File
            elif self.combo.currentIndex() == 1:
                # Error handling when "Cancel" SaveDialog
                if saveDialog[0] != "":
                    plainFileImg = self.plainImage
                    cv2.imwrite(saveDialog[0], plainFileImg)
                    successDialog(self)
                else:
                    pass

            # Save as JPG File
            elif self.combo.currentIndex() == 2:
                # Error handling when "Cancel" SaveDialog
                if saveDialog[0] != "":
                    plainFileImg = self.plainImage
                    cv2.imwrite(saveDialog[0], plainFileImg)
                    successDialog(self)
                else:
                    pass
            else:
                pass
        except Exception as error:
            errorWhileSavingDialog(self, error)
