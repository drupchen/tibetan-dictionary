from pathlib import Path
import re


def format_for_omegat(content):
    content = re.sub(r'་([^། ])', r'-\1', content)
    return content


def format_dict_files(content):
    lines = content.strip().split('\n')
    for num, line in enumerate(lines):
        # print(num + 1, line)
        entry, deftn = line.split('\t')
        if '|' in deftn:
            deftn = '|'.join(sorted(list(set(deftn.split('|')))))
        entry = format_for_omegat(entry)
        lines[num] = entry + '\t' + deftn

    return '\n'.join(lines)


for f in Path('glossaries').glob('*.txt'):
    print(f.name)
    # if not f.name.startswith('33'):
    #     continue
    content = f.read_text()
    content = format_dict_files(content)
    f.write_text(content + '\n')
