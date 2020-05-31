import mysql.connector as mq
from os.path import exists
from sys import argv
from projectClasses import Protein


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
                    seq = seq + c.rstrip('\n')
            lst.append(Protein(name, seq))
            name = c

    return lst


def push_to_db(val_list):
    mydb = mq.connect(host="localhost", user="root", passwd="L4qjg0ss", database="SE")
    mycursor = mydb.cursor()
    sql = "INSERT INTO proteins (name,sequence,error) VALUES (%s, %s, %s)"

    mycursor.execute(sql, val_list)
    mydb.commit()
    mydb.close()
    # print(mycursor.rowcount," was inserted.")


def main():
    fname = argv[1]
    if not exists(fname):
        print("Error: File does not exist")
        exit(1)

    else:
        plist = read_protein(fname)
        l = len(plist)
        # push_to_db(plist)
        fr = open('out.txt', 'w')
        fr.write('name,sequence,error\n')
        print("Creating Database And Writing to file out.txt")
        for i in range(0, l):
            push_to_db([plist[i].name, plist[i].seq, plist[i].err])
            fr.write('%s,%s,%s\n' % (plist[i].name, plist[i].seq, plist[i].err))
        print("\nAll Operations Successful")
        exit(0)


if __name__ == "__main__":
    main()
