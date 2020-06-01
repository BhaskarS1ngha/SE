import mysql.connector as mq
from os.path import exists
from sys import argv
from projectClasses import Protein


def connect_to_database():
    mydb = mq.connect(host="localhost", user="root", passwd="L4qjg0ss", database="SE")


def read_amino_acids(filename):
    fp = open(filename, 'r')
    if not fp:
        print("Error in opening file")
        exit(1)

    name = list()
    notation = ''
    reference_dict = dict()

    c = fp.readline()
    while True:
        if not c:
            break
        else:
            tempstrlist = c.split()
            notation = tempstrlist[0]
            if (tempstrlist[1][3] == ':'):
