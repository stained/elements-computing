class AInstruction:
    def __init__(self, value, index):
        self.value = value[1:]
        self.index = str(index)

    def __str__(self):
         return self.index + ":[A] Value: " + self.value

    def to_binary(self):
        # MSB = 0 (A instruction) + 15 value bits
        return "0" + '{0:b}'.format(int(self.value)).zfill(15)