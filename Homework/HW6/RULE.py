class RULE:

    def __init__(self, ranges, maxSize):
        self.ranges = ranges
        self.maxSize = maxSize

        t = {} #: 大概率是dict，小概率是list，取决于range.txt是什么
        for range in ranges:
