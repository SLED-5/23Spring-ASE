<small><p>&nbsp;
<a name=top></a>
<table><tr> 
<td><a href="/README.md#top">home</a>
<td><a href="/ROADMAP.md">roadmap</a>
<td><a href="http:github.com/timm/tested/issues">issues</a>
<td> <a href="/LICENSE.md">&copy;2022,2023</a> by <a href="http://menzies.us">tim menzies</a>
</tr></table></small>
<img  align=center width=600 src="/docs/img/banner.png"></p>
<p> <img src="https://img.shields.io/badge/task-ai-blueviolet"><a
href="https://github.com/timm/tested/actions/workflows/tests.yml"> <img 
 src="https://github.com/timm/tested/actions/workflows/tests.yml/badge.svg"></a> <img 
 src="https://img.shields.io/badge/language-lua-orange"> <img 
 src="https://img.shields.io/badge/purpose-teaching-yellow"> <a 
 href="https://zenodo.org/badge/latestdoi/569981645"> <img 
 src="https://zenodo.org/badge/569981645.svg" alt="DOI"></a></p>


# Scripting Tricks


If you look at my code, there are some common things:


- written in  a version control systems (Github)
- undergoing continuous integration every time  I commit anything (e.g. resteting all scripts) 
- coded in LUA
- an initial help string (from which I derive global settings)
  - this is used to drive a really simple way to control the code via command-line flags
- a random number generator (which is initialized from one the settings in the help string)
- a reader system that inputs CSV files with named columns
  - this generated a data model of five classes seen in most of my code (DATA, ROW, COLS, NUM, SYM)
  - which is all in [next lecture](/docs/onData.md)


## Version Contol


