
from os.path import exists
from sys import argv


class Protein:
    name = ''
    seq = ''

    def __init__(self, nm, sec):
        self.name = nm
        self.seq = sec

    def get_data(self):
        return self.name, self.seq


def read_protein(fname):
    fp = open(fname, 'r')
    if not fp:
        print("Error in opening file")
        exit(1)
    lst = list()
    while True:
        name = ''
        seq = ''
        c = fp.readline()
        if not c:
            break
        elif c == '>':
            name = name+c
            while True:
                c = fp.read(1)
                if c == '\n':
                    break
                name = name+c
            while True:
                c = fp.read(1)
                if c == '>':
                    fp.seek((fp.tell() - 1), 0)
                    break
                seq = seq+c
            lst.append(Protein(name, seq))

    return lst


def main():
    fname = argv[1]
    if not exists(fname):
        print("Error: File does not exist")
        exit(1)

    else:
        plist = read_protein(fname)
        l = len(plist)
        for i in range(0, l):
            print(plist[i].name, plist[i].seq)
        exit(0)


if __name__ == "__main__":
    main()
