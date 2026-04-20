<div align="center">

<img src="Resources/karvit_logo.png" alt="KarvIt logo" width="120" />

# KarvIt | Digital Forensics

**Disk imaging and signature-based file carving in a clean desktop app.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-2F6FED)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)
![Processing](https://img.shields.io/badge/Processing-Local%20%2F%20Offline-2E9E6B)

[Features](#features) · [Setup](#requirements-and-setup) · [Usage](#usage) · [Resources](#resources) · [Safety](#safety-limitations-and-responsible-use) · [Structure](#project-structure)

</div>

---

## Overview

KarvIt is a Python/Tkinter desktop tool for **disk imaging** and **signature-based file carving**. It brings two common forensic tasks into a single interface: creating an image of a removable drive, and recovering files from an existing disk image.

The interface uses a light theme. All fonts ship with the repository and are loaded locally, so the app needs no network access to render. Processing stays on your device.

<!-- Optional: add a screenshot
<p align="center"><img src="Resources/screenshot_dashboard.png" alt="KarvIt dashboard" width="800" /></p>
-->

## Features

### Dashboard and navigation
- Sidebar navigation: **Dashboard**, **Disk Imager**, **File Carver**, **Recovery History**, **About**.
- Dashboard cards for quick access to Disk Imager and File Carver.

### Disk Imager
- Removable-drive selection with a refresh option and drive metadata.
- Output folder and filename selection.
- Destination validation (writability check).
- Source-volume protection: output cannot be written to the selected source volume.
- Overwrite confirmation when the target file already exists.
- Explicit confirmation before acquisition starts.
- Imaging is performed by the external **Win32DiskImager** tool. Install it, or browse to its executable from within the app.

### File Carver
- Recovers **PNG**, **JPEG**, **PDF**, and **EVTX** files.
- Existing-image selection, plus handoff from Disk Imager to File Carver.

### Recovery History
- Currently an empty state only. Recovery runs are **not** persisted between sessions.

## Installation

### Prerequisites

- Python 3.12
- Git
- Windows 10/11

### Setup

**1. Clone the repository**

```powershell
git clone https://github.com/Nikhil-tech-eng/Karv_it
cd Karv_It
```

**2. Create a virtual environment**

```powershell
py -3.12 -m venv venv
```

**3. Activate the virtual environment**

```powershell
venv\Scripts\activate
```

**4. Upgrade pip**

```powershell
python -m pip install --upgrade pip
```

**5. Install dependencies**

```powershell
pip install -r requirements.txt
```

**6. Run KarvIt**

```powershell
python main.py
```

## Usage

### Create a disk image
1. Open **Disk Imager** and connect the removable drive.
2. Select the source drive (use **Refresh** if it is not listed).
3. Choose an output folder and filename. The output must not be on the source volume.
4. Confirm the overwrite prompt if the file exists.
5. Review the details and confirm acquisition.

### Carve files from an image
1. Open **File Carver** and select an existing disk image, or continue directly from Disk Imager.
2. Choose a recovery type: PNG, JPEG, PDF, or EVTX.
3. Start the recovery.

**Supported image extensions:** `.dd`, `.img`, `.raw`, `.001`, `.E01`, `.e01`, `.iso` (the file chooser also allows all files).

**Output files** are written relative to the current working directory:

| Type | Output file |
|------|-------------|
| PNG  | `carved_png_files_1.png` |
| JPEG | `carved_JPEG_files_1.jpeg` |
| PDF  | `carved_PDF_files_1.pdf` |
| EVTX | `carved_log_files_1.evtx` |

## Resources

The `Resources/` folder contains:

- The KarvIt logo.
- A sample zipped disk image. Unzip it to try carving PNG and JPEG files.
- Local fonts: **Inter** (UI) and **JetBrains Mono** (technical data), with their OFL license files under `Resources/fonts/`. Windows loads them privately for the app; they are **not** installed system-wide.

## Safety, limitations, and responsible use

**Confirmed behavior**

- Acquisition requires explicit confirmation.
- The destination is checked for writability.
- The app asks before overwriting an existing file.
- Output on the selected source volume is blocked.

**Not implemented**

- Hardware write-blocking or forensic write protection
- Image verification or hashing
- Chain-of-custody tracking
- Persistent recovery history

**Notes**

- Carving is signature-based recovery for the listed formats. Recovery is not guaranteed.
- Use KarvIt only on media you are authorized to examine.
- For real investigations, use appropriate forensic write-blocking procedures.

## Project structure

```text
Karv_It/
├── main.py               # Application entry point and dashboard
├── disk_imager_gui.py    # Disk Imager interface and acquisition flow
├── file_carver_gui.py    # File Carver interface and carving logic
├── ui_theme.py           # Light theme, fonts, and styling
├── requirements.txt      # Python dependencies
└── Resources/            # Logo, sample image archive, and fonts
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

Bundled fonts (Inter and JetBrains Mono) are licensed under the **SIL Open Font License 1.1**. The license files are in `Resources/fonts/`.

## Author

Nikhil Teckchandani
Developer of KarvIt

[![GitHub](https://img.shields.io/badge/GitHub-Nikhil-2DA44E?logo=github&logoColor=white)](https://github.com/Nikhil-tech-eng)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nikhil-2DA44E?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nikhil-teckchandani-aa8b0b368/)
[![Email](https://img.shields.io/badge/Email-Nikhil-2DA44E?logo=gmail&logoColor=white)](mailto:teckchandaninikhil@gmail.com)

## Contributing and Feedback

Bug reports and suggestions are welcome. Please open an [issue](../../issues) with the steps to reproduce the problem and your Windows and Python versions.

## Disclaimer

KarvIt is provided as-is, without warranty. The author is not responsible for data loss or misuse. Use it only on media you are authorized to examine.

---

<div align="center">
<sub>Built with Python and Tkinter</sub>
</div>