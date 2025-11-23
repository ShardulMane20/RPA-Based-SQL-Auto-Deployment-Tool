"""
Production Build Script for Zanvar SQL Tool
Final Release Version - with Release Notes Display
"""

import os
import sys
import shutil
import subprocess
import datetime
from pathlib import Path

# ============================================================================
# PROJECT CONFIGURATION
# ============================================================================
PROJECT_NAME = "Zanvar SQL Application"
COMPANY_NAME = "Shardul Mane & Team"
VERSION = "1.2.4"
RELEASE_TYPE = "Production"
SOURCE_FILE = "main.py"
ICON_FILE = "assets/logo.ico"

# Build directories
BUILD_DIR = "build"
DIST_DIR = "dist"
RELEASE_DIR = "release"

# Inno Setup path (customize if needed)
ISCC_PATH = r"D:\Softwears\Inno Setup\Inno Setup 6\ISCC.exe"

# ============================================================================
# PRE-BUILD VALIDATION
# ============================================================================
def validate_environment():
    """Validate build environment and dependencies"""
    print("=" * 80)
    print("VALIDATING BUILD ENVIRONMENT")
    print("=" * 80)
    
    # Check if main.py exists
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ ERROR: {SOURCE_FILE} not found!")
        sys.exit(1)
    print(f"✓ Source file found: {SOURCE_FILE}")
    
    # Check if assets directory exists
    if not os.path.exists("assets"):
        print("❌ ERROR: assets directory not found!")
        sys.exit(1)
    print("✓ Assets directory found")
    
    # Check if icon exists
    if not os.path.exists(ICON_FILE):
        print(f"⚠ WARNING: Icon file not found: {ICON_FILE}")
        print("  Continuing without icon...")
    else:
        print(f"✓ Icon file found: {ICON_FILE}")
    
    # Check for PyInstaller
    try:
        subprocess.run(["pyinstaller", "--version"], 
                      capture_output=True, check=True)
        print("✓ PyInstaller is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERROR: PyInstaller not found!")
        print("  Install it with: pip install pyinstaller")
        sys.exit(1)
    
    # Check for Inno Setup - Try PATH first, then custom path
    iscc_found = False
    iscc_command = None
    
    try:
        result = subprocess.run(["ISCC", "/?"], 
                      capture_output=True, check=False)
        if result.returncode == 0 or result.returncode == 1:  # ISCC returns 1 for /? flag
            print("✓ Inno Setup is installed (found in PATH)")
            iscc_found = True
            iscc_command = "ISCC"
    except FileNotFoundError:
        pass
    
    # Try custom path if not found in PATH
    if not iscc_found and os.path.exists(ISCC_PATH):
        try:
            result = subprocess.run([ISCC_PATH, "/?"], 
                          capture_output=True, check=False)
            if result.returncode == 0 or result.returncode == 1:  # ISCC returns 1 for /? flag
                print(f"✓ Inno Setup found at: {ISCC_PATH}")
                iscc_found = True
                iscc_command = ISCC_PATH
        except Exception as e:
            print(f"  Debug: Error running ISCC: {e}")
    
    if not iscc_found:
        print("❌ ERROR: Inno Setup Compiler (ISCC) not found!")
        print("  Install Inno Setup from: https://jrsoftware.org/isinfo.php")
        print(f"  Or update ISCC_PATH in this script to point to ISCC.exe")
        print(f"  Current ISCC_PATH: {ISCC_PATH}")
        if os.path.exists(ISCC_PATH):
            print(f"  Note: File exists but cannot be executed")
        sys.exit(1)
    
    print()
    return iscc_command

