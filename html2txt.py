import sys
import os
from bs4 import BeautifulSoup


def get_contents_for_file(filename):
    soup = BeautifulSoup(open(filename, encoding='iso-8859-2'))
    result = soup.get_text()

    lines = [l for l in result.split('\n') if l != '' and not l.startswith('Opracowanie Centrum Nowych Technologii') and not l.startswith('Pytania i uwagi dotyczące archiwum')]

    # Usuwanie metainformacji
    lines2 = []
    omit = False
    for line in lines:
        if line.strip().startswith('Archiwum ROL:') or omit and not line.strip().startswith('Dział'):
            omit = True
            continue
        elif line.strip().startswith('Dział'):
            omit = False
            continue
        lines2.append(line)

    # Usuniecie incjalow autora - za krotkie, by byc uzyteczne, a wprowadza niepotrzebny szum
    if len(lines2) > 0:
        lines2.pop()
    else:
        print("Empty file: ", filename)

    result = '\n'.join(lines2)
    result = [r for r in result.split() if r]
    return ' '.join(result)

all_contents = []

def scan_dir(initial_dir=sys.argv[1]):
    entries = os.listdir(initial_dir)
    for e in entries:
        path = os.path.join(initial_dir, e)
        if os.path.isfile(path) and e.endswith('.html'):
            print("Plik", e)
            all_contents.append(get_contents_for_file(path))
        elif os.path.isdir(path):
            scan_dir(path)

if __name__ == '__main__':
    scan_dir()

    f = open('result.txt', 'w')
    for fcontent in all_contents:
        if fcontent.strip():
            f.write(fcontent + '\n')
    f.close()

