import re

# Read from requirements.txt (not own file)
with open('requirements.txt') as f:
    content = f.read()

def extract_section(section_name: str, output_file: str, display_name: str):
    """Extract a section from requirements.txt and write to output file."""
    match = re.search(r'# SECTION: ' + re.escape(section_name) + r'\n(.*?)(?=# SECTION:|$)', content, re.DOTALL)
    if match:
        lines = [l.strip() for l in match.group(1).split('\n') if l.strip() and not l.strip().startswith('#')]
        with open(output_file, 'w') as f:
            f.write('\n'.join(lines))
        print('Extracted {} packages for "{}" section -> {}'.format(len(lines), display_name, output_file))
        for l in lines[:5]:
            print('  ' + l)
        if len(lines) > 5:
            print('  ...')
    else:
        print('Section "{}" not found!'.format(section_name))

# Extract 'all' section
extract_section('all', 'temp_all.txt', 'all')

# Extract except-core-host section
extract_section('except-core-host', 'temp_no_host.txt', 'except-core-host')

# Extract except-core-client section
extract_section('except-core-client', 'temp_no_client.txt', 'except-core-client')