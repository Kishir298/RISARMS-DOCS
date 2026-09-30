import re

with open('requirements.txt', 'r') as f:
    content = f.read()

# Check if the except-core-client section exists
if '# SECTION: except-core-client' not in content:
    print('Adding missing section...')
    # Replace the last section
    old = '''# DEVELOPMENT / TEST DEPENDENCIES
pytest>=8
pytest-cov>=5
pytest-asyncio>=0.23
httpx==0.28.1
ruff
black'''

    new = '''# SECTION: except-core-client
# =============================================================================
# CORE RUNTIME - EXCEPT CORE-CLIENT (core-client has no direct deps, same as all)
platformdirs>=4
python-dotenv>=1.0
sympy>=1.13
requests>=2.31
windows-curses>=2.3; sys_platform == "win32"
PyYAML>=6.0
fastapi==0.141.1
uvicorn[standard]==0.52.4
sqlalchemy==2.0.52
psycopg[binary]==3.3.4
pydantic==2.13.5
pydantic-settings==2.15.0
python-multipart==0.0.32

# EXTRAS - All optional (same as all)
textual>=0.70
textual-dev>=0.70
numpy
scipy
sounddevice
soundfile
silero-vad
faster-whisper
torch
torchaudio
speechbrain
openwakeword
pyttsx3
pycaw; sys_platform == "win32"
comtypes; sys_platform == "win32"
pywin32; sys_platform == "win32"
pypdf>=4
python-docx>=1.1
boto3>=1.28

# DEVELOPMENT / TEST DEPENDENCIES
pytest>=8
pytest-cov>=5
pytest-asyncio>=0.23
httpx==0.28.1
ruff
black'''

    content = content.replace(
        '''# DEVELOPMENT / TEST DEPENDENCIES
pytest>=8
pytest-cov>=5
pytest-asyncio>=0.23
httpx==0.28.1
ruff
black''',
        new
    )

    with open('requirements.txt', 'w') as f:
        f.write(content)
    print('Fixed!')