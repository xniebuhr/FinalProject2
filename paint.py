from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QPaintEvent
from PyQt6.QtCore import Qt

class HangmanCanvas(QWidget):
    """
    A class to handle the drawing of the man on the gallows
    """
    def __init__(self) -> None:
        """
        Calls the constructor of the parent class and sets up the list to hold all the parts to draw
        """
        super().__init__()
        self.parts_to_draw: list[str] = []

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Draws the gallows and any body parts in the list
        """
        painter: QPainter = QPainter(self)
        pen: QPen = QPen(Qt.GlobalColor.white, 3)
        painter.setPen(pen)
        for part in self.parts_to_draw:
            match part:
                case "gallows":
                    self.paint_gallows(painter)
                case "head":
                    self.paint_head(painter)
                case "body":
                    self.paint_body(painter)
                case "leftarm":
                    self.paint_leftarm(painter)
                case "rightarm":
                    self.paint_rightarm(painter)
                case "leftleg":
                    self.paint_leftleg(painter)
                case "rightleg":
                    self.paint_rightleg(painter)

    def paint_gallows(self, painter: QPainter) -> None:
        """
        Draws the gallows for the man
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawLine(0, 250, 170, 250)
        painter.drawLine(80, 250, 80, 20)
        painter.drawLine(80, 20, 200, 20)
        painter.drawLine(200, 20, 200, 60)

    def paint_head(self, painter: QPainter) -> None:
        """
        Draws the head of the hangman
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawEllipse(180, 60, 40, 40)

    def paint_body(self, painter: QPainter) -> None:
        """
        Draws the body of the hangman
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawLine(200, 100, 200, 170)

    def paint_leftarm(self, painter: QPainter) -> None:
        """
        Draws the left arm of the hangman
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawLine(200, 110, 170, 140)

    def paint_rightarm(self, painter: QPainter) -> None:
        """
        Draws the right arm of the hangman
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawLine(200, 110, 230, 140)

    def paint_leftleg(self, painter: QPainter) -> None:
        """
        Draws the left leg of the hangman
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawLine(200, 170, 170, 210)

    def paint_rightleg(self, painter: QPainter) -> None:
        """
        Draws the right leg of the hangman
        :param painter: The QPainter object to draw the lines with
        """
        painter.drawLine(200, 170, 230, 210)

    def add_body_part(self, name: str) -> None:
        """
        Adds the specified body part to the list and updates to draw all body parts on the screen
        :param name: The name of the body part to add
        """
        if name not in self.parts_to_draw:
            self.parts_to_draw.append(name)
            self.update()

    def reset_drawing(self) -> None:
        """
        Removes all body parts from the list and updates to reset the drawing
        """
        self.parts_to_draw.clear()
        self.update()