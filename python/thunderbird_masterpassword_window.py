import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit
from PyQt5 import QtGui
import os

# TODO: Find out default language and show language depending on default language:
# - German in default language is German
# - English otherwise

app = QApplication(sys.argv)
window = QWidget()

window.setWindowTitle("Password Required - Mozilla Thunderbird")
# TODO: Include the default22.png Thunderbird icon from a system directory,
# depending on the previously determined installation path of Thunderbird.
window.setWindowIcon(QtGui.QIcon(os.path.join("data", "default22.png")))
window.setGeometry(100, 100, 390, 150)
# TODO: Let the window sporn in the center of the screen.
window.move(50, 50)

key = QLabel(parent=window)
pixmap = QtGui.QPixmap(os.path.join("data", "key_screenshot.png"))
key.setPixmap(pixmap)
key.move(15,15)

# TODO: Include the key icon from a system directory.
msg = QLabel("Please enter your Primary Password.", parent=window)
msg.move(70, 30)

textfield = QLineEdit(parent=window)
textfield.move(70, 70)
textfield.setMinimumWidth(300)

window.show()

# Start the application's event loop (`app.exec_()`), wrapped in a call to
# `sys.exit()` to cleanly exit the program and release memory resources when 
# the application terminates.
sys.exit(app.exec_())
