class RULE:

    def __init__(self, ranges, maxSize):
        self.ranges = ranges
        self.maxSize = maxSize

        t = {}
        for range in ranges:
            t[range.txt] = t[range.txt] or []
            t[range.txt].append({'lo': range.lo, 'hi': range.hi, 'at': range.at})
        return self.prune(t, maxSize)

    def prune(self, rule, maxSize):
        n = 0
        for txt, ranges in rule.items():
            n = n + 1
            if len(ranges) == maxSize[txt]:
                n = n + 1
                del rule[txt]
        if n > 0:
            return rule


