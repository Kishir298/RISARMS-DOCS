import re

with open('requirements.txt') as f:
    content = f.read()

# Extract 'all' section
match = re.search(r'# SECTION: all\n(.*?)(?=# SECTION:|\$)', content, re.DOTALL)
if match:
    lines = [l.strip() for l in match.group(1).split('\n') if l.strip() and not l.strip().startswith('#')]
    with open('temp_all.txt', 'w') as f:
        f.write('\n'.join(lines))
    print('Extracted {} packages for "all" section'.format(len(lines)))
    for l in lines[:5]:
        print('  ' + l)
    print('  ...')

# Extract except-core-host section
match = re.search(r'# SECTION: except-core-host\n(.*?)(?=# SECTION:|\$)', content, re.DOTALL)
if match:
    lines = [l.strip() for l in match.group(1).split('\n') if l.strip() and not l.strip().startswith('#')]
    with open('temp_no_host.txt', 'w') as f:
        f.write('\n'.join(lines))
    print('Extracted {} packages for \"except-core-host\" section'.format(len(lines)))

# Extract except-core-client section
match = re.search(r'# SECTION: except-core-client\n(.*?)(?=# SECTION:|\$)', content, re.DOTALL)
if match:
    lines = [l.strip() for l in match.group(1).split('\n') if l.strip() and not l.strip().startswith('#')]
    with open('temp_no_client.txt', 'w') as f:
        f.write('\n'.join(lines))
    print('Extracted {} packages for \"except-core-client\" section'.format(len(lines)))