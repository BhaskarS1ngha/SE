import mysql.connector as mq
from os.path import exists
from sys import argv


class Protein:
    name = ''
    seq = ''
    err = 0

    def __init__(self, nm, sec):
        self.name = nm
        self.seq = sec
        self.err_check()

    def err_check(self):
        seq_length = len(self.seq)
        if (seq_length % 3) == 0:
            self.err = 0
        else:
            self.err = 1

    def get_data(self):
        return self.name, self.seq, self.err


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
    mydb = mq.connect(host="localhost", user="root", passwd="L4qjg0ss", database="proteins")
    mycursor = mydb.cursor()

    mycursor.execute("SHOW TABLES")

    for x in mycursor:
        print(x)
    fname = argv[1]
    if not exists(fname):
        print("Error: File does not exist")
        exit(1)

    else:
        plist = read_protein(fname)
        l = len(plist)
        fr=open('out.txt', 'w')
        fr.write('name,sequence,error\n')
        for i in range(0,l):
            fr.write('%s,%s,%s\n' % (plist[i].name, plist[i].seq, plist[i].err))
        exit(0)


if __name__ == "__main__":
    main()
