---                                           __      
---                           __             /\ \__   
---     ____    ___    _ __  /\_\    _____   \ \ ,_\  
---    /',__\  /'___\ /\`'__\\/\ \  /\ '__`\  \ \ \/  
---   /\__, `\/\ \__/ \ \ \/  \ \ \ \ \ \L\ \  \ \ \_ 
---   \/\____/\ \____\ \ \_\   \ \_\ \ \ ,__/   \ \__\
---    \/___/  \/____/  \/_/    \/_/  \ \ \/     \/__/
---                                    \ \_\          
---                                     \/_/          
local the,help = {},[[   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE:   script.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
]]
local b4={}; for k,v in pairs(_ENV) do b4[k]=v end -- cache old names (so later, we can find rogues)
-----------------------------------------------------------------------------------------
-- ## Classes
local id,obj=0
function obj(s,    t,new) --> t; create a klass and a constructor 
  function new(_,...) id=id+1; local i=setmetatable({a=s,id=id}, t); t.new(i,...); return i end
  t={}; t.__index = t;return setmetatable(t, {__call=new}) end

-- ### SYM
-- Summarize a stream of symbols.
local NUM,SYM = obj"NUM",obj"SYM"
function SYM.new(i) --> SYM; constructor
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

-- ### NUM
-- Summarizes a stream of numbers.
function NUM.new(i) --> NUM;  constructor; 
  i.n, i.mu, i.m2 = 0, 0, 0
  i.lo, i.hi = math.huge, -math.huge end

function NUM.add(i,n) --> NUM; add `n`, update lo,hi and stuff needed for standard deviation
  if n ~= "?" then
    i.n  = i.n + 1
    local d = n - i.mu
    i.mu = i.mu + d/i.n
    i.m2 = i.m2 + d*(n - i.mu)
    i.lo = math.min(n, i.lo)
    i.hi = math.max(n, i.hi) end end

function NUM.mid(i,x) return i.mu end --> n; return mean
function NUM.div(i,x)  --> n; return standard deviation using Welford's algorithm http://t.ly/nn_W
    return (i.m2 <0 or i.n < 2) and 0 or (i.m2/(i.n-1))^0.5  end
-------------------------------------------------------------------------------
-- ## Misc support functions
-- ### Numerics
local Seed,rand,rint,rnd
Seed=937162211
function rint(lo,hi) return math.floor(0.5 + rand(lo,hi)) end --> n ; a integer lo..hi-1

function rand(lo,hi) --> n; a float "x" lo<=x < x
  lo, hi = lo or 0, hi or 1
  Seed = (16807 * Seed) % 2147483647
  return lo + (hi-lo) * Seed / 2147483647 end

function rnd(n, nPlaces) --> num. return `n` rounded to `nPlaces`
  local mult = 10^(nPlaces or 3)
  return math.floor(n * mult + 0.5) / mult end

-- ### Lists
local map,kap,sort,keys
-- Note the following conventions for `map`.
-- - If a nil first argument is returned, that means :skip this result"
-- - If a nil second argument is returned, that means place the result as position size+1 in output.
-- - Else, the second argument is the key where we store function output.
function map(t, fun,     u) --> t; map a function `fun`(v) over list (skip nil results) 
  u={}; for k,v in pairs(t) do v,k=fun(v); u[k or (1+#u)]=v end;  return u end
 
function kap(t, fun,     u) --> t; map function `fun`(k,v) over list (skip nil results) 
  u={}; for k,v in pairs(t) do v,k=fun(k,v); u[k or (1+#u)]=v; end; return u end

function sort(t, fun) --> t; return `t`,  sorted by `fun` (default= `<`)
  table.sort(t,fun); return t end

function keys(t) --> ss; return list of table keys, sorted
  return sort(kap(t, function(k,_) return k end)) end

-- ### Strings
local fmt,oo,o,coerce
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

-- ### Main
local settings, cli,main
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
-- the start up actions (and before each run, it resets the random number seed and settongs);
-- and, finally, returns the number of test crashed to the operating system.
function main(options,help,funs,     k,saved,fails)  --> nil; main program
  saved,fails={},0
  for k,v in pairs(cli(settings(help))) do options[k] = v; saved[k]=v end 
  if options.help then print(help) else 
    for what,fun in pairs(funs) do
      if options.go=="all" or what==options.go then
         for k,v in pairs(saved) do options[k]=v end
         Seed = options.seed
         if funs[what]()==false then fails=fails+1
                                     print("❌ fail:",what) 
                                else print("✅ pass:",what) end end end end
  for k,v in pairs(_ENV) do 
    if not b4[k] then print( fmt("#W ?%s %s",k,type(v)) ) end end 
  os.exit(fails) end 
-------------------------------------------------------------------------------
--- ## Examples
local egs={}
local function eg(key,str, fun) --> nil; register an example.
  egs[key]=fun
  help=help..fmt("  -g  %s\t%s\n",key,str) end

--- eg("crash","show crashing behavior", function()
---   return the.some.missing.nested.field end)

eg("the","show settings",function() oo(the) end)

eg("rand","generate, reset, regenerate same", function()
  local num1,num2 = NUM(),NUM()
  Seed=the.seed; for i=1,10^3 do num1:add( rand(0,1) ) end
  Seed=the.seed; for i=1,10^3 do num2:add( rand(0,1) ) end
  local m1,m2 = rnd(num1:mid(),10), rnd(num2:mid(),10)
  return m1==m2 and .5 == rnd(m1,1) end )

eg("sym","check syms", function()
  local sym=SYM()
  for _,x in pairs{"a","a","a","a","b","b","c"} do sym:add(x) end
  return "a"==sym:mid() and 1.379 == rnd(sym:div())end)

eg("num", "check nums", function()
  local num=NUM()
  for _,x in pairs{1,1,1,1,2,2,3} do num:add(x) end
  return 11/7 == num:mid() and 0.787 == rnd(num:div()) end )

main(the,help, egs)
