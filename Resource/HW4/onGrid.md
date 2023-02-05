
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

# onGrid.lua

## Your task this week

As a team, implement the [grid.lua](/src/grid.lua) repgrid
processor.

Then, as a team, use it on 3 people (see Task5, below).

What to hand-in
- all the code in a GH repo
- the Task5  report, somewhere in that code, in some prominent place.

## About the code

grid.lua implements an requirements engineering tool for finding tacit knowledge.
Why is that important?

A common theme in many reports of algorithmic discrimination is that the developers of "it" are not sensitive (enough)
to the concerns of the people that use it.

Chapter six of Safiya Noble’s book Algorithms of Oppression [^1]  tells the sad tale of  how a design quirk of  Yelp ruined a small business. 
- As one of Noble’s interviewees put it “ Black people don’t ‘check in’ and let people know where they’re at when they sit in my (hair dressing salon). i
  They already feel like they are being hunted;  they aren’t going to tell the Man where they are”. Hence, that salon fell in the Yelp ratings (losing customers) since its patrons rarely  pressed the   “checked-in”  button.  There are many  other examples where software engineers fielded AI models, without noticing biases in those models:
- Amazon had to scrap an automated recruiting tool as it was found to be biased against women [^2].
- A widely used face recognition software was found to be biased against dark-skinned women [^3] and dark-skinned men  [^4].
- Google Translate, the most popular translation engine in the world, shows gender bias. 
  “She is an engineer, He is a nurse” is translated into Turkish and then again into English becomes “He is an engineer, She is a nurse” [^5].  
- For our purposes, the  important point of the first Noble example is this: if software designers had been more intentional about soliciting feedback from 
    the Black community, then they could have changed how check-ins are weighted in the overall Yelp rating system.  
- As to the other examples, in each case there was some discriminatory effect which was easy to detect and repair [^6], but developers just failed to test for those biases.  

[^1]: Noble, Safiya Umoja. "Algorithms of oppression." Algorithms of Oppression. New York University Press, 2018.
[^2]: https://reut.rs/2Od9fPr
[^3]: https://news.mit.edu/2018/study-finds-gender-skin-type-bias-artificial-intelligence-systems-0212
[^4]: https://www.nytimes.com/2020/06/24/technology/facial-recognition-arrest.html
[^5]: https://science.sciencemag.org/content/356/ 6334/183
[^6]: Chakraborty, Joymallya, Suvodeep Majumder, and Tim Menzies. "Bias in machine learning software: why? how? what to do?." Foundations of Software Engineering, 2021

There is a solution to all these problems:
- if a small group of people build software for the larger community, 
- that smaller group needs to listen more to the  concerns of the larger community. 

For that to work, the smaller group of developers have to admit the larger group into their design processes– either via

-  changing the reward structures such that there are inducements for the few to listen to the many (e.g. by better government legislation or  professional standards); 
- or (b) inclusion practices that admits the broader community into the developer community;
- or by (c) review practices where the developers can take better and faster feedback from the community.  

## Tool Support

How can we look outside our current tools? Find out what people really want? Without those questions being distorted by a 100 existing design decisions.

- Optimizers, thoerem provers, data miners all explore the space of ideas in some data set or some program.
- But how do we break out of that myopic view?
- Look for the thing that we do not know, yet, but should?
- How do we find the tacid knowledge that lays around us, invisible to our current gaze?

Let's go ask George Kelly (1905–1967), American psychologist, therapist, educator and personality theorist. 


> "Who can say what nature is? Is it what now exists about us, including all the tiny hidden
things that wait so patiently to be discovered? Or is it the vista of all that is destined to occur,
whether tomorrow or in some distant eon of time? Or is nature, infinitely more varied than this,
the myriad trains of events that might ensue if we were to be so bold, ingenious, and irreverent
as to take a hand in its management?"<br>&nbsp;<br>
"Personal construct theory neither offers nor demands a firm answer to any of these questions, and in this respect it is unique. Rather than depending upon bedrock assumptions about
the inherent nature of the universe, or upon fragments of truth believed to have been accumulated, it is a notion about how man (sic) may launch out from a position of admitted ignorance, and
how he (sic)  may aspire from one day to the next to transcend his  (sic) own dogmatisms. It is, then, a
theory of man’s  (sic) personal inquiry—a psychology of the human quest. It does not say what has
or will be found, but proposes rather how we might go about looking for it."    
-- George Kelly

<img src="/etc/img/repgrid.png">

