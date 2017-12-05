# Kaster Password Manager
## Description
Kaster is an offline password manager that is made for the Linux operating system, and is probably okay enough to use as long as you are a Linux user. Instead of remembering lots of passwords, you only need to remember one password: the master password that you create with Kaster. This only master password is also the thing that is used to generate the key that decrypt the saved passwords, so remember it, and don't tell it with anyone.  
This is an offline password manager, and it stores passwords in files that Kaster creates on your computer. So, you have to...um...protect those files and don't mess up with them, I guess.
## Installation
```
git clone https://github.com/NOVAglow/kaster.git
cd kaster/src
chmod +x kaster.py
sudo ./kaster.py --help
```
## Example usage:
### 1. Creating a Kaster account and saving a new login (in this example, backup password)
```
$ sudo ./kaster.py --vault --account
In session: pre_vault.check_user_account()...
No account created.
Finish session: pre_vault.check_user_account()...
No account created, create one now? [Y|N] y
Sign Up
==============================
Username: novak_topofus
Password: 
Your password is: 'ZIV~6;;HX-^il&W5.uMp|6M+Nbs"'
(Exclude the single quotes around it)
Please REMEMBER this password.
Hit Enter to continue
New account for user novak_topofus created.
$ sudo ./kaster.py --vault --new --name="System Backup" --login= --password= --comment="Backup password on my computer"
In session: pre_vault.check_user_account()...
Username: novak_topofus
Account state: OK
Finish session: pre_vault.check_user_account()...

Sign In
==============================
Username: novak_topofus
Password: 
Input for login is empty, assigning login to username: novak_topofus
Input for password is empty, assigning to a random password...
New login created.
$
```
### 2. List saved logins and copy password to clipboard
```
$ sudo ./kaster.py --vault --list
In session: pre_vault.check_user_account()...
Username: novak_topofus
Account state: OK
Finish session: pre_vault.check_user_account()...

ID   |Login name
=====|==========
1675 | System Backup
9343 | www.amazon.com
$ sudo ./kaster.py --vault --getpass=1675
In session: pre_vault.check_user_account()...
Username: novak_topofus
Account state: OK
Finish session: pre_vault.check_user_account()...

Sign In
==============================
Username: novak_topofus
Password: 
Password for login #1675 copied.
$
```
### 3. Generate some random passwords
```
$ sudo ./kaster.py --gen -l 20 -d 5
Output [1] [c"\-oorcg]^([fW5Pt:
Output [2] #TpGVagSGlMLL/*8B&<I
Output [3] D=d|dUcTGbePV61f(G"G
Output [4] p^[OmgxHRlxu}ZOo,/5{
Output [5] OmzX^^K@Fcfdm&P2VyE{
$
```
## Dependencies
1. [pyperclip](https://pypi.python.org/pypi/pyperclip) (which by the way, is depended on `xclip`)
2. [PyCrypto](https://pypi.python.org/pypi/pycrypto)
## License
[MIT License](https://github.com/NOVAglow/kaster/blob/master/LICENSE)
