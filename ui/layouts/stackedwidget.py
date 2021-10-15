from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout


class StackedWidget(QStackedWidget):
    def __init__(self):
        super(StackedWidget, self).__init__()

        rootVBox = QVBoxLayout(self)
        rootHBox = QHBoxLayout()
        rootHBox.addStretch()
        rootVBox.addStretch()

        self.buttonNext = QPushButton("Next")
        self.buttonNext.clicked.connect(self.buttonNextConnect)

        self.buttonBack = QPushButton("Back")
        self.buttonBack.clicked.connect(self.buttonBackConnect)

        rootHBox.addWidget(self.buttonBack)
        rootHBox.addWidget(self.buttonNext)

        rootVBox.addWidget(self)
        rootVBox.addStretch(2)
        # left, top, right, bottom
        rootVBox.setContentsMargins(5, 0, 5, 10)
        rootVBox.addLayout(rootHBox)

    def buttonNextConnect(self):
        if self.currentIndex() == self.count() - 1:
            self.finish()
        if self.currentIndex() < self.count() - 1:
            self.setCurrentIndex(self.currentIndex() + 1)

    def buttonBackConnect(self):
        if self.currentIndex() > 0:
            self.setCurrentIndex(self.currentIndex() - 1)

    def stackedIndexChanged(self, index):
        if index == self.count() - 1:
            self.buttonNext.setText("Finish")
        else:
            self.buttonNext.setText("Next")

    def finish(self):
        self.accept()

    def addPages(self, *pages):
        """
        Args:
            pages (QWidget/object)
        """
        for page in pages:
            self.addWidget(page)
        self.currentChanged.connect(self.stackedIndexChanged)
