#!/usr/bin/env python3
"""
Smart installer for Agentic Scheduler that handles Python 3.13 compatibility
"""
import subprocess
import sys
import platform
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major != 3:
        print("❌ Python 3 required")
        return False

    if version.minor < 11:
        print("⚠️ Python 3.11+ recommended, but trying anyway...")
        return True

    if version.minor >= 13:
        print("🎯 Python 3.13 detected - using compatible requirements")
        return "py313"

    return True


def main():
    print("🚀 Agentic Scheduler Installer")
    print("=" * 40)

    # Check Python version
    py_version = check_python_version()
    if not py_version:
        sys.exit(1)

    # Check if in project directory
    if not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)

    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")

    # Activate virtual environment (this affects the current process)
    activate_cmd = "venv/bin/activate" if platform.system() != "Windows" else "venv\\Scripts\\activate"
    print(f"🔧 Activating virtual environment... (run: source {activate_cmd})")

    # Determine which requirements file to use
    if py_version == "py313":
        req_file = "requirements-py313.txt"
    else:
        req_file = "requirements.txt"

    if not Path(req_file).exists():
        print(f"❌ Requirements file {req_file} not found")
        sys.exit(1)

    # Install requirements
    pip_cmd = f"venv/bin/pip" if platform.system() != "Windows" else "venv\\Scripts\\pip"
    install_cmd = f"{pip_cmd} install -r {req_file}"

    print(f"📦 Installing dependencies from {req_file}...")
    print("This may take a few minutes...")

    if run_command(install_cmd, "Installing dependencies"):
        print("\n🎉 Installation completed successfully!")
        print("\nTo run the application:")
        print(f"1. source {activate_cmd}")
        print("2. python main.py")
        print("3. Open http://localhost:8000 in your browser")
    else:
        print("\n❌ Installation failed. Trying alternative methods...")

        # Try alternative installation methods
        alt_methods = [
            f"{pip_cmd} install --upgrade pip",
            f"{pip_cmd} install --user -r {req_file}",
        ]

        for method in alt_methods:
            print(f"\n🔄 Trying: {method}")
            if run_command(method, "Alternative installation"):
                print("🎉 Alternative installation succeeded!")
                break
        else:
            print("\n❌ All installation methods failed.")
            print("\nTroubleshooting suggestions:")
            print("1. Try installing manually: pip install fastapi uvicorn pydantic")
            print("2. Check your internet connection")
            print("3. Try a different Python version (3.11 or 3.12)")
            print("4. Use minimal requirements: pip install -r requirements-minimal.txt")
            sys.exit(1)


if __name__ == "__main__":
    main()
