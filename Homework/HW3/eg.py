"""
function DATA.around(i,row1,  rows,cols) --> t; sort other `rows` by distance to `row`
  return sort(map(rows or i.rows, function(row2)  return {row=row2, dist=i:dist(row1,row2,cols)} end),lt"dist") end
"""

import utils
def lt():
    def fun(a, b):
        return a > b

l = [2,1]
x = sorted(l, key=lt)
print(x)