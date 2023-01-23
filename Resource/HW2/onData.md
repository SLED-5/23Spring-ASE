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


# How TESTED stores DATA


A repeated structure in my code are the following classes:


|class | notes |
|------|-------|
|NUM   | summarize stream of numbers|
|SYM   | summarize stream of symbols|
|ROW | container for one record |
|COLS  | factory for createing NUMs and SYms|
|DATA | container for ROWs, summaized into NUMs or SSYMs|


Conceptually there is a sixth class that is a super class
of NUM and SYM... but I don't actually implement that.


My CSV parser generates theses instances from data where row1 is some column headers 
and the other rows are the actual data.
```
Clndrs,Volume, HpX,  Lbs-,  Acc+,  Model, origin, Mpg+
4,      97,     52,  2130,  24.6,  82,    2,      40
4,      97,     54,  2254,  23.5,  72,    2,      20
4,      97,     78,  2188,  15.8,  80,    2,      30
4,     151,     90,  2950,  17.3,  82,    1,      30
6,     200,     ?,   2875,  17,    74,    1,      20
6,     146,     97,  2815,  14.5,  77,    3,      20
8,     267,    125,  3605,  15,    79,    1,      20
8,     307,    130,  4098,  14,    72,    1,      10
```
In these names:
- we skip columns whose names end in `X`;
- if the name starts in uppercase, we have a number
- if the name ends with "-" or "+" then its a goal we want to minimize or maximize
  - and for such items, we will set "w" to 1.


```
list of names      call                 weight    goal?
--------------     ----------------     ------    -----


{ "Clndrs",        NUM(1, "Clndrs")     1         n
  "Volume",        NUM(2, "Volume")     1         n
  "HpX",           NUM(3, "HpX")        1         n
  "Lbs-",          NUM(4, "Lbs-")         -1         y
  "Acc+",          NUM(5, "Acc+")       1            y
  "Model",         NUM(6, "Model")      1         n
  "origin",        SYM(7, "origin")               n
  "Mpg+"}          NUM(8, "Mgp+")       1            y
```
So the these CSV first line gets processed by a factory
that generates a set of goals `i.y` and other columns `i.x`:
```lua
COLS=obj"COLS"
function COLS.new(i,t,     col,cols)
  i.names, i.all, i.x, i.y = t, {}, {}, {}
  for n,s in pairs(t) do  -- like PYTHONS's for n,s in enumerate(t) do..
    col = s:find"^[A-Z]+" and NUM(n,s) or SYM(n,s)
    push(i.all, col)
    if not s:find"X$" then
      push(s:find"[!+-]$" and i.y or i.x, col) end end end
```
## DATA, ROW, COLS


```mermaid
classDiagram
COL <--  NUM
COL <--  SYM
DATA "1" -- "1..*" ROW  : rows 
DATA "1" -- "1" COLS  : cols
COLS "1" -- "1..*" COL  
class COLS {
   name: strs
   x : ROWs
   y : ROWs
   all: rows
}
class ROW {
  cells : lst
}
class COL {
  n,at: int,int
  txt: str
}
class NUM {
  w : -1 or 1
  mu,m2 : 0,0
  lo,hi: num
}
class SYM {
  has : dict
  mode : str
  most: 0
}
```


In the above, DATA is the ringmaster that controls eigjt special cases:


- DATA is loaded from either 
  - a disc csv file [1]
  - rows from some other source  [2]
- When receiving new data, that data could be
  - a simple list [3]
  - a ROW (which is a container for a list) [4]
- When that data arrives, it is either
  -the first row (with the column names) [5]
  - or it is all other other rows of data. [6]
- When we work with data, we can either share the same ROWs [7] (e.g.
  if we are recursively cluster the same data) 
  or make new rows each time [8].


```lua
function ROW.new(i,t) i.cells=t; i.yseen=false end


function DATA.new(i,src,     fun)
  i.rows, i.cols = {}, nil
  fun = function(x) i:add(x) end
  if type(src) == "string" then csv(src,fun)  -- [1] load from a csv file on disk
                           else map(src or {}, fun)  -- [2] load from a list
                           end end
  
function DATA.add(i,t)
  if   i.cols          -- [6] true if we have already seen the column names
  then t = t.cells and t or ROW(t) -- [3][4][7]
       -- t =ROW(t.cells and t.cells or t) -- [3][4][8] "t" can be a ROW or a simple list
       push(i.rows, t) -- add new data to "i.rows"
       i.cols:adds(t)  -- update the summary information in "ic.ols"
  else i.cols=COLS(t)  -- [5] here, we create "i.cols" from the first row
       end end
```
Note that adding something to DATA means also updating the column summaries:
```lua
function COLS.add(i,row)
  for _,t in pairs({i.x,i.y}) do -- update all the columns we are no skipping
    for _,col in pairs(t) do
      col:add(row.cells[col.at]) end end end
```
One thing we can do here is  create a new table with the identical structure. 
```lua
function DATA.clone(i,  init,     data)
  data=DATA({i.cols.names})
  map(init or {}, function(x) data:add(x) end)
  return data end
```


