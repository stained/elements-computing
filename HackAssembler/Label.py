class Label:
    def __init__(self, label):
        self.label = label[1:-1]

    def __str__(self):
         return "[L] Label: " + self.label
