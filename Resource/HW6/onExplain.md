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



# XAI (Explainable AI)

## ASE23 Homework

[ [code](/src/xpln.lua) | [required output](/etc/out/xpln.out) ]

## Things to Watch For
The following ideas will be useful for the final project

- the _sampling tax_: the less we look, the more we miss important stuff.
  - We can calculate that by comparing (a) what happens what we get with SWAY with (b) what we get after evaluating `all` examples 
- the _explanation tax_ : prediction is hard and the simplifications we use for explanation compromise
    predictive performance.
  - We can calculate that by comparing (a) what happens what we get with SWAY with (b) what we get after building and applying some explanation
- _explanation variance_ : explanations generated from a few random probes of a complex multi-dimensional
   can be widely variable.
   - We can calculate this by running our explanation algorithm many times with different random number seeds.

To say that another way

- _sampleTax_ = all - sway
- _explanationTax_ = sway - explain
- _explanation variance_ = run model $N$ times, printing model

## Quotes on Explanation

_If you cannot – in the long run – tell everyone what you have been doing, your doing has been worthless._<br>- Erwin Schrödinger

_A theory that you can't explain to a bartender is probably no damn good_<br>- Ernst Rutherford

## Why Explanations?

For some good clean fun, have a read about explanation and sewer control [^malt21].
- Offers a very practical example of how explanation can be used in modern SE.

[^malt21]: [XAI Tools in the Public Sector: A Case Study on Predicting Combined Sewer Overflows](https://www.evernote.com/shard/s14/sh/25f4e214-e798-4fea-b978-e70426adb942/c17a39dbe423d1ec88dec8c7633ba365)
Nicholas Maltbie, Nan Niu, Matthew Van Doren, and Reese Johnson. 2021.
Proceedings of the 29th ACM Joint European Software Engineer-
ing Conference and Symposium on the Foundations of Software Engineering
(ESEC/FSE ’21), August 23ś28, 2021, Athens, Greece.


From Chen et al. [^chen18]:
- If no human ever needs
to understand a model [^haha], then it does not need to be comprehensible.
For example, a neural net could control the carburetor of an internal
combustion engine since that carburetor will never dispute the model
or ask for clarification of any of its reasoning. 
- On the other
hand:
   - if a model is to be used to persuade software engineers to
   change what they are doing, it needs to be comprehensible so humans
   can debate the merits of its conclusions
   - Several researchers
   demand that software analytics models needs to be expressed in a
   simple way that is easy for software practitioners to interpret
   [^dam][^rahul].
   - According to Kim et al. [^kim], software analytics aim
   to obtain actionable insights from software artifacts that help
   practitioners accomplish tasks related to software development,
   systems, and users.
   - Sawyer et al.
   comments that actionable insight is the key driver for businesses
   to invest in data analytics initiatives [^sawyer]. 

[^haha]: This is very rarely the case especially during debugging.

[^rudin]: Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead
 Cynthia Rudin 
 Nature Machine Intelligence volume 1, 206–215 (2019)
 https://www.nature.com/articles/s42256-019-0048-x

[^chen18]: Di Chen, Wei Fu, Rahul Krishna, and Tim Menzies. 2018. Applications of psychological science for actionable analytics. In Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2018). Association for Computing Machinery, New York, NY, USA, 456–467. https://doi.org/10.1145/3236024.3236050
[^sawyer]: Robert Sawyer. 2013. BIâĂŹs Impact on Analyses and Decision Making Depends
  on the Development of Less Complex Applications. In Principles and Applications
  of Business Intelligence Research. IGI Global, 83–95
[^kim]: Miryung Kim, Thomas Zimmermann, Robert DeLine, and Andrew Begel. 2016.
  The Emerging Role of Data Scientists on Software Development Teams. 
  In Proceedings of the 38th International Conference on Software Engineering (ICSE ’16). ACM,
  New York, NY, USA, 96–107. DOI:http://dx.doi.org/10.1145/2884781.2884783
[^rahul]: Rahul Krishna and Tim Menzies. 2015. 
  Actionable= Cluster+ Contrast?. In Automated Software Engineering Workshop (ASEW), ASE'15.
