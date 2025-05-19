# Python Password Manager (PPWM)

### Created by Benjamin Dunkley

### Published June 7 2024

### ICS4U

Python Password Manager Help File (Same as PPWM-info.rtf)

Welcome to the Python Password Manager. This program allows you to securely store, encrypt, and manage your passwords.

# Features:

Add and manage password entries for different services.

Save your password data and encryption key as PNG files.

Load password data and encryption key from PNG files.

View, edit, copy, and delete existing password entries.

Operates locally and fully offline for secure password management.

# IMPORTANT NOTICE

# The entries shown on the screen are not saved until you press ‘Save and Quit’! Closing the program using the ‘Close’ button will result in the loss of your passwords. Always press ‘Save and Quit’ when you are done accessing your passwords.

# Instructions:

#### Adding a New Entry:

Enter the service name in the 'Service' field.

Enter the username in the 'Username' field.

Enter the password in the 'Password' field.

Confirm the password in the 'Confirm Password' field.

Click 'Add to List' to add your entry to the temporary list.

#### Viewing a Password:

Click the 'eye' icon next to the entry to view the password.

Copying a Password:

Click the 'copy' icon next to the entry to copy the password to your clipboard.

#### Editing an Entry:

Click the 'edit' icon next to the entry.

Update the service, username, or password in the dialog boxes that appear.

Click 'OK' to save changes.

#### Deleting an Entry:

Click the 'delete' icon next to the entry to remove it from the list.

#### Saving Data and Key:

Click 'Save and Quit' to save the password data and encryption key as PNG files.

Follow the prompts to choose locations and filenames for the files.

#### Loading Data and Key:

Click 'Open' to load an existing key and password data from PNG files.

Follow the prompts to select the key file first, then the data file.

Ensure the key file is loaded before attempting to load the data file.

# Security:

The program uses AES encryption to secure your password data.

Ensure you keep your key and data files safe, as both are required to access your passwords. It is recommended that they be stored in separate locations and use file names that you can easily remember. It is encouraged to keep copies of these important files on a secondary location, like a cloud storage server, or a USB stick.

# Program Dependencies:

All dependencies can be installed using 'pip install -r requirements.txt'

OS (Python default module)

Tkinter (Python default module)

TTKthemes (pip install ttkthemes)

json (Python default module)

Crypto.Cipher (pip install pycryptodome)

Crypto.Random (pip install pycryptodome)

PIL (pip install pillow)

## All Icons used with permission from Icons8

### https://icons8.com
