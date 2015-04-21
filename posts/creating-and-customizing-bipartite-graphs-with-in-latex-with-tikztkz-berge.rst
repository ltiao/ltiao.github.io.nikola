.. title: Creating and customizing bipartite graphs with in LaTeX with TikZ/tkz-berge
.. slug: creating-and-customizing-bipartite-graphs-with-in-latex-with-tikztkz-berge
.. date: 2015-04-21 23:51:24 UTC+10:00
.. tags: latex,graph theory,tikz,tkz-berge,tkz-graph
.. category: 
.. link: 
.. description: 
.. type: text

In one of my recent projects, I had to draw a `directed`_, `weighted`_, 
`bipartite graph`_. Naturally, I immediately turned to `TikZ`_, an excellent
LaTeX library for creating graphics programmatically, thinking that it would
be trival. Turns out I was wrong.

I provide a quick synopsis here for the process I went through to obtain the
desired results, mainly for my own future reference, since I'm bound to forget
everything about it in a week.

.. TEASER_END

These answers to these StackExchange Questions were useful starting points 
that directed me to what I needed:

* http://tex.stackexchange.com/questions/15088/bipartite-graphs  
* http://tex.stackexchange.com/questions/54342/create-a-command-to-draw-edges-in-a-bipartite-graph

At first, I wanted a "pure" TikZ solution and was reluctant to resort to any
additional packages beyond it. However, after sifting through the documentation 
for the packages `tkz-graph` and `tkz-berge`, I quickly changed my mind. 
The former helps you "create graph diagrams as sim­ply as pos­si­ble" and the 
latter leverages the former to provide "a col­lec­tion of use­ful macros for draw­ing
clas­sic graphs of graph the­ory, or to make other graphs."

Their package documentations are linked below, though I should warn you first
that the documentation for `tkz-graph` `only comes in French`_.

* http://mirrors.ctan.org/macros/latex/contrib/tkz/tkz-graph/doc/tkz-graph-screen.pdf
* http://mirrors.ctan.org/macros/latex/contrib/tkz/tkz-berge/doc/tkz-berge-screen.pdf 

With `tkz-berge`, drawing a `complete bipartite graph`_ couldn't get any easier: 

.. code:: latex

   \documentclass[11pt]{scrartcl} 

   \usepackage{tikz}
   \usepackage{tkz-graph}
   \usepackage{tkz-berge} 

   \begin{document} 

   \begin{tikzpicture} 
       \grCompleteBipartite[RA=4,RB=3,RS=6]{3}{5} 
   \end{tikzpicture} 

   \end{document}

Here ``RA`` and ``RB`` are the radius of the nodes in the respective parts of 
the graph and ``RS`` is the distance between the two parts. In this graph, the
first part has 3 nodes and the other has 5 parts.


.. code:: latex

   \begin{tikzpicture}
   \GraphInit[vstyle=Dijkstra]
   \SetVertexNoLabel
   \begin{scope}[rotate=270]
     \begin{scope}[xshift=1 cm]
       \grEmptyPath[prefix=u,RA=2,RS=0]{4}
     \end{scope}
     \grEmptyPath[prefix=v,RA=2,RS=6]{5}
   \end{scope}
   \AssignVertexLabel[Math]{u}{u_1, u_2, u_3, u_4}
   \AssignVertexLabel[Math]{v}{v_1, v_2, v_3, v_4, v_5}
   \EdgeFromOneToAll[style={->},label=5]{u}{v}{1}{5}
   \Edge[style={->},label=5](u3)(v4)
   \node [fit=(u0) (u3),label=above:$U$,style={ellipse,draw,inner sep=-2pt,text width=2cm, line width=1pt}] {};
   \node [fit=(v0) (v4),label=above:$V$,style={ellipse,draw,inner sep=-2pt,text width=2cm, line width=1pt}] {};
  \nd{tikzpicture}


.. _directed: http://en.wikipedia.org/wiki/Directed_graph
.. _weighted: http://en.wikipedia.org/wiki/Graph_%28mathematics%29#Weighted_graph
.. _bipartite graph: http://en.wikipedia.org/wiki/Bipartite_graph
.. _complete bipartite graph: http://en.wikipedia.org/wiki/Complete_bipartite_graph
.. _only comes in French: http://tex.stackexchange.com/questions/165868/where-can-i-find-documentaion-for-tkz-graph-in-english
.. _TikZ: http://www.texample.net/tikz/