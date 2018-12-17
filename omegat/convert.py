from pathlib import Path
from collections import OrderedDict
import re

from wylieconvert import *


def w2u(text):
    return wylie2unicode(text, dir='wylieconvert/Lingua-BO-Wylie')


def convert_entry(line):
    entry, definition = line.split('|')
    return w2u(entry), definition


def convert_everything(line):
    entry, definition = line.split('|')
    return w2u(entry), w2u(definition)


def _convert_left_right(line, left, right, regex, change='inmatch'):
    entry, definition = line.split('|')
    parts = re.split(regex, definition)
    for num, p in enumerate(parts):
        if change == 'inmatch':
            if num % 2:
                p = p.lstrip(left).rstrip(right)
                parts[num] = left + w2u(p) + right
        if change == 'outmatch':
            if not num % 2:
                parts[num] = w2u(p)

    definition = ''.join(parts)
    return w2u(entry), definition


def convert_curly(line):
    l, r, regex = '{', '}', r'(\{.+?\})'
    return _convert_left_right(line, l, r, regex, change='inmatch')


def convert_parens(line):
    l, r, regex = '(', ')', r'(\s*\(.+?\)\s*)'
    return _convert_left_right(line, l, r, regex, change='outmatch')


dicts = {
    "01-Hopkins2015": "entry",
    "02-RangjungYeshe": "curly",
    "03-Berzin": "entry",
    "04-Berzin-Def": "entry",
    "05-Hackett-Def2015": "entry",
    "05-Hopkins-Def2015": "entry",
    "06-Hopkins-Comment": "curly",
    "07-JimValby": "entry",
    "08-IvesWaldo": "entry",
    "09-DanMartin": "entry",
    "10-RichardBarron": "curly",
    "11-Hopkins-Divisions2015": "entry",
    "12-Hopkins-Divisions,Tib2015": "parens",
    "13-Hopkins-Examples": "entry",
    "14-Hopkins-Examples,Tib": "all",
    "15-Hopkins-Skt": "entry",
    "15-Hopkins-Skt2015": "entry",
    "16-Hopkins-Synonyms": "entry",
    "17-Hopkins-TibetanSynonyms": "all",
    "17-Hopkins-TibetanSynonyms2015": "all",
    "18-Hopkins-TibetanDefinitions2015": "all",
    "19-Hopkins-TibetanTenses2015": "all",
    "20-Hopkins-others'English2015": "entry",
    "21-Mahavyutpatti-Skt": "entry",
    "22-Yoghacharabhumi-glossary": "entry",
    "23-GatewayToKnowledge": "entry",
    "26-Verbinator": "curly",
    "33-TsepakRigdzin": "curly",
    "34-dung-dkar-tshig-mdzod-chen-mo-Tib": "all",
    "35-ThomasDoctor": "entry",
    "36-ComputerTerms": "entry",
    "37-dag_tshig_gsar_bsgrigs-Tib": "all",
    "38-Gaeng,Wetzel": "entry",
    "40-CommonTerms-Lin": "entry",
    "42-Sera-Textbook-Definitions": "curly",
    "43-84000Dict": "entry",
    "44-84000Definitions": "entry",
    "45-84000Synonyms": "curly",
    "46-84000Skt": "all"
}

dict_path = Path('../_input/dictionaries/public')
out_path = Path('glossaries')
if not out_path.is_dir():
    out_path.mkdir(exist_ok=True)

for dict, mode in dicts.items():
    if dict == "02-RangjungYeshe":
        continue
    print(dict)
    filepath = dict_path / dict
    lines = filepath.read_text().strip().split('\n')
    out = OrderedDict()
    for line in lines:
        if '|' in line:
            parsed = tuple
            if mode == 'entry':
                parsed = convert_entry(line)
            elif mode == 'curly':
                parsed = convert_curly(line)
            elif mode == 'all':
                parsed = convert_everything(line)
            elif mode == 'parens':
                parsed = convert_parens(line)
            else:
                raise ValueError('mode should be: entry, curly, all or parens')
            entry, content = parsed
            entry = entry.strip('་').replace('་', '-')
            content = content.replace('\t', '')
            if entry not in out.keys():
                out[entry] = []

            out[entry].append(content)

    for k, v in out.items():
        out[k] = ' | '.join(v)

    out = ['\t'.join((k, v)) for k, v in out.items()]
    outfile = out_path / str(dict + '.txt')
    outfile.write_text('\n'.join(out) + '\n')
