.. title: Modeling Reputation Systems: Preliminaries
.. slug: reputation-systems-preliminaries
.. date: 2015-05-09 00:26:17 UTC+10:00
.. tags: mathjax, reputation systems, linear algebra, computer science
.. category: compsci
.. link: 
.. description: 
.. type: text

Consider the following sets

.. math:: 

   U = \{\, u_i \mid i = 1, \dotsc, m \,\} 
   \qquad
   \text{and}
   \qquad
   V = \{\, v_j \mid j = 1, \dotsc, n \,\}

which may represent, respectively, a panel of judges and group of contestants, an array 
of sensors and set of physical measurements, a group of graders and set of exam papers, 
a number of customers and set of products, a group of film critics and a set of movies
or broadly speaking, a set of :math:`m` *assessors* and a set of :math:`n` target *items*.

.. TEASER_END

Consider the binary relation :math:`\mathcal{A} \subseteq U \times V` over :math:`U` and 
:math:`V` where :math:`(u, v) \in \mathcal{A}` if and only if assessor :math:`u` evaluated 
item :math:`v`. We denote the evaluation given by assessor :math:`u` to item :math:`v` by
:math:`\chi(u, v)` where :math:`\chi: \mathcal{A} \to \mathbb{R}`. 

Unless :math:`\mathcal{A} = U \times V`, i.e. if :math:`\mathcal{A}` is a proper subset of
:math:`U \times V`, :math:`\chi` is a partial function from :math:`U \times V` to :math:`\mathbb{R}` 
(:math:`\chi: U \times V \not \to \mathbb{R}`) and is undefined for :math:`(u, v) \notin \mathcal{A}`.