"""Windows Hardware Compatibility Guide
Best-fit PC hardware per Windows version. Quiet by design: no sounds,
no animations, one scrolling list, filters on the left.
"""
import os
import sys
from dataclasses import dataclass

# Safe graphics defaults (the setup script can override with -UseGpu).
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
if os.environ.get("HWG_USE_GPU") != "1":
    os.environ.setdefault("QT_OPENGL", "software")
    os.environ.setdefault("QT_QUICK_BACKEND", "software")

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

RETRO = "Retro Preservation"
LEGACY = "Legacy Gaming & Productivity"
MODERN = "Modern (Workstation / Gaming / VMs)"
USE_CASES = ["All", RETRO, LEGACY, MODERN]
TIERS = ["All", "Budget", "Max Performance"]


@dataclass
class Config:
    os: str
    use_case: str
    tier: str
    summary: str
    parts: list
    notes: list


CONFIGS = [
    Config(
        "Windows 95 (OSR2)", RETRO, "Budget",
        "Simple, period-correct machine. Fewer parts, fewer driver fights.",
        [("CPU", "Pentium MMX 200 or Pentium II 266"),
         ("Chipset", "Intel 430TX or 440LX"),
         ("RAM", "64 MB SDRAM"),
         ("GPU", "Matrox Millennium II or S3 Trio64 (PCI)"),
         ("Sound", "Sound Blaster 16 (ISA) for DOS game compatibility"),
         ("Storage", "CompactFlash-to-IDE adapter, 4-8 GB, FAT32 (OSR2 only)")],
        ["Original release (OSR1) has no FAT32 or USB. Use OSR2 or later.",
         "AGP and USB need OSR2.1+ and the chipset INF/AGP patch.",
         "Very large RAM (over ~480 MB) can stop boot. Stay well under."],
    ),
    Config(
        "Windows 95 (OSR2)", RETRO, "Max Performance",
        "Fastest sensible build before Win95 stops cooperating.",
        [("CPU", "Pentium II 400 or Pentium III 450 (Katmai)"),
         ("Chipset", "Intel 440BX"),
         ("RAM", "128-256 MB SDRAM"),
         ("GPU", "3dfx Voodoo2 (Glide) plus Matrox G200 for 2D"),
         ("Sound", "Sound Blaster AWE64 (ISA) plus wavetable header"),
         ("Storage", "CF-to-IDE or small IDE drive, FAT32, under 32 GB")],
        ["Voodoo2 drivers are very stable here. Glide games look best.",
         "Newer NVIDIA/ATI drivers mostly stop at Win98. Stick to 3dfx/Matrox.",
         "Disable CPU features the OS cannot use if you see random freezes."],
    ),
    Config(
        "Windows 98 SE", RETRO, "Budget",
        "Easy, forgiving 98 box. Good for most late 90s games.",
        [("CPU", "Pentium III 600-800 MHz or Celeron equivalent"),
         ("Chipset", "Intel 440BX or i815"),
         ("RAM", "256 MB"),
         ("GPU", "GeForce2 MX or Voodoo3 3000 (AGP)"),
         ("Sound", "Sound Blaster Live! or onboard AC'97"),
         ("Storage", "20-40 GB IDE or CF adapter, FAT32")],
        ["Install chipset INF first, then AGP/VGART, then graphics driver.",
         "Unofficial Service Pack fixes many USB and storage quirks.",
         "AC'97 onboard works but gives poor DOS sound. Add a Live! if needed."],
    ),
    Config(
        "Windows 98 SE", RETRO, "Max Performance",
        "The ceiling for 98 SE: fast, but needs a few memory tweaks.",
        [("CPU", "Pentium III 1.0-1.13 GHz or Tualatin 1.4 GHz"),
         ("Chipset", "Intel 440BX (Tualatin adapter), i815EP or VIA Apollo Pro 133A"),
         ("RAM", "256-512 MB (never over 512 MB without limiting)"),
         ("GPU", "GeForce4 Ti 4200/4600 or FX 5900 (AGP); Voodoo5 5500 for Glide"),
         ("Sound", "Sound Blaster Live! (EMU10K1) or Audigy"),
         ("Storage", "IDE/SATA-to-IDE bridge, keep disk under 137 GB without a patch")],
        ["Over 512 MB RAM can cause 'insufficient memory' errors. Set MaxFileCache.",
         "Last NVIDIA Win9x driver family is 81.98. Check release notes for your card.",
         "Large disks need the 48-bit LBA patch (ESDI_506.PDR) past 137 GB."],
    ),
    Config(
        "Windows XP", LEGACY, "Budget",
        "Cheap, reliable XP gaming and office machine.",
        [("CPU", "Athlon 64 3200+ or Pentium 4 3.0 GHz"),
         ("Chipset", "Intel i865/i915 or NVIDIA nForce4"),
         ("RAM", "1-2 GB DDR"),
         ("GPU", "GeForce 6600 GT or 7600 GT"),
         ("Sound", "Onboard AC'97 or Audigy SE"),
         ("Storage", "80-250 GB SATA or PATA, IDE mode")],
        ["Set SATA to IDE/compatible mode, or load the AHCI driver with F6.",
         "SP3 recommended. 32-bit XP uses about 3.2 GB of RAM.",
         "Realtek AC'97 drivers are stable. HD Audio needs the Microsoft UAA package."],
    ),
    Config(
        "Windows XP", LEGACY, "Max Performance",
        "Peak XP: fast Core 2 era machine with solid driver support.",
        [("CPU", "Core 2 Quad Q9650 or Core 2 Duo E8600"),
         ("Chipset", "Intel P45 / X38 (ICH10), IDE or slipstreamed AHCI"),
         ("RAM", "4 GB DDR2/DDR3 (about 3.2 GB usable in 32-bit)"),
         ("GPU", "GeForce 8800 GTX, GTX 260 or GTX 460-era"),
         ("Sound", "Creative X-Fi Titanium or Audigy 2 ZS"),
         ("Storage", "SATA SSD, aligned partition")],
        ["Final NVIDIA XP driver is 342.01 (up to roughly GTX 700-series).",
         "XP has no TRIM. Leave free space on the SSD.",
         "Slipstream SATA/AHCI drivers with nLite, or use IDE mode in BIOS.",
         "XP x64 can use more RAM but has weaker driver support."],
    ),
    Config(
        "Windows 7", LEGACY, "Budget",
        "Stable and low-fuss. Best on Intel 8/9-series boards.",
        [("CPU", "Core i5-4590 (Haswell)"),
         ("Chipset", "Intel H81 / B85 / H97"),
         ("RAM", "8 GB DDR3"),
         ("GPU", "GTX 1050 Ti or RX 580"),
         ("Sound", "Onboard Realtek HD Audio"),
         ("Storage", "SATA SSD 240-500 GB")],
        ["USB 3.0 may need drivers added to the installer (no native xHCI).",
         "Install SHA-2 update rollups before Windows Update will work.",
         "NVIDIA R470 branch is the last Win7 driver family."],
    ),
    Config(
        "Windows 7", LEGACY, "Max Performance",
        "The most capable hardware Win7 still treats well.",
        [("CPU", "Core i7-4790K (Haswell) or i7-6700K (Skylake, needs USB drivers)"),
         ("Chipset", "Intel Z97 (easiest) or Z170 with injected drivers"),
         ("RAM", "16-32 GB DDR3 or DDR4"),
         ("GPU", "GTX 1080 Ti or RTX 20-series (final NVIDIA branch)"),
         ("Sound", "Realtek onboard or Sound Blaster Z"),
         ("Storage", "SATA SSD; NVMe only with hotfixes")],
        ["NVMe boot needs KB2990941 and KB3087873 slipstreamed.",
         "100-series and newer boards lack native Win7 USB. Inject drivers.",
         "Newer CPUs (Kaby Lake and later) are not officially supported."],
    ),
    Config(
        "Windows 10", MODERN, "Budget",
        "Solid everyday and light gaming build with wide driver support.",
        [("CPU", "Ryzen 5 5600 or Core i5-12400"),
         ("Chipset", "AMD B550 or Intel B660"),
         ("RAM", "16 GB DDR4-3200"),
         ("GPU", "RTX 3060 or RX 6600"),
         ("Sound", "Onboard Realtek"),
         ("Storage", "500 GB-1 TB NVMe")],
        ["Mainstream security updates ended October 2025. Check extended update status.",
         "Easiest option for older hardware that fails Windows 11 checks."],
    ),
    Config(
        "Windows 10", MODERN, "Max Performance",
        "Workstation, gaming and virtualization with passthrough support.",
        [("CPU", "Ryzen 9 5950X or Core i9-12900K"),
         ("Chipset", "AMD X570 or Intel Z690"),
         ("RAM", "64 GB DDR4 (ECC on Ryzen Pro / Xeon platforms)"),
         ("GPU", "RTX 4070-4080 class or Radeon RX 7900 class"),
         ("Sound", "Onboard or USB DAC"),
         ("Storage", "2 TB NVMe Gen4 plus bulk SATA")],
        ["Enable VT-x/VT-d or AMD-V/IOMMU in BIOS for virtual machines.",
         "Hyper-V and WSL2 work well. Check IOMMU groups for GPU passthrough."],
    ),
    Config(
        "Windows 11", MODERN, "Budget",
        "Meets requirements cleanly, with long driver support ahead.",
        [("CPU", "Ryzen 5 7600 or Core i5-13400"),
         ("Chipset", "AMD B650 or Intel B760"),
         ("RAM", "16 GB DDR5"),
         ("GPU", "RX 7600 or RTX 4060"),
         ("Sound", "Onboard Realtek"),
         ("Storage", "1 TB NVMe")],
        ["Needs TPM 2.0 (firmware TPM is fine), Secure Boot and UEFI.",
         "Official CPU support starts around Intel 8th gen and Ryzen 2000."],
    ),
    Config(
        "Windows 11", MODERN, "Max Performance",
        "Top-end workstation, gaming and virtualization.",
        [("CPU", "Ryzen 9 9950X or Core Ultra 9"),
         ("Chipset", "AMD X870E or Intel Z890"),
         ("RAM", "64-128 GB DDR5 (ECC on workstation platforms)"),
         ("GPU", "RTX 4090 / 50-series or Radeon RX 7900 XTX"),
         ("Sound", "Onboard or external DAC"),
         ("Storage", "2-4 TB NVMe Gen4/Gen5")],
        ["Keep virtualization-based security on unless a VM tool conflicts.",
         "Update chipset and firmware first. Newer CPUs depend on current drivers."],
    ),
]

