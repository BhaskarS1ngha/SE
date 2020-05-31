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
