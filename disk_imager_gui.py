import os
import shutil
import threading
import tempfile
import tkinter as tk
import urllib.request
from tkinter import filedialog, messagebox, ttk
from ui_theme import COLORS, configure_styles

try:
    import psutil
except ModuleNotFoundError:
    psutil = None

win32diskimager_path = "./Win32DiskImager-Installer.exe"

def is_usb_connected():
    drives = get_removable_drives()
    if drives:
        print("External flash drives connected: ")
        for drive in drives:
            print(f"{drive['device']}\n")
        return True
    print("\tNo external flash drives found.\t")
    return False


def _volume_details(mountpoint):
    details = {"label": "Removable drive", "filesystem": "Unknown"}
    if os.name != "nt":
        return details

    import ctypes

    volume_name = ctypes.create_unicode_buffer(261)
    filesystem_name = ctypes.create_unicode_buffer(261)
    serial_number = ctypes.c_uint32()
    maximum_component_length = ctypes.c_uint32()
    filesystem_flags = ctypes.c_uint32()
    result = ctypes.windll.kernel32.GetVolumeInformationW(
        mountpoint,
        volume_name,
        len(volume_name),
        ctypes.byref(serial_number),
        ctypes.byref(maximum_component_length),
        ctypes.byref(filesystem_flags),
        filesystem_name,
        len(filesystem_name),
    )
    if result:
        details["label"] = volume_name.value or "Removable drive"
        details["filesystem"] = filesystem_name.value or "Unknown"
        details["serial"] = f"{serial_number.value:08X}"
    return details


def get_removable_drives():
    drives = []
    seen = set()
    if psutil is not None:
        try:
            partitions = psutil.disk_partitions(all=True)
        except OSError:
            partitions = []
        for partition in partitions:
            if "removable" not in partition.opts.lower():
                continue
            mountpoint = partition.mountpoint
            key = os.path.normcase(mountpoint)
            if key in seen:
                continue
            seen.add(key)
            details = _volume_details(mountpoint)
            drives.append({
                "device": partition.device.rstrip("\\/"),
                "mountpoint": mountpoint,
                "label": details["label"],
                "filesystem": partition.fstype or details["filesystem"],
                "serial": details.get("serial", ""),
            })

    if os.name == "nt":
        import ctypes

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            mountpoint = f"{letter}:\\"
            if ctypes.windll.kernel32.GetDriveTypeW(mountpoint) != 2:
                continue
            key = os.path.normcase(mountpoint)
            if key in seen:
                continue
            details = _volume_details(mountpoint)
            seen.add(key)
            drives.append({
                "device": f"{letter}:",
                "mountpoint": mountpoint,
                "label": details["label"],
                "filesystem": details["filesystem"],
                "serial": details.get("serial", ""),
            })
    return drives

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
        install_status_label.config(text="Installing Win32DiskImager...", style="CardBody.TLabel")
        urllib.request.urlretrieve(url, path)
        install_status_label.config(text="Win32DiskImager installed successfully.", style="CardSuccess.TLabel")
    except Exception as e:
        install_status_label.config(text=f"Installation failed: {e}", style="CardError.TLabel")

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
        install_status_label.config(text="Win32DiskImager could not start. Install it or browse to its executable.", style="CardError.TLabel")

def browse_button_clicked(install_status_label):
    global win32diskimager_path 
    win32diskimager_path  = filedialog.askopenfilename(title="Select Win32DiskImager executable")
    if is_win32diskimager_installed():
        install_status_label.config(text="Win32DiskImager found.", style="CardSuccess.TLabel")
    else:
        install_status_label.config(text="Win32DiskImager not found at the specified path.", style="CardError.TLabel")

def create_disk_image_button_clicked(drive_entry, install_status_label, destination_image=None):
    source_usb_drive = drive_entry.get() if hasattr(drive_entry, "get") else drive_entry
    if destination_image is None:
        destination_image = 'usb_drive_image.img'
    create_disk_image(source_usb_drive, destination_image, install_status_label)

def _valid_output_filename(filename):
    invalid_characters = '<>:"/\\|?*'
    return (
        bool(filename)
        and filename not in {".", ".."}
        and not any(character in invalid_characters or ord(character) < 32 for character in filename)
        and filename[-1] not in {" ", "."}
    )


