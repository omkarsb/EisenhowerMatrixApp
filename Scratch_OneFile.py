import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QListWidgetItem, QInputDialog, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QFont

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super(DraggableListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.startPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()
        super(DraggableListWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.startPos is not None:
            distance = (event.pos() - self.startPos).manhattanLength()
            if distance >= QApplication.startDragDistance():
                self.startDrag(Qt.MoveAction)
        super(DraggableListWidget, self).mouseMoveEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            item = QListWidgetItem(event.mimeData().text())
            self.addItem(item)
            event.acceptProposedAction()
            # Remove the item from the source widget
            source_widget = event.source()
            if source_widget is not self:
                row = source_widget.currentRow()
                item = source_widget.takeItem(row)
                del item

    def startDrag(self, supportedActions):
        item = self.currentItem()
        mime = QMimeData()
        mime.setText(item.text())
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec_(Qt.MoveAction)

class EisenhowerMatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        hlayout_top = QHBoxLayout()
        hlayout_bottom = QHBoxLayout()

        # Define a font for the tasks
        font = QFont()
        font.setPointSize(14)  # Set font size
        font.setFamily("Arial")  # Set font family

        # Common style for all quadrants
        common_style = "border-radius: 15px; padding: 10px; font: 14pt Arial;"

        self.urgent_important = DraggableListWidget(self)
        self.urgent_important.setStyleSheet(common_style + "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFD700, stop:1 #B8860B); color: #000000;")
        
        self.not_urgent_important = DraggableListWidget(self)
        self.not_urgent_important.setStyleSheet(common_style + "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF4500, stop:1 #B22222); color: #FFFFFF;")
        
        self.urgent_not_important = DraggableListWidget(self)
        self.urgent_not_important.setStyleSheet(common_style + "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #87CEEB, stop:1 #4682B4); color: #000000;")
        
        self.not_urgent_not_important = DraggableListWidget(self)
        self.not_urgent_not_important.setStyleSheet(common_style + "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #32CD32, stop:1 #006400); color: #000000;")

        vlayout_top_left = QVBoxLayout()
        vlayout_top_left.addWidget(QLabel("LOW Importance + HIGH Urgency"))
        vlayout_top_left.addWidget(self.urgent_important)
        hlayout_top.addLayout(vlayout_top_left)

        vlayout_top_right = QVBoxLayout()
        vlayout_top_right.addWidget(QLabel("HIGH Importance + HIGH Urgency"))
        vlayout_top_right.addWidget(self.not_urgent_important)
        hlayout_top.addLayout(vlayout_top_right)

        vlayout_bottom_left = QVBoxLayout()
        vlayout_bottom_left.addWidget(QLabel("LOW Importance + Low Urgency"))
        vlayout_bottom_left.addWidget(self.urgent_not_important)
        hlayout_bottom.addLayout(vlayout_bottom_left)

        vlayout_bottom_right = QVBoxLayout()
        vlayout_bottom_right.addWidget(QLabel("HIGH Importance + LOW Urgency"))
        vlayout_bottom_right.addWidget(self.not_urgent_not_important)
        hlayout_bottom.addLayout(vlayout_bottom_right)

        layout.addLayout(hlayout_top)
        layout.addLayout(hlayout_bottom)

        btn_add = QPushButton('Add Task', self)
        btn_add.clicked.connect(self.add_task)
        layout.addWidget(btn_add)

        self.setLayout(layout)
        self.setWindowTitle('Eisenhower Matrix')
        self.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D3D3D3, stop:1 #808080); border-radius: 20px;")
        self.show()

    def add_task(self):
        task, ok = QInputDialog.getText(self, 'Add Task', 'Enter the task:')
        if ok and task:
            item = QListWidgetItem(task)
            self.urgent_important.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EisenhowerMatrixApp()
    sys.exit(app.exec_())