CONFIGS += [
    # ---- Windows 1.0 ----
    Config(
        "Windows 1.0", RETRO, "Budget",
        "Original 1985 setup. Tiled windows on top of MS-DOS.",
        [("CPU", "Intel 8088 at 4.77 MHz (IBM PC/XT or compatible)"),
         ("Chipset", "Original PC/XT bus"),
         ("RAM", "256 KB"),
         ("GPU", "CGA, EGA or Hercules"),
         ("Sound", "PC speaker only"),
         ("Storage", "Two 360 KB floppy drives, MS-DOS 2.0 or later")],
        ["A mouse is strongly recommended (serial or bus mouse).",
         "Emulators like PCem, 86Box and DOSBox-X are the smoothest way to run it."],
    ),
    Config(
        "Windows 1.0", RETRO, "Max Performance",
        "Best the original Windows can use.",
        [("CPU", "Intel 80286 at 8-12 MHz (IBM PC/AT class)"),
         ("Chipset", "AT-class bus"),
         ("RAM", "640 KB plus expanded memory (EMS)"),
         ("GPU", "EGA"),
         ("Sound", "PC speaker only"),
         ("Storage", "20 MB hard disk plus a floppy drive")],
        ["Windows 1.0 can use EMS memory for extra room.",
         "Use release 1.03 or later for better keyboard and language support."],
    ),
    # ---- Windows 2.x ----
    Config(
        "Windows 2.x (2.03 / 2.11)", RETRO, "Budget",
        "First version with overlapping windows.",
        [("CPU", "8086 or 8088"),
         ("Chipset", "PC/XT class"),
         ("RAM", "512 KB"),
         ("GPU", "EGA or VGA"),
         ("Sound", "PC speaker only"),
         ("Storage", "20 MB hard disk, MS-DOS 3.x")],
        ["Version 2.03 and later support overlapping windows.",
         "No native sound card support."],
    ),
    Config(
        "Windows 2.x (2.03 / 2.11)", RETRO, "Max Performance",
        "Windows/386 2.11 multitasks DOS programs.",
        [("CPU", "386DX at 16-25 MHz (Windows/386)"),
         ("Chipset", "386 AT class"),
         ("RAM", "2-4 MB"),
         ("GPU", "VGA"),
         ("Sound", "PC speaker only"),
         ("Storage", "40 MB hard disk")],
        ["Windows/286 uses the high memory area on a 286.",
         "Windows/386 runs DOS programs in virtual 8086 mode."],
    ),
    # ---- Windows 3.0 ----
    Config(
        "Windows 3.0", RETRO, "Budget",
        "Where Windows became popular.",
        [("CPU", "286 at 12 MHz or 386SX-16"),
         ("Chipset", "AT class"),
         ("RAM", "2 MB"),
         ("GPU", "VGA"),
         ("Sound", "PC speaker"),
         ("Storage", "40 MB IDE, MS-DOS 5.0")],
        ["Standard mode on 286, 386 Enhanced mode on 386 and newer.",
         "Windows 3.1 is usually the better choice."],
    ),
    Config(
        "Windows 3.0", RETRO, "Max Performance",
        "Fast 386/486 with sound via Multimedia Extensions.",
        [("CPU", "386DX-33 or 486"),
         ("Chipset", "VLB or ISA board"),
         ("RAM", "8 MB"),
         ("GPU", "SVGA such as Tseng ET4000"),
         ("Sound", "AdLib or Sound Blaster with Multimedia Extensions 1.0"),
         ("Storage", "120 MB IDE")],
        ["Sound needs the Multimedia Extensions add-on.",
         "Use a 3.0a build for better stability."],
    ),
    # ---- Windows 3.1 ----
    Config(
        "Windows 3.1", RETRO, "Budget",
        "Reliable and light. Good for DOS-era work.",
        [("CPU", "386SX-25"),
         ("Chipset", "ISA board"),
         ("RAM", "4 MB"),
         ("GPU", "VGA"),
         ("Sound", "AdLib or Sound Blaster Pro"),
         ("Storage", "80 MB IDE, MS-DOS 6.22")],
        ["Needs MS-DOS underneath.",
         "Add Win32s 1.30c to run some 32-bit programs."],
    ),
    Config(
        "Windows 3.1", RETRO, "Max Performance",
        "Best 3.1 machine: fast 486 or early Pentium.",
        [("CPU", "486 DX2-66 or early Pentium"),
         ("Chipset", "VLB or early PCI (Intel 430 series)"),
         ("RAM", "16 MB"),
         ("GPU", "S3 or Tseng SVGA with 3.1 drivers"),
         ("Sound", "Sound Blaster 16 with 3.1 drivers"),
         ("Storage", "IDE disk, under 504 MB (or 2 GB FAT16 with a fixed BIOS)")],
        ["Use 32-bit disk access only if the controller is WD1003 compatible.",
         "Keep partitions small. FAT16 limits apply."],
    ),
    # ---- Windows for Workgroups 3.11 ----
    Config(
        "Windows for Workgroups 3.11", RETRO, "Budget",
        "3.1 plus built-in networking.",
        [("CPU", "386SX-33"),
         ("Chipset", "ISA board"),
         ("RAM", "4 MB"),
         ("GPU", "VGA"),
         ("Sound", "Sound Blaster Pro"),
         ("Storage", "80 MB IDE")],
        ["Add an NE2000-compatible network card for file sharing.",
         "Internet needs the TCP/IP-32 add-on."],
    ),
    Config(
        "Windows for Workgroups 3.11", RETRO, "Max Performance",
        "Most capable 3.x build with 32-bit file access.",
        [("CPU", "486 DX4-100 or Pentium 75"),
         ("Chipset", "Intel 430 series or VLB"),
         ("RAM", "16-32 MB"),
         ("GPU", "S3 SVGA with 3.11 drivers"),
         ("Sound", "Sound Blaster 16"),
         ("Storage", "IDE disk with 32-bit file access (VFAT)")],
        ["32-bit file access (VFAT) is built in and speeds up disks.",
         "3Com 3C509 ISA is a well-supported network card."],
    ),
    # ---- Windows NT 3.1 ----
    Config(
        "Windows NT 3.1", RETRO, "Budget",
        "First NT. Heavy for its time, strict about hardware.",
        [("CPU", "486DX at 33 MHz"),
         ("Chipset", "ISA or EISA board"),
         ("RAM", "16 MB"),
         ("GPU", "VGA or S3 based card"),
         ("Sound", "Sound Blaster (limited driver support)"),
         ("Storage", "90 MB free, IDE or SCSI")],
        ["Check the Microsoft Hardware Compatibility List for each part.",
         "Minimum 12 MB RAM, but 16 MB is far more usable."],
    ),
    Config(
        "Windows NT 3.1", RETRO, "Max Performance",
        "Fastest hardware this release supported.",
        [("CPU", "Pentium 90 or DEC Alpha AXP"),
         ("Chipset", "Intel Neptune/Triton or EISA"),
         ("RAM", "32 MB"),
         ("GPU", "S3 928 or similar"),
         ("Sound", "Sound Blaster 16 (verify driver)"),
         ("Storage", "Adaptec 1542 SCSI with NTFS")],
        ["Runs on x86, MIPS and Alpha.",
         "NTFS and long file names are supported."],
    ),
    # ---- Windows NT 3.5 ----
    Config(
        "Windows NT 3.5", RETRO, "Budget",
        "Faster and lighter than 3.1.",
        [("CPU", "486 DX2-66"),
         ("Chipset", "Intel Saturn or Triton"),
         ("RAM", "16 MB"),
         ("GPU", "S3 805 or 928"),
         ("Sound", "Sound Blaster 16"),
         ("Storage", "IDE disk, 200 MB")],
        ["NT 3.5 is noticeably lighter on memory than 3.1.",
         "Verify each part against the Hardware Compatibility List."],
    ),
    Config(
        "Windows NT 3.5", RETRO, "Max Performance",
        "Solid server-grade setup for 1994.",
        [("CPU", "Pentium 133"),
         ("Chipset", "Intel 430FX or 430HX"),
         ("RAM", "64 MB"),
         ("GPU", "Matrox MGA or S3 Trio64"),
         ("Sound", "Sound Blaster 16"),
         ("Storage", "Adaptec 2940 SCSI")],
        ["PCI support is solid. Prefer SCSI for storage.",
         "SP3 recommended."],
    ),
    # ---- Windows NT 3.51 ----
    Config(
        "Windows NT 3.51", RETRO, "Budget",
        "Last NT with the Program Manager shell.",
        [("CPU", "Pentium 75"),
         ("Chipset", "Intel 430 series"),
         ("RAM", "32 MB"),
         ("GPU", "S3 Trio64 or ATI Mach64"),
         ("Sound", "Sound Blaster 16"),
         ("Storage", "IDE disk, 500 MB")],
        ["Install SP5 for stability.",
         "Uses the Windows 3.x style shell."],
    ),
    Config(
        "Windows NT 3.51", RETRO, "Max Performance",
        "Best NT 3.51 machine.",
        [("CPU", "Pentium 200 or Pentium Pro"),
         ("Chipset", "Intel 440FX"),
         ("RAM", "128 MB"),
         ("GPU", "Matrox Millennium"),
         ("Sound", "Sound Blaster 16"),
         ("Storage", "Adaptec 2940 SCSI")],
        ["Runs on x86, MIPS, Alpha and PowerPC.",
         "SP5 plus the Pentium Pro fixes if you use that CPU."],
    ),
    # ---- Windows NT 4.0 ----
    Config(
        "Windows NT 4.0", RETRO, "Budget",
        "Windows 95 shell on the NT core.",
        [("CPU", "Pentium 133"),
         ("Chipset", "Intel 430HX or VX"),
         ("RAM", "64 MB"),
         ("GPU", "Matrox Millennium or S3 ViRGE"),
         ("Sound", "Sound Blaster 16 or AWE32"),
         ("Storage", "IDE or SCSI, 2 GB")],
        ["Install Service Pack 6a.",
         "No USB and no Plug and Play."],
    ),
    Config(
        "Windows NT 4.0", RETRO, "Max Performance",
        "Fast workstation for 1998-99.",
        [("CPU", "Pentium II 450 or Pentium III 600"),
         ("Chipset", "Intel 440BX"),
         ("RAM", "256-512 MB"),
         ("GPU", "Matrox G200 or G400"),
         ("Sound", "Sound Blaster Live!"),
         ("Storage", "Adaptec 2940 SCSI or IDE")],
        ["Keep the boot partition under about 7.8 GB at install.",
         "DirectX 3 is the officially supported version."],
    ),
    # ---- Windows 98 First Edition ----
    Config(
        "Windows 98 (First Edition)", RETRO, "Budget",
        "Original 98 release. Works, but 98 SE is better.",
        [("CPU", "Pentium 233 MMX"),
         ("Chipset", "Intel 440LX"),
         ("RAM", "64 MB"),
         ("GPU", "Riva 128 or ATI Rage Pro"),
         ("Sound", "Sound Blaster 16"),
         ("Storage", "4-8 GB IDE, FAT32")],
        ["First Edition has USB and internet sharing bugs.",
         "98 SE fixes most of them."],
    ),
    Config(
        "Windows 98 (First Edition)", RETRO, "Max Performance",
        "Best the first release handles well.",
        [("CPU", "Pentium II 450"),
         ("Chipset", "Intel 440BX"),
         ("RAM", "128-256 MB"),
         ("GPU", "Voodoo2 plus Matrox G200"),
         ("Sound", "Sound Blaster Live!"),
         ("Storage", "20 GB IDE, FAT32")],
        ["Install chipset INF first, then video drivers.",
         "Consider upgrading to 98 SE if stability matters."],
    ),
    # ---- Windows 2000 ----
    Config(
        "Windows 2000", RETRO, "Budget",
        "Stable NT 5.0 for office and light games.",
        [("CPU", "Pentium III 600"),
         ("Chipset", "Intel i815"),
         ("RAM", "256 MB"),
         ("GPU", "GeForce2 MX"),
         ("Sound", "Onboard AC'97"),
         ("Storage", "40 GB IDE")],
        ["Install SP4 and Update Rollup 1.",
         "Big drives need 48-bit LBA (SP3 or newer, registry setting)."],
    ),
    Config(
        "Windows 2000", RETRO, "Max Performance",
        "Best-supported Windows 2000 build.",
        [("CPU", "Pentium 4 or Athlon XP 2800+"),
         ("Chipset", "Intel i865 or NVIDIA nForce2"),
         ("RAM", "1 GB"),
         ("GPU", "GeForce4 Ti or FX 5900"),
         ("Sound", "Sound Blaster Live! or Audigy"),
         ("Storage", "SATA in IDE mode, or PATA")],
        ["DirectX 9.0c is the last version for this OS.",
         "Driver support ends around the GeForce 6/7 era. Check vendor archives."],
    ),
    # ---- Windows ME ----
    Config(
        "Windows ME", RETRO, "Budget",
        "Short-lived consumer release. Use carefully.",
        [("CPU", "Pentium II 400 or Celeron 500"),
         ("Chipset", "Intel 440BX or i810"),
         ("RAM", "128 MB"),
         ("GPU", "TNT2 or GeForce2 MX"),
         ("Sound", "Sound Blaster Live!"),
         ("Storage", "20 GB IDE, FAT32")],
        ["No real-mode DOS boot. Old DOS games may need workarounds.",
         "Turn off System Restore if it slows or destabilizes the machine."],
    ),
    Config(
        "Windows ME", RETRO, "Max Performance",
        "Highest practical ME build.",
        [("CPU", "Pentium III 1.0 GHz"),
         ("Chipset", "Intel i815"),
         ("RAM", "256-384 MB (stay under 512 MB)"),
         ("GPU", "GeForce4 MX or Ti"),
         ("Sound", "Sound Blaster Live! or Audigy"),
         ("Storage", "40 GB IDE")],
        ["Over 512 MB RAM can cause errors. Limit with MaxFileCache.",
         "Windows 98 SE is more stable for the same hardware."],
    ),
    # ---- Windows Vista ----
    Config(
        "Windows Vista", LEGACY, "Budget",
        "Works well once SP2 and updates are in.",
        [("CPU", "Core 2 Duo E6300 or Athlon 64 X2"),
         ("Chipset", "Intel G31 or NVIDIA nForce 430"),
         ("RAM", "2 GB DDR2"),
         ("GPU", "GeForce 8500 GT or Radeon HD 2400"),
         ("Sound", "Onboard HD Audio"),
         ("Storage", "160 GB SATA")],
        ["Install SP2 and the Platform Update.",
         "Aero needs a WDDM graphics driver."],
    ),
    Config(
        "Windows Vista", LEGACY, "Max Performance",
        "Best Vista hardware with solid drivers.",
        [("CPU", "Core 2 Quad Q9550"),
         ("Chipset", "Intel P45"),
         ("RAM", "4-8 GB DDR2/DDR3 (64-bit edition)"),
         ("GPU", "GeForce 8800 GTX or GTX 280"),
         ("Sound", "Creative X-Fi or onboard HD Audio"),
         ("Storage", "SATA SSD")],
        ["Use 64-bit Vista if you want more than 4 GB.",
         "Support ended April 2017. Use only offline or for retro purposes."],
    ),
    # ---- Windows 8 ----
    Config(
        "Windows 8", LEGACY, "Budget",
        "Fast boot with native USB 3.0.",
        [("CPU", "Core i3-3220"),
         ("Chipset", "Intel H61 or B75"),
         ("RAM", "4-8 GB DDR3"),
         ("GPU", "GeForce GTX 650"),
         ("Sound", "Onboard HD Audio"),
         ("Storage", "SATA SSD")],
        ["USB 3.0 works without extra drivers.",
         "Windows 8 support ended January 2016. Upgrade to 8.1 if you can."],
    ),
    Config(
        "Windows 8", LEGACY, "Max Performance",
        "Top Ivy Bridge setup.",
        [("CPU", "Core i7-3770K"),
         ("Chipset", "Intel Z77"),
         ("RAM", "16 GB DDR3"),
         ("GPU", "GTX 780 or GTX 970"),
         ("Sound", "Realtek onboard"),
         ("Storage", "SATA SSD")],
        ["UEFI and Secure Boot supported.",
         "No Start button until 8.1."],
    ),
    # ---- Windows 8.1 ----
    Config(
        "Windows 8.1", LEGACY, "Budget",
        "Polished Windows 8 with better stability.",
        [("CPU", "Core i5-4590"),
         ("Chipset", "Intel H81 or B85"),
         ("RAM", "8 GB DDR3"),
         ("GPU", "GTX 1050 Ti"),
         ("Sound", "Onboard Realtek"),
         ("Storage", "SATA SSD")],
        ["Extended support ended January 2023.",
         "NVIDIA R470 branch is the last driver family."],
    ),
    Config(
        "Windows 8.1", LEGACY, "Max Performance",
        "Highest practical 8.1 build.",
        [("CPU", "Core i7-4790K"),
         ("Chipset", "Intel Z97"),
         ("RAM", "16-32 GB DDR3"),
         ("GPU", "GTX 1080 Ti"),
         ("Sound", "Realtek onboard or Sound Blaster Z"),
         ("Storage", "SATA SSD, or NVMe with hotfix KB2990941")],
        ["NVMe boot needs the hotfix.",
         "Newer CPUs lack official driver support."],
    ),
]

