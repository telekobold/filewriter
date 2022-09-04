# filewriter

This project contains a simple email worm.

The worm's payload does not lead to any data loss, but creates 10 copies of each 
text and each Word file in each sub-directory in the user's directory, which 
contains the text of the respective file in a wildly jumbled form. Additionally, 
any file ending with ".jpeg", ".jpg", ".png", ".mp3" or ".ogg" in each 
sub-directory is marked as hidden.

The email sending functionality requires Mozilla Thunderbird. It reads the 
complete address book and one's email address, asks for one's password in a 
popping up window, and then sends a copy of the worm to each email address from 
the address book.

Currently, the worm is implemented only in the Python programming language. The
Python implementation runs under both Linux and Windows. Maybe, 
an implementation in C will follow in future.

To prevent chaos, the application of the payload to the complete user directory 
(under Linux called the users *home directory*) and the application of the email 
sending functionality to the real Thunderbird directory are commented out. 
Instead, payload and email sending functionality are applied to two (presumably 
non-existent) sub-directories of the user's own directory.

**The purpose of this project is just to find out how things work and share**
**collected knowledge with others. It shall not be abused to cause harm to** 
**anyone.** Please refer to the [hacker ethics](https://www.ccc.de/en/hackerethics), 
especially the point "Don't litter other people's data."
