from PyQt5 import QtWidgets


class TextArea(QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show()
