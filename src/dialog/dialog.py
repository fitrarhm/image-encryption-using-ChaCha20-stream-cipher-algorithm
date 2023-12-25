from PyQt5.QtWidgets import QMessageBox


def generalError(self, error):
    QMessageBox.warning(self, "Peringatan",
                        "Error! \n"
                        "\n"
                        "Maaf Citra Plaintext atau Ciphertext tidak didukung!\n"
                        "\n"
                        f"{error}"
                        )


def successDialog(self):
    QMessageBox.information(self, "Informasi",
                            "\n"
                            "Citra berhasil disimpan\n")


def invalidCipherDialog(self):
    QMessageBox.warning(self, "Peringatan",
                        "\n"
                        "Format Ciphertext tidak valid BMP, PNG atau JPG!\n")


def failPlaintextDialog(self, error):
    QMessageBox.warning(self, "Peringatan",
                        "\n"
                        "Ada yang salah dengan Plaintext! \n"
                        f"{error}")


def errorWhileSavingDialog(self, error): QMessageBox.warning(self, "Peringatan",
                                                             "\n"
                                                             "Ada yang salah! \n"
                                                             f"{error}!")


def failCipherDialog(self, error):
    QMessageBox.warning(self, "Peringatan",
                        "Ada yang salah dengan Ciphertext! \n"
                        f"{error}")


def invalidCipherDialog(self):
    QMessageBox.warning(self, "Peringatan",
                        "Format Ciphertext tidak valid BMP atau PNG!")
