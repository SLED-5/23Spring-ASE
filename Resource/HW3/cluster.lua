---             ___                        __                     
---            /\_ \                      /\ \__                  
---      ___   \//\ \     __  __    ____  \ \ ,_\     __    _ __  
---     /'___\   \ \ \   /\ \/\ \  /',__\  \ \ \/   /'__`\ /\`'__\
---    /\ \__/    \_\ \_ \ \ \_\ \/\__, `\  \ \ \_ /\  __/ \ \ \/ 
---    \ \____\   /\____\ \ \____/\/\____/   \ \__\\ \____\ \ \_\ 
---     \/____/   \/____/  \/___/  \/___/     \/__/ \/____/  \/_/ 
                                                           
local the,help = {},[[   
cluster.lua : an example csv reader script
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE: cluster.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../etc/data/auto93.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512

ACTIONS:
]]
local b4={}; for k,v in pairs(_ENV) do b4[k]=v end -- lua trivia (used to find rogue locals)
local id,obj=0 --classes
local cosine,Seed,rand,rint,rnd --maths
local map,kap,sort,keys,push,any,many,lt --lists
local fmt,oo,o,coerce,csv,show --strings
local settings,cli,main --settings
-----------------------------------------------------------------------------------------
-- ## Classes
function obj(s,    t,new) --> t; create a klass and a constructor 
  function new(_,...) id=id+1; local i=setmetatable({a=s,id=id}, t); t.new(i,...); return i end
  t={}; t.__index = t;return setmetatable(t, {__call=new}) end

local NUM,SYM,ROW,COLS,DATA = obj"NUM",obj"SYM",obj"ROW",obj"COLS",obj"DATA"
-- ### SYM
-- Summarize a stream of symbols.
function SYM.new(i,at,txt) --> SYM; constructor
  i.at, i.txt = at or 0, txt or "" -- col position and name
  i.n   = 0
  i.has = {}
  i.most, i.mode = 0,nil end

function SYM.add(i,x) --> nil;  update counts of things seen so far
  if x ~= "?" then 
   i.n = i.n + 1 
   i.has[x] = 1 + (i.has[x] or 0)
   if i.has[x] > i.most then
     i.most,i.mode = i.has[x], x end end end 

function SYM.mid(i,x) return i.mode end --> n; return the mode

function SYM.div(i,x,    fun,e) --> n; return the entropy
  function fun(p) return p*math.log(p,2) end
  e=0; for _,n in pairs(i.has) do e = e + fun(n/i.n) end 
  return -e end

function SYM.rnd(i,x,n) return x end --> s; return `n` unchanged (SYMs do not get rounded)

function SYM.dist(i,s1,s2)
  return s1=="?" and s2=="?" and 1 or (s1==s2) and 0 or 1 end 
-- ### NUM
-- Summarizes a stream of numbers.
function NUM.new(i,at,txt) --> NUM;  constructor; 
  i.at, i.txt = at or 0, txt or "" -- column position and name
  i.n, i.mu, i.m2 = 0, 0, 0
  i.lo, i.hi = math.huge, -math.huge 
  i.w = i.txt:find"-$" and -1 or 1 end

function NUM.add(i,n,    d) --> NUM; add `n`, update lo,hi and stuff needed for standard deviation
  if n ~= "?" then
    i.n  = i.n + 1
    d = n - i.mu
    i.mu = i.mu + d/i.n
    i.m2 = i.m2 + d*(n - i.mu)
    i.lo = math.min(n, i.lo)
    i.hi = math.max(n, i.hi) end end

function NUM.mid(i,x) return i.mu end --> n; return mean

function NUM.div(i,x)  --> n; return standard deviation using Welford's algorithm http://.ly/nn_W
    return (i.m2 <0 or i.n < 2) and 0 or (i.m2/(i.n-1))^0.5  end

function NUM.rnd(i,x,n) return x=="?" and x or rnd(x,n) end --> n; return number, rounded

function NUM.norm(i,n)
  return n == "?" and n  or (n - i.lo)/(i.hi - i.lo + 1E-32) end

function NUM.dist(i,n1,n2)
  if n1=="?" and n2=="?" then return 1 end
  n1,n2 = i:norm(n1), i:norm(n2)
  if n1=="?" then n1 = n2<.5 and 1 or 0 end
  if n2=="?" then n2 = n1<.5 and 1 or 0 end
  return math.abs(n1 - n2) end 

-- ### COLS
-- Factory for managing a set of NUMs or SYMs
function COLS.new(i,t,     col,cols) --> COLS; generate NUMs and SYMs from column names
  i.names, i.all, i.x, i.y, i.klass = t, {}, {}, {}
  for n,s in pairs(t) do  -- like PYTHONS's for n,s in enumerate(t) do..
    col = s:find"^[A-Z]+" and NUM(n,s) or SYM(n,s)
    push(i.all, col)
    if not s:find"X$" then
      if s:find"!$" then i.klass = col end
      push(s:find"[!+-]$" and i.y or i.x, col) end end end

function COLS.add(i,row) --> nil; update the (not skipped) columns with details from `row`
  for _,t in pairs({i.x,i.y}) do 
    for _,col in pairs(t) do
      col:add(row.cells[col.at]) end end end

-- ### ROW
-- Store one record.
function ROW.new(i,t) i.cells=t; end --> ROW; 
--
-- ### DATA
-- Store many rows, summarized into columns
function DATA.new(i,src,     fun) --> DATA; A container of `i.rows`, to be summarized in `i.cols`
  i.rows, i.cols = {}, nil
  fun = function(x) i:add(x) end
  if type(src) == "string" then csv(src,fun)  -- load from a csv file on disk
                           else map(src or {}, fun)  --  load from a list
                           end end
  
function DATA.add(i,t) --> nil; add a new row, update column headers
  if   i.cols          --] true if we have already seen the column names
  then t = t.cells and t or ROW(t) -- ensure is a ROW, reusing old rows in the are passed in
       -- t =ROW(t.cells and t.cells or t) -- make a new ROW
       push(i.rows, t) -- add new data to "i.rows"
       i.cols:add(t)  -- update the summary information in "ic.ols"
  else i.cols=COLS(t)  end end --  here, we create "i.cols" from the first row

function DATA.clone(i,  init,     data) --> DATA; return a DATA with same structure as `ii. 
  data=DATA({i.cols.names})
  map(init or {}, function(x) data:add(x) end)
  return data end

