import sys, keyboard, time
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
class Window(QMainWindow):

    # static class variables for code
    entered_string: str = ''
    delay: float = 0
    repeat: int = 0

    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("Autotyper Test")
        width = 700
        height = 400
        # setting  the fixed height of window
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        # background
        oImage = QImage("background.png")
        # resize Image to widgets size
        sImage = oImage.scaled(QSize(700, 400))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        # show all the widgets
        self.UiComponents()
        # On button click
        self.show()

    def UiComponents(self):
        self.string_button = QPushButton('Enter String Here', self)
        self.string_button.setGeometry(80, 90, 330, 70)
        self.string_button.setFont(QFont('Times', 35))
        self.string_button.setStyleSheet("""
            QPushButton {
        background-color: white;
        border-radius: 10px;
            }
            QPushButton:hover {
        background-color: grey;
        border-radius: 10px;
            }
        """)
        self.string_button.clicked.connect(self.enter_string)

        self.delay = QLineEdit(self)
        self.delay.setGeometry(180, 195, 230, 45)
        self.delay.setStyleSheet('border-radius: 10px')
        # Connect the editingFinished signal of the QLineEdit to the update_delay method
        self.delay.editingFinished.connect(self.update_delay)

        self.repeat = QLineEdit(self)
        self.repeat.setGeometry(190, 282, 220, 45)
        self.repeat.setStyleSheet('border-radius: 10px')
        self.repeat.editingFinished.connect(self.update_repeat)

        self.cancel = QLabel("] to cancel", self)
        self.cancel.setGeometry(250, 355, 150, 30)
        self.cancel.setStyleSheet("""
            QLabel {
        background-color: red;
        border-radius: 5px;
            }
        """)
        self.cancel.setAlignment(Qt.AlignCenter)
# -------
        # Add the label to display the entered string value
        self.entered_string_label = QLabel('', self)
        self.entered_string_label.setGeometry(440, 90, 230, 60)
        # not wrapping ----------------------------------------------------------------------
        self.entered_string_label.setWordWrap(True)
        self.entered_string_label.setStyleSheet("""
            QLabel {
        background-color: white;
        border-radius: 10px;
            }
        """)
        self.entered_string_label.setAlignment(Qt.AlignCenter)

# -------
        self.start = QPushButton('Click to start', self)
        self.start.setGeometry(70, 355, 150, 30)
        self.start.setStyleSheet("""
            QPushButton {
        background-color: green;
        border-radius: 5px;
            }
            QPushButton:hover {
        background-color: lightgreen;
        border-radius: 5px;
            }
        """)
        self.start.clicked.connect(self.begin)

    def update_canceled(self):
        Window.canceled = True
        print(f"Updated canceled to {Window.canceled}")

    def update_repeat(self):
        if self.repeat.text() == None:
            Window.repeat = 0
            print(f"Updated repeat to {Window.repeat}")
        else:
            Window.repeat = int(self.repeat.text())
            print(f"Updated repeat to {Window.repeat}")

    def update_delay(self):
        if self.delay.text() == '':
            Window.delay = 0
            print(f"Updated delay to {Window.delay}")
        else:
            Window.delay = float(self.delay.text())
            print(f"Updated delay to {Window.delay}")

    def enter_string(self):
        # Create a new QDialog
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Enter String")
        self.dialog.setFixedWidth(300)
        self.dialog.setFixedHeight(150)

        # Create a QLineEdit
        self.string_edit = QLineEdit(self.dialog)
        self.string_edit.setGeometry(10, 10, 280, 80)
        self.string_edit.returnPressed.connect(self.dialog.accept)

        # Create a "Done" button
        self.done_button = QPushButton("Done", self.dialog)
        self.done_button.setGeometry(100, 100, 100, 30)
        self.done_button.clicked.connect(self.on_done_button_clicked)

        # Show the dialog
        self.dialog.exec_()

    # on done button clicked method is for Qframe of enter string
    def on_done_button_clicked(self):
        # Set the text of the QLineEdit in the main window to the text in the popup window
        self.entered_string = self.string_edit.text()
        self.entered_string_label.setText(self.entered_string)
        # Close the popup window
        self.dialog.accept()
        print("entered text: ", self.entered_string)

# START OF AUTOTYPER CODE----------------------------------------------------------------

    def begin(self):
        #delete toBegin label here
        delay, repeat = float(Window.delay), int(Window.repeat)
        keyboard.wait('[')
        for i in range(repeat):
            keyboard.write(self.entered_string)
            keyboard.press_and_release('enter')   
            time.sleep(delay)
            if(keyboard.is_pressed(']')):
                print('paused!')
                return 
        



app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
