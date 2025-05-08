from logic import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def main() -> None:
    """
    Creates the gui window and starts the event loop
    """
    app: QApplication = QApplication(sys.argv)

    try:
        window: MainWindow = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print('An unexpected error occurred: ' + str(e))

if __name__ == '__main__':
    main()