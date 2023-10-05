from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QListWidgetItem
from PyQt5.QtGui import QFont
from DraggableListWidget import DraggableListWidget

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