A "good" repository has "bling" boasting its competency (see my badges above).
- To build you own bling, see [https://shields.io/](https://shields.io/).
- Make sure your bling includes
  - Something that links to your GH tests: <a href="https://github.com/timm/tested/actions/workflows/tests.yml"> <img src="https://github.com/timm/tested/actions/workflows/tests.yml/badge.svg"></a> 
  - Something that shows you are running long term backups of your repo: <a href="https://zenodo.org/badge/latestdoi/569981645"> <img src="https://zenodo.org/badge/569981645.svg" alt="DOI"></a>


|Recommended files | Notes |
|------------------:|:------|
| /.gitignore | lists of files never to commit (e.g. compiler intermediaries). To find the right ignores for your tools, see the [Github ignore repo](https://github.com/github/gitignore/) |
| [/.github/workflows/tests.yaml](.github/workflows/tests.yml) | on each commit, runs the /src/lua files with `lua file.lua -g all` and reports a crash if any produce a non-zero error code|
| /CITATION.cff | for bibliography information<br>To make your own file, use [this generator](https://citation-file-format.github.io/cff-initializer-javascript/#/) |
| /LICENSE.md  | open source license<br>To browse different licenses, go to [choose a license](https://choosealicense.com/licenses/)| 
| /Makefile| for any tricky scripting stuff: pretty tricky stuff (not for everyone)<br>For notes on cool Makefile tricks, see [Automation and Make](https://swcarpentry.github.io/make-novice/08-self-doc/index.html)|
| /README.md| top-level doco file|
| /docs | for markdown files<br> Anything starting with `on*` is a lecture file. All other files are generated from the comments in the files in `/src/*.lua`.|
| /etc | for local config files|
| /etc/img | for images|
| /etc/out | cache for experimental output logs|
| /src | for code|


## About LUA


I use LUA as an executable specification language. Students rewrite
my code in whatever language they like (that is not LUA).  


- For quick tutorials on LUA, see  [learnlua](https://learnxinyminutes.com/docs/lua/)
- For full details on LUA, see the [Programming in LUA](https://www.lua.org/pil/contents.html) book.


LUA is an ultra lightweight scripting language comprising less than
two dozen keywords: **and, break, do, else, elseif, end, false, for, function, if, in, local, nil, not, or, repeat, return, then, true, until, while**.  
LUA has a considerably smaller footprint
than other programming languages
(with its complete source code and
documentation taking a mere 1.3 MB).  Despite this it is very powerful language
For example, here is define generic N-levels deep print function for LUA lists, as well
as the mapping functions that makes that so simple to implement:
```lua
fmt=string.format
function sort(t, fun) table.sort(t,fun); return t end


function map(t, fun,     u) --> t; map a function `fun`(v) over list (skip nil results) 
  u={}; for k,v in pairs(t) do v,k=fun(v); u[k or (1+#u)]=v end;  return u end


  function kap(t, fun,     u) --> t; map function `fun`(k,v) over list (skip nil results) 
  u={}; for k,v in pairs(t) do v,k=fun(k,v); u[k or (1+#u)]=v; end; return u end


function show (k,v) if not tostring(k):find"^_" then return fmt(":%s %s",o(k),o(v)) end end


function o(t,flag)
  if type(t)~="table" then return tostring(t) end
  return "{"..table.concat(#t>0 and not flag and map(t,o) 
                                or sort(kap(t,show)),
                           " ").."}" end
```
Note that in the above, functions can be  treated as variables; i,e, LUA
has first-class functions. LUA also has tail call optimization which means functions
that call themselves as the last step in their code can recurse indefinitely.
I actually view LUA as LISP
(without
  (all
    (those
      (infuriating
        (silly
           (parentheses)))))).


### Some Coding Convetions
- The help file /docs/X.md is generated from the doco in /src/X.lua
- Vars are global by default unless marked with "local" or 
   defined in function argument lists.
- Functions must be  names before they are used
- There is only one underling data structure (a table):
  - Tables can have numeric or symbolic keys.
  - Simple tables have consecutive numeric keys amd are said to have size #t>0i
  - Other tables have symbolic keys and are said to have size #t==0.
- Tables start and end with {}
- Global settings are stores in `the` table which is generated from
  `help`. E.g. from the above the.budget =16
- For all `key=value` in `the`, a command line flag `-k X` means `value`=X
- At startup, we run `go[the.go]`
- `for pos,x in pairs(t) do` is the same as python's 
  `for pos,x in enumerate(t) do`
- In my object system, instances are named `i` (since that is shorter than `self`)


In the public function arguments, the following conventions apply (usually):
- Four spaces denote start of local args.  
- Two spaces denote start of optional args
- n = number; e.g. n, nItems, n1
- s = string; e.g. s, sName, s1
- t = table; e.g. t, t1
- is = boolean; e.g. isHappy
- x = anything; e.g x
- fun = function; e.g. fun, accessFun
- UPPER = class; e.g. NUM
- lower = instance; e.g. num,num1
- xs = a table of "x"; e.g. ns is a list of numbers and ss is a list of strings.
  


## Test-Drive Development


Have lots of unit tests!  
Run them, a lot!   
Get them all passing before checking back to main!   
Do not make test-driven development into a  religion!   


<img src="https://github.com/txt/se20/blob/master/etc/img/tddscreen.png">


Tests suites that run every time you save code


TDD= red, green, refactor
-  Build tests first
- Repeat:
  - Red = fund a broken test
  - Green= fix the test
  - Refactor= sometimes, clean things up
    - Refactoring means functionality _stays the same_ but the resulting _code is simpler_.


[^Karac]:  (2018)
 [What Do We (Really) Know about Test-Driven Development? ](https://www.researchgate.net/profile/Itir_Karac/publication/326239274_What_Do_We_Really_Know_about_Test-Driven_Development/links/5cee7550299bf1f881494cf6/What-Do-We-Really-Know-about-Test-Driven-Development.pdf)   
    Itir Karac and Burak Turhan
   TDD’s perceived superiority over, satm a test-last approach might have been due to the fact that most of the 
  experiments employed a coarse-grained test-last process closer to the waterfall
  approach as a control group


TDD perhaps oversold [^Karac].
- But, at the very least, it is  a great way to "get into the zone" faster, every morning
- Also, a good way to share code 
  - "what does your code do? lets look at the tests!"
  - "Hey, nice trick, lets document it in a trick so everyone can know it from now on"
 
The end of my code ends with a set of `eg` definitions for a test suite.
I've coded this many ways but some things are constant. 
- Each test has a short name [1]
- Each test has a longer help text [2]
- Each test includes some executable code [3].


E.g. here's a demo that normalizes all row cells:


```lua
-- [1] short name  [2] longer help text              [3] code function
eg("norm",         "does data normalization work?",  function()
  local data,rows,row,x
  data=DATA(the.file)
  for i=1,10 do 
    row = any(data.rows)
    for _,col in pairs(data.cols.x) do
      x = row.cells[col.at]
      print(x, col:norm(x))  end end end )
```
On the command line, this example can called with the `-g` flag ("g" for "go").
For example, to run the above:


```
lua code.lua -g norm
```
There is also a `all` flag which runs all tests:


```
lua code.lua -g all
```
If  test returns false, it is called a failure. When called with the `-g all` flag, the
numbers of failures is return to the operating system.


## Pseudo-random numbers
Just to show a sample of the code we are going to explore...
- Computers cannot  really do random numbers
  - and often you do not  want to
    - when debugging you want to reproduce a prior sequence.
- Psuedo-random numbers: 
  - Comptue a new number from a seed. Update the seed. Return the number.
  - To rerun old sequence, reset the seed
- Empirical notes: 
  - keep track of your seeds (reproducability)
  - always reset your seed in the right place (war story: 2 years of work lost)
- Here is a very simpler random generator [(Lehmer, aka Park-Miller)](https://en.wikipedia.org/wiki/Lehmer_random_number_generator). 
  Lets just say that more complex generators
  are much more complex:
  
```lua
Seed=937162211
function rand(lo,hi)
  lo, hi = lo or 0, hi or 1
  Seed = (16807 * Seed) % 2147483647
  return lo + (hi-lo) * Seed / 2147483647 end


function rint(lo,hi) return math.floor(0.5 + rand(lo,hi)) end
```


## Settings


The code using options whose defaults are defined and extracted from
a help string (offered at start of file):


```lua
local the,help={},[[  
fish1,lua : sort many <X,Y> things on Y, after peeking at just a few Y things
(c)2022 Tim Menzies <timm@ieee.org> BSD-2


Note: fish1 is just a demonststraing of this kind of processing.
It is designed to be incomplete, to have flaws. If you look at this
case say say "a better way to do this wuld be XYZ", then fish1 has
been successful.


USAGE: lua fish1.lua [OPTIONS] [-g [ACTIONS


OPTIONS:
  -b  --budget  number of evaluations = 16
  -f  --file    csv data file         = ../etc/data/auto93.csv
  -g  --go      start up action       = ls
  -h  --help    show help             = false
  -p  --p       distance coefficient  = 2
  -s  --seed    random number seed    = 10019


ACTIONS:
]] 
```
Note the hook from here to the above library
- at start up, my code runs eg[`the.go`] which has a default of `ls` and which can be changed on the command line using the `-g` flag;
- before running any demo, my code resets the seed to the value of `the.seed` which has a default value of `10019` and a which can be changed on the command-line using the `-s` flag.


The  parser is simple (if you understand  regular expression captures):


```lua
function settings(s,    t) 
  -- e.g.             -h           --help show help   = false
  t={};s:gsub("\n[%s]+[-][%S]+[%s]+[-][-]([%S]+)[^\n]+= ([%S]+)",
              function(k,v) t[k]=coerce(v) end)
  return t end


function coerce(s,    fun)
  function fun(s1)
    if s1=="true" then return true elseif s1=="false" then return false end
    return s1 end
  return math.tointeger(s) or tonumber(s) or fun(s:match"^%s*(.-)%s*$") end
```
The default settings can also be updated via the command-line
(which in LUA can be found in the `args` array):


```lua
function cli(options) 
  for k,v in pairs(options) do
    v=tostring(v)
    for n,x in ipairs(arg) do
      if x=="-"..(k:sub(1,1)) or x=="--"..k then
         v = v=="false" and "true" or v=="true" and "false" or arg[n+1] end end
    options[k] = coerce(v) end 
  return options end


the = cli(settings(help))
```
Note one short cut in the above:
- when the `cli` function looks for update, 
  - if the default is non-boolean then the flag `-x` must be followed by a value
  - if the default is a boolean, then the flag `-x` has no value (and the default is just inverted, so trues become falses and falses become trues)