VERSIONS = [
    "Windows 1.0", "Windows 2.x (2.03 / 2.11)", "Windows 3.0", "Windows 3.1",
    "Windows for Workgroups 3.11", "Windows NT 3.1", "Windows NT 3.5",
    "Windows NT 3.51", "Windows 95 (OSR2)", "Windows NT 4.0",
    "Windows 98 (First Edition)", "Windows 98 SE", "Windows 2000", "Windows ME",
    "Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 8.1",
    "Windows 10", "Windows 11",
]
# Chronological order; sort is stable so Budget stays before Max Performance.
CONFIGS.sort(key=lambda c: VERSIONS.index(c.os))

THEMES = {
    "dark": dict(bg="#202020", side="#272727", card="#2d2d2d", border="#3d3d3d",
                 text="#f3f3f3", sub="#b5b5b5", accent="#60cdff",
                 accent_text="#000000", hover="#383838"),
    "light": dict(bg="#f3f3f3", side="#ebebeb", card="#ffffff", border="#e0e0e0",
                  text="#1a1a1a", sub="#5c5c5c", accent="#0067c0",
                  accent_text="#ffffff", hover="#e1e1e1"),
}


def build_qss(t):
    return f"""
    QWidget {{ color:{t['text']}; font-family:'Segoe UI Variable','Segoe UI',sans-serif; font-size:10.5pt; }}
    QMainWindow, QWidget#root, QWidget#viewport, QWidget#page {{ background:{t['bg']}; }}
    QScrollArea {{ border:none; background:{t['bg']}; }}
    QFrame#sidebar {{ background:{t['side']}; border-right:1px solid {t['border']}; }}
    QFrame#card {{ background:{t['card']}; border:1px solid {t['border']}; border-radius:10px; }}
    QLabel {{ background:transparent; }}
    QLabel#title {{ font-size:15pt; font-weight:600; }}
    QLabel#heading {{ font-size:10pt; font-weight:600; color:{t['sub']}; padding:8px 4px 2px 4px; }}
    QLabel#sub {{ color:{t['sub']}; }}
    QLabel#badge {{ background:{t['accent']}; color:{t['accent_text']};
                    border-radius:9px; padding:2px 10px; font-size:9pt; }}
    QLabel#badge2 {{ background:{t['hover']}; color:{t['text']};
                     border-radius:9px; padding:2px 10px; font-size:9pt; }}
    QPushButton {{ background:transparent; border:none; padding:8px 12px; border-radius:6px; text-align:left; }}
    QPushButton:hover {{ background:{t['hover']}; }}
    QPushButton:checked {{ background:{t['hover']}; font-weight:600; border-left:3px solid {t['accent']}; }}
    QPushButton#notes {{ color:{t['accent']}; padding:4px 0px; }}
    QPushButton#notes:hover {{ background:transparent; text-decoration:underline; }}
    QPushButton#notes:checked {{ background:transparent; border:none; font-weight:normal; }}
    QPushButton#theme {{ border:1px solid {t['border']}; text-align:center; }}
    QComboBox {{ background:{t['card']}; border:1px solid {t['border']}; border-radius:6px; padding:6px 10px; }}
    QComboBox:hover {{ background:{t['hover']}; }}
    QComboBox::drop-down {{ border:none; width:24px; }}
    QComboBox QAbstractItemView {{ background:{t['card']}; color:{t['text']}; border:1px solid {t['border']};
                                   selection-background-color:{t['accent']}; selection-color:{t['accent_text']}; outline:none; }}
    QScrollBar:vertical {{ width:10px; background:transparent; margin:2px; }}
    QScrollBar::handle:vertical {{ background:{t['border']}; border-radius:4px; min-height:30px; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0px; }}
    """


