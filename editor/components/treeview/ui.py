from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication


class ProjectTreeView(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        model = QFileSystemModel()
        model.setRootPath('C:\\')
        self.setModel(model)
        self.doubleClicked.connect(self.test)

    def test(self, signal):
        file_path = self.model().filePath(signal)
        print(file_path)
