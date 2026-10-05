#!/usr/bin/env python3
"""Generate unified requirements.txt with three install commands - ATOMIC."""

import os
import tempfile

# Define sections as data structures (single source of truth)
CORE_RUNTIME_ALL = [
    "platformdirs>=4",
    "python-dotenv>=1.0",
    "sympy>=1.13",
    "requests>=2.31",
    'windows-curses>=2.3; sys_platform == "win32"',
    "PyYAML>=6.0",
    "fastapi==0.141.1",
    "uvicorn[standard]==0.52.4",
    "sqlalchemy==2.0.52",
    "psycopg[binary]==3.3.4",
    "pydantic==2.13.5",
    "pydantic-settings==2.15.0",
    "python-multipart==0.0.32",
]

CORE_RUNTIME_NO_HOST = [
    "platformdirs>=4",
    "python-dotenv>=1.0",
    "sympy>=1.13",
    "requests>=2.31",
    'windows-curses>=2.3; sys_platform == "win32"',
    # PyYAML, fastapi, uvicorn, sqlalchemy, psycopg, pydantic, pydantic-settings, python-multipart
    # are provided by CORE-HOST/RESCS
]

CORE_RUNTIME_NO_CLIENT = CORE_RUNTIME_ALL  # CORE-CLIENT has no direct deps

EXTRAS_ALL = [
    "textual>=0.70",
    "textual-dev>=0.70",
    "numpy",
    "scipy",
    "sounddevice",
    "soundfile",
    "silero-vad",
    "faster-whisper",
    "torch",
    "torchaudio",
    "speechbrain",
    "openwakeword",
    "pyttsx3",
    'pycaw; sys_platform == "win32"',
    'comtypes; sys_platform == "win32"',
    'pywin32; sys_platform == "win32"',
    "pypdf>=4",
    "python-docx>=1.1",
    "boto3>=1.28",
]

DEV_DEPS = [
    "pytest>=8",
    "pytest-cov>=5",
    "pytest-asyncio>=0.23",
    "httpx==0.28.1",
    "ruff",
    "black",
]

SECTIONS = {
    "all": CORE_RUNTIME_ALL + EXTRAS_ALL + DEV_DEPS,
    "except-core-host": CORE_RUNTIME_NO_HOST + EXTRAS_ALL + DEV_DEPS,
    "except-core-client": CORE_RUNTIME_NO_CLIENT + EXTRAS_ALL + DEV_DEPS,
}

HEADER = """# RISARMS Ecosystem - Unified Requirements with Three Install Commands
# Location: C:\\Users\\rishi\\Desktop\\RISARMS\\RISARMS-DOCS\\requirements.txt
#
# THREE INSTALL COMMANDS (use generated manifest files, NOT pip --exclude):
# =============================================================================
#
# COMMAND 1 - EVERYTHING (all packages + all extras from all 7 repos):
#   pip install -r C:\\Users\\rishi\\Desktop\\RISARMS\\RISARMS-DOCS\\requirements.txt
#
# COMMAND 2 - EVERYTHING EXCEPT CORE-HOST:
#   pip install -r C:\\Users\\rishi\\Desktop\\RISARMS\\RISARMS-DOCS\\requirements-no-host.txt
#
# COMMAND 3 - EVERYTHING EXCEPT CORE-CLIENT:
#   pip install -r C:\\Users\\rishi\\Desktop\\RISARMS\\RISARMS-DOCS\\requirements-no-client.txt
#
# GENERATED MANIFEST FILES (run this script to regenerate):
#   requirements.txt              - all packages
#   requirements-no-host.txt      - excludes CORE-HOST/RESCS deps
#   requirements-no-client.txt    - excludes CORE-CLIENT deps (same as all)
#
# =============================================================================
"""

def build_section(name: str) -> str:
    """Build a requirements section from package lists."""
    lines = [f"# SECTION: {name}", "# ============================================================================="]
    if name == "all":
        lines.append("# CORE RUNTIME - All projects")
        lines.extend(CORE_RUNTIME_ALL)
    elif name == "except-core-host":
        lines.append("# CORE RUNTIME - EXCEPT CORE-HOST (excludes PyYAML and fastapi stack)")
        lines.extend(CORE_RUNTIME_NO_HOST)
    elif name == "except-core-client":
        lines.append("# CORE RUNTIME - EXCEPT CORE-CLIENT (core-client has no direct deps, same as all)")
        lines.extend(CORE_RUNTIME_NO_CLIENT)

    lines.append("")
    lines.append("# EXTRAS - All optional dependencies from all projects")
    lines.extend(EXTRAS_ALL)
    lines.append("")
    lines.append("# DEVELOPMENT / TEST DEPENDENCIES")
    lines.extend(DEV_DEPS)
    return "\n".join(lines) + "\n"

def main():
    # Build all content first (validate before writing)
    all_content = HEADER + "\n\n".join(build_section(name) for name in SECTIONS)
    
    # Atomic write: write to temp file first, then rename
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        newline='\n',
        dir='.',
        delete=False,
        prefix='requirements.',
        suffix='.tmp'
    ) as tmp:
        tmp.write(all_content)
        tmp_path = tmp.name
    
    try:
        os.replace(tmp_path, 'requirements.txt')
        print('requirements.txt written successfully (atomic)')
        
        # Also generate the individual manifest files
        for name in ["except-core-host", "except-core-client"]:
            section_content = HEADER + "\n\n" + build_section(name)
            manifest_name = f"requirements-no-{'host' if name == 'except-core-host' else 'client'}.txt"
            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                newline='\n',
                dir='.',
                delete=False,
                prefix=f'{manifest_name}.',
                suffix='.tmp'
            ) as tmp:
                tmp.write(section_content)
                tmp_path = tmp.name
            os.replace(tmp_path, manifest_name)
            print(f'{manifest_name} written successfully (atomic)')
            
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise

if __name__ == "__main__":
    main()