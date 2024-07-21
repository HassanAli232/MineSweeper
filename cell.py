from PyQt6.QtWidgets import (
    QPushButton,
    QSizePolicy, 
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QMouseEvent, QIcon
from PyQt6.QtMultimedia import QSoundEffect


class Cell(QPushButton):

    def __init__(self, i, j, game = None, isMine : bool = False):
        super().__init__()
        
        self.i = i
        self.j = j
        self.isMine = isMine
        self.revealed = False
        self.game = game
        self.total = 0
        

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setContentsMargins(0, 0, 0, 0)
        policy = QSizePolicy.Policy.Expanding
        self.setSizePolicy(policy, policy)
        self.clicked.connect(self.click)
        self.setProperty("class", "cell")

        # Create a QSoundEffect instance for the click sound
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("./sounds/funny_click.wav"))

    def incrementMines(self, n:int = 1):
        if self.isMine:
            return
        
        self.total += n

    def setState(self, isMine: bool = True) -> None:
        self.total = -1
        self.isMine = isMine

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_click()
        elif event.button() == Qt.MouseButton.LeftButton:
            
            self.click()
        else:
            super().mouseReleaseEvent(event)
    
    def _play_sound(self):
        self.sound_effect.play()
        
        
    def right_click(self):
        print(self.text(), "was right-clicked.")
        if self.icon().isNull():
            self.setIcon(QIcon("./images/flag.png"))
        else:
            self.setIcon(QIcon())

    def click(self):
        if not self.isMine:
            self._play_sound()
        self.show()

    def show(self):
        if self.revealed:
            return
        
        self.setProperty("class", "disabledCell")
        self.setDisabled(True)
        self.style().unpolish(self) # type: ignore
        
        self.revealed = True       

        if self.isMine:
            self.setIcon(QIcon("./images/mine.png"))
            self.game.endGame()

        elif self.total > 0:
            self.setText(str(self.total))
        elif self.total == 0:
            self.flood()
        

    def flood(self):
        if self.isMine:
            return
        
        self.game.trigger(self.i, self.j) # type: ignore
        