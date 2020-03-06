
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
    name = ''
    c = fp.readline()
    while True:
        seq = ''
        if not c:
            break
        elif c[0] == '>':
            name = c.rstrip('\n')
            while True:
                c = fp.readline()
                if not c or c[0] == '>':
                    break
                else:
                    seq = seq+c.rstrip('\n')
            lst.append(Protein(name, seq))
            name = c

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
            nm=plist[i].name
            sq=plist[i].seq
            print(plist[i].name, plist[i].seq)
           # k=input()
        exit(0)


if __name__ == "__main__":
    main()
