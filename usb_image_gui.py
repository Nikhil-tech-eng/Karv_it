from PIL import Image, ImageTk
import subprocess
import urllib.request
import os
import psutil
import tkinter as tk
import threading
from tkinter import ttk, filedialog
from ui_theme import font_for

win32diskimager_path = "./Win32DiskImager-Installer.exe"

def is_usb_connected():
    partitions = psutil.disk_partitions(all=True)
    external_drives = [partition.device for partition in partitions if 'removable' in partition.opts.lower()]
    if external_drives:
        print("External flash drives connected: ")
        for drive in external_drives:
            print(f"{drive}\n")
        return True
    else:
        print("\tNo external flash drives found.\t")
        return False

def is_win32diskimager_installed():    
    global win32diskimager_path
    try:
        expected_size = 190976
        actual_size = os.path.getsize(win32diskimager_path)
        if (os.path.isfile(win32diskimager_path) and expected_size == actual_size):
            return True
        else:
            return True          #False
    except FileNotFoundError as e:
        print(e)
        return False

def download_installer(url, path, install_status_label):
    try:
        install_status_label.config(text="Installing Win32DiskImager...", foreground="green", font=font_for(install_status_label.winfo_toplevel(), "body"))
        urllib.request.urlretrieve(url, path)
        install_status_label.config(text="Win32DiskImager Successfully Installed !!!", foreground="green", font=font_for(install_status_label.winfo_toplevel(), "body"))
    except Exception as e:
        install_status_label.config(text=f"Installation failed: {e}", foreground="red", font=font_for(install_status_label.winfo_toplevel(), "body"))

def download_and_install_win32diskimager(install_status_label):
    # Specify the URL of the Win32DiskImager installer
    win32diskimager_url = "https://win32diskimager.b-cdn.net/win32diskimager-1.0.0-install.exe"

    win32diskimager_path = "Win32DiskImager-Installer.exe"
    # Download the installer in a separate thread
    install_thread = threading.Thread(target=download_installer, args=(win32diskimager_url, win32diskimager_path, install_status_label))
    install_thread.start()

def create_disk_image(source_usb_drive, destination_image, install_status_label):
    try:
        subprocess.run([win32diskimager_path, 'drive_image.dd', source_usb_drive, '--output', destination_image], shell=True, check=True)
        print("Exiting Win32DiskImager... ")
        return
    except subprocess.CalledProcessError as e:
        install_status_label.config(text="Win32DiskImager Not Found !!! Please Install Or Browse For Win32DiskImager", font=font_for(install_status_label.winfo_toplevel(), "supporting"), foreground="red")

def browse_button_clicked(install_status_label):
    global win32diskimager_path 
    win32diskimager_path  = filedialog.askopenfilename(title="Select Win32DiskImager executable")
    if is_win32diskimager_installed():
        install_status_label.config(text="Win32DiskImager Found", foreground="green", font=font_for(install_status_label.winfo_toplevel(), "body"))
    else:
        install_status_label.config(text="Win32DiskImager not found at the specified path.", foreground="red", font=font_for(install_status_label.winfo_toplevel(), "body"))

def create_disk_image_button_clicked(drive_entry, install_status_label):
    source_usb_drive = drive_entry.get()
    destination_image = 'usb_drive_image.img'
    create_disk_image(source_usb_drive, destination_image, install_status_label)

# Create themed Tkinter window
root = tk.Tk()
root.title("KarvIt: File Carving Tool")
global bg_color
bg_color = "#0CF5EA"
logo_image = Image.open("./logo.png")
logo_image = logo_image.resize((75, 75))
logo_tk_image = ImageTk.PhotoImage(logo_image)
logo_label = ttk.Label(root, image=logo_tk_image, background=bg_color)
logo_label.place(x=2, y=2, anchor='nw')

if is_usb_connected():
    # Set window dimensions
    window_width = 500
    window_height = 350
    root.geometry(f"{window_width}x{window_height}")

    style = ttk.Style()
    # Configure background color
    style.configure('TButton', background=bg_color, relief='raised', padding=(5, 5), bordercolor="ff00ff", font=font_for(root, "button"))

    # Configure fonts
    font_bold = font_for(root, "section_heading")
    font_normal = font_for(root, "body")

    root.configure(bg=bg_color)
    # Widgets
    usb_label = ttk.Label(root, text="KarvIt - Disk Imager ", font=font_bold, foreground="#3C4692", background=bg_color)
    usb_label.pack(pady=20)

    download_label = ttk.Label(root, text="To Install Win32DiskImager, Click Below: ", font=font_normal, foreground="#000000", background=bg_color)
    download_label.pack(pady=3)

    install_button = ttk.Button(root, text="Install Win32DiskImager", command=lambda: download_and_install_win32diskimager(install_status_label))
    install_button.pack(pady=3)

    verify_label = ttk.Label(root, text="To Verify Win32DiskImager, Click Below: ", font=font_normal, foreground="#000000", background=bg_color)
    verify_label.pack(pady=3)

    browse_button = ttk.Button(root, text="Browse for Win32DiskImager", command=lambda: browse_button_clicked(install_status_label))
    browse_button.pack(pady=5)

    install_status_label = ttk.Label(root, text="", font=font_normal, background=bg_color)
    install_status_label.pack(pady=3)

    drive_label = ttk.Label(root, text="Enter Drive Name (e.g., E: ) ~ ", font=font_normal, background=bg_color)
    drive_label.pack(pady=3)

    drive_entry = ttk.Entry(root, font=font_normal)
    drive_entry.pack(pady=3)

    create_image_button = ttk.Button(root, text="Create Disk Image", command=lambda: create_disk_image_button_clicked(drive_entry, install_status_label))
    create_image_button.pack(pady=3)

else:
    # Set window dimensions
    window_width = 500
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")
    root.configure(bg=bg_color)
    # Configure fonts
    font_bold = font_for(root, "section_heading")
    font_normal = font_for(root, "body")

    exit_label = ttk.Label(root, text="Please Connect An External Flash Drive...", font=font_bold, foreground="white", background="red")
    exit_label.pack(pady=100)

# Start the Tkinter event loop
root.mainloop()