# ============================================================================
# CLEAN PREVIOUS BUILDS
# ============================================================================
def clean_previous_builds():
    """Remove previous build artifacts"""
    print("=" * 80)
    print("CLEANING PREVIOUS BUILDS")
    print("=" * 80)
    
    dirs_to_clean = [BUILD_DIR, DIST_DIR, "__pycache__"]
    files_to_clean = ["*.spec", "installer.iss"]
    
    for directory in dirs_to_clean:
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
            print(f"✓ Cleaned: {directory}/")
    
    for pattern in files_to_clean:
        for file in Path(".").glob(pattern):
            try:
                os.remove(file)
                print(f"✓ Removed: {file}")
            except Exception as e:
                print(f"⚠ Could not remove {file}: {e}")
    
    print()

# ============================================================================
# BUILD EXECUTABLE
# ============================================================================
def build_executable():
    """Build executable using PyInstaller"""
    print("=" * 80)
    print("BUILDING EXECUTABLE")
    print("=" * 80)
    
    # Prepare PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",  # No console window
        f"--name={PROJECT_NAME}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        "--clean",
        "--noconfirm",
        
        # Add icon if available
        *([f"--icon={ICON_FILE}"] if os.path.exists(ICON_FILE) else []),
        
        # Include data files
        f"--add-data=assets{os.pathsep}assets",
        
        # Hidden imports
        "--hidden-import=pyodbc",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        
        # Optimize
        "--optimize=2",
        
        # Entry point
        SOURCE_FILE
    ]
    
    print("Running PyInstaller...")
    print(f"Command: {' '.join(pyinstaller_cmd)}")
    print()
    
    try:
        result = subprocess.run(pyinstaller_cmd, check=True, 
                              capture_output=False, text=True)
        print()
        print("✓ Executable built successfully!")
        
        # Verify executable exists
        exe_path = os.path.join(DIST_DIR, f"{PROJECT_NAME}.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"  Location: {exe_path}")
            print(f"  Size: {size_mb:.2f} MB")
        else:
            print("❌ ERROR: Executable not found after build!")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: PyInstaller failed!")
        print(f"  {e}")
        sys.exit(1)
    
    print()

# ============================================================================
# CREATE DOCUMENTATION PACKAGE
# ============================================================================
def create_release_notes_file():
    """Create release notes file that will be shown during installation"""
    
    print("CREATING RELEASE NOTES")
    
    # Create release directory if it doesn't exist
    os.makedirs(RELEASE_DIR, exist_ok=True)
    
    # Create release notes in RTF format for better formatting in Inno Setup
    release_notes_txt = f"""{'' * 80}
{PROJECT_NAME} - Version {VERSION}
{COMPANY_NAME}
Release Date: {datetime.datetime.now().strftime("%B %d, %Y")}
{'' * 80}

WHAT'S NEW IN VERSION {VERSION}

  ✓ Enhanced query execution performance
  ✓ Improved database connection stability
  ✓ Modern user interface updates
  ✓ Bug fixes and optimizations

INSTALLATION INSTRUCTIONS

  1. Follow the installation wizard steps
  2. Choose installation directory
  3. Select additional shortcuts (optional)
  4. Complete the installation

SYSTEM REQUIREMENTS

  • Operating System: Windows 10/11 (64-bit)
  • RAM: Minimum 4GB
  • Disk Space: 100MB free space
  • Database: Microsoft SQL Server (any version)

KEY FEATURES

  ✓ Connect to SQL Server instances
  ✓ Execute queries across multiple databases
  ✓ View formatted query results
  ✓ Export results to log files
  ✓ Query history management
  ✓ Modern, intuitive user interface

FIRST TIME SETUP

  1. Launch {PROJECT_NAME} after installation
  2. Enter your SQL Server connection details:
     - Server name (e.g., localhost\\SQLEXPRESS)
     - Username (SQL Server authentication)
     - Password
  3. Click "Connect"
  4. Select databases and start querying

IMPORTANT NOTES

  • Administrator privileges may be required for installation
  • Ensure SQL Server is accessible before running the application
  • Your connection credentials are stored locally and securely

SUPPORT & CONTACT

  For technical support or questions:
  
  Website: https://www.zanvargroup.com
  Email: shardulmane369@gmail.com
  

{'' * 80}

Thank you for choosing {PROJECT_NAME}!

{'' * 80}
"""
    
    # Save as TXT file for the installer
    notes_txt_path = os.path.join(RELEASE_DIR, "RELEASE_NOTES.txt")
    with open(notes_txt_path, "w", encoding="utf-8") as f:
        f.write(release_notes_txt)
    
    print(f"✓ Release notes created: {notes_txt_path}")
    print()
    
    return notes_txt_path

# ============================================================================
# CREATE INSTALLER
# ============================================================================
def create_installer(iscc_command, release_notes_path):
    """Create Windows installer using Inno Setup"""
    print("=" * 80)
    print("CREATING INSTALLER")
    print("=" * 80)
    
    build_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Create Inno Setup script with InfoBefore page to show release notes
    inno_script = f'''
; Zanvar SQL Tool Installer Script
; Generated on {build_date}

[Setup]
; Application Information
AppName={PROJECT_NAME}
AppVersion={VERSION}
AppPublisher={COMPANY_NAME}
AppCopyright=Copyright (C) {datetime.datetime.now().year} {COMPANY_NAME}
AppContact=shardulmane369@gmail.com
AppSupportURL=shardulmane369@gmail.com

; Installation Directories
DefaultDirName={{autopf}}\\{PROJECT_NAME}
DefaultGroupName={PROJECT_NAME}
DisableProgramGroupPage=yes

; Output Configuration
OutputDir={RELEASE_DIR}
OutputBaseFilename={PROJECT_NAME.replace(" ", "_")}_v{VERSION}_Setup
SetupIconFile={ICON_FILE if os.path.exists(ICON_FILE) else ""}

; Compression
Compression=lzma2/max
SolidCompression=yes
LZMAUseSeparateProcess=yes

; Architecture
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Visual Appearance
WizardStyle=modern

; Show release notes before installation
InfoBeforeFile={release_notes_path}

; Miscellaneous
DisableWelcomePage=no
DisableReadyPage=no
DisableDirPage=no
ShowLanguageDialog=auto
AppendDefaultDirName=yes
UsePreviousAppDir=yes

; Uninstallation
UninstallDisplayIcon={{app}}\\{PROJECT_NAME}.exe
UninstallDisplayName={PROJECT_NAME}
CreateUninstallRegKey=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"
Name: "quicklaunchicon"; Description: "Create a &Quick Launch shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
; Main executable
Source: "{os.path.join(DIST_DIR, PROJECT_NAME + '.exe')}"; DestDir: "{{app}}"; Flags: ignoreversion

; Assets directory
Source: "assets\\*"; DestDir: "{{app}}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; Release notes
Source: "{release_notes_path}"; DestDir: "{{app}}"; Flags: ignoreversion

; Documentation (if exists)
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "LICENSE"; DestDir: "{{app}}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
; Start Menu shortcuts
Name: "{{group}}\\{PROJECT_NAME}"; Filename: "{{app}}\\{PROJECT_NAME}.exe"; Comment: "Launch {PROJECT_NAME}"
Name: "{{group}}\\Release Notes"; Filename: "{{app}}\\RELEASE_NOTES.txt"; Comment: "View Release Notes"
Name: "{{group}}\\Uninstall {PROJECT_NAME}"; Filename: "{{uninstallexe}}"

; Desktop shortcut
Name: "{{userdesktop}}\\{PROJECT_NAME}"; Filename: "{{app}}\\{PROJECT_NAME}.exe"; Tasks: desktopicon; Comment: "Launch {PROJECT_NAME}"

; Quick Launch shortcut
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{PROJECT_NAME}"; Filename: "{{app}}\\{PROJECT_NAME}.exe"; Tasks: quicklaunchicon

[Run]
; Option to launch after installation
Filename: "{{app}}\\{PROJECT_NAME}.exe"; Description: "Launch {PROJECT_NAME}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up on uninstall
Type: files; Name: "{{app}}\\query_history.pkl"
Type: filesandordirs; Name: "{{app}}\\assets"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Welcome to {PROJECT_NAME} Setup!' + #13#10#13#10 +
         'This wizard will guide you through the installation of {PROJECT_NAME} version {VERSION}.' + #13#10#13#10 +
         'Click Next to continue.', mbInformation, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Installation completed successfully!' + #13#10#13#10 +
           '{PROJECT_NAME} has been installed on your computer.' + #13#10#13#10 +
           'Click Finish to exit Setup.', mbInformation, MB_OK);
  end;
end;
'''
    
    # Write Inno Setup script
    script_path = "installer.iss"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(inno_script)
    
    print(f"✓ Inno Setup script created: {script_path}")
    print()
    
    # Compile installer
    print("Compiling installer...")
    try:
        subprocess.run([iscc_command, script_path], check=True)
        print()
        print("✓ Installer created successfully!")
        
        # Find and display installer info
        installer_name = f"{PROJECT_NAME.replace(' ', '_')}_v{VERSION}_Setup.exe"
        installer_path = os.path.join(RELEASE_DIR, installer_name)
        
        if os.path.exists(installer_path):
            size_mb = os.path.getsize(installer_path) / (1024 * 1024)
            print(f"  Location: {installer_path}")
            print(f"  Size: {size_mb:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Inno Setup compilation failed!")
        print(f"  {e}")
        sys.exit(1)
    
    print()

# ============================================================================
# FINAL CLEANUP AND SUMMARY
# ============================================================================
def final_cleanup():
    """Clean up temporary files and show summary"""
    print("=" * 80)
    print("FINAL CLEANUP")
    print("=" * 80)
    
    # Remove temporary files
    temp_files = ["installer.iss"]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"✓ Removed: {temp_file}")
    
    # Remove .spec file
    spec_file = f"{PROJECT_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"✓ Removed: {spec_file}")
    
    print()

