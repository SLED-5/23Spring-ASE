local the={bootstrap=512, conf=0.05, cliff=.4, cohen=.35,
  Fmt    = "%6.2f", width=40}

local function erf(x,    a1,a2,a3,a4,a5,p,sign,t)
    -- from Abramowitz and Stegun 7.1.26
    -- https://s3.amazonaws.com/nrbook.com/AandS-a4-v1-2.pdf
    -- (easier to read at https://en.wikipedia.org/wiki/Error_function#Approximation_with_elementary_functions)
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    -- Save the sign of x
    sign = 1
    if x < 0 then
        sign = -1
    end
    x = math.abs(x)
    -- A&S formula 7.1.26
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    return sign*y
end

local function gaussian(mu,sd)  --> n; return a sample from a Gaussian with mean `mu` and sd `sd`
  mu,sd = mu or 0, sd or 1
  local sq,pi,log,cos,r = math.sqrt,math.pi,math.log,math.cos,math.random
  return  mu + sd * sq(-2*log(r())) * cos(2*pi*r())  end

local function samples(t,n,    u)
  u= {}; for i=1,n or #t do u[i]=t[math.random(#t)] end; return u end

local function cliffsDelta(ns1,ns2) --> bool; true if different by a trivial amount
  local n,gt,lt = 0,0,0
  if #ns1> 128 then ns1 = samples(ns1,128) end
  if #ns2> 128 then ns2 = samples(ns2,128) end
  for _,x in pairs(ns1) do
    for _,y in pairs(ns2) do
      n = n + 1
      if x > y then gt = gt + 1 end
      if x < y then lt = lt + 1 end end end
  return math.abs(lt - gt)/n <= the.cliff end

local function add(i,x)
  i.n  = i.n+1
  d    = x-i.mu
  i.mu = i.mu + d/i.n
  i.m2 = i.m2 + d*(x-i.mu)
  i.sd = i.n<2 and 0 or (i.m2/(i.n - 1))^.5 end

function NUM(  t,    i)
  i= {n=0,mu=0,m2=0,sd=0}
  for _,x in pairs(t or {}) do add(i,x) end
  return i end

local function delta(i, other,      y,z,e)
  e, y, z= 1E-32, i, other
  return math.abs(y.mu - z.mu) / ((e + y.sd^2/y.n + z.sd^2/z.n)^.5) end

local function bootstrap(y0,z0)
  local n, x,y,z,xmu,ymu,zmu,yhat,zhat,tobs
  x, y, z, yhat, zhat = NUM(), NUM(), NUM(), {}, {}
  -- x will hold all of y0,z0
  -- y contains just y0
  -- z contains just z0
  for _,y1 in pairs(y0) do add(x,y1); add(y,y1) end
  for _,z1 in pairs(z0) do add(x,z1); add(z,z1) end
  xmu, ymu, zmu = x.mu, y.mu, z.mu
  -- yhat and zhat are y,z fiddled to have the same mean
  for _,y1 in pairs(y0) do yhat[1+#yhat] = y1 - ymu + xmu end
  for _,z1 in pairs(z0) do zhat[1+#zhat] = z1 - zmu + xmu end
  -- tobs is some difference seen in the whole space
  tobs = delta(y,z)
  n = 0
  for _= 1,the.bootstrap do
    -- here we look at some delta from just part of the space
    -- it the part delta is bigger than the whole, then increment n
    if delta(NUM(samples(yhat)), NUM(samples(zhat))) > tobs then n = n + 1 end end
  -- if we have seen enough n, then we are the same
  -- On Tuesdays and Thursdays I lie awake at night convinced this should be "<"
  -- and the above "> obs" should be "abs(delta - tobs) > someCriticalValue".
  return n / the.bootstrap >= the.conf end

function RX(t,s)
  table.sort(t)
  return {name=s or "", rank=0, n=#t, show="", has=t} end

function mid(t,     n)
  t= t.has and t.has or t
  local n = #t//2
  return #t%2==0 and (t[n] +t[n+1])/2 or t[n+1] end

function div(t)
  t= t.has and t.has or t
  return (t[ #t*9//10 ] - t[ #t*1//10 ])/2.56 end

function merge(rx1,rx2,    rx3)
  rx3 = RX({}, rx1.name)
  for _,t in pairs{rx1.has,rx2.has} do
     for _,x in pairs(t) do rx3.has[1+#rx3.has] = x end end
  table.sort(rx3.has)
  rx3.n = #rx3.has
  return rx3 end

function scottKnot(rxs,      all,cohen)
  local function merges(i,j,    out)
    out = RX({},rxs[i].name)
    for k = i, j do out = merge(out, rxs[j]) end
    return out
  end --------
  local function same(lo,cut,hi)
    l= merges(lo,cut)
    r= merges(cut+1,hi)
    return cliffsDelta(l.has, r.has) and bootstrap(l.has, r.has)
  end --------------------------
  local function recurse(lo,hi,rank)
    local cut,best,l,l1,r,r1,now,b4
    b4 = merges(lo,hi)
    best = 0
    for j = lo,hi do
      if j < hi  then
        l   = merges(lo,  j)
        r   = merges(j+1, hi)
        now = (l.n*(mid(l) - mid(b4))^2 + r.n*(mid(r) - mid(b4))^2) / (l.n + r.n)
        if now > best then
          if math.abs(mid(l) - mid(r)) >= cohen then
            cut, best = j, now
    end end end end
    if cut and not same(lo,cut,hi) then
      rank = recurse(lo,    cut, rank) + 1
      rank = recurse(cut+1, hi,  rank)
    else
      for i = lo,hi do rxs[i].rank = rank end end
    return rank
  end ---------
  table.sort(rxs, function(x,y) return mid(x) < mid(y) end)
  cohen = div(merges(1,#rxs)) * the.cohen
  recurse(1, #rxs, 1)
  return rxs end

function tiles(rxs) --> ss; makes on string per treatment showing rank, distribution, and values
  local huge,min,max,floor = math.huge,math.min,math.max,math.floor
  local lo,hi = huge, -huge
  for _,rx in pairs(rxs) do
    lo,hi = min(lo,rx.has[1]), max(hi, rx.has[#rx.has]) end
  for _,rx in pairs(rxs) do
    local t,u = rx.has,{}
    local function of(x,most) return max(1, min(most, x)) end
    local function at(x)  return t[of(#t*x//1, #t)] end
    local function pos(x) return floor(of(the.width*(x-lo)/(hi-lo+1E-32)//1, the.width)) end
    for i=1,the.width do u[1+#u]=" " end
    local a,b,c,d,e= at(.1), at(.3), at(.5), at(.7), at(.9)
    local A,B,C,D,E= pos(a), pos(b), pos(c), pos(d), pos(e)
    for i=A,B do u[i]="-" end
    for i=D,E do u[i]="-" end
    u[the.width//2] = "|"
    u[C] = "*"
    rx.show = table.concat(u) .." {"..string.format(the.Fmt,a)
    for _,x in pairs{b,c,d,e} do
      rx.show=rx.show.. ", "..string.format(the.Fmt,x) end
    rx.show = rx.show .."}"
  end
  return rxs end
-----------------------------
local eg={}
eg.ok = function(  n) math.randomseed(n or 1) end

eg.sample = function()
  for i=1,10 do
    print("",table.concat(samples{"a","b","c","d","e"})) end end

eg.num = function()
  n=NUM{1,2,3,4,5,6,7,8,9,10}
  print("",n.n, n.mu, n.sd) end

eg.gauss = function(    t,n)
  t,n={}
  for i=1,10^4 do t[1+#t] = gaussian(10,2) end
  n=NUM(t)
  print("",n.n,n.mu,n.sd) end

eg.bootmu = function(     a,b,cl,bs)
  a,b={},{}
  for i=1,100 do a[1+#a]= gaussian(10,1) end
  print("","mu","sd","cliffs","boot","both")
  print("","--","--","------","----","----")
  for mu=10,11,.1 do
    b={}
    for i=1,100 do b[1+#b]= gaussian(mu,1) end
    cl=cliffsDelta(a,b)
    bs=bootstrap(a,b)
    print("",mu,1,cl,bs,cl and bs) end end

function eg.basic()
  print("\t\ttruee", bootstrap( {8, 7, 6, 2, 5, 8, 7, 3},
                                {8, 7, 6, 2, 5, 8, 7, 3}),
              cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3},
                           {8, 7, 6, 2, 5, 8, 7, 3}))
  print("\t\tfalse", bootstrap(  {8, 7, 6, 2, 5, 8, 7, 3},
                                 {9, 9, 7, 8, 10, 9, 6}),
             cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3},
                          {9, 9, 7, 8, 10, 9, 6}))
    print("\t\tfalse",
                    bootstrap({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6},
                               {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9}),
                  cliffsDelta({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6},
                              {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9})
   ) end

eg.pre =function()
  print("\neg3")
  local d=1
  for i=1,10 do
    local t1,t2={},{}
    for j=1,32 do t1[1+#t1]=gaussian(10,1); t2[1+#t2]=gaussian(d*10,1) end
    print("\t",d,d<1.1 and "true" or "false",bootstrap(t1,t2),bootstrap(t1,t1))
    d=d+0.05 end end

eg.five=function()
  for _,rx in pairs(tiles(scottKnot{
         RX({0.34,0.49,0.51,0.6,.34,.49,.51,.6},"rx1"),
         RX({0.6,0.7,0.8,0.9,.6,.7,.8,.9},"rx2"),
         RX({0.15,0.25,0.4,0.35,0.15,0.25,0.4,0.35},"rx3"),
         RX({0.6,0.7,0.8,0.9,0.6,0.7,0.8,0.9},"rx4"),
         RX({0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4},"rx5")})) do
    print(rx.name,rx.rank,rx.show) end end

eg.six=function()
  for _,rx in pairs(tiles(scottKnot{
         RX({101,100,99,101,99.5,101,100,99,101,99.5},"rx1"),
         RX({101,100,99,101,100,101,100,99,101,100},"rx2"),
         RX({101,100,99.5,101,99,101,100,99.5,101,99},"rx3"),
         RX({101,100,99,101,100,101,100,99,101,100},"rx4")})) do
    print(rx.name,rx.rank,rx.show) end end

eg.tiles =function(        rxs,a,b,c,d,e,f,g,h,j,k)
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i=1,1000 do a[1+#a] = gaussian(10,1) end
  for i=1,1000 do b[1+#b] = gaussian(10.1,1) end
  for i=1,1000 do c[1+#c] = gaussian(20,1) end
  for i=1,1000 do d[1+#d] = gaussian(30,1) end
  for i=1,1000 do e[1+#e] = gaussian(30.1,1) end
  for i=1,1000 do f[1+#f] = gaussian(10,1) end
  for i=1,1000 do g[1+#g] = gaussian(10,1) end
  for i=1,1000 do h[1+#h] = gaussian(40,1) end
  for i=1,1000 do j[1+#j] = gaussian(40,3) end
  for i=1,1000 do k[1+#k] = gaussian(10,1) end
  for k,v in pairs{a,b,c,d,e,f,g,h,j,k} do rxs[k] =  RX(v,"rx"..k) end
  table.sort(rxs,function(a,b) return mid(a) < mid(b) end)
  for _,rx in pairs(tiles(rxs)) do
    print("",rx.name,rx.show) end end

eg.sk =function(        rxs,a,b,c,d,e,f,g,h,j,k)
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i=1,1000 do a[1+#a] = gaussian(10,1) end
  for i=1,1000 do b[1+#b] = gaussian(10.1,1) end
  for i=1,1000 do c[1+#c] = gaussian(20,1) end
  for i=1,1000 do d[1+#d] = gaussian(30,1) end
  for i=1,1000 do e[1+#e] = gaussian(30.1,1) end
  for i=1,1000 do f[1+#f] = gaussian(10,1) end
  for i=1,1000 do g[1+#g] = gaussian(10,1) end
  for i=1,1000 do h[1+#h] = gaussian(40,1) end
  for i=1,1000 do j[1+#j] = gaussian(40,3) end
  for i=1,1000 do k[1+#k] = gaussian(10,1) end
  for k,v in pairs{a,b,c,d,e,f,g,h,j,k} do rxs[k] =  RX(v,"rx"..k) end
  for _,rx in pairs(tiles(scottKnot(rxs))) do
    print("",rx.rank,rx.name,rx.show) end end


for k,fun in pairs(eg) do eg.ok(); print("\n"..k);fun() end
