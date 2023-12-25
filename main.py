from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMenu, QAction, QMessageBox
from PyQt5 import uic, QtCore, QtGui
import sys
import os
import time
import resource_rc
from src.enkripsi import EnkripsiUI
from src.dekripsi import DekripsiUI
from src.testVector import TestVectorUI

# Taskbar icon
try:
    import ctypes
    myappid = 'fitrarahim.pengamancitra.chacha20.1.0' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Get path Location
def getLoc(f):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, f)

# Main UI
class MainUI(QMainWindow):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(getLoc('ui/main.ui'), self)

        # Define Widgets
        self.winEnkripsiBtn = self.findChild(QPushButton, "pushButton")
        self.winDekripsiBtn = self.findChild(QPushButton, "pushButton_2")

        self.plaintextBtnMenu = self.findChild(QAction, 'actionPlaintext')
        self.ciphertextBtnMenu = self.findChild(QAction, 'actionCipherText')
        self.keluarBtnMenu = self.findChild(QAction, 'actionExit')
        self.miniBtnMenu = self.findChild(QAction, 'actionPerkecil')
        self.maxiBtnMenu = self.findChild(QAction, 'actionPerbesar')
        self.spekBtnMenu = self.findChild(QAction, 'actionSpek')
        self.penggunaanBtnMenu = self.findChild(QAction, 'actionPenggunaan')
        self.tentangBtnMenu = self.findChild(QAction, 'actionTentang')
        self.testVectorBtnMenu = self.findChild(QAction, 'actionTest_Vector')

        # Do something
        self.winEnkripsiBtn.clicked.connect(self.view_Enkripsi)
        self.winDekripsiBtn.clicked.connect(self.view_Dekripsi)

        self.plaintextBtnMenu.triggered.connect(self.view_Enkripsi)
        self.ciphertextBtnMenu.triggered.connect(self.view_Dekripsi)
        self.keluarBtnMenu.triggered.connect(self.exit)
        self.miniBtnMenu.triggered.connect(self.showNormal)
        self.maxiBtnMenu.triggered.connect(self.showMaximized)

        self.spekBtnMenu.triggered.connect(self.spekDialog)
        self.penggunaanBtnMenu.triggered.connect(self.usageDialog)
        self.tentangBtnMenu.triggered.connect(self.aboutDialog)

        self.testVectorBtnMenu.triggered.connect(self.viewTestVector)

    def view_Enkripsi(self):
        self.enk = EnkripsiUI()
        self.enk.show()

    def view_Dekripsi(self):
        self.dek = DekripsiUI()
        self.dek.show()

    def exit(self):
        QtCore.QCoreApplication.quit()

    def aboutDialog(self):
        QMessageBox.about(self, "Tentang",
                          "\n"
                          "ChaCha Image Encryption\n"
                          "Versi 1.0\n"
                          "\n"
                          "Aplikasi ini merupakan program untuk mengamankan\n"
                          "data citra menggunakan algoritma ChaCha20\n"
                          "\n"
                          "© www.fitrarahim.net, 2022\n"
                          )

    def usageDialog(self):
        QMessageBox.about(self, "Penggunaan",
                          "\n"
                          "Enkripsi & Dekripsi :\n"
                          "\n"
                          "Enkripsi : Proses mengamankan citra bitmap\n"
                          "Dekripsi : Proses mengembalikan citra bitmap yang diamankan\n"
                          "\n"
                          "Contoh : \n"
                          "\n"
                          "Buka Aplikasi > Pilih Menu Enkripsi atau Dekripsi\n"
                          "\n"
                          "Pilih Enkripsi > Masukkan citra > Kata Sandi (Key & Nonce) > Tekan Enkripsi\n"
                          "Pilih Dekripsi > Masukkan citra > Kata Sandi (Key) > Tekan Dekripsi\n"
                          "\n"
                          )

    def spekDialog(self):
        QMessageBox.about(self, "Spesifikasi",
                          "\n"
                          "Aplikasi berjalan pada Windows 10 64 bit [Teruji]\n"
                          "\n"
                          "Di program dengan : \n"
                          "Python versi 3.9\n"
                          "Modul PyQt5\n"
                          "Modul Pycryptodome\n"
                          "Modul Opencv Python\n"
                          "Modul Matplotlib\n"
                          "Modul Numpy\n"
                          "Dan lain-lain\n"
                          "\n"
                          "Versi Algoritma ChaCha20 yang digunakan adalah : \n"
                          "128 bit Constant \n"
                          "256 bit Key\n"
                          "32   bit Block Counter\n"
                          "96   bit Nonce\n"
                          "\n"
                          )

    def testing(self):
        print('Tester')

    def viewTestVector(self):
        self.test = TestVectorUI()
        self.test.show()

        # Execute Main App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(getLoc('favicon/icon.ico')))
    mainWindow = MainUI()
    mainWindow.show()
    sys.exit(app.exec())
