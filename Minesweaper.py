import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QFrame, 
)
from PyQt6.QtCore import Qt
from sweeperGrid import SweeperGrid

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(600, 450)
        
        # Create the main vertical layout
        self.main_layout = QVBoxLayout()
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)


        restart = QPushButton("restart")
        restart.clicked.connect(self.reload)
        restart.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Create the header layout
        header_layout = QHBoxLayout()
        header_layout.addWidget(QPushButton("Home"), alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(QPushButton("Settings"), alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(restart, alignment=Qt.AlignmentFlag.AlignRight)
        
        
        # Create the grid layout for the main content
        self.ROWS = 12
        self.COLS = 20
        self.grid_layout = SweeperGrid(self.ROWS, self.COLS)
        
                

        # Add header layout and grid layout to the main layout
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget(line)  # Add the line separator
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(self.grid_layout)
        

        # Set the main layout on the central widget
        self.setLayout(self.main_layout)

    def reload(self):
        self.main_layout.removeItem(self.grid_layout)
        self.grid_layout = SweeperGrid(self.ROWS, self.COLS)
        self.main_layout.addLayout(self.grid_layout)

    def push(self):
        print("button pressed.")


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)  
        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        print("Running window 1.")

if __name__ == "__main__":
    app = App(sys.argv)

    try:
        with open("MainWindowStyle.css", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet not found.")
        
    app.run()
    sys.exit(app.exec())