Repertory grids are a tool proposed by the  cognitive psychologist George Kelly as a method for eliciting  tacit knowledge. From [Wikipedia](https://en.wikipedia.org/wiki/George_Kelly_(psychologist)):

- Kelly believed in a non-invasive or non-directive approach to psychotherapy.
- Rather than having the therapist interpret the person's psyche (which would amount to imposing the doctor's constructs on the patient)
- The therapist should just act as a facilitator of the patient finding his or her own constructs. 
- The patient's behavior is then mainly explained as ways to selectively observe the world, act upon it and update the construct system in such a way as to increase predictability. 
To help the patient find his or her constructs, Kelly developed the repertory grid interview technique.

Kelly explicitly stated that each individual's task in understanding their personal psychology is to put in order the facts of his or her own experience. 

- Then the individual, like the scientist, is to test the accuracy of that constructed knowledge by performing those actions the constructs suggest.
- If the results of their actions are in line with what the knowledge predicted, then they have done a good job of finding the order in their personal experience.
- If not, then they can modify the construct: their interpretations or their predictions or both.
- This method of discovering and correcting constructs is roughly analogous to the general scientific method that is applied in various ways by 
   modern sciences to discover truths about the universe.


Nui and Easterbrook comment that repertory grids are widely recognized as a domain-independent method for externalizing individuals’ personal constructs. 

Interviewees are invited to offer their own examples from their own domain. 
- Then they are asked: “Given 3 examples (picked at random), on what dimension is one example most different to the other two?”   