class Card(QFrame):
    def __init__(self, cfg):
        super().__init__()
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(10)

        head = QHBoxLayout()
        title = QLabel(cfg.os)
        title.setObjectName("title")
        head.addWidget(title)
        head.addStretch()
        b1 = QLabel(cfg.tier)
        b1.setObjectName("badge")
        b2 = QLabel(cfg.use_case.split(" (")[0])
        b2.setObjectName("badge2")
        head.addWidget(b1)
        head.addWidget(b2)
        lay.addLayout(head)

        summary = QLabel(cfg.summary)
        summary.setObjectName("sub")
        summary.setWordWrap(True)
        lay.addWidget(summary)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(6)
        grid.setColumnStretch(1, 1)
        for i, (k, v) in enumerate(cfg.parts):
            key = QLabel(k)
            key.setObjectName("sub")
            key.setMinimumWidth(80)
            val = QLabel(v)
            val.setWordWrap(True)
            grid.addWidget(key, i, 0, Qt.AlignmentFlag.AlignTop)
            grid.addWidget(val, i, 1)
        lay.addLayout(grid)

        self.notes_label = QLabel("\n".join("\u2022 " + n for n in cfg.notes))
        self.notes_label.setWordWrap(True)
        self.notes_label.setObjectName("sub")
        self.notes_label.setVisible(False)
        btn = QPushButton("Show driver notes")
        btn.setObjectName("notes")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        def toggle(on):
            self.notes_label.setVisible(on)
            btn.setText("Hide driver notes" if on else "Show driver notes")

        btn.toggled.connect(toggle)
        lay.addWidget(btn, 0, Qt.AlignmentFlag.AlignLeft)
        lay.addWidget(self.notes_label)


