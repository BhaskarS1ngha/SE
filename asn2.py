import mysql.connector as mq
from os.path import exists
from sys import argv
from projectClasses import Protein


codonDict = {
    'phe' : ['ttt','ttc'],
    'leu': ['tta','ttg','ctt','ctc','cta','ctg'],
    'ile': ['att','atc', 'ata'],
    'met': ['atg'],
    'val':['gtt', 'gtc', 'gta', 'gtg'],
    'ser': ['tct', 'tcc', 'tca', 'tcg','agt', 'agc'],
    'pro': ['cct', 'ccc','cca', 'ccg'],
    'thr': ['act', 'acc', 'aca', 'acg'],
    'ala': ['gct', 'gcc', 'gca', 'gcg'],
    'tyr': ['tat', 'tac'],
    'stop' :['taa' ,'tag' ,'tga'],
    'his' :['cat', 'cac'],
    'gin': ['caa', 'cag'],
    'asn': ['aat', 'aac'],
    'lys': ['aaa', 'aag'],
    'asp': ['gat', 'gac'],
    'glu': ['gaa', 'gag'],
    'cys': ['tgt', 'tgc'],
    'trp': ['tgg'],
    'arg': ['cgt', 'cgc', 'cga', 'cgg', 'aga', 'agg'],
    'gly': ['ggt', 'ggc', 'gga', 'ggg']
}


def get_amino_acid_notn(amino_acid):
    amino_dict = read_amino_acids("aminoAcids.txt")
    key_list = amino_dict.keys()
    for key in key_list:
        temp_notation = amino_dict[key]
        for x in temp_notation:
            if x == amino_acid:
                return key


def get_amino_acid(codon):
    key_list = codonDict.keys()
    for key in key_list:
        temp_codon = codonDict[key]
        for x in temp_codon:
            if x == codon:
                return get_amino_acid_notn(key)

def connect_to_database():
    mydb = mq.connect(host="localhost", user="root", passwd="L4qjg0ss", database="SE")
    return mydb


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
            if (len(tempstrlist[1]) >= 3):
                aminoAcidList = tempstrlist[1].split(':')
            else:
                aminoAcidList = tempstrlist[1]

            reference_dict[tempstrlist[0]] = aminoAcidList
            c = fp.readline()
    #print(reference_dict)
    return reference_dict


def update_gen_len():
    mydb=connect_to_database()
    print(mydb)
    mycursor = mydb.cursor()
    mycursor.execute("update proteins set lenofgeneseq = Length(sequence)")
    mydb.commit()
    #print(mycursor.rowcount)


def get_amino_acid_seq(gen_seq, len_gene):
    i = 0
    amino_seq = ''
    while i < len_gene:
        codon = gen_seq[i:i + 3]
        i += 3
        amino_seq += get_amino_acid(codon)
    return amino_seq



def update_amino_acid():
    mydb = connect_to_database()
    sql = "select name, sequence, error, lenOfGeneSeq from proteins"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        if row[2] != 0:
            seq = row[1]
            gene_len = row[3]
            aminoSeq = "\"" + get_amino_acid_seq(seq, gene_len) + "\""
            sql = "update proteins set aminoAcidSequence = %s where name = %s "
            val = [aminoSeq, row[0]]
            mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    mydb.close()

update_amino_acid()