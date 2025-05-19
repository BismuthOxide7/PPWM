# Imports all dependencies 
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from ttkthemes import ThemedTk
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PIL import Image, ImageTk

# The password manager is defined within a class to avoid the use of global variables
class PasswordManager:
    # Initialisation function
    def __init__(self):
        # Creates an empty list for the later user info entries and sets a default AES key
        self.entries = []
        self.aes_key = None

    # Function for adding the user info to the entires list from the input fields
    def add_entry(self, service, username, password):
        self.entries.append({"service": service, "username": username, "password": password})

    # Function for turning the entres list into a JSON for easier handling
    def to_json(self):
        return json.dumps(self.entries)

    # Function for turning an imported JSON back to the entries list to be displayed
    def from_json(self, data):
        self.entries = json.loads(data)

    # Pads and encrypts data using AES
    def encrypt_data(self, data):
        cipher = AES.new(self.aes_key, AES.MODE_ECB)
        data_bytes = self.pad_data(data.encode())
        return cipher.encrypt(data_bytes)

    # Decrypts and unpads AES encrypted data
    def decrypt_data(self, encrypted_data):
        cipher = AES.new(self.aes_key, AES.MODE_ECB)
        decrypted_data = cipher.decrypt(encrypted_data)
        return self.unpad_data(decrypted_data).decode()

    # Function to pad the data to match the expected length of data for AES encryption
    def pad_data(self, data):
        block_size = AES.block_size
        padding_length = block_size - len(data) % block_size
        padding = bytes([padding_length]) * padding_length
        return data + padding

    # Removes the padding from encrypted data
    def unpad_data(self, data):
        padding_length = data[-1]
        return data[:-padding_length]

    # Function to save the encrypted data and AES key 
    def save_files(self):
        # Resets the isErrored state to false
        isErrored = False
        # Creates a 128-bit AES key if it hasn't already been done
        if self.aes_key is None:
            self.aes_key = get_random_bytes(16) 

        # FIle path for the user data file
        data_file_path = filedialog.asksaveasfilename(title="Save Password Data File",defaultextension=".png", filetypes=[("PNG files", "*.png")])
        
        # Error handling statement
        if data_file_path:
            try:
                self.save_data_as_png(data_file_path)
                messagebox.showinfo("Success", "Data saved successfully!")
            except Exception as e:
                isErrored = True
                messagebox.showerror("Error", f"Failed to save data: {e}")

        # Key file data path
        key_file_path = filedialog.asksaveasfilename(title="Save Key",defaultextension=".png", filetypes=[("PNG files", "*.png")])
        
        # Error handling statement
        if key_file_path:
            try:
                self.save_key_as_png(key_file_path)
                messagebox.showinfo("Success", "Key saved successfully!")
            except Exception as e:
                isErrored = True
                messagebox.showerror("Error", f"Failed to save key: {e}")
        
        # Closes the program if both files are saved without error
        if not isErrored:
            quit()

    # Function to handle importing files
    def open_files(self):
        # Open Key File first
        key_file_path = filedialog.askopenfilename(title="Select Key File", filetypes=[("PNG files", "*.png")])
        
        # Error handling statement
        if key_file_path:
            try:
                self.load_key_from_png(key_file_path)
                messagebox.showinfo("Success", "Key loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load key: {e}")
        
        # Open Data File after
        data_file_path = filedialog.askopenfilename(title="Select Data File", filetypes=[("PNG files", "*.png")])
        
        # Error handling statement
        if data_file_path and self.aes_key:
            try:
                self.load_data_from_png(data_file_path)
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
        elif not self.aes_key:
            messagebox.showerror("Error", "Please load the key file first.")
        
    # Function to prepare and save the user data as a PNG
    def save_data_as_png(self, file_path):
        # Create the JSON
        json_data = self.to_json()
        # Encrypt the JSON
        encrypted_data = self.encrypt_data(json_data)
        # Convert the encrypted string to hexadecimal
        hex_data = encrypted_data.hex()
        # Decide how large the image must be
        num_pixels = len(hex_data) // 6 + (1 if len(hex_data) % 6 != 0 else 0)
        image_size = int(num_pixels ** 0.5) + 1
        # Create an image file of appropriate size
        image = Image.new('RGB', (image_size, image_size))
        # Creates a list of tuples of pixel color values
        pixels = [(0, 0, 0)] * (image_size * image_size)
        # Assigns RGB values from every six characters of the hex data (hex color code to RGB)
        for i in range(num_pixels):
            hex_color = hex_data[i*6 : (i+1)*6].ljust(6, '0')
            color = tuple(int(hex_color[j:j+2], 16) for j in (0, 2, 4))
            pixels[i] = color
        # Inserts the pixel data to the image file
        image.putdata(pixels)
        # Saves the image file
        image.save(file_path)

    # Function to save the AES encryption key as a PNG
    def save_key_as_png(self, file_path):
        # Convert the key to Hexadecimal
        hex_key = self.aes_key.hex()
        # Determine appropriate image size
        image_size = len(hex_key)
        image_width = int(image_size ** 0.5) + 1
        image_height = (image_size + image_width - 1) // image_width
        # Create an image of appropriate size
        image = Image.new("RGB", (image_width, image_height))
        # Creates a list of pixels
        pixels = []
        # FIlls the list with tuples corresponding to the RGB representation of the Hex data used as color codes
        for i in range(0, len(hex_key), 6):
            pixel_color = tuple(int(hex_key[j:j + 2], 16) for j in range(i, min(i + 6, len(hex_key)), 2))
            pixels.append(pixel_color)
        # Inserts the pixel data to the image
        image.putdata(pixels)
        # Saves the image representation of the AES key 
        image.save(file_path)

    # Function to handle the decryption of the data PNG
    def load_data_from_png(self, file_path):
        # Opens the image
        image = Image.open(file_path)
        # Gets the pixel data
        pixels = list(image.getdata())
        # Converts the RGB data back to Hex
        hex_data = ''.join(f'{r:02x}{g:02x}{b:02x}' for r, g, b in pixels)
        hex_data = hex_data.rstrip('0')
        # Converts the hex into bytes
        encrypted_data = bytes.fromhex(hex_data)
        # Decrypts the hex bytes and saves to the JSON
        json_data = self.decrypt_data(encrypted_data)
        # Converts the JSON to the list
        self.from_json(json_data)
        # Refreshes the list
        self.refresh_list()

    # Function to handle the descryption of the key PNG
    def load_key_from_png(self, file_path):
        # Opens the Image
        image = Image.open(file_path)
        # Gets the pixel data
        pixels = list(image.getdata())
        # Converts the RGB data back to Hex
        hex_key = ''.join(f'{r:02x}{g:02x}{b:02x}' for r, g, b in pixels)
        hex_key = hex_key.rstrip('0')
        # Decrypts the hex bytes to use as the decryption key
        self.aes_key = bytes.fromhex(hex_key)

    # Main function for creating all of the GUI widgets and managing the other functions
    def create_widgets(self):
        # Creates the window root with a theme, disables the maximise button, and gives it a name
        self.root = ThemedTk(theme="breeze", themebg=True, fonts=True)
        self.root.resizable(0, 0)
        self.root.title("Python Password Manager")
    
        # Adds an icon image to the root window
        icon = Image.open(r'icons\PWMicon.png')
        photo = ImageTk.PhotoImage(icon)
        self.root.iconphoto(1, photo)

        # Prepares the icons for UI buttons
        view = Image.open(r'icons\eye.png')
        invis = Image.open(r'icons\invis.png')
        edit = Image.open(r'icons\edit.png')
        clear = Image.open(r'icons\clear.png')
        copy = Image.open(r'icons\copy.png')
        copied = Image.open(r'icons\copied.png')

        self.viewIcon = ImageTk.PhotoImage(view)
        self.invisIcon = ImageTk.PhotoImage(invis)
        self.editIcon = ImageTk.PhotoImage(edit)
        self.deleteIcon = ImageTk.PhotoImage(clear)
        self.copyIcon = ImageTk.PhotoImage(copy)
        self.copiedIcon = ImageTk.PhotoImage(copied)

        # Creates the main frame for the button and input fields
        mainFrame = tk.Frame(self.root)
        mainFrame.pack(expand=1, pady=10)

        # Creates the Open button, Save and Quit button, and Help button
        ttk.Button(mainFrame, text="Open", command=self.open_files).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(mainFrame, text="Save and Quit", command=self.save_files).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(mainFrame, text="Help", command=self.help).grid(row=0, column=7, padx=5, pady=5)

        # Creates the label and entry for the Service field
        tk.Label(mainFrame, text="Service:").grid(row=1, column=0, padx=5, pady=5)
        self.service_entry = ttk.Entry(mainFrame, width=20)
        self.service_entry.grid(row=1, column=1, padx=5, pady=5)
        # Creates the label and entry for the Username field
        tk.Label(mainFrame, text="Username:").grid(row=1, column=2, padx=5, pady=5)
        self.username_entry = ttk.Entry(mainFrame, width=20)
        self.username_entry.grid(row=1, column=3, padx=5, pady=5)
        # Creates the label and entry for the Password field
        tk.Label(mainFrame, text="Password:").grid(row=1, column=4, padx=5, pady=5)
        self.password_entry = ttk.Entry(mainFrame, show="*", width=20)
        self.password_entry.grid(row=1, column=5, padx=5, pady=5)
        # Creates the button to view/hide the password field
        self.view_password_button = ttk.Button(mainFrame, image=self.viewIcon, command=self.view_password_input)
        self.view_password_button.grid(row=1, column=6, padx=1, pady=5)
        # Creates the 'add to list' button to add the user data to the list
        ttk.Button(mainFrame, text="Add to List", command=self.add_to_list).grid(row=1, column=7, padx=5, pady=5)

        # Creates the label and entry for the password confirmation field
        tk.Label(mainFrame, text="Confirm Password:").grid(row=2, column=4, padx=5, pady=5)
        self.confirm_password_entry = ttk.Entry(mainFrame, show="*", width=20)
        self.confirm_password_entry.grid(row=2, column=5, padx=5, pady=5)
        
        # Creates the frame for the entered password list
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(pady=10)

        # Refreshes the list of passwords
        self.refresh_list()

        # Begins the main program loop
        self.root.mainloop()

    # Function to handle the view password button
    def view_password_input(self):
        # Checks if the input field is displaying astersisks or the password
        if self.password_entry.cget('show') == "*":
            # If it is, then change it to show the actual text, and change the icon of the button
            self.password_entry.configure(show='')
            self.confirm_password_entry.configure(show='')
            self.view_password_button.configure(image=self.invisIcon)
        else:
            # Otherwise, ensure the password is not visible, and chage the icon of the button
            self.password_entry.configure(show='*')
            self.confirm_password_entry.configure(show='*')
            self.view_password_button.configure(image=self.viewIcon)

    # Function that handles the list of user informaton
    def refresh_list(self):
        # Creates a list to hold the view and copy buttons associated with the individual entries
        self.viewButtonsList = []
        self.copyButtonsList = []

        # Deletes existing widgets, if any are present
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Loop to dispay every user entry
        for i, entry in enumerate(self.entries):
            # Creates a frame to hold the list entries
            frame = tk.Frame(self.list_frame)
            frame.pack(fill=tk.X, pady=5)

            # Creates and places the service, username, and password (defaulted to ********) data entry
            service_label = tk.Label(frame, text=entry["service"], width=20)
            service_label.pack(side=tk.LEFT, padx=5)
            username_label = tk.Label(frame, text=entry["username"], width=20)
            username_label.pack(side=tk.LEFT, padx=5)
            password_label = tk.Label(frame, text="********", width=20)
            password_label.pack(side=tk.LEFT, padx=5)
            
            # Creates a button to be able to view a given password
            viewButton = ttk.Button(frame, image=self.viewIcon, command=lambda e=entry, l=password_label, v=i: self.view_password_from_list(e, l, v))
            viewButton.pack(side=tk.LEFT, padx=1)
            self.viewButtonsList.append(viewButton)

            # Creates a button to be able to copy a given password 
            copyButton = ttk.Button(frame, image=self.copyIcon, command=lambda e=entry, v=i: self.copy_password_from_list(e,v))
            copyButton.pack(side=tk.LEFT, padx=1)
            self.copyButtonsList.append(copyButton)
            
            # Creates the edit and delet buttons (which are not saved to variables because they do not have chaning icons)
            ttk.Button(frame, image=self.editIcon, command=lambda i=i: self.edit_entry(i)).pack(side=tk.LEFT, padx=1)
            ttk.Button(frame, image=self.deleteIcon, command=lambda i=i: self.delete_entry(i)).pack(side=tk.LEFT, padx=1)

    # Function to handle the 'view password' button in the entries list. 
    def view_password_from_list(self, entry, label, indexValue):
        # If the label is displaying asterisks, change it to the actual entry and update the button icon
        if label.cget('text') == "********":
            label.config(text=entry["password"])
            self.viewButtonsList[indexValue].configure(image=self.invisIcon)
        # Otherwise, display asterisks, and use the original button icon    
        else:
            label.config(text = "********")
            self.viewButtonsList[indexValue].configure(image=self.viewIcon)
    
    # Function to handle the 'copy password' button
    def copy_password_from_list(self,entry,indexValue):
        self.refresh_list()
        # Copies the given password entry to the clipboard and updates the button icon
        self.root.clipboard_clear()
        self.root.clipboard_append(entry["password"])
        self.copyButtonsList[indexValue].configure(image=self.copiedIcon)

    # Function to open the 'Help' file
    def help(self):
        os.startfile(r'ppwm-info.rtf',)

    # Function to allow editing of a given entry
    def edit_entry(self, index):
        # Determines the entry that is being edited 
        entry = self.entries[index]
        # Allows all values to be changed using simpleDialogs
        new_service = simpledialog.askstring("Edit Service", "Service:", initialvalue=entry["service"])
        new_username = simpledialog.askstring("Edit Username", "Username:", initialvalue=entry["username"])
        new_password = simpledialog.askstring("Edit Password", "Password:", initialvalue=entry["password"],show="*")
        # If statements to handle bad inputs
        if new_service == None:
            new_service = entry["service"]
        if new_username == None:
            new_username = entry["username"]
        if new_password == None:
            new_password = entry["password"]
        # Ensures that all dialogs have been answered and updates the values. 
        if new_service and new_username and new_password:
            self.entries[index] = {"service": new_service, "username": new_username, "password": new_password}
            self.refresh_list()

    # Function to handle deletion of a given entry
    def delete_entry(self, index):
        del self.entries[index]
        self.refresh_list()

    # Function to handle the 'Add to List' button
    def add_to_list(self):
        # Get the user entries from the GUI
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirmPassword = self.confirm_password_entry.get()
        # Check if all entries were filled
        if service and username and password and confirmPassword:
            # Check that the password was confirmed
            if password == confirmPassword:
                self.add_entry(service, username, password)
                self.service_entry.delete(0, tk.END)
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                self.confirm_password_entry.delete(0, tk.END)
                self.refresh_list()
            else:
                # Error message for bad passwords
                messagebox.showerror("Password Error", "Passwords do not match. Double check your inputs and try again.")
        else:
            # Error message for missing inputs
            messagebox.showerror("Input Error", "Please fill in all fields.")

# This was reccomended to be added, it is to ensure the program runs correctly
if __name__ == "__main__":
    # Sets the working directory to the PPWM folder no matter where it is installed
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    # Starts the program
    password_manager = PasswordManager()
    password_manager.create_widgets()