## SYM


When a DATA instance stores some rows,
those rows are summarized in NUM or SYM instances. Note that:
 NUM and SYM all have:
 - an `add` method (for updating stuff) and
 -  a `mid` method for reporting central tendancy (mid=middle)
- a `div` methods for reporting the diversion around that center (div=diversity)


```lua
local SYM = lib.obj"SYM"
function SYM:new() --> SYM; constructor
  self.n   = 0
  self.has = {}
  self.most, self.mode = 0,nil end


function SYM:add(x) --> nil;  update counts of things seen so far
  if x ~= "?" then
   self.n = self.n + 1
   self.has[x] = 1 + (self.has[x] or 0) -- if "x" not seen before, init counter to 0
   if self.has[x] > self.most then
     self.most,self.mode = self.has[x], x end end end


function SYM:mid(x) --> n; return the mode
  return self.mode end


function SYM:div(x) --> n; return the entropy
  local function fun(p) return p*math.log(p,2) end
  local e=0; for _,n in pairs(self.has) do e = e - fun(n/self.n) end
  return e end
```
<img src="https://miro.medium.com/max/720/1*mEIWwyolHOdY3TmBus7HtQ.webp" align=right width=400>


By the way, to understand SYM.div (entropy), think of it as
- the effort required by binary chop to find clumps of a signal hiding in a stream of noise
- and the more diverse the distribution, the greater that effort.


e.g. in a vector of size 4,
  - nazis have a "1" near one end
  - and England are all the other bits
- This means that 1/4% of the time we need to do binary chops to find nazies (i.e. $p_{\mathit{nazis}}=.25$)
- and 75% if the time we need to binary chops to find Englad (i.e. $p_{\mathit{england}}$=.75)
- Each chop will cost us $log2(p_i)$ so the total effort is $e=-\sum_i(p_i\times log_2(p_i))$ 
  - By convention, we  add a minus sign at the front (else all entropies will be negative).


(Actually, formally entropy has other definition: 
- The entropy of a discrete random variable is a lower bound on the expected number of bits required to transfer the result of the random variable.
- Also, entropy of continuous distributions is defined, but we do not use that in this subject.)


## NUM
```lua
local NUM = lib.obj"NUM"
function NUM:new() --> NUM;  constructor;
  self.n, self.mu, self.m2 = 0, 0, 0
  self.lo, self.hi = math.huge, -math.huge end


function NUM:add(n) --> NUM; add `n`, update min,max,standard deviation
  if n ~= "?" then
    self.n  = self.n + 1
    local d = n - self.mu
    self.mu = self.mu + d/self.n
    self.m2 = self.m2 + d*(n - self.mu)
    self.sd = (self.m2 <0 or self.n < 2) and 0 or (self.m2/(self.n-1))^0.5
    self.lo = math.min(n, self.lo)
    self.hi = math.max(n, self.hi) end end


function NUM:mid(x) return self.mu end --> n; return mean
function NUM:div(x) return self.sd end --> n; return standard deviation
```
If we are talking standard deviation, then we had better talk about normal curves.


The French mathematician Abraham de Moivre [^deMo1718]
  notes that probabilities associated with discretely 
  generated random variables (such as are obtained by flipping a coin or rolling a die) can 
  be approximated by the area under the graph of an exponential function.


This function was generalized by  Laplace[^Lap1812] 
  into the first central limit theorem, which proved that probabilities for almost 
  all independent and identically distributed random variables converge rapidly 
  (with sample size) to the area under an exponential function—that is, to a normal 
  distribution.


This function was extended, extensively by Gauss. Now its a curve with an area under the curve of one.
  As standard deviation shrinks, the curve spikes upwards.


<p align=center><img align=center src="/etc/img/norm.png" align=right width=600></p>


To sample from a normal curve
from a Gaussian with mean `mu` and diversity `sd`


      mu + sd * sqrt(-2*log(random)) * cos(2*pi*random)


_Beware:_
Not all things are normal Gaussians. 
<img src="/etc/img/weibull.png" align=right width=300 > If you want to get fancy, you can use Weibull functions
to make a variety of shapes (just by adjusting $\lambda,k$):


<p align=center><img src="/etc/img/weibulleq.png" wdith=300 ></p>


<br clear=all>


Another thing you should know is that even if normality holds, conclusions based on the normal curve (that hold
across the whole population) may not be appropriate for any individual in that population. Rose[^rose] offers two
examples of this:


<img src="https://images.thestar.com/content/dam/thestar/news/insight/2016/01/16/when-us-air-force-discovered-the-flaw-of-averages/norma.jpg" align=right width=300>


