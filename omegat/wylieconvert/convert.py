from subprocess import Popen, PIPE
import os
from pathlib import Path

# Limitation:
# wylie2unicode and unicode2wylie both send the string to be transcoded as the commandline argument Perl receives.
# As such, strings should not be higher than the limit allowed for command-line arguments.
# For Windows:  according to https://stackoverflow.com/a/14177376
#               2047 or 8191 characters
# For Posix:    according to https://stackoverflow.com/a/14176172
#               2097152 (my output of "getconf ARG_MAX")


def wylie2unicode(text, dir='Lingua-BO-Wylie'):
    """
    Transcodes a wylie string in unicode (See above limitation)

    :param text: to be transcoded
    :param dir: path to the dir containing the Perl project
    :return: the converted string
    """
    current = os.getcwd()
    os.chdir(dir)
    out = Popen(['perl', 'wylie2unicode.pl', text], shell=False, stdout=PIPE)
    out = bytes.decode(out.communicate()[0])
    os.chdir(current)
    return out


def unicode2wylie(text, dir='Lingua-BO-Wylie'):
    """
    Transcodes a unicode string in wylie (See above limitation)

    :param text: to be transcoded
    :param dir: path to the dir containing the Perl Project
    :return: the converted string
    """
    current = os.getcwd()
    os.chdir(dir)
    out = Popen(['perl', '-CA', 'unicode2wylie.pl', text], shell=False, stdout=PIPE)
    out = bytes.decode(out.communicate()[0])
    os.chdir(current)
    return out


def batch_convert(mode, include_orig):
    """
    Wrapper to Lingua-BO-Wylie/bin/wylie.pl

    Reads .txt files in input/ and writes transcoded files in /output
    all arguments are exposed except the orig/transcoded separator
    :param mode: wylie2unicode or unicode2wylie
    :param include_orig: includes the original string in the output if True
    """
    # setting the folders
    in_path = Path('input')
    out_path = Path('output')
    in_path.mkdir(exist_ok=True)
    out_path.mkdir(exist_ok=True)

    if len(list(in_path.glob('*.txt'))) == 0:
        exit(print('There are no .txt files to convert'))
    if mode != 'u2w' and mode != 'w2u':
        exit(print('accepted modes are u2w and w2u'))

    # conversion
    to_convert = list(in_path.glob('*.txt'))
    args = []
    if mode == 'u2w':
        args.append('-u')
    if include_orig:
        args.append('-r')
        args.append('\n\t')  # hardcoded separator between the transcoded and the original

    current = Path(__file__).parent
    os.chdir(str(current)+'/Lingua-BO-Wylie/bin/')
    for f in to_convert:
        in_file = str(Path.resolve(Path.cwd() / '..' / '..' / '..' / f))
        out_file = str(Path.resolve(Path.cwd() / '..' / '..' / '..' / str(out_path / f.name)))
        Path(out_file).write_text('')  # create the output file
        Popen(['perl', 'wylie.pl'] + args + [in_file, out_file])
    os.chdir(current)
