import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)
window = QWidget()

# TODO: Include the default22.png Thunderbird icon from a system directory.
window.setWindowTitle("Password Required - Mozilla Thunderbird")
window.setGeometry(100, 100, 390, 150)
# TODO: Let the window sporn in the center of the screen.
window.move(50, 50)
# TODO: Include the key icon from a system directory.
msg = QLabel("Please enter your Primary Password.", parent=window)
msg.move(60, 30)

window.show()

# Start the application's event loop (`app.exec_()`), wrapped in a call to
# `sys.exit()` to cleanly exit the program and release memory resources when 
# the application terminates.
sys.exit(app.exec_())
