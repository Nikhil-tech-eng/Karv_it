import os
import tkinter as tk
from tkinter import ttk, filedialog
from ui_theme import COLORS, configure_styles


def main():
    global root
    root = tk.Tk()
    root.title("KarvIt | File Carver")
    root.geometry("900x650")
    root.minsize(760, 560)
    configure_styles(root)
    root.configure(bg=COLORS["background"])
    create_file_carver_page(root).pack(fill="both", expand=True, padx=32, pady=28)
    root.mainloop()

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Forensic disk images", "*.dd *.img *.raw *.001 *.E01 *.e01 *.iso"), ("All files", "*.*")]
    )
    file_var.set(file_path)

def carve_png_files():
    print("Carving PNG files...")
    src_file_path = file_var.get()
    dst_file_path = "./carved_png_files"

    # Define header and footer for PNG files
    PNG_HEADER = bytes([0x89, 0x50, 0x4e, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    PNG_FOOTER = bytes([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82])

    # Set the chunk size
    chunk_size = 1024 * 1024  

    # Initialize position and counter for carved files
    position = 0
    count = 0

    with open(src_file_path, "rb") as file:
        while True:
            # Read a chunk from the file
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file

            # Search for the header in the chunk
            header_index = chunk.find(PNG_HEADER)

            while header_index != -1:
                # Calculate the absolute position of the header in the entire file
                absolute_header_index = position + header_index

                # Search for the footer in the chunk starting from the header
                footer_index = chunk.find(PNG_FOOTER, header_index)

                if footer_index != -1:
                    # Calculate the end of the footer
                    footer_end = absolute_header_index + footer_index + len(PNG_FOOTER)

                    # Ensure the footer is after the header
                    if absolute_header_index < footer_end:
                        count += 1
                        dst_data = chunk[header_index:footer_end]
                        dst_file_name = f"{dst_file_path}_{count}.png"
                        open(dst_file_name, "wb").write(dst_data)
                        print("Carved:", dst_file_name)

                    # Update position to search for the next PNG file
                    position = footer_end

                # Find the next header in the remaining part of the chunk
                header_index = chunk.find(PNG_HEADER, header_index + 1)

        # Print the total number of carved files
        print(f"Successfully Carved {count} PNG Files...")
    
    status_label.configure(text=f"Successfully Carved {count} PNG files.", style="CardSuccess.TLabel")
    
    
def carve_jpeg_files():
    print("Carving JPEG files...")

    src_file_path = file_var.get()
    dst_file_path = "./carved_JPEG_files"

    # Define header and footer for JPEG files
    JPEG_HEADER = bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46])
    JPEG_FOOTER = bytes([0xFF, 0xD9])

    # Set the chunk size
    chunk_size = 1024 * 1024

    # Initialize position and counter for carved files
    position = 0
    count = 0

    with open(src_file_path, "rb") as file:
        while True:
            # Read a chunk from the file
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file

            # Search for the header in the chunk
            header_index = chunk.find(JPEG_HEADER)

            while header_index != -1:
                # Calculate the absolute position of the header in the entire file
                absolute_header_index = position + header_index

                # Search for the footer in the chunk starting from the header
                footer_index = chunk.find(JPEG_FOOTER, header_index)

                if footer_index != -1:
                    # Calculate the end of the footer
                    footer_end = absolute_header_index + footer_index + len(JPEG_FOOTER)

                    # Ensure the footer is after the header
                    if absolute_header_index < footer_end:
                        count += 1
                        dst_data = chunk[header_index:footer_end]
                        dst_file_name = f"{dst_file_path}_{count}.jpeg"
                        open(dst_file_name, "wb").write(dst_data)
                        print("Carved:", dst_file_name)

                    # Update position to search for the next JPEG file
                    position += footer_end

                # Find the next header in the remaining part of the chunk
                header_index = chunk.find(JPEG_HEADER, header_index + 1)

    # Print the total number of carved files
    print(f"Successfully Carved {count} JPEG Files...")

    status_label.configure(text=f"Successfully Carved {count} JPEG files.", style="CardSuccess.TLabel")

def carve_pdf_files():
    print("Carving PDF files...")

    src_file_path = file_var.get()
    dst_file_path = "./carved_PDF_files"

    # Define header and footer for PDF files
    PDF_HEADER = bytes([0x25, 0x50, 0x44, 0x46, 0x2D, 0x31, 0x2E])
    PDF_FOOTER = bytes([0x25, 0x25, 0x45, 0x4F, 0x46])

    # Set the chunk size
    chunk_size = 1024 * 1024

    # Initialize position and counter for carved files
    position = 0
    count = 0

    with open(src_file_path, "rb") as file:
        while True:
            # Read a chunk from the file
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file

            # Search for the header in the chunk
            header_index = chunk.find(PDF_HEADER)

            while header_index != -1:
                # Calculate the absolute position of the header in the entire file
                absolute_header_index = position + header_index

                # Search for the footer in the chunk starting from the header
                footer_index = chunk.find(PDF_FOOTER, header_index)

                if footer_index != -1:
                    # Calculate the end of the footer
                    footer_end = absolute_header_index + footer_index + len(PDF_FOOTER)

                    # Ensure the footer is after the header
                    if absolute_header_index < footer_end:
                        count += 1
                        dst_data = chunk[header_index:footer_end]
                        dst_file_name = f"{dst_file_path}_{count}.pdf"
                        open(dst_file_name, "wb").write(dst_data)
                        print("Carved:", dst_file_name)

                    # Update position to search for the next PDF file
                    position += footer_end

                # Find the next header in the remaining part of the chunk
                header_index = chunk.find(PDF_HEADER, header_index + 1)

    # Print the total number of carved files
    print(f"Successfully Carved {count} PDF Files...")

    status_label.configure(text=f"Successfully Carved {count} PDF files.", style="CardSuccess.TLabel")

