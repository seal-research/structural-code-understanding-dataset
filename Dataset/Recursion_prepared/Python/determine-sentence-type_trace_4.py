import re

txt = """
This is a test"""

def haspunctotype(s):
    return 'S' if '.' in s else 'E' if '!' in s else 'Q' if '?' in s else 'N'


if __name__ == "__main__":
    txt = re.sub('\n', '', txt)
    pars = [s.strip() for s in re.split("(?:(?:(?<=[\?\!\.])(?:))|(?:(?:)(?=[\?\!\.])))", txt)]
    if len(pars) % 2:
        pars.append('')  # if ends without punctuation
    for i in range(0, len(pars)-1, 2):
        print((pars[i] + pars[i + 1]).ljust(54), "==>", haspunctotype(pars[i + 1]))
