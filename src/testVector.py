from PyQt5.QtWidgets import QWidget, QPushButton, QPlainTextEdit, QLineEdit, QSpinBox
from PyQt5 import uic
import sys
import os
from Crypto.Cipher import ChaCha20
from .dialog.dialog import errorWhileSavingDialog


# Get path Location
def getLoc(f):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, f)


# Enkripsi UI
class TestVectorUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(getLoc("ui/wgtTestVector.ui"), self)

        # Define Widget
        self.txtkey = self.findChild(QLineEdit, "txtKey")
        self.txtnonce = self.findChild(QLineEdit, "txtNonce")
        self.txtPlaintext = self.findChild(QPlainTextEdit, "txtPlaintext")
        self.txtCipherText = self.findChild(QPlainTextEdit, "txtCipherText")
        self.txtbc = self.findChild(QSpinBox, 'txtbc')
        self.testBtn = self.findChild(QPushButton, "btnTest")
        self.clearBtn = self.findChild(QPushButton, "btnClear")

        self.start = 0

        # Do Something
        self.testBtn.clicked.connect(self.doTest)
        self.clearBtn.clicked.connect(self.clear)

    def doTest(self):
        try:
            self.start = self.start + 1
            key = self.txtKey.text()
            nonce = self.txtnonce.text()
            plaintext = self.txtPlaintext.toPlainText()
            block_counter = self.txtbc.value()

            kk = bytes.fromhex(key)
            nc = bytes.fromhex(nonce)
            pt = bytes.fromhex(plaintext)
            bc = int(block_counter) * 64

            # pycryptodome chacha20 packages
            cipher = ChaCha20.new(key=kk, nonce=nc)
            cipher.seek(bc)
            ciphertext = cipher.encrypt(pt)

            result = (
                f"===========================| START TEST VECTOR {self.start} |============================|\n"
                "\n"
                "__________________________________________________________________________________________\n"
                "INPUT =\n"
                f"Key :\n{kk.hex()}\n"
                "\n"
                f"Nonce :\n{nc.hex()}\n"
                "\n"
                f"Block Counter :\n{block_counter}\n"
                "\n"
                f"Plaintext :\n{pt.hex()}\n"
                "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"
                "\n"

                "__________________________________________________________________________________________\n"
                "OUTPUT =\n"
                f"Ciphertext :\n{ciphertext.hex()}\n"
                "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"
                "\n"
                "====================================| END VECTOR |======================================|\n"
                "\n"
                "\n"
            )

            self.txtCipherText.insertPlainText(result)
        except Exception as error:
            errorWhileSavingDialog(self, error)

    def clear(self):
        self.start = 0
        self.txtkey.clear()
        self.txtnonce.clear()
        self.txtPlaintext.clear()
        self.txtCipherText.clear()
        self.txtbc.setValue(0)