[^dam]: Hoa Khanh Dam, Truyen Tran, and Aditya Ghose. 2018. Explainable software analytics. 
   In Proceedings of the 40th International Conference on Software Engineering: New Ideas and Emerging Results (ICSE-NIER '18). Association for Computing Machinery, New York, NY, USA, 53–56. https://doi.org/10.1145/3183399.3183424

More generally, in SE, there are many available models-as-a-service,
not all of which can be   inspected
- "Model stores" are cloud-based
services that charge a fee for using models hidden away behind a
firewall (e.g. AWS market-place, and the Wolfram neural net repository.
- Adams et al. [^xiu] discusses model stores (also known as  "machine
learning as a service"), and warns that  these models  are often
low quality   (e.g. if it comes from  a hastily constructed prototype
from a Github repository, dropped into a container, and then sold
as a cloud-based service).
- Ideally, we use software testing to
defend ourselves against potentially low quality models. 
- But   model
owners may not publish verification results or detailed specifications--
which means standard testing methods are unsure what to test for.

[^xiu]: M. Xiu, Z. M. J. Jiang and B. Adams, "An Exploratory Study of Machine Learning Model Stores," in IEEE Software, vol. 38, no. 1, pp. 114-122, Jan.-Feb. 2021, doi: 10.1109/MS.2020.2975159.]

[^slack]: D. Slack, S. Hilgard, E. Jia, S. Singh, and H. Lakkaraju, “Fooling
LIME and SHAP: Adversarial attacks on post hoc explanation
method" in 3rd AAAI/ACM Conference on AI, Ethics, and Society,
2020

[^noble]: Algorithms of Oppression  
How Search Engines Reinforce Racism
by Safiya Umoja Noble
Published by: NYU Press, 2018


<img align=right width=500 src="/etc/img/lime.png">

An alternative to standard testing is to run an _explanation_ algorithm that offers a high-level picture of 
how model features influence each other. 
- Unfortunately,  the better we get at  generating explanations,
the better we also get at generating misleading explanations. 
- For example, Slack et al.'s lying algorithm [^slack]
knows how to detect explanation algorithms.
- That liar algorithm can then switch to  models which, by design,   disguise  biases against  marginalized groups (e.g. some specific gender, race, or age grouping). 

The Slack et al.'s results are particularly troubling.
- An alarming number   commercially deployed models  having discriminatory properties [^noble]
- For example, the (in)famous COMPAS model decides the likelihood of a criminal defendant reoffending. 
-The model suffers from alarmingly different false positive rates for Black defendants than White defendants.  
- Noble's
book _Algorithms of Oppression_ offers a long list of other models with
discriminatory properties [^noble].

Cynthia Rudin is adamant on the need for interpretable models [^rudin].
- She laments the proprietary COMPAS model, which contains hundreds of variables, and is sold by a marketing team as part of a
"risk reduction" platform. 
- She compares it to a three line open source model, which has a similar performance,
and is not marketed by anyone. 
- Rhetorically, she asks which would you want to use?


## How

Adadi and Berrada [^adadi] identified 17 XAI techniques by surveying
381 papers published between 2004 and 2018.
- According to the survey, most 
recent work done in the XAI field offers a post-hoc, local
explanation. 
  - i.e. AFTER some other model has run
  - offer some details about one particular examples
- In this class we explore
  - semi-local ante-hoc explanation (generating explanations from data, with no other model intervening)

<img width=600 src="/etc/img/explainWhen.png">

<img align=right width=500 src="/etc/img/lime.png">

Examples of post-hoe local explanation
- LIME [^lime]
- Given a model with uncertain class boundaries
- Sample around some local example, building lots of little regressions models (lots of straingth lines in a tiny region)
- Average out the effects in that model to see how changing each variable changes the class.<br clear=all>

[^lime]: Marco Tulio Ribeiro, Sameer Singh, and Carlos Guestrin. 2016. 
  ["Why Should I Trust You?": Explaining the Predictions of Any Classifier"](https://www.kdd.org/kdd2016/papers/files/rfp0573-ribeiroA.pdf).
  In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16). 
  Association for Computing Machinery, New York, NY, USA, 1135–1144. https://doi.org/10.1145/2939672.2939778

[^adadi]: Adadi, Amina and Mohammed Berrada. 
  [“Peeking Inside the Black-Box: A Survey on Explainable Artificial Intelligence (XAI).”](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8466590)
IEEE Access 6 (2018): 52138-52160.
[^vilone]: Vilone, Giulia, and Luca Longo. ["Classification of explainable artificial intelligence methods through their output formats."](https://www.mdpi.com/2504-4990/3/3/32/pdf)
 Machine Learning and Knowledge Extraction 3.3 (2021): 615-661.

Volone and Longa [^vilone] offer many cool examples. They note that there are many kinds of explanation outputs including
- visual (eg. see example below)
- numerical  (e.g. surface charts, see below)
- textual (e.g. rules)
- mixed (see example below)

<img src="/etc/img/explainEg.png">


<img align=right width=400  src="/etc/img/surface.png">

Our clustering tools would be called "numerical" by Volone. Here's an example of _surface charts_ from that  paper.
- And this week's homework is to go from numerical to textual

<br clear=all><img src="/etc/img/nasa.png" align=right width=250>

In the past NASA used my methods to "explain" how best to configure control software for re-entry systems. Suppose you search
            your discretization ranges (from last week) for the best two (that best seem to distinguish best from rest). You can then show
            the users some surface charts of where you find best performance. <br clear=all>


If a model is not interpretable, there are some explanation
algorithms that might mitigate that problem. For example:
- In _secondary learning_ (or post-hoc learning) the examples given to (say) a neural network
are used to train a rule-based learner and those learners could
be said to “explain” the neural net [13].
-  In contrast set learning for instance-based reasoning, data is
clustered and users are shown the difference between a few
exemplars selected from each cluster (see below)

Such explanation facilities are post-processors to the original learning method. 
An alternative simpler approach would be to use learners that generate comprehensible models in the first place.
Gigerenzer [^Gigerenzer] argues convincingly 
for the construction of tiny models comprising
tiny rule fragments that can be quickly comprehended by (e,g,)
- doctors in emergency rooms making rapid decisions;
- or by soldiers on guard making snap decisions about whether to fire or not on a potential enemy; 
- or by stockbrokers making instant decisions about buying or selling stock.

Here are the "fast and frugal trees" (FFT)  as approved by Gigerenzer and 
implemented by Phillips et al. [^phillips]  and used by Chen et al. [^chen18].
- An FFT is a binary decision tree of limited depth $d$
- At each level there is one sub-tree and one  leaf node that selects for either one of the two classes
  - So there are two choices at each level
- At the leaves there are two leaves, one to each class (serves  as a final "catch all").
- Chen et al. used FFT for multi-goal reasoning:
  - At each level discretiztion  was repeated looking for the simple
    split that best satisfied some multi-goal criteria (e.g. find the fewest methods with most
    errors and least false alarms).
  - For trees of size $d$, Chen generated $2^d$ trees and, using the training data, selected the one
    with overall best score. This one tree was then applied to the test data.

[^phillips]:  Phillips, N., Neth, H., Woike, J., & Gaissmaier, W. (2017). 
  [FFTrees: A toolbox to create, visualize, and evaluate fast-and-frugal decision trees](https://journal.sjdm.org/17/17217/jdm17217.pdf)
  Judgment and Decision Making, 12(4), 344-368. doi:10.1017/S1930297500006239

[^Gigerenzer]: Gigerenzer, G. (2008). [Why Heuristics Work](https://library.mpib-berlin.mpg.de/ft/gg/GG_Why_2008.pdf). 
    Perspectives on Psychological Science, 3(1), 20–29. https://doi.org/10.1111/j.1745-6916.2008.00058.x

<img src="/etc/img/fft.png">


<img align=right src="/etc/img/fft-results.png">

To say the least, this approach can kicked b*tt. Here is FFT trees compared to number other supposedly better learning 
methods [^chen18]. This trick of "try building the model a few different ways, then pick the best"
seems to work much better than forging ahead with only a single model-generation strategy.


So, sometimes, there is no explanation tax. That is, we can explain something without compromising
predictive performance.

<br clear=all>

## Explanation via contrast set learning for instance-based reasoning 

### Changes to Code
- `the` ==> `is`
-  Now  I demand ranges have to have at least `1/is.bins` of the rows
- if `is.Reuse` is false, then when exploring sub-trees we do not use one of the poles from the parent
  - which will nearly double the number of evaluations
- My `sway` function now returns the number of evaluations made to the `y` variables.
  - So we get difference counts if we do/do not use `is.Reuse`.

### Algorithm

Data is
clustered and users are shown the difference between a few
exemplars selected from each cluster.

Procedurally, this means the rules are built from the bins you generated last week. That is:
- first you build the clusters
- then find the ranges that distinguish (say) the best cluster from some random sample of the rest
- then you explore those ranges looking for  rules that select for the best cluster.

Important point:
- this rule generator does not evaluate any extra _y_ values
- rather, once it has the best cluster and some of the rest,
  - "success" means "can you find some constraint that selects for lots of best and not much of rest".


Just to visualize that, suppose we have these clusters:

```
398  {:Acc+ 15.6 :Lbs- 2970.4 :Mpg+ 23.8}
| 199
| | 99
| | | 49
| | | | 24  {:Acc+ 17.3 :Lbs- 2623.5 :Mpg+ 30.4}
| | | | 25  {:Acc+ 16.3 :Lbs- 2693.4 :Mpg+ 29.2}
| | | 50
| | | | 25  {:Acc+ 15.8 :Lbs- 2446.1 :Mpg+ 27.2}
| | | | 25  {:Acc+ 16.7 :Lbs- 2309.2 :Mpg+ 26.0}
| | 100
| | | 50
| | | | 25  {:Acc+ 16.2 :Lbs- 2362.5 :Mpg+ 32.0}
| | | | 25  {:Acc+ 16.4 :Lbs- 2184.1 :Mpg+ 34.8} <== best
| | | 50
| | | | 25  {:Acc+ 16.2 :Lbs- 2185.8 :Mpg+ 29.6} 
| | | | 25  {:Acc+ 16.3 :Lbs- 2179.4 :Mpg+ 26.4}
| 199
| | 99
| | | 49
| | | | 24  {:Acc+ 16.6 :Lbs- 2716.9 :Mpg+ 22.5}
| | | | 25  {:Acc+ 16.1 :Lbs- 3063.5 :Mpg+ 20.4}
| | | 50
| | | | 25  {:Acc+ 17.4 :Lbs- 3104.6 :Mpg+ 21.6}
| | | | 25  {:Acc+ 16.3 :Lbs- 3145.6 :Mpg+ 22.0}
| | 100
| | | 50
| | | | 25  {:Acc+ 12.4 :Lbs- 4320.5 :Mpg+ 12.4}
| | | | 25  {:Acc+ 11.3 :Lbs- 4194.2 :Mpg+ 12.8} 
| | | 50
| | | | 25  {:Acc+ 13.7 :Lbs- 4143.1 :Mpg+ 18.0}
| | | | 25  {:Acc+ 14.4 :Lbs- 3830.2 :Mpg+ 16.4}
```
A "good" rule selects for lots of "best" and nothing much of the rest.

For example, suppose we generate we look at "best" and (say) a random sample of the rest. We might find these
ranges:


```lua
Clndrs   -inf   4
Clndrs   4      inf

Volume   -inf   90
Volume   90     115
Volume   115    inf

Model   -inf    76
Model   76      79
Model   79      80
Model   80      inf

origin   1      1
origin   2      2
origin   3      3
```


Lets sort these ranges by how well they select for `best` using probability $\times$  support; i.e. $b^2/(b+r)$.

```lua
-- A query that scores a distribution by b^2/(b+r)
-- e.g. value({:best 12 :rest 7}, 12, 48, "best") ==> 0.87
function value(has,  nB,nR,sGoal,    b,r)
  b,r = 0,0
  for x,n in pairs(has) do
    if x==sGoal then b = b + n else r = r + n end end
  b,r = b/(nB+1/m.huge), r/(nR+1/m.huge) -- handling zero divide errors
  return b^2/(b+r) end
```

Here's what that returns:

```
                  Val:  {:best 12 :rest 48}  <== ALL
                  ====   ==================
origin     3   3  0.87  {:best 12 :rest 7}
Clndrs  -inf   4  0.72  {:best 12 :rest 19}
Volume  -inf  90  0.69  {:best 9 :rest 3}
Model     79  80  0.43  {:best 6 :rest 4}
Model     76  79  0.36  {:best 6 :rest 9}
Volume    90 115  0.17  {:best 3 :rest 6}
origin    2    2  0             {:rest 8}
origin    1    1  0             {:rest 33}
Volume  115  inf  0             {:rest 39}
Model    80  inf  0             {:rest 8}
Clndrs    4  inf  0             {:rest 29}
Model  -inf   76  0             {:rest 27}
```

So now lets try rules using the first item, the first 2 items, the first 3 items etc):


```lua
{:origin {3}}
{:Clndrs {{-inf 4}} :origin {3}}
{:Clndrs {{-inf 4}} :Volume {{-inf 90}} :origin {3}}
{:Clndrs {{-inf 4}} :Model {{79 80}} :Volume {{-inf 90}} :origin {3}}
{:Clndrs {{-inf 4}} :Model {{76 80}} :Volume {{-inf 90}} :origin {3}}
{:Clndrs {{-inf 4}} :Model {{76 80}} :Volume {{-inf 115}} :origin {3}}
...
```
Something to think about:
- Most of these values are ranges 
     $\text{lo} {\le} x < \text{hi}$ but for `origin` all we see is `{3}`. Why?
- In line 4 of this display, `Model` is shown as `{79 80}` but in line5 it is shown as `{76 80}`. Why?

Anyway, even after trying all that, it turns out that nothing is beating using just the first rule. So lets see how that works out:

```
                         Mid                                     Div
                         -------------------------------------   ----------------------------------------
all                     {:Acc+ 15.5 :Lbs- 2800 :Mpg+ 20 :N 398}  {:Acc+ 2.71 :Lbs- 887.21 :Mpg+ 7.75 :N 398}
sort with   398 evals   {:Acc+ 18.8 :Lbs- 1985 :Mpg+ 40 :N 12}   {:Acc+ 2.48 :Lbs- 200.39 :Mpg+ 0 :N 12}
sway with     6 evals   {:Acc+ 16.6 :Lbs- 2019 :Mpg+ 40 :N 12}   {:Acc+ 2.6 :Lbs- 129.84 :Mpg+ 7.75 :N 12}
```

### Sampling Tax

Recall that the sampling tax is ALL - SWAY.

The line `sort with 398 evals` assumes we can look at all the variables (i.e. we score EVERYTHING then sorted using 
[`better`](https://github.com/timm/tested/blob/main/src/xpln.lua#L267-L274).
(which is is the _opposite_ of fishing). The _smapling_ tax is how much we lose by looking at just 6 $y$ variables (and not 398).
In this case, the tax was very small:
Ok, so with just 6 evals:
- SWAY  knocked 50% of the median weight
- SWAY doubled miles per hour. 
- and when SWAY (with 6 evals) is comapred to using all 398 $Y$ values, we see very small deltas; 
  - ie. in this case, the sampling tax is very small
  - yes, the `mid` values are differenet but looking at the `div`s for those values, it may be sol close to be within noise.

==> Your challenge for the end of term project: for multiple runs with different random seeds, can you keep the sampling tax low?

### Explanation Tax

Recall that the explanation tax is SWAY - EXPLAIN.

Ok, that was Sway
How well does our rule `{:origin {3}}` select
for the that best sway cluster? To answer that question, we apply our rule to `all` and look at what we get:


```
                        Mid                                      Div
                        ---------------------------------------  ----------------------------------------
all                     {:Acc+ 15.5 :Lbs- 2800 :Mpg+ 20 :N 398} {:Acc+ 2.71 :Lbs- 887.21 :Mpg+ 7.75 :N 398}
xpln on       6 evals   {:Acc+ 16.4 :Lbs- 2155 :Mpg+ 30 :N 79}  {:Acc+ 2.13 :Lbs- 349.61 :Mpg+ 7.75 :N 79}
```
Here comes the _explanation tax_. Note that even though our rules are trying to select for `best`, they only get some way there
- we can change mid weight from 2800 to 2155
- and we can change mid acceleration from 20 to 30
- both of which is _less_ that the improvements seen 

==> Your challenge for the end-of-term project, can you reduce this explanation tax?

### Explanation Variance
Recall that the explanation variance comes from 20 repeated runs with different random number seeds. We find:
- six different kinds of rules
- of which 15/20 say `origin` is the key factor;
- of which 2/20 take us to worse place;

repeats|Model                    | selected instances | comment
-|-------------------------|-----------------------------------------|-------
1|true (use all the data)  |         {:Acc+ 15.5 :Lbs- 2800 :Mpg+ 20 :N 398}  | |
9|{:origin {3}} | 	{:Acc+ 16.4 :Lbs- 2155 :Mpg+ 30 :N 79} | :white_check_mark: :white_check_mark: :white_check_mark:|
6|{:origin {2}} | {:Acc+ 15.7 :Lbs- 2234 :Mpg+ 30 :N 70}| :white_check_mark: :white_check_mark:|
1|{:Model {{81 inf}}} | 	{:Acc+ 16.2 :Lbs- 2395 :Mpg+ 30 :N 60}| :white_check_mark: :white_check_mark: :white_check_mark:|
1|{:Clndrs {{-inf 5}} :origin {2}} | 	{:Acc+ 15.5 :Lbs- 2219 :Mpg+ 30 :N 63}| :white_check_mark: :white_check_mark:|
2|{:Clndrs {{-inf 4}}} | 	{:Acc+ 13.5 :Lbs- 2330 :Mpg+ 20 :N 4}| :x: :white_check_mark:|
1|{:Clndrs {{-inf 4}} :Model {{79 81}} :Volume {{-inf 112}} :origin {2 3}}|	{:Acc+ 12.5 :Lbs- 2420 :Mpg+ 20 :N 1}| :x: :white_check_mark:|


==> Your challenge for the end-of-term project: for multiple runs with different random seeds, can you keep your explanation variance low?

## Coding Details

RULEs storage ranges from different columns, sorted out into their different columns:

```lua
function RULE(ranges,maxSize,      t)
  t={}
  for _,range in pairs(ranges) do
    t[range.txt] = t[range.txt] or {}
    push(t[range.txt], {lo=range.lo,hi=range.hi,at=range.at}) end 
  return prune(t, maxSize) end
```

Lets say some attribute (say, day of week) has (say) 7 ranges and this rule contains all 7 ranges. That means that that part of the rule will
select for anything at all (day=mon or day=tues or day=wed or day=thurs or day=frid or day=sat or day=sund). Such tests
are superfluous and we can return them.  If all the attributes are superfluous, then we can actually delete the rule.


```lua
function prune(rule, maxSize,     n)
  n=0
  for txt,ranges in pairs(rule) do
    n = n+1
    if #ranges == maxSize[txt] then  n=n+1; rule[txt] = nil end end
  if n > 0 then return rule end end -- returns nil if all attributes pruned
``` 

One thing a rule can do is select some subset of the rows. Now this is a little bit tricky since this divides into two problems:
- Conjunctive case: for _one_ rule with _multiple_ attributes, if any attribute does not match the row, we return false.
- Disjunctive case: for _one_ attribute with _multiple_ ranges, if any range matches the row,  we return true.

Other nuances are that if a row has an unknown value, then we will just accept it (and this policy is debatable).

Also, depending on how you built your ranges, there are factors to consider. In my ranges.
- for numeric ranges, recall our bins are $\text{lo} {\le} x < \text{hi}$ 
- for symblic ranges, `lo`==`hi` and we justneed to test for `lo`.
- Your ranges may differ. Reflect on your code. Do the right thing.

```lua
function selects(rule,rows,    disjunction,conjunction)
  function disjunction(ranges,row,    x) 
    for _,range in pairs(ranges) do
      local lo, hi, at = range.lo, range.hi, range.at
      x = row[at]
      if x == "?"         then return true end
      if lo==hi and lo==x then return true end
      if lo<=x  and x< hi then return true end end 
    return false end 
  function conjunction(row)
    for _,ranges in pairs(rule) do 
      if not disjunction(ranges,row) then return false end end
    return true end 
  return map(rows, function(r) if conjunction(r) then return r end end) end
``` 

Printing a rule is surprisingly tricky
- One one range continues into the next, then you should print them both as one 
  -e.g not _model = 65 to 77 and 77 to 90_
    - but _model = 65 to 90_
- Ranges (as we built them last week) contain a lot of details we do not need to see in a rule pretty-print. So `pretty` cleans up those details.

```lua
function  showRule(rule,    merges,merge,pretty)
  function pretty(range)
    return range.lo==range.hi and range.lo or {range.lo, range.hi} end
  function merges(attr,ranges) 
   return map(merge(sort(ranges,lt"lo")),pretty),attr end
  function merge(t0) -- similar merge algorithm to discritization. If anything merges, loop agian
    local t,j, left,right={},1
    while j<=#t0 do
      left,right = t0[j],t0[j+1]
      if right and left.hi == right.lo then left.hi = right.hi; j=j+1 end
      push(t, {lo=left.lo, hi=left.hi})
      j=j+1 end
    return #t0==#t and t or merge(t) end 
  return kap(rule,merges) end
```

And that's nearly all there is to the rule generation, except for the top-level processing:
- Start by calling SWAY to find `best` and `rest`
- Then call `bins` to find the ranges that distinguish `best` from `rest`.
- Sort the ranges by their values (using the `value` function, see above)
- Try the first ranked range
- Try a combination of the first and second ranked range
- Try a combination of the first and second and third ranked range
- etc
- Return the best rule (as decided by `value` (see above).

There are a few tricky bits:
- We need to find out the max number of ranges per attribute (since RULE needs that to make and prune a RULE)
- When we try to create a new rule, sometimes that returns nil (see above) so we need to skip that case.
- At least in my code, I found that that everything I wanted to score things was in my `scocre` function,
  so I passed that to my subroutine.

```lua
-- [1] Collect all the ranges into one flat list
-- [2] sort them by their `value`.
-- [3] then pass all that to `firstN`
-- [4] along the way, keep track of max ranges per attribute
-- [5] skip over rules that prune themselves to nil
-- [6] pass my score function to `firstN`
function xpln(data,best,rest,      maxSizes,tmp,v,score)
  function v(has) 
    return value(has, #best.rows, #rest.rows, "best") end
  function score(ranges,       rule,bestr,restr)
    rule = RULE(ranges,maxSizes)
    if rule then                                                              -- [5]
      oo(showRule(rule))
      bestr= selects(rule, best.rows)
      restr= selects(rule, rest.rows)
      if #bestr + #restr > 0 then 
        return v({best= #bestr, rest=#restr}),rule end end 
  end ---------------------------------------------------
  tmp,maxSizes = {},{}
  for _,ranges in pairs(bins(data.cols.x,{best=best.rows, rest=rest.rows})) do
    maxSizes[ranges[1].txt] = #ranges                                          -- [4]
    print""
    for _,range in pairs(ranges) do
      print(range.txt, range.lo, range.hi)
      push(tmp, {range=range, max=#ranges,val= v(range.y.has)})  end end       -- [1]
  local rule,most=firstN(sort(tmp,gt"val"),score)                              -- [2,3,6]
  return rule,most end
```

Here's the actual search. Note that this is a greedy search and can probably be improved 100 ways.
```lua
-- [1] For i=1 to #ranges do, try the first one, then the first two, then firtt three...
-- [2] Watch and keep the best rule seen so far.
-- [3] Only some ranges are useful, we should skip the rest.
function firstN(sortedRanges,scoreFun,           first,useful,most,out)
  print""
  map(sortedRanges,function(r) print(r.range.txt,r.range.lo,r.range.hi,rnd(r.val),o(r.range.y.has)) end)
  first = sortedRanges[1].val
  function useful(range)
    if range.val>.05 and range.val> first/10 then return range end      --- [3]
  end -------------------------------
  sortedRanges = map(sortedRanges,useful) -- reject  useless ranges
  most,out = -1
  for n=1,#sortedRanges do                                              --- [1]
    local tmp,rule = scoreFun(map(slice(sortedRanges,1,n),on"range"))
    if tmp and tmp > most then out,most = rule,tmp end end              --- [2]
  return out,most end
```