function DATA.stats(i,  what,cols,nPlaces,fun) --> t; reports mid or div of cols (defaults to i.cols.y)
  function fun(k,col) return col:rnd(getmetatable(col)[what or "mid"](col),nPlaces),col.txt end
  return kap(cols or i.cols.y, fun) end

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

-------------------------------------------------------------------------------
-- ## Misc support functions
function show(node,what,cols,nPlaces,    lvl) --> nil; prints the tree generated from `DATA:tree`.
  if node then
    lvl = lvl or 0
    io.write(("| "):rep(lvl)..#node.data.rows.."  ")
    print((not node.left or lvl==0) and  o(node.data:stats("mid",node.data.cols.y,nPlaces)) or "")
    show(node.left, what,cols, nPlaces, lvl+1)
    show(node.right, what,cols,nPlaces, lvl+1) end end

-- ### Numerics
Seed=937162211
function rint(lo,hi) return math.floor(0.5 + rand(lo,hi)) end --> n; a integer lo..hi-1

function rand(lo,hi) --> n; a float "x" lo<=x < x
  lo, hi = lo or 0, hi or 1
  Seed = (16807 * Seed) % 2147483647
  return lo + (hi-lo) * Seed / 2147483647 end

function rnd(n, nPlaces) --> num; return `n` rounded to `nPlaces`
  local mult = 10^(nPlaces or 3)
  return math.floor(n * mult + 0.5) / mult end

function cosine(a,b,c,    x1,x2,y) --> n,n;  find x,y from a line connecting `a` to `b`
  x1 = (a^2 + c^2 - b^2) / (2*c)
  x2 = math.max(0, math.min(1, x1)) -- in the incremental case, x1 might be outside 0,1
  y  = (a^2 - x2^2)^.5
  return x2, y end
-- ### Lists
-- Note the following conventions for functions passed to  `map` or `kap`.
-- - If a nil first argument is returned, that means :skip this result"
-- - If a nil second argument is returned, that means place the result as position size+1 in output.
-- - Else, the second argument is the key where we store function output.
function map(t, fun,     u) --> t; map a function `fun`(v) over list (skip nil results) 
  u={}; for k,v in pairs(t) do v,k=fun(v); u[k or (1+#u)]=v end;  return u end
 
function kap(t, fun,     u) --> t; map function `fun`(k,v) over list (skip nil results) 
  u={}; for k,v in pairs(t) do v,k=fun(k,v); u[k or (1+#u)]=v; end; return u end

function sort(t, fun) --> t; return `t`,  sorted by `fun` (default= `<`)
  table.sort(t,fun); return t end

function lt(x) --> fun;  return a function that sorts ascending on `x`
  return function(a,b) return a[x] < b[x] end end

function keys(t) --> ss; return list of table keys, sorted
  return sort(kap(t, function(k,_) return k end)) end

function push(t, x) --> any; push `x` to end of list; return `x` 
  table.insert(t,x); return x end

function push(t, x) --> any; push `x` to end of list; return `x` 
  table.insert(t,x); return x end

function any(t) return t[rint(#t)] end  --> x; returns one items at random

function many(t,n,    u)  --> t1; returns some items from `t`
   u={}; for i=1,n do u[1+#u]=any(t) end; return u end

-- ### Strings
function fmt(sControl,...) --> str; emulate printf
  return string.format(sControl,...) end

function oo(t) print(o(t)); return t end --> t; print `t` then return it
function o(t,isKeys,     fun) --> s; convert `t` to a string. sort named keys. 
  if type(t)~="table" then return tostring(t) end
  fun= function(k,v) if not tostring(k):find"^_" then return fmt(":%s %s",o(k),o(v)) end end
  return "{"..table.concat(#t>0 and not isKeys and map(t,o) or sort(kap(t,fun))," ").."}" end

function coerce(s,    fun) --> any; return int or float or bool or string from `s`
  function fun(s1)
    if s1=="true" then return true elseif s1=="false" then return false end
    return s1 end
  return math.tointeger(s) or tonumber(s) or fun(s:match"^%s*(.-)%s*$") end

function csv(sFilename,fun,    src,s,t) --> nil; call `fun` on rows (after coercing cell text)
  src,s,t  = io.input(sFilename)
  while true do
    s = io.read()
    if   s
    then t={}; for s1 in s:gmatch("([^,]+)") do t[1+#t]=coerce(s1) end; fun(t)
    else return io.close(src) end end end

-- ### Main
function settings(s,    t) --> t;  parse help string to extract a table of options
  t={};s:gsub("\n[%s]+[-][%S]+[%s]+[-][-]([%S]+)[^\n]+= ([%S]+)",function(k,v) t[k]=coerce(v) end)
  return t end

function cli(options) --> t; update key,vals in `t` from command-line flags
  for k,v in pairs(options) do
    v=tostring(v)
    for n,x in ipairs(arg) do
      if x=="-"..(k:sub(1,1)) or x=="--"..k then
         v = v=="false" and "true" or v=="true" and "false" or arg[n+1] end end
    options[k] = coerce(v) end 
  return options end

-- `main` fills in the settings, updates them from the command line, runs
-- the start up actions (and before each run, it resets the random number seed and settings);
-- and, finally, returns the number of test failures  to the operating system.
function main(options,help,funs,     saved,fails)  --> nil; main program
  saved,fails={},0
  for k,v in pairs(cli(settings(help))) do options[k] = v; saved[k]=v end 
  if options.help then print(help) else 
    for _,what in pairs(keys(funs)) do
      if options.go=="all" or what==options.go then
         for k,v in pairs(saved) do options[k]=v end
         Seed = options.seed
         if funs[what]()==false then fails=fails+1
                                     print("❌ fail:",what) 
                                else print("✅ pass:",what) end end end end
  for k,v in pairs(_ENV) do -- LUA trivia. Looking for rogue locals
    if not b4[k] then print( fmt("#W ?%s %s",k,type(v)) ) end end 
  os.exit(fails) end  -- returns failure count. and count==0 means "success!"
-------------------------------------------------------------------------------
--- ## Examples
local egs,eg={}
function eg(key,str, fun) --> nil; register an example.
  egs[key]=fun
  help=help..fmt("  -g  %s\t%s\n",key,str) end

--- eg("crash","show crashing behavior", function()
---   return the.some.missing.nested.field end)

eg("the","show settings",function() oo(the) end)

eg("sym","check syms", function()
  local sym=SYM()
  for _,x in pairs{"a","a","a","a","b","b","c"} do sym:add(x) end
  return "a"==sym:mid() and 1.379 == rnd(sym:div())end)

eg("num", "check nums", function()
  local num=NUM()
  for _,x in pairs{1,1,1,1,2,2,3} do num:add(x) end
  return 11/7 == num:mid() and 0.787 == rnd(num:div()) end )

eg("data","read DATA csv", function(     data) 
  data=DATA(the.file)
  return #data.rows == 398 and
         data.cols.y[1].w == -1 and
         data.cols.x[1].at == 1 and 
         #data.cols.x==4 end)

eg("clone", "duplicate structure", function(     data1,data2)
  data1=DATA(the.file)
  data2=data1:clone(data1.rows)
  return #data1.rows == #data2.rows and
         data1.cols.y[1].w == data2.cols.y[1].w and
         data1.cols.x[1].at == data2.cols.x[1].at and 
         #data1.cols.x==#data2.cols.x end)

eg("around", "sorting nearest neighbors", function(     data)
  data=DATA(the.file)
  print(0,0,o(data.rows[1].cells))
  for n,t in   pairs(data:around(data.rows[1])) do
    if n %50 ==0 then print(n, rnd(t.dist,2) ,o(t.row.cells)) end end end)

eg("half", "1-level bi-clustering", function(     data)
  data=DATA(the.file)
  local left,right,A,B,mid,c = data:half() 
  print(#left,#right,#data.rows)
  print(o(A.cells),c)
  print(o(mid.cells)) 
  print(o(B.cells)) end)

eg("cluster", "N-level bi-clustering", function(     data)
  data=DATA(the.file)
  show(data:cluster(),"mid",data.cols.y,1)
  end)

eg("optimize", "semi-supervised optimization", function(     data)
  data=DATA(the.file)
  show(data:sway(),"mid",data.cols.y,1)
  end)

main(the,help,egs)