def show_summary():
    """Display build summary"""
    print("=" * 80)
    print("BUILD SUMMARY")
    print("=" * 80)
    print()
    print(f"Project: {PROJECT_NAME}")
    print(f"Version: {VERSION}")
    print(f"Release Type: {RELEASE_TYPE}")
    print(f"Build Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Build Artifacts:")
    print(f"  📦 Executable: {DIST_DIR}/{PROJECT_NAME}.exe")
    print(f"  💿 Installer: {RELEASE_DIR}/{PROJECT_NAME.replace(' ', '_')}_v{VERSION}_Setup.exe")
    print(f"  📄 Release Notes: {RELEASE_DIR}/RELEASE_NOTES.txt")
    print()
    print("Features:")
    print("  ✓ Release notes will be displayed during installation")
    print("  ✓ Release notes included in Start Menu shortcuts")
    print("  ✓ Release notes saved in installation directory")
    print()
    print("=" * 80)
    print("✅ BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Test the installer on a clean system")
    print("  2. Verify release notes display correctly during installation")
    print("  3. Verify all features work correctly")
    print("  4. Package all files in release/ folder for delivery")
    print()

# ============================================================================
# MAIN BUILD PROCESS
# ============================================================================
def main():
    """Main build process"""
    print()
    print("=" * 80)
    print(f"{PROJECT_NAME} - PRODUCTION BUILD")
    print(f"Version {VERSION}")
    print(f"{COMPANY_NAME}")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Validate environment
        iscc_command = validate_environment()
        
        # Step 2: Clean previous builds
        clean_previous_builds()
        
        # Step 3: Build executable
        build_executable()
        
        # Step 4: Create release notes
        release_notes_path = create_release_notes_file()
        
        # Step 5: Create installer with release notes
        create_installer(iscc_command, release_notes_path)
        
        # Step 6: Final cleanup
        final_cleanup()
        
        # Step 7: Show summary
        show_summary()
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print("❌ Build cancelled by user")
        return 1
    except Exception as e:
        print()
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())