def carve_evtx_files():
    print("Carving EVTX files...")
    src_file_path = file_var.get()
    
    dst_file_path = "./carved_log_files"

    # Define header and footer for EVTX files
    EVTX_HEADER = bytes([0x45, 0x6C, 0x66, 0x46, 0x69, 0x6C, 0x65])
    EVTX_FOOTER = bytes([0x68, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x68, 0x03, 0x00, 0x00])

    # Set the chunk size
    chunk_size = 1024 * 1024

    # Initialize position and counter for carved files
    position = 0
    count = 0

    with open(src_file_path, "rb") as file:
        while True:
            # Read a chunk from the file
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file

            # Search for the header in the chunk
            header_index = chunk.find(EVTX_HEADER)

            while header_index != -1:
                # Calculate the absolute position of the header in the entire file
                absolute_header_index = position + header_index

                # Search for the footer in the chunk starting from the header
                footer_index = chunk.find(EVTX_FOOTER, header_index)

                if footer_index != -1:
                    # Calculate the end of the footer
                    footer_end = absolute_header_index + footer_index + len(EVTX_FOOTER)

                    # Ensure the footer is after the header
                    if absolute_header_index < footer_end:
                        count += 1
                        dst_data = chunk[header_index:footer_end]
                        dst_file_name = f"{dst_file_path}_{count}.evtx"
                        open(dst_file_name, "wb").write(dst_data)
                        print("Carved:", dst_file_name)

                    # Update position to search for the next EVTX file
                    position += footer_end

                # Find the next header in the remaining part of the chunk
                header_index = chunk.find(EVTX_HEADER, header_index + 1)

    # Print the total number of carved files
    print(f"Successfully Carved {count} EVTX Files...")

    status_label.configure(text=f"Successfully Carved {count} EVTX files.", style="CardSuccess.TLabel")

def exit_application():
    print("Closing Window...")
    root.destroy()


def create_file_carver_page(parent):
    global file_var, status_label, root
    root = parent.winfo_toplevel()
    page = ttk.Frame(parent, padding=4)
    page.columnconfigure(0, weight=1)
    page.rowconfigure(4, weight=1)

    ttk.Label(page, text="RECOVERY  /  SIGNATURE SCAN", style="Eyebrow.TLabel").grid(row=0, column=0, sticky="w", pady=(2, 4))
    ttk.Label(page, text="Recover files from a disk image", style="Heading.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 10))

    source = ttk.Frame(page, style="Surface.TFrame", padding=16)
    source.grid(row=2, column=0, sticky="ew")
    source.columnconfigure(0, weight=1)
    ttk.Label(source, text="Source image", style="CardHeading.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
    file_var = tk.StringVar(master=page)
    file_entry = ttk.Entry(source, textvariable=file_var, state="readonly", style="FieldMono.TEntry")
    file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
    ttk.Button(source, text="Browse image...", style="Secondary.TButton", command=browse_file).grid(row=1, column=1, sticky="e")
    source_summary = ttk.Label(source, text="No image selected. Supported: .dd, .img, .raw, .001, .E01, .iso", style="CardSmall.TLabel", wraplength=700)
    source_summary.grid(row=2, column=0, columnspan=2, sticky="w", pady=(7, 0))

    ttk.Label(page, text="Recovery options", style="Heading.TLabel").grid(row=3, column=0, sticky="w", pady=(18, 9))
    options = ttk.Frame(page)
    options.grid(row=4, column=0, sticky="ew")
    options.columnconfigure((0, 1), weight=1, uniform="recovery")
    recoveries = [
        ("PNG", "Portable Network Graphics", carve_png_files),
        ("JPEG", "JPEG image files", carve_jpeg_files),
        ("PDF", "Portable documents", carve_pdf_files),
        ("EVTX", "Windows event logs", carve_evtx_files),
    ]
    recovery_buttons = []
    for index, (file_type, detail, callback) in enumerate(recoveries):
        row, column = divmod(index, 2)
        card = ttk.Frame(options, style="Surface.TFrame", padding=15)
        card.grid(row=row, column=column, sticky="nsew", padx=(0, 6) if column == 0 else (6, 0), pady=(0, 10))
        card.columnconfigure(0, weight=1)
        ttk.Label(card, text=file_type, style="CardHeading.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(card, text=detail, style="CardBody.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 9))
        button = ttk.Button(card, text=f"Recover {file_type}", command=callback, style="Secondary.TButton", state="disabled")
        button.grid(row=2, column=0, sticky="w")
        recovery_buttons.append(button)

    results = ttk.Frame(page, style="Surface.TFrame", padding=(14, 10))
    results.grid(row=5, column=0, sticky="ew", pady=(3, 0))
    ttk.Label(results, text="Results", style="CardHeading.TLabel").pack(anchor="w")
    status_label = ttk.Label(results, text="Select a disk image to enable recovery options.", style="CardBody.TLabel", wraplength=700)
    status_label.pack(anchor="w", pady=(3, 0))

    def update_source_status(*_):
        selected_path = file_var.get()
        selected = bool(selected_path)
        for button in recovery_buttons:
            button.configure(state="normal" if selected else "disabled")
        source_summary.configure(
            text=f"Selected image: {os.path.basename(selected_path)}" if selected else "No image selected. Supported: .dd, .img, .raw, .001, .E01, .iso"
        )
        status_label.configure(text="Image ready. Choose a recovery type." if selected else "Select a disk image to enable recovery options.", style="CardBody.TLabel")

    file_var.trace_add("write", update_source_status)
    return page

if __name__ == "__main__":
    main()