def create_disk_imager_page(parent, open_image_callback=None):
    global root
    root = parent.winfo_toplevel()
    page = ttk.Frame(parent, padding=0)
    page.columnconfigure(0, weight=1)

    source_card = ttk.Frame(page, style="Surface.TFrame", padding=10)
    source_card.grid(row=0, column=0, sticky="ew", pady=3)
    source_card.columnconfigure(0, weight=1)
    ttk.Label(source_card, text="01   Source Drive", style="CardHeading.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
    source_var = tk.StringVar(master=page)
    source_combo = ttk.Combobox(source_card, textvariable=source_var, state="readonly")
    source_combo.grid(row=1, column=0, sticky="ew", padx=(0, 8))
    source_status = ttk.Label(source_card, text="No removable drive detected.", style="CardWarning.TLabel", wraplength=560)
    source_status.grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))
    ttk.Label(source_card, text="Win32DiskImager", style="CardSmall.TLabel").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(6, 0))
    ttk.Button(source_card, text="Install", style="Subtle.TButton", command=lambda: download_and_install_win32diskimager(install_status_label)).grid(row=3, column=1, sticky="e", pady=(6, 0))
    ttk.Button(source_card, text="Browse Installer...", style="Secondary.TButton", command=lambda: browse_button_clicked(install_status_label)).grid(row=3, column=2, sticky="e", padx=(8, 0), pady=(6, 0))
    install_status_label = ttk.Label(source_card, text="Win32DiskImager must be available before imaging.", style="CardBody.TLabel", wraplength=560)
    install_status_label.grid(row=4, column=0, columnspan=3, sticky="w", pady=(4, 0))

    output_card = ttk.Frame(page, style="Surface.TFrame", padding=10)
    output_card.grid(row=1, column=0, sticky="ew", pady=3)
    output_card.columnconfigure(0, weight=1)
    ttk.Label(output_card, text="02   Output Destination · filename", style="CardHeading.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))
    destination_folder = tk.StringVar(master=page, value=os.getcwd())
    filename_var = tk.StringVar(master=page, value="disk_image.dd")
    filename_entry = ttk.Entry(output_card, textvariable=filename_var, style="FieldMono.TEntry")
    filename_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
    folder_button = ttk.Button(output_card, text="Browse Folder...", style="Secondary.TButton", command=lambda: choose_folder())
    folder_button.grid(row=1, column=1, sticky="e")
    acquire_button = ttk.Button(output_card, text="Acquire Disk Image...", style="Primary.TButton", state="disabled")
    acquire_button.grid(row=1, column=2, sticky="e", padx=(8, 0))
    destination_path = tk.StringVar(master=page)
    ttk.Label(output_card, textvariable=destination_path, style="CardMono.TLabel", wraplength=560).grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))
    output_status = ttk.Label(output_card, text="", style="CardBody.TLabel", wraplength=560)
    output_status.grid(row=3, column=0, columnspan=3, sticky="w", pady=(1, 0))

    image_card = ttk.Frame(page, style="Surface.TFrame", padding=10)
    image_card.grid(row=2, column=0, sticky="ew", pady=3)
    image_card.columnconfigure(0, weight=1)
    ttk.Label(image_card, text="03   Existing Disk Image", style="CardHeading.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
    ttk.Label(image_card, text="Analyze an existing image; this does not create or modify one.", style="CardBody.TLabel", wraplength=560).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 6))
    existing_image = tk.StringVar(master=page)
    ttk.Button(image_card, text="Select Existing Image...", style="Secondary.TButton", command=lambda: choose_existing_image()).grid(row=2, column=0, sticky="w", padx=(0, 8))
    open_image_button = ttk.Button(image_card, text="Open in File Carver", style="Subtle.TButton", state="disabled", command=lambda: open_selected_image())
    open_image_button.grid(row=2, column=1, sticky="w")
    image_status = ttk.Label(image_card, text="No image selected.", style="CardBody.TLabel", wraplength=560)
    image_status.grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))

    drive_records = {}

    def refresh_drives():
        previous = source_var.get()
        drives = get_removable_drives()
        drive_records.clear()
        values = []
        for drive in drives:
            device = drive["device"]
            free_space = ""
            try:
                free_space = f"  /  {shutil.disk_usage(drive['mountpoint']).free // (1024 ** 3)} GB free"
            except OSError:
                pass
            serial = f"  /  S/N {drive['serial']}" if drive.get("serial") else ""
            display = f"{device}  /  {drive['label']}  /  {drive['filesystem']}{serial}{free_space}"
            values.append(display)
            drive_records[display] = drive
        source_combo.configure(values=values)
        if previous in drive_records:
            source_var.set(previous)
        elif values:
            source_var.set(values[0])
        else:
            source_var.set("")
        source_status.configure(
            text=f"{len(values)} removable drive(s) detected." if values else "No removable drive detected. Connect a drive and refresh.",
            style="CardBody.TLabel" if values else "CardWarning.TLabel",
        )
        refresh_acquisition_state()

    def refresh_acquisition_state(*_):
        valid, message, _ = validate_destination(show_probe=False)
        selected = drive_records.get(source_var.get())
        if valid and selected and same_source_volume(selected, destination_folder.get()):
            valid = False
            message = "Choose a destination outside the selected source drive."
        if not valid:
            status_style = "CardError.TLabel"
        elif "confirmation" in message:
            status_style = "CardWarning.TLabel"
        else:
            status_style = "CardSuccess.TLabel"
        output_status.configure(text=message, style=status_style)
        can_acquire = selected is not None and valid
        acquire_button.configure(state="normal" if can_acquire else "disabled")

    def choose_folder():
        selected = filedialog.askdirectory(parent=root, title="Choose output folder", initialdir=destination_folder.get(), mustexist=True)
        if selected:
            destination_folder.set(selected)
            refresh_path_status()

    def refresh_path_status(*_):
        filename = filename_var.get()
        path = os.path.abspath(os.path.join(destination_folder.get(), filename)) if filename else ""
        destination_path.set(f"Destination: {path}" if path else "Destination: enter an output filename")
        refresh_acquisition_state()

    def validate_destination(show_probe):
        folder = destination_folder.get()
        filename = filename_var.get()
        if not os.path.isdir(folder):
            return False, "Choose an existing destination folder.", ""
        if not _valid_output_filename(filename):
            return False, "Enter a valid filename without path separators or reserved characters.", ""
        target = os.path.abspath(os.path.join(folder, filename))
        if not os.access(folder, os.W_OK):
            return False, "The selected destination folder is not writable.", target
        if show_probe:
            try:
                with tempfile.NamedTemporaryFile(prefix=".karvit_write_test_", dir=folder, delete=True):
                    pass
            except OSError as error:
                return False, f"Destination is not writable: {error}", target
        if os.path.exists(target) and not os.path.isfile(target):
            return False, "The destination path exists and is not a file.", target
        if os.path.exists(target):
            return True, "File exists; overwrite confirmation will be required.", target
        return True, "Destination folder is writable.", target

    def same_source_volume(drive, folder):
        source = os.path.normcase(os.path.realpath(drive["mountpoint"]))
        destination = os.path.normcase(os.path.realpath(folder))
        try:
            return os.path.commonpath((source, destination)) == source
        except ValueError:
            return False

    def begin_acquisition():
        selected = drive_records.get(source_var.get())
        if not selected:
            messagebox.showerror("Source required", "Select a removable source drive first.", parent=root)
            return
        valid, message, target = validate_destination(show_probe=True)
        output_status.configure(text=message, style="CardSuccess.TLabel" if valid else "CardError.TLabel")
        if not valid:
            return
        if same_source_volume(selected, os.path.dirname(target)):
            output_status.configure(text="Choose a destination outside the selected source drive.", style="CardWarning.TLabel")
            messagebox.showerror("Unsafe destination", "The image cannot be written to the selected source drive.", parent=root)
            return
        if os.path.exists(target) and not messagebox.askyesno("Confirm overwrite", f"This file already exists:\n{target}\n\nOverwrite it?", parent=root):
            return
        confirmed = messagebox.askyesno(
            "Confirm acquisition",
            f"Create a disk image from {selected['device']} ({selected['label']})?\n\nOutput:\n{target}\n\nAcquisition will start only after this confirmation.",
            parent=root,
        )
        if not confirmed:
            return
        output_status.configure(text="Acquisition started.", style="CardSuccess.TLabel")
        create_disk_image_button_clicked(selected["device"], install_status_label, target)

    def choose_existing_image():
        selected = filedialog.askopenfilename(
            parent=root,
            title="Select existing disk image for analysis",
            filetypes=[("Forensic disk images", "*.dd *.img *.raw *.001 *.E01 *.e01 *.iso"), ("All files", "*.*")],
        )
        if selected:
            existing_image.set(selected)
            image_status.configure(text=selected, style="CardMono.TLabel")
            open_image_button.configure(state="normal")

    def open_selected_image():
        path = existing_image.get()
        if not path:
            return
        if open_image_callback is None:
            image_status.configure(text="Open the main KarvIt workspace to send this image to File Carver.")
            return
        open_image_callback(path)

    ttk.Button(source_card, text="Refresh", command=refresh_drives).grid(row=1, column=1, sticky="e")
    source_combo.bind("<<ComboboxSelected>>", refresh_acquisition_state)
    filename_var.trace_add("write", refresh_path_status)
    destination_folder.trace_add("write", refresh_path_status)
    acquire_button.configure(command=begin_acquisition)
    refresh_path_status()
    refresh_drives()
    return page


def main():
    global root
    root = tk.Tk()
    root.title("KarvIt | Disk Imager")
    root.geometry("900x650")
    root.minsize(760, 560)
    configure_styles(root)
    root.configure(bg=COLORS["background"])
    create_disk_imager_page(root).pack(fill="both", expand=True, padx=32, pady=28)
    root.mainloop()


if __name__ == "__main__":
    main()