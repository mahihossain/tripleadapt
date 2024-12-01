

class ActivityState:

    def __init__(self, ident , seq , help , start, end, duration):
        self.ident = ident
        self.seq = int(seq)
        self.help = help
        self.start = start
        self.end = end
        self.duration = duration