class MainWindow(QMainWindow):
    def __init__(self, theme="dark"):
        super().__init__()
        self.setWindowTitle("Windows Hardware Compatibility Guide")
        self.resize(1100, 740)
        self.setMinimumSize(820, 520)
        self.theme = theme
        self.use_filter = "All"
        self.tier_filter = "All"
        self.os_filter = "All versions"
        self.cards = []

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Sidebar
        side = QFrame()
        side.setObjectName("sidebar")
        side.setFixedWidth(270)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(12, 16, 12, 16)
        sl.setSpacing(2)
        sl.addWidget(self._heading("Use case"))
        self._add_group(sl, USE_CASES, self._set_use)
        sl.addSpacing(8)
        sl.addWidget(self._heading("Tier"))
        self._add_group(sl, TIERS, self._set_tier)
        sl.addSpacing(8)
        sl.addWidget(self._heading("Windows version"))
        self.os_combo = QComboBox()
        self.os_combo.addItems(["All versions"] + VERSIONS)
        self.os_combo.setMaxVisibleItems(12)
        self.os_combo.currentTextChanged.connect(self._set_os)
        sl.addWidget(self.os_combo)
        sl.addStretch()
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        sl.addWidget(self.theme_btn)
        outer.addWidget(side)

        # Content
        right = QVBoxLayout()
        right.setContentsMargins(28, 20, 28, 12)
        right.setSpacing(8)
        self.count_label = QLabel()
        self.count_label.setObjectName("sub")
        right.addWidget(self.count_label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.viewport().setObjectName("viewport")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.page_layout = QVBoxLayout(self.page)
        self.page_layout.setContentsMargins(0, 0, 8, 12)
        self.page_layout.setSpacing(14)
        self.scroll.setWidget(self.page)
        right.addWidget(self.scroll, 1)

        foot = QLabel("Examples of well-supported hardware, not strict requirements. "
                      "Check driver release notes for your exact parts.")
        foot.setObjectName("sub")
        foot.setWordWrap(True)
        right.addWidget(foot)
        outer.addLayout(right, 1)

        self.apply_theme()
        self.apply_filters()

    def _heading(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("heading")
        return lbl

    def _add_group(self, layout, options, callback):
        group = QButtonGroup(self)
        group.setExclusive(True)
        for i, opt in enumerate(options):
            b = QPushButton(opt)
            b.setCheckable(True)
            b.setChecked(i == 0)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _=False, o=opt: callback(o))
            group.addButton(b)
            layout.addWidget(b)
        if not hasattr(self, "_groups"):
            self._groups = []
        self._groups.append(group)

    def _set_use(self, value):
        self.use_filter = value
        self.apply_filters()

    def _set_tier(self, value):
        self.tier_filter = value
        self.apply_filters()

    def _set_os(self, value):
        self.os_filter = value
        self.apply_filters()

    def apply_filters(self):
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.cards = []
        for cfg in CONFIGS:
            if self.os_filter != "All versions" and cfg.os != self.os_filter:
                continue
            if self.use_filter != "All" and cfg.use_case != self.use_filter:
                continue
            if self.tier_filter != "All" and cfg.tier != self.tier_filter:
                continue
            card = Card(cfg)
            self.cards.append(card)
            self.page_layout.addWidget(card)
        self.page_layout.addStretch()
        self.count_label.setText(f"Showing {len(self.cards)} of {len(CONFIGS)}")

    def apply_theme(self):
        QApplication.instance().setStyleSheet(build_qss(THEMES[self.theme]))
        self.theme_btn.setText("Switch to light" if self.theme == "dark" else "Switch to dark")

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()


def system_theme():
    try:
        scheme = QGuiApplication.styleHints().colorScheme()
        return "dark" if scheme == Qt.ColorScheme.Dark else "light"
    except Exception:
        return "dark"


def self_test():
    """Build the window offscreen and return (cards_shown, total)."""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow(system_theme())
    return len(win.cards), len(CONFIGS)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow(system_theme())
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
