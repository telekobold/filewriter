import base64
import sqlite3

encrypted_username = ""
encrypted_password = ""

u_b64_decoded = base64.b64decode(encrypted_username)
p_b64_decoded = base64.b64decode(encrypted_password)

pw_database = 
