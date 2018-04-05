=======================
Kaster Password Manager
=======================

Description
-----------
Kaster is an offline password manager for GNU/Linux systems.
Instead of remembering a lot of passwords, you only need to remember your SUDO password
and your Kaster account's password. You may have to remember more passwords, but sure
Kaster is here to make you remember fewer passwords. Kaster uses your Kaster account's
master password to decrypt your saved passwords, so remember it and keep it secret.

This is an offline password manager and it stores your passwords in files that it creates
on your GNU/Linux machine so you are supposed to NOT mess up with those files. Doing the
``rm`` command with the wrong directory or files may end up deleting Kaster's files and
result in the loss of saved passwords.

Installation
------------

::

  git clone https://github.com/NOVAglow/kaster.git
  cd kaster/src
  sudo ./install.sh

Example usage
-------------
1. Generate a random password

  ::

    $ sudo ./kaster.py --gen
    K.}7b^UA>'z@zl.Upu7Tqe?dkI

2. Generate 5 random passwords and write output to ``~/passwds.txt``

  ::

    $ sudo ./kaster.py --gen -d 5 -o ~/passwds.txt
    jLV&u]sVuBelw;_EK=&x}MouB.
    ={fv5jFUU3AUT|9MCs5
    sS4*{0a~k?3sv\A:cl$JWr&+NQmP
    TqWR%?4"96Q78CJ=?:yU:dw\qp
    o/d\Xv51mjoZ^Kpy@{

3. Create a Kaster account and save a new login/credentials

  ::

    $ sudo ./kaster.py --vault --account
    WARNING::pre_vault.py -> check_user_account(): /usr/share/kaster/0000.kas not found, assuming that no account is created
    No account created, create one now? [Y|N] y

    Sign Up
    ==============================
    Username: novak_topofus
    Password:
    Confirm password:
    $ sudo ./kaster.py --vault --new --name="System Backup password" --password="example123" --comment="Backup password on my computer" --login=
    Sign In
    ==============================
    Username: novak_topofus
    Password:

4. List saved logins and copy a saved password to clipboard using login's ID

  ::

    $ sudo ./kaster.py --vault --list
    ID   | Login name
    ==== | ==========
    4097 | GitHub
    7109 | www.amazon.com
    7441 | System Backup password
    $ sudo ./kaster.py --vault --getpass=4097
    Sign In
    ==============================
    Username: novak_topofus
    Password:

Dependencies
------------
1. `pyperclip <http://pypi.python.org/pypi/pyperclip>`_ (which itself is depended on a copy mechanism)
2. `PyCrypto <https://pypi.python.org/pypi/pycrypto>`_

License
-------
`MIT License <LICENSE>`_
