"""
function DATA.better(i,row1,row2,    s1,s2,ys,x,y) --> bool; true if `row1` dominates (via Zitzler04).
  s1,s2,ys,x,y = 0,0,i.cols.y
  for _,col in pairs(ys) do
    x  = col:norm( row1.cells[col.at] )
    y  = col:norm( row2.cells[col.at] )
    s1 = s1 - math.exp(col.w * (x-y)/#ys)
    s2 = s2 - math.exp(col.w * (y-x)/#ys) end
  return s1/#ys < s2/#ys end

function DATA.dist(i,row1,row2,  cols,      n,d) --> n; returns 0..1 distance `row1` to `row2`
  n,d = 0,0
  for _,col in pairs(cols or i.cols.x) do
    n = n + 1
    d = d + col:dist(row1.cells[col.at], row2.cells[col.at])^the.p end
  return (d/n)^(1/the.p) end

function DATA.around(i,row1,  rows,cols) --> t; sort other `rows` by distance to `row`
  return sort(map(rows or i.rows,
                  function(row2)  return {row=row2, dist=i:dist(row1,row2,cols)} end),lt"dist") end

function DATA.half(i,rows,  cols,above) --> t,t,row,row,row,n; divides data using 2 far points
  local A,B,left,right,c,dist,mid,some,project
  function project(row)    return {row=row, dist=cosine(dist(row,A), dist(row,B), c)} end
  function dist(row1,row2) return i:dist(row1,row2,cols) end
  rows = rows or i.rows
  some = many(rows,the.Sample)
  A    = above or any(some)
  B    = i:around(A,some)[(the.Far * #rows)//1].row
  c    = dist(A,B)
  left, right = {}, {}
  for n,tmp in pairs(sort(map(rows, project), lt"dist")) do
    if   n <= #rows//2
    then push(left,  tmp.row); mid = tmp.row
    else push(right, tmp.row) end end
  return left, right, A, B, mid, c end

function DATA.cluster(i,  rows,min,cols,above) --> t; returns `rows`, recursively halved
  local node,left,right,A,B,mid
  rows = rows or i.rows
  min  = min or (#rows)^the.min
  cols = cols or i.cols.x
  node = {data=i:clone(rows)} --xxx cloning
  if #rows > 2*min then
    left, right, node.A, node.B, node.mid = i:half(rows,cols,above)
    node.left  = i:cluster(left,  min, cols, node.A)
    node.right = i:cluster(right, min, cols, node.B) end
  return node end

function DATA.sway(i,  rows,min,cols,above) --> t; returns best half, recursively
  local node,left,right,A,B,mid
  rows = rows or i.rows
  min  = min or (#rows)^the.min
  cols = cols or i.cols.x
  node = {data=i:clone(rows)} --xxx cloning
  if #rows > 2*min then
    left, right, node.A, node.B, node.mid = i:half(rows,cols,above)
    if i:better(node.B,node.A) then left,right,node.A,node.B = right,left,node.B,node.A end
    node.left  = i:sway(left,  min, cols, node.A) end
  return node end
"""
def x():
    return [1,2,3,4,5]
y = x()
print(y[3])