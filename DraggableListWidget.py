from PyQt5.QtWidgets import QListWidget, QApplication, QListWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

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
