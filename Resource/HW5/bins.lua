--<!-- vim: set syntax=lua ts=2 sw=2 et : -->
-- This code suppprts entropy-merge discretization. This is an bottom-up entropy-based supervised clustering algorithm
-- that divided numerics into (say) 16 bins, then recursively merges adjacent bins in the splits are less informative than the combination.
-- At its start, this code uses recursive Fastmap to find a few `best` examples, then a sample of the `rest`. `bins.lua`
-- then prunes bins that have similar distributions in `best` and `rest
local the,help = {}, [[
  
bins: multi-objective semi-supervised discetization
(c) 2023 Tim Menzies <timm@ieee.org> BSD-2
  
USAGE: lua bins.lua [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -f  --file    data file                    = ../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
]]
-- ## Tricks 

-- Magic regex trick to match keys and values from `help`
local magic = "\n[%s]+[-][%S][%s]+[-][-]([%S]+)[^\n]+= ([%S]+)"
  
-- Trick for finding rogue names,  escaped into the global space.
local b4={}; for k,v in pairs(_ENV) do b4[k]=v end 
-- Trick that lets us define everything in any order.
local adds,add,any,at,better,bin,bins
local copy,cli,csv,cells,cliffsDelta,coerce
local diffs,dist,div,eg,extend,fmt,gt,half,has,go,itself
local kap,keys,lines,locals,lt,main,many,map,merge,merge2,mergeAny,mid
local no,norm,o,oo,per,push,rint,rand,rnd,row,rogues
local say,sayln,Seed,showTree,sort,slice,stats,sway,tree,value
local COL,COLS,DATA,NUM,RANGE,SYM
-- Trick to  shorten call to maths functions
local m = math

-- ## <a name=create>Creation</a>

-- Create a `NUM` or a `SYM`. Column
-- names are a little language that    
-- e.g. makes `NUM`s if name starts in upper case; or
-- e.g. makes goals if the name ends with
-- the maximize (`+`) or minimize (`-`) or klass (`!`) symbol.
function COL(n,s,    col)
   col = s:find"^[A-Z]" and NUM(n,s) or SYM(n,s) 
   col.isIgnored  = col.txt:find"X$"
   col.isKlass    = col.txt:find"!$"
   col.isGoal     = col.txt:find"[!+-]$"
   return col end

-- Create a `NUM` to summarize a stream of numbers.
function NUM(n,s) 
  return {at= n or 0, txt= s or "", n=0,
          hi= -m.huge, lo= m.huge, 
          ok=true, has={},
          w= (s or ""):find"-$" and -1 or 1} end

-- Create a `SYM` to summarize a stream of symbols.
function SYM(n,s)
  return {at=n or 0, txt=s or "", n=0, 
          mode=nil,  most=0,
          isSym=true, has={}} end

-- Create a set of `NUM`s or `SYM`s columns.
-- Once created, all cols are stored in `all`
-- while the non-skipped cols are also stored as
-- either `cols.x` independent input variables or
-- `cols.y` dependent goal variables.
function COLS(ss,     col,cols)
  cols={names=ss, all={},x={},y={}}
  for n,s in pairs(ss) do  
    col = push(cols.all, COL(n,s))
    if not col.isIgnored then
      if col.isKlass then cols.klass = col end
      push(col.isGoal and cols.y or cols.x, col) end end 
  return cols end

-- Create a RANGE  that tracks the y dependent values seen in 
-- the range `lo` to `hi` some independent variable in column number `at` whose name is `txt`. 
-- Note that the way this is used (in the `bins` function, below)
-- for  symbolic columns, `lo` is always the same as `hi`.
function RANGE(at,txt,lo,hi) 
  return {at=at,txt=txt,lo=lo,hi=lo or hi or lo,y=SYM()} end

-- Create a `DATA` to contain `rows`, summarized in `cols`.
DATA={}
function DATA.new() return {rows={},cols=nil} end  -- initially, no `cols`

-- Create a new DATA by reading csv file whose first row 
-- are the comma-separate names processed by `COLS` (above).
-- into a new `DATA`. Every other row is stored in the DATA by
-- calling the 
-- `row` function (defined below).
function DATA.read(sfile,    data) 
  data=DATA.new()
  csv(sfile, function(t) row(data,t) end); return data end

-- Create a new DATA with the same columns as  `data`. Optionally, load up the new
-- DATA with the rows inside `ts`.
function DATA.clone(data,  ts,    data1)
  data1 = row(DATA.new(), data.cols.names)
  for _,t in pairs(ts or {}) do row(data1,t) end
  return data1 end

-- ## Update

-- Update `data` with  row `t`. If `data.cols`
-- does not exist, the use `t` to create `data.cols`.
-- Otherwise, add `t` to `data.rows` and update the summaries in `data.cols`.
-- To avoid updating skipped columns, we only iterate
-- over `cols.x` and `cols.y`.
function row(data,t)
  if data.cols  then
    push(data.rows,t)
    for _,cols in pairs{data.cols.x, data.cols.y} do
      for _,col in pairs(cols) do 
	     add(col, t[col.at]) end end 
  else data.cols = COLS(t) end 
  return data end

-- Update one COL with `x` (values from one cells of one row).
-- Used  by (e.g.) the `row` and `adds` function.
-- `SYM`s just increment a symbol counts.
-- `NUM`s store `x` in a finite sized cache. When it
-- fills to more than `the.Max`, then at probability 
-- `the.Max/col.n` replace any existing item
-- (selected at random). If anything is added, the list
-- may not longer be sorted so set `col.ok=false`.
function add(col,x,  n)
  if x ~= "?" then
    n = n or 1
    col.n = col.n + n
    if   col.isSym
    then col.has[x] = n + (col.has[x] or 0) 
         if col.has[x] > col.most then
           col.most, col.mode = col.has[x],x end 
    else col.lo, col.hi = m.min(x,col.lo), m.max(x,col.hi) 
      local all,pos
      all = #col.has
      pos = (all < the.Max and all+1) or (rand() < the.Max/col.n and rint(1,all))
      if pos then
        col.has[pos] = x
        col.ok = false end end end end 

-- Update a COL with multiple items from `t`. This is useful when `col` is being
-- used outside of some DATA.
function adds(col,t) 
  for _,x in pairs(t or {}) do add(col,x) end; return col end

-- Update a RANGE to cover `x` and `y`
function extend(range,n,s)
  range.lo = m.min(n, range.lo)
  range.hi = m.max(n, range.hi)
  add(range.y, s) end

-- ## Query

-- A query that returns contents of a column. If `col` is a `NUM` with
-- unsorted contents, then sort before return the contents.
-- Called by (e.g.) the `mid` and `div` functions.
function has(col)
  if not col.isSym and not col.ok then sort(col.has) end 
  col.ok = true -- the invariant here is that "has" is ready to be shared.
  return col.has end

-- A query that  returns a `cols`'s central tendency  
-- (mode for `SYM`s and median for `NUM`s). Called by (e.g.) the `stats` function.
function mid(col,    mode,most)
  return col.isSym and col.mode or per(has(col), .5) end 

-- A query that returns a `col`'s deviation from central tendency    
-- (entropy for `SYM`s and standard deviation for `NUM`s)..
function div(col,    e)
  if   col.isSym 
  then e=0
       for _,n in pairs(col.has) do e= e-n/col.n*m.log(n/col.n,2) end
       return e
  else return (per(has(col),.9) - per(has(col), .1))/2.58 end end

-- A query that returns `mid` or `div` of `cols` (defaults to `data.cols.y`).
function stats(data,  fun,cols,nPlaces,     tmp)
  cols= cols or data.cols.y
  tmp = kap(cols,
            function(k,col) return rnd((fun or mid)(col),nPlaces), col.txt end)
  tmp["N"] = #data.rows
  return tmp,map(cols,mid)  end

-- A query that normalizes `n` 0..1. Called by (e.g.) the `dist` function.
function norm(num,n)
  return x=="?" and x or (n - num.lo)/(num.hi - num.lo + 1/m.huge) end

-- A query that returns the score a distribution of symbols inside a SYM.
function value(has,  nB,nR,sGoal,    b,r)
  sGoal,nB,nR = sGoal or true, nB or 1, nR or 1
  b,r = 0,0
  for x,n in pairs(has) do
    if x==sGoal then b = b + n else r = r + n end end
  b,r = b/(nB+1/m.huge), r/(nR+1/m.huge)
  return b^2/(b+r) end

-- A query that returns the distances 0..1 between rows `t1` and `t2`.   
-- If any values are unknown, assume max distances.
function dist(data,t1,t2,  cols,    d,n,dist1)
  function dist1(col,x,y)
    if x=="?" and y=="?" then return 1 end
    if   col.isSym
    then return x==y and 0 or 1 
    else x,y = norm(col,x), norm(col,y)
         if x=="?" then x= y<.5 and 1 or 1 end	
         if y=="?" then y= x<.5 and 1 or 1 end	
         return m.abs(x-y) end 
  end --------------
  d, n = 0, 1/m.huge	
  for _,col in pairs(cols or data.cols.x) do
    n = n + 1
    d = d + dist1(col, t1[col.at], t2[col.at])^the.p end 
  return (d/n)^(1/the.p) end

-- A query that returns true if `row1` is better than another.
-- This is Zitzler's indicator predicate that
-- judges the domination status 
-- of pair of individuals by running a “what-if” query. 
-- It checks what we lose if we (a) jump from one 
-- individual to another (see `s1`), or if we (b) jump the other way (see `s2`).
-- The jump that losses least indicates which is the best row.
function better(data,row1,row2,    s1,s2,ys,x,y) 
  s1,s2,ys,x,y = 0,0,data.cols.y
  for _,col in pairs(ys) do
    x  = norm(col, row1[col.at] )
    y  = norm(col, row2[col.at] )
    s1 = s1 - m.exp(col.w * (x-y)/#ys)
    s2 = s2 - m.exp(col.w * (y-x)/#ys) end
  return s1/#ys < s2/#ys end

-- ## Clustering

-- Cluster `rows` into two sets by
-- dividing the data via their distance to two remote points.
-- To speed up finding those remote points, only look at
-- `some` of the data. Also, to avoid outliers, only look
-- `the.Far=.95` (say) of the way across the space. 
function half(data,  rows,cols,above)
  local left,right,far,gap,some,proj,cos,tmp,A,B,c = {},{}
  function gap(r1,r2) return dist(data, r1, r2, cols) end
  function cos(a,b,c) return (a^2 + c^2 - b^2)/(2*c) end
  function proj(r)    return {row=r, x=cos(gap(r,A), gap(r,B),c)} end
  rows = rows or data.rows
  some = many(rows,the.Halves)
  A    = (the.Reuse and above) or any(some)
  tmp  = sort(map(some,function(r) return {row=r, d=gap(r,A)} end ),lt"d")
  far  = tmp[(#tmp*the.Far)//1]
  B,c  = far.row, far.d
  for n,two in pairs(sort(map(rows,proj),lt"x")) do
    push(n <= #rows/2 and left or right, two.row) end
  return left,right,A,B,c end

-- Cluster, recursively, some `rows` by  dividing them in two, many times
function tree(data,  rows,cols,above,     here)
  rows = rows or data.rows
  here = {data=DATA.clone(data,rows)}
  if #rows >= 2*(#data.rows)^the.min then
    local left,right,A,B = half(data, rows, cols, above)
    here.left  = tree(data, left,  cols, A)
    here.right = tree(data, right, cols, B) end
  return here end 

-- Cluster can be displayed by this function.
function showTree(tree,  lvl,post)
  if tree then 
    lvl  = lvl or 0
    io.write(fmt("%s[%s] ",("|.. "):rep(lvl), #(tree.data.rows)))
    print((lvl==0 or not tree.left) and o(stats(tree.data)) or "")
    showTree(tree.left, lvl+1)
    showTree(tree.right,lvl+1) end end

-- ## Optimization

-- Recursively prune the worst half the data. Return
-- the survivors and some sample of the rest.
function sway(data,     worker,best,rest)
  function worker(rows,worse,  above)
    if   #rows <= (#data.rows)^the.min 
    then return rows, many(worse, the.rest*#rows) 
    else local l,r,A,B = half(data, rows, cols, above)
         if better(data,B,A) then l,r,A,B = r,l,B,A end
         map(r, function(row) push(worse,row) end) 
         return worker(l,worse,A) end 
  end ----------------------------------
  best,rest = worker(data.rows,{})
  return DATA.clone(data,best), DATA.clone(data,rest) end 

-- ## Discretization

-- Return RANGEs that distinguish sets of rows (stored in `rowss`).
-- To reduce the search space,
-- values in `col` are mapped to small number of `bin`s.
-- For NUMs, that number is `the.bins=16` (say) (and after dividing
-- the column into, say, 16 bins, then we call `mergeAny` to see
-- how many of them can be combined with their neighboring bin).
function bins(cols,rowss)
  local out = {}
  for _,col in pairs(cols) do
    local ranges = {}
    for y,rows in pairs(rowss) do
      for _,row in pairs(rows) do
        local x,k = row[col.at]
        if x ~= "?" then
          k = bin(col,x)
          ranges[k] = ranges[k] or RANGE(col.at,col.txt,x)
          extend(ranges[k], x, y) end end end
    ranges = sort(map(ranges,itself),lt"lo")
    out[1+#out] = col.isSym and ranges or mergeAny(ranges) end
  return out end

-- Map `x` into a small number of bins. `SYM`s just get mapped
-- to themselves but `NUM`s get mapped to one of `the.bins` values.
-- Called by function `bins`.
function bin(col,x,      tmp)
  if x=="?" or col.isSym then return x end
  tmp = (col.hi - col.lo)/(the.bins - 1)
  return col.hi == col.lo and 1 or m.floor(x/tmp + .5)*tmp end

-- Given a sorted list of ranges, try fusing adjacent items
-- (stopping when no more fuse-ings can be found). When done,
-- make the ranges run from minus to plus infinity
-- (with no gaps in between).
-- Called by function `bins`.
function mergeAny(ranges0,     noGaps)
  function noGaps(t)
    for j = 2,#t do t[j].lo = t[j-1].hi end
    t[1].lo  = -m.huge
    t[#t].hi =  m.huge
    return t 
  end ------
  local ranges1,j,left,right,y = {},1
  while j <= #ranges0 do
    left, right = ranges0[j], ranges0[j+1]
    if right then
      y = merge2(left.y, right.y)
      if y then
        j = j+1 -- next round, skip over right.
        left.hi, left.y = right.hi, y end end
    push(ranges1,left)
    j = j+1 
  end
  return #ranges0==#ranges1 and noGaps(ranges0) or mergeAny(ranges1) end

-- If the whole is as good (or simpler) than the parts,
-- then return the 
-- combination of 2 `col`s.
-- Called by function `mergeMany`.
function merge2(col1,col2,   new)
  new = merge(col1,col2)
  if div(new) <= (div(col1)*col1.n + div(col2)*col2.n)/new.n then
    return new end end

-- Merge two `cols`. Called by function `merge2`.
function merge(col1,col2,    new)
  new = copy(col1)
  if   col1.isSym 
  then for x,n in pairs(col2.has) do add(new,x,n) end
  else for _,n in pairs(col2.has) do add(new,n)   end
       new.lo = m.min(col1.lo, col2.lo)
       new.hi = m.max(col1.hi, col2.hi) end 
  return new end

   
-- ## Miscellaneous Support Code
-- ### Meta

-- Return self
function itself(x) return x end

-- ### Maths

-- Round numbers
function rnd(n, nPlaces) 
  local mult = 10^(nPlaces or 2)
  return math.floor(n * mult + 0.5) / mult end

-- Random number generation.
Seed=937162211 -- seed
function rint(nlo,nhi)  -- random ints  
  return m.floor(0.5 + rand(nlo,nhi)) end

function rand(nlo,nhi) -- random floats
  nlo, nhi = nlo or 0, nhi or 1
  Seed = (16807 * Seed) % 2147483647
  return nlo + (nhi-nlo) * Seed / 2147483647 end

-- Non-parametric effect-size test
--  M.Hess, J.Kromrey. 
--  Robust Confidence Intervals for Effect Sizes: 
--  A Comparative Study of Cohen's d and Cliff's Delta Under Non-normality and Heterogeneous Variances
--  American Educational Research Association, San Diego, April 12 - 16, 2004    
--  0.147=  small, 0.33 =  medium, 0.474 = large; med --> small at .2385
function cliffsDelta(ns1,ns2) 
  if #ns1 > 256     then ns1 = many(ns1,256) end
  if #ns2 > 256     then ns2 = many(ns2,256) end
  if #ns1 > 10*#ns2 then ns1 = many(ns1,10*#ns2) end
  if #ns2 > 10*#ns1 then ns2 = many(ns2,10*#ns1) end
  local n,gt,lt = 0,0,0
  for _,x in pairs(ns1) do
    for _,y in pairs(ns2) do
      n = n + 1
      if x > y then gt = gt + 1 end
      if x < y then lt = lt + 1 end end end
  return m.abs(lt - gt)/n > the.cliffs end

-- Given two tables with the same keys, report if their
-- values are different.
function diffs(nums1,nums2)
  return kap(nums1, function(k,nums) 
              return cliffsDelta(nums.has,nums2[k].has),nums.txt end) end

-- ### String to thing

-- Coerce string to boolean, int,float or (failing all else) strings.
function coerce(s,    fun) 
  function fun(s1)
    if s1=="true" then return true elseif s1=="false" then return false end
    return s1 end
  return math.tointeger(s) or tonumber(s) or fun(s:match"^%s*(.-)%s*$") end

-- Split a string `s`  on commas.
function cells(s,    t)
  t={}; for s1 in s:gmatch("([^,]+)") do t[1+#t] = coerce(s1) end; return t end

-- Run `fun` for all lines in a file.
function lines(sFilename,fun,    src,s) 
  src = io.input(sFilename)
  while true do
    s = io.read(); if s then fun(s) else return io.close(src) end end end

-- Run `fun` on the cells  in each row of a csv file.
function csv(sFilename,fun)
  lines(sFilename, function(line) fun(cells(line)) end) end

-- ### Lists

-- Push an item `x` onto  a list.    
-- Return a list, sorted on `fun`.   
-- Return a function sorting down on field `x`.    
-- Return a function sorting up on field `x`.    
-- Return one item at random.    
-- Return many items, selected at random.   
-- Map a function on  table (results in items 1,2,3...)    
push = function(t,x) t[#t+1]=x; return x end
sort = function(t,f) table.sort(t,f); return t end
at   = function(x)   return function(t) return t[x] end end
lt   = function(x)   return function(a,b) return a[x] < b[x] end end
gt   = function(x)   return function(a,b) return a[x] > b[x] end end
any  = function(t)   return t[rint(#t)] end
many = function(t,n,    u) u={}; for i=1,n do push(u, any(t)) end; return u end 
map  = function(t, fun) return kap(t, function(_,v) return fun(v) end) end
keys = function(t)      return sort(kap(t,function(k,_) return k end)) end

-- Map a function on table (results in items key1,key2,...)
function kap(t, fun,     u) 
  u={}; for k,v in pairs(t) do v,k=fun(k,v); u[k or (1+#u)]=v; end; return u end

-- Return the `p`-ratio item in `t`; e.g. `per(t,.5)` returns the medium.
function per(t,p) 
  p=math.floor(((p or .5)*#t)+.5); return t[m.max(1,m.min(#t,p))] end

-- Deep copy of a table `t`.
function copy(t,    u) 
  if  type(t)~="table" then return t end
  u={}; for k,v in pairs(t) do u[k] = copy(v) end; return u end

-- Return a portion of `t`; go,stop,inc defaults to 1,#t,1.
-- Negative indexes are supported.
function slice(t, go, stop, inc,    u) 
  if go   and go   < 0 then go=#t+go     end
  if stop and stop < 0 then stop=#t+stop end
  u={}
  for j=(go or 1)//1,(stop or #t)//1,(inc or 1)//1 do u[1+#u]=t[j] end
  return u end

-- ### Strings

-- `fmt` means `string.format`.
fmt  = string.format

-- print to standard error
function say(...)   io.stderr:write(fmt(...)) end
function sayln(...) io.stderr:write(fmt(...).."\n") end

-- Print a nested table (sorted by the keys of the table).
function oo(t) print(o(t)); return t end
function o(t,    fun) 
  if type(t)~="table" then return tostring(t) end
  function fun (k,v) return fmt(":%s %s",k,o(v)) end 
  return "{"..table.concat(#t>0  and map(t,o) or sort(kap(t,fun))," ").."}" end

-- ### Main Control

-- Rune all the functions whose name matches
-- the command-line flag `-g xx`. Show the help
-- string if the `-h` flag is set. Return to the operating
-- system the number of failing `funs`.
function main(funs,the,help,    y,n,saved,k,val,ok)
  y,n,saved = 0,0,copy(the)
  if   the.help 
  then os.exit(print(help)) end
  for _,pair in pairs(funs) do
    k = pair.key
    if k:find(".*"..the.go..".*") then
      for k,v in pairs(saved) do the[k]=v end
      Seed = the.seed
      math.randomseed(Seed)
      print(fmt("\n▶️  %s %s",k,("-"):rep(60)))
      ok,val = pcall(pair.fun)
      if not ok         then n=n+1; sayln("❌ FAIL %s %s",k,val); 
                                    sayln(debug.traceback()) 
      elseif val==false then n=n+1; sayln("❌ FAIL %s",k)
      else                   y=y+1; sayln("✅ PASS %s",k) end end end
  if y+n>0 then sayln("\n🔆 %s\n",o({pass=y, fail=n, success=100*y/(y+n)//1})) end
  rogues()
  return fails end

-- Return any rogue locals (i.e. all those we did not
-- trap in the `b4` list at top of file).
function rogues() 
  for k,v in pairs(_ENV) do 
    if not b4[k] then print(fmt("#W ?%s %s",k,type(v))) end end end

-- Update `t` using command-line options. For boolean
-- flags, just flip the default values. For others, read
-- the new value from the command line.
function cli(t)
  for k,v in pairs(t) do
    v = tostring(v)
    for n,x in ipairs(arg) do
      if x=="-"..(k:sub(1,1)) or x=="--"..k then
        v= v=="false" and "true" or v=="true" and "false" or arg[n+1] end end 
    t[k] = coerce(v) end 
  return t end

-- ## <a name=egs>Examples</a>

-- Place to store examples.
local egs = {}
help = help .. "\nACTIONS:\n"

-- Used `go` to define an example
function go(key,xplain,fun)
  help =  help ..fmt("  -g  %s\t%s\n",key,xplain)
  egs[1+#egs] = {key=key,fun=fun} end

-- Disable an example by renaming it `no`. 
function no(_,__,___) return true end

go("the","show options",function() oo(the) end)

go("rand","demo random number generation", function(     t,u)
  Seed=1; t={}; for i=1,1000 do push(t,rint(100)) end
  Seed=1; u={}; for i=1,1000 do push(u,rint(100)) end
  for k,v in pairs(t) do assert(v==u[k]) end end)

go("some","demo of reservoir sampling", function(     num1)
  the.Max = 32
  num1 = NUM()
  for i=1,10000 do add(num1,i) end
  oo(has(num1)) end)

go("nums","demo of NUM", function(     num1,num2)
  num1,num2 = NUM(), NUM()
  for i=1,10000 do add(num1, rand()) end
  for i=1,10000 do add(num2, rand()^2) end
  print(1,rnd(mid(num1)), rnd(div(num1)))
  print(2,rnd(mid(num2)), rnd(div(num2))) 
  return .5 == rnd(mid(num1)) and mid(num1)> mid(num2) end)

go("syms","demo SYMS", function(    sym)
  sym=adds(SYM(), {"a","a","a","a","b","b","c"})
  print (mid(sym), rnd(div(sym))) 
  return 1.38 == rnd(div(sym)) end)

go("csv","reading csv files", function(     n)
  n=0; csv(the.file, function(t) n=n+#t end) 
  return 3192 == n end)

go("data", "showing data sets", function(    data,col) 
  data=DATA.read(the.file)
  col=data.cols.x[1]
  print(col.lo,col.hi, mid(col),div(col))
  oo(stats(data)) end)

go("clone","replicate structure of a DATA",function(    data1,data2)
  data1=DATA.read(the.file)
  data2=DATA.clone(data1,data1.rows) 
  oo(stats(data1))
  oo(stats(data2)) end)

go("cliffs","stats tests", function(   t1,t2,t3)
  assert(false == cliffsDelta( {8,7,6,2,5,8,7,3},{8,7,6,2,5,8,7,3}),"1")
  assert(true  == cliffsDelta( {8,7,6,2,5,8,7,3}, {9,9,7,8,10,9,6}),"2") 
  t1,t2={},{}
  for i=1,1000 do push(t1,rand()) end --rand()/10) end
  for i=1,1000 do push(t2,rand()^.5) end --rand()*10) end
  assert(false == cliffsDelta(t1,t1),"3") 
  assert(true  == cliffsDelta(t1,t2),"4") 
  local diff,j=false,1.0
  while not diff  do
    t3=map(t1,function(x) return x*j end)
    diff=cliffsDelta(t1,t3)
    print(">",rnd(j),diff) 
    j=j*1.025 end end)

go("dist","distance test", function(    data,num)
  data = DATA.read(the.file)
  num  = NUM()
  for _,row in pairs(data.rows) do
    add(num,dist(data, row, data.rows[1])) end
  oo{lo=num.lo, hi=num.hi, mid=rnd(mid(num)), div=rnd(div(num))} end)

go("half","divide data in halg", function(   data,l,r)
  data = DATA.read(the.file)
  local left,right,A,B,c = half(data) 
  print(#left,#right)
  l,r = DATA.clone(data,left), DATA.clone(data,right)
  print("l",o(stats(l)))
  print("r",o(stats(r))) end)
 
go("tree","make snd show tree of clusters", function(   data,l,r)
  showTree(tree(DATA.read(the.file))) end)

go("sway","optimizing", function(    data,best,rest)
  data = DATA.read(the.file)
  best,rest = sway(data)
  print("\nall ", o(stats(data))) 
  print("    ",   o(stats(data,div))) 
  print("\nbest", o(stats(best))) 
  print("    ",   o(stats(best,div))) 
  print("\nrest", o(stats(rest))) 
  print("    ",   o(stats(rest,div))) 
  print("\nall ~= best?", o(diffs(best.cols.y, data.cols.y)))
  print("best ~= rest?", o(diffs(best.cols.y, rest.cols.y))) end)

go("bins", "find deltas between best and rest", function(    data,best,rest, b4)
  data = DATA.read(the.file)
  best,rest = sway(data)
  print("all","","","",o{best=#best.rows, rest=#rest.rows})
  for k,t in pairs(bins(data.cols.x,{best=best.rows, rest=rest.rows})) do
    for _,range in pairs(t) do
      if range.txt ~= b4 then print"" end
      b4 = range.txt
      print(range.txt,range.lo,range.hi,
           rnd(value(range.y.has, #best.rows,#rest.rows,"best")), 
           o(range.y.has)) end end end)

-- ## Start-up

--  Parse the `help` string to make the `the` config variables.
help:gsub(magic, function(k,v) the[k] = coerce(v) end)

-- If not being loaded by other file, then return whatever `main` returns.
if   not pcall(debug.getlocal,4,1) 
then os.exit( main(egs, cli(the), help) ) end

-- Else, bundle the locals (so the other file can use them), and return them.
local _locals,_i={},1 
while true do
  local _name, _value = debug.getlocal(1, _i)
  if not _name then break end
  if _name:sub(1,1) ~= "_" then _locals[_name]=_value end
  _i = _i + 1 end
return _locals  
