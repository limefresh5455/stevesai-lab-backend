import re
import glob

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Add data prop to the component signature
    content = re.sub(r'export default function (\w+)\(\) \{', r'export default function \1({ data }: { data?: any }) {', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

files = glob.glob('src/components/sections/*.tsx')
for f in files:
    process_file(f)