[^easter07]: N. Niu and S. Easterbrook, 
  ["So, You Think You Know Others' Goals? A Repertory Grid Study,"](https://homepages.uc.edu/~niunn/papers/SW07.pdf)
   in IEEE Software, vol. 24, no. 2, pp. 53-61, March-April 2007, doi: 10.1109/MS.2007.52.

[^kelly]: Kelly, George A. ["A brief introduction to personal construct theory."](https://www.aippc.it/wp-content/uploads/2019/04/2017.01.003.025.pdf)
    Perspectives in personal construct theory 1 (1970): 29.

## How to build a repgrid interpreter

0. Write something that can import the repgrid format (see below) and generate a DATA.
1. Cluster the rows (as per usual). Here, we do not use `the.Far`. Rather, we cluster on the furthest two items we can find.
2. Transpose the data, then cluster the attributes (uses the same code as part1)

(Actually, for pragmatic reasons, we reverse 1,2 in the following code. But the principle still holds: cluster in one direction, transpose the data,
cluster again).

### Repgrid format 

In the following `_` is a variable set to an empty space.  This file returns a dictionary with keys `domain, cols, rows`.
- cols are a list that start and end with some text describing opposite ends of some dimension.
- rows is a kludge to labels the columns with long names.
  - row[1] labels the last column and has many spaces before we get to it.
  - the last row labels the first column, so it has no rows before it.
 

```lua
local _ = " "
return {
 domain="dissementian platforms",
 cols={   {'DevelopmentTool', 5, 3, 3, 1, 1, 1, 1, 3, 5, 5, 'Application'},
               {'Multimedia', 2, 1, 1, 5, 5, 5, 5, 5, 1, 2, 'Programming'},
  {'CommunicationTechnology', 1, 3, 1, 3, 2, 5, 4, 3, 1, 1, 'ApplicationTechnology'},
       {'HumanOrientedTool' , 2, 1, 1, 1, 3, 5, 3, 2, 2, 2, 'SystemTool'},
{'ConventionalCommunication', 1, 5, 3, 4, 1, 1, 4, 5, 4, 4, 'NovelCommunication'},
      {'OnlyActAsProgrammed', 1, 4, 1, 1, 1, 1, 1, 5, 3, 1, 'Semi-autonomous'},
       {'ConventionalSystem', 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 'IntelligentSystem'},
      {'TargetedOnInterface', 1, 1, 1, 1, 1, 5, 5, 5, 3, 3, 'TargetedOnOverallSystem'}},
rows={                      { _, _, _, _, _, _, _, _, _, 'BroadbandNetworks'},
                            { _, _, _, _, _, _, _, _, 'InformationHighway'},
                            { _, _, _, _, _, _, _, 'IntelligentAgents'},
                            { _, _, _, _, _, _, 'KnowledgeBasedSystems'},
                            { _, _, _, _, _,  'ObjectOrientedSystems'},
                            { _, _, _, _,  'CrossPlatformGUIs'},
                            { _, _, _,  'VisualProgramming'},
                            { _, _,  'MultimediaAndHypermedia'},
                            { _, 'VirtualReality'},
                            {'ElectronicPublishing'}}
}
```

### Tasks1: repcols (lua grid.lua -g repcols)

Imports the format and builds a DATA whose `rows` are the columns listed above In my code, I take the column names and them as a final field marked with an "X" (so I will ignore them)

For example, here is the above imported into attributes `Num1,Num2,,thingX` (for the rows and the final strings from the column names).

Here is my `data.cols.all`:
```lua
{:a NUM :at 1 :hi 5 :id 3 :lo 1 :m2 13.5 :mu 1.75 :n 8 :txt Num1 :w 1}
{:a NUM :at 2 :hi 5 :id 4 :lo 1 :m2 17.875 :mu 2.375 :n 8 :txt Num2 :w 1}
{:a NUM :at 3 :hi 3 :id 5 :lo 1 :m2 6.0 :mu 1.5 :n 8 :txt Num3 :w 1}
{:a NUM :at 4 :hi 5 :id 6 :lo 1 :m2 18.875 :mu 2.125 :n 8 :txt Num4 :w 1}
{:a NUM :at 5 :hi 5 :id 7 :lo 1 :m2 14.875 :mu 1.875 :n 8 :txt Num5 :w 1}
{:a NUM :at 6 :hi 5 :id 8 :lo 1 :m2 32.0 :mu 3.0 :n 8 :txt Num6 :w 1}
{:a NUM :at 7 :hi 5 :id 9 :lo 1 :m2 20.0 :mu 3.5 :n 8 :txt Num7 :w 1}
{:a NUM :at 8 :hi 5 :id 10 :lo 2 :m2 10.875 :mu 4.125 :n 8 :txt Num8 :w 1}
{:a NUM :at 9 :hi 5 :id 11 :lo 1 :m2 16.0 :mu 2.5 :n 8 :txt Num9 :w 1}
{:a NUM :at 10 :hi 5 :id 12 :lo 1 :m2 15.875 :mu 2.375 :n 8 :txt Num10 :w 1}
{:a SYM :at 11 :has {} :id 13 :most 0 :n 0 :txt thingX}
```

Here are my `data.rows`:
```lua
{:a ROW :cells {5 3 3 1 1 1 1 3 5 5 DevelopmentTool:Application} :id 14}
{:a ROW :cells {2 1 1 5 5 5 5 5 1 2 Multimedia:Programming} :id 15}
{:a ROW :cells {1 3 1 3 2 5 4 3 1 1 CommunicationTechnology:ApplicationTechnology} :id 16}
{:a ROW :cells {2 1 1 1 3 5 3 2 2 2 HumanOrientedTool:SystemTool} :id 17}
{:a ROW :cells {1 5 3 4 1 1 4 5 4 4 ConventionalCommunication:NovelCommunication} :id 18}
{:a ROW :cells {1 4 1 1 1 1 1 5 3 1 OnlyActAsProgrammed:Semi-autonomous} :id 19}
{:a ROW :cells {1 1 1 1 1 1 5 5 1 1 ConventionalSystem:IntelligentSystem} :id 20}
{:a ROW :cells {1 1 1 1 1 5 5 5 3 3 TargetedOnInterface:TargetedOnOverallSystem} :id 21}
```


## Task2: cluster the attributes (lua grid.lua -g synonyms)

Here are the clusters found for the above attributes. Note the synonyms in the leaf clusters; i.e if you wanted to throw away half the columns,
you could pick any one of these leaf synonyms.
- And to work on smaller number of columns, just work back up the tree.

```lua
74
|.. 51
|.. |.. 30
|.. |.. |.. HumanOrientedTool:SystemTool
|.. |.. |.. CommunicationTechnology:ApplicationTechnology
|.. |.. 49
|.. |.. |.. Multimedia:Programming
|.. |.. |.. TargetedOnInterface:TargetedOnOverallSystem
|.. 61
|.. |.. 54
|.. |.. |.. ConventionalCommunication:NovelCommunication
|.. |.. |.. DevelopmentTool:Application
|.. |.. 43
|.. |.. |.. ConventionalSystem:IntelligentSystem
|.. |.. |.. OnlyActAsProgrammed:Semi-autonomous
```

**Improtant point**:

## Task3: flip the matrix (lua grid.lua -g reprows)

Here, we load the data as in Task1, then we build a new DATA on the transposed information

here is is my `data.cols.all` in the flipped space:

```lua
{:a NUM :at 1 :hi 5 :id 3 :lo 1 :m2 27.6 :mu 2.8 :n 10 :txt DevelopmentTool:Application :w 1}
{:a NUM :at 2 :hi 5 :id 4 :lo 1 :m2 33.6 :mu 3.2 :n 10 :txt Multimedia:Programming :w 1}
{:a NUM :at 3 :hi 5 :id 5 :lo 1 :m2 18.4 :mu 2.4 :n 10 :txt CommunicationTechnology:ApplicationTechnology :w 1}
{:a NUM :at 4 :hi 5 :id 6 :lo 1 :m2 13.6 :mu 2.2 :n 10 :txt HumanOrientedTool:SystemTool :w 1}
{:a NUM :at 5 :hi 5 :id 7 :lo 1 :m2 23.6 :mu 3.2 :n 10 :txt ConventionalCommunication:NovelCommunication :w 1}
{:a NUM :at 6 :hi 5 :id 8 :lo 1 :m2 20.9 :mu 1.9 :n 10 :txt OnlyActAsProgrammed:Semi-autonomous :w 1}
{:a NUM :at 7 :hi 5 :id 9 :lo 1 :m2 25.6 :mu 1.8 :n 10 :txt ConventionalSystem:IntelligentSystem :w 1}
{:a NUM :at 8 :hi 5 :id 10 :lo 1 :m2 30.4 :mu 2.6 :n 10 :txt TargetedOnInterface:TargetedOnOverallSystem :w 1}
{:a SYM :at 9 :has {} :id 11 :most 0 :n 0 :txt thingX}
```

Here are my `data.rows` in the flipped space:
```lua
{:a ROW :cells {5 2 1 2 1 1 1 1 ElectronicPublishing} :id 12}
{:a ROW :cells {3 1 3 1 5 4 1 1 VirtualReality} :id 13}
{:a ROW :cells {3 1 1 1 3 1 1 1 MultimediaAndHypermedia} :id 14}
{:a ROW :cells {1 5 3 1 4 1 1 1 VisualProgramming} :id 15}
{:a ROW :cells {1 5 2 3 1 1 1 1 CrossPlatformGUIs} :id 16}
{:a ROW :cells {1 5 5 5 1 1 1 5 ObjectOrientedSystems} :id 17}
{:a ROW :cells {1 5 4 3 4 1 5 5 KnowledgeBasedSystems} :id 18}
{:a ROW :cells {3 5 3 2 5 5 5 5 IntelligentAgents} :id 19}
{:a ROW :cells {5 1 1 2 4 3 1 3 InformationHighway} :id 20}
{:a ROW :cells {5 2 1 2 4 1 1 3 BroadbandNetworks} :id 21}
```
## Task4: protoypes (lua grid.lua -f prototypes)

Cluster the examples to find which are mostly repeats of the other. Observe in the collowing how "intellgent" and "kowledgebaed" are in the same leaves.
If you wanted to throw away half the rows,
you could pick any one of these leaf nearest neighbors..
- And to work on smaller number of rows, just work back up the tree.


```lua
74
|.. 48
|.. |.. 33
|.. |.. |.. CrossPlatformGUIs
|.. |.. |.. VisualProgramming
|.. |.. 75
|.. |.. |.. ObjectOrientedSystems
|.. |.. |.. 28
|.. |.. |.. |.. MultimediaAndHypermedia
|.. |.. |.. |.. ElectronicPublishing
|.. 65
|.. |.. 42
|.. |.. |.. IntelligentAgents
|.. |.. |.. KnowledgeBasedSystems
|.. |.. 43
|.. |.. |.. BroadbandNetworks
|.. |.. |.. 34
|.. |.. |.. |.. VirtualReality
|.. |.. |.. |.. InformationHighway
```

## Task5: Use this tool on 3 people


As a team, go find 3 people who all know something about some topic (cars, what to watch on Netflix, best cafes in Hillsborough street, football) and

- From person1, run a  repgrid session to get 6 to 10 examples
- Collect their attributes
- Then for person2, person3, for the same 6 to 10 examples
  - build separate repgrids
- Wrote at most 500 words (ascii text .md file) on the similarities, differences in what was found
- Important note:
  - you interview the 3 people separately and the 3 people do not communicate with each other
  - do not assume that the attributes from person1 will apply to person2,person3
    - in fact, never tell person2,person3 about the attributes found by the people before them.
      - so NAME the examples but let your people DESCRIBE them.

Recall the interview process.
- Place a blank sheet of paper on the table
- Ask them for 3 examples then some attribute along which one example is very different 
  to the other two.
  - ask for two "ends" of the attribute
  - score the examples 1,2,3,4,5 between those poles.
- Repeat
  - and for each new set of 3, fill in all the older attributes 1..5

Expect that it will take an hour to get (say) 10 examples and 10 attributes from one person.