- Meet "Norma", a statue crafted in the 1940s from the average measurements of 15,000 women, from the
  United States (and if you want to meed "Normman", see
  [here](https://www.cabinetmagazine.org/issues/15/cambers.php)).
  In her time, "Norma" was something of a cultural icon:
  - A notable physical anthropologist argued that Norma’s physique was “a kind of perfection of bodily form,” 
  - artists proclaimed her beauty an “excellent standard” 
  - physical education instructors used her as a model for how young women should look, suggesting exercise based on a student’s deviation from the ideal.
  - But in reality, "Norma" did not exist.
    - In   1945, an American newspaper gave its  "Norma" prize to the woman who best matched this statue.
    - Only 40 of the 3,864 contestants were average size on just five of the nine dimensions 
    - No contestant (not even the winner) same close on all nine dimensions. 
- In 1950, worried about increasing number of crashes in their new jet fighters, the US Air Force double checked if their cockpits (designed for the average man, as measured by a 1926 study)
  was the right shape. 
  - Using measurement for 4,063 crew men, researchers asked how many fell within the mid 30% of values (across ten
  dimensions judged relevant to cockpit performance).
  - The answers was: zero , and less than 3.5 per cent of pilots where  average on any three dimensions.
  - Shocked, the US Air Force changed cockpits to include adjustable seats, pedals, etc. 
  - And the result?
    - Far fewer plane crashes, and far more potential pilots available for recruitment.
    - And you got adjustable seats in your car.


Or you could forget all about parametric assumptions.
Many things get improved by going beyond the Gaussian guess [^dou95]:
Not everything is best represented by a smooth curve with one peek that is symmetrical around that peek:


[^rose]: [When U.S. air force discovered the flaw of averages](https://www.thestar.com/news/insight/2016/01/16/when-us-air-force-discovered-the-flaw-of-averages.html)
  Toronto Star, Todd Rose
  Sat., Jan. 16, 2016


<img  align=right width=400 src="https://github.com/txt/fss17/raw/master/img/notnorm8.png">


To avoid the trap of the normal assumption, do things:
- like cluster the data and generate different conclusions per cluster.
- go fully non-parametric, use reservoir sampling (below). Then to sample, grab three numbers $a,b,c$ and use $x=a+f\times(b-c)$ for some small $f$ (say $f=0.1$).


All that said, Gaussians take up far less space and are very easy to update. So all engineers should know their gaussians.


And I find Gaussians better for small samples (under 20) than  using a  [Reservoir Sampler](/docs/onSome.md)


<br clear=all>


[^Cox07]:      [Regular Expression Matching Can Be Simple And Fast (but is slow in Java, Perl, PHP, Python, Ruby, ...)](https://swtch.com/~rsc/regexp/regexp1.html), 
  Russ Cox rsc@swtch.com, January 2007
[^deMo1718]:   Schneider, Ivor (2005), "Abraham De Moivre, The Doctrine of Chances (1718, 1738, 1756)", 
  in Grattan-Guinness, I. (ed.), Landmark Writings in Western Mathematics 1640–1940, Amsterdam: Elsevier, pp. 105–120, ISBN 0-444-50871-6.
[^dou95]: James Dougherty, Ron Kohavi, and Mehran Sahami. 1995. 
  [Supervised and unsupervised discretization of continuous features](https://ai.stanford.edu/~ronnyk/disc.pdf)
  In Proceedings of the Twelfth International Conference on International Conference 
  on Machine Learning (ICML'95). Morgan Kaufmann Publishers Inc., San Francisco, 
  CA, USA, 194–202.
[^Fisher38]:   Fisher, Ronald A.; Yates, Frank (1948) [1938]. Statistical tables for biological, agricultural and medical research (3rd ed.). 
  London: Oliver & Boyd. pp. 26–27. OCLC 14222135. 
[^Lap1812]:    Pierre-Simon Laplace, Théorie analytique des probabilités 1812, “Analytic Theory of Probability"
[^Lehmer69]:   W. H. Payne; J. R. Rabung; T. P. Bogyo (1969). "Coding the Lehmer pseudo-random number generator" (PDF). 
  Communications of the ACM. 12 (2): 85–86. doi:10.1145/362848.362860
[^ResXX]:      Bad me. I can recall where on the web I found this one.
[^Shannon48]:  Shannon, Claude E. (July 1948). "A Mathematical Theory of Communication". Bell System Technical Journal. 27 (3): 379–423. 
  doi:10.1002/j.1538-7305.1948.tb01338.x. hdl:10338.dmlcz/101429. 
  <a href="https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf">(PDF)</a>
[^Thom68]:     Ken Thompson, “Regular expression search algorithm,” Communications of the ACM 11(6) (June 1968), pp. 419–422. 
  http://doi.acm.org/10.1145/363347.363387 <a href="https://www.oilshell.org/archive/Thompson-1968.pdf">(PDF)</a>
[^Welford62]:  Welford, B. P. (1962). "Note on a method for calculating corrected sums of squares and products". Technometrics. 4 (3): 419–420. doi:10.2307/1266577. JSTOR 1266577.
