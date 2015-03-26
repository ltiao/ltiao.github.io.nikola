.. title: Coursework Experience
.. slug: coursework-experience
.. date: 2015-03-18 13:35:04 UTC+11:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

.. contents::

Semester 2 - 2014
-----------------

COMP6741: Parameterized and Exact Computation
***********************************************

- Description: [COMP6741]_
- Grade: **Distinction**
- Assignments:
  
  * **Assignment 1**

    Using conventional techniques to solve NP-Complete problems
    related to scheduling, SAT solving, and computing domatic numbers.

    The following techniques were used:

    + Dynamic programming
    + Branch and bound
    + Inclusion-exclusion

  * **Assignment 2**

    Solving NP-Complete problems relating to the generalization of
    the Independent Set problem, coined "d-packing", where instead
    of requiring all vertices to be nonadjacent, we require their
    (geodesic) distance to be greater than d. I.e. 1-packing is equivalent
    to Independent Set.

    The following techniques were involved:
    
    + Branch and bound
    + Inclusion-exclusion
    + Fixed-parameter tractable (FPT) algorithms
    + Construction FPT reduction algorithms to prove W[1]-hardness
    + Prove FPT, parameterized by treewidth through
      treewidth decomposition / formalization in Monadic
      Second Order logic and Courcelle's theorem 

  * **Assignment 3**

    + Devising a randomized FPT algorithm for solving subgraph isomorphism problems. 
    + Exercises relating to the Composition Theorem, a tool for proving.
      kernel lower bounds (i.e. the nonexistence of a polynomial kernel).
    + Devising an iterative compression algorithm to solve feedback vertex set problems
      in tournament graphs.

COMP4418: Knowledge Representation and Reasoning
************************************************

- Description: [COMP4418]_
- Grade: **High Distinction**
- Assignments: 

  * **Assignment 1**

    + Exercises and proofs on propositional logic, first-order
      logic, and unit propagation rules.
    
    + Implemented logician Hao Wang's automated theorem prover 
      [Hao1961]_ based on Gentzen's Sequent Calculus.

      (Implementation in **Prolog**).
    + Analyzing the empirical hardness of SAT, with respect to 
      clause-to-variable ratio.

      (Random SAT instance generation in **Python**, solved using
      **pycosat**, a Python interface for **PicoSAT** and analysis
      performed in **IPython Notebook** with **pandas** and **matplotlib**) 

  * **Assignment 2**

    + Solving automated planning problems using the classical representation
      and subsequently the Graphplan algorithm.

      (Visualization of Graphplan algorithm in **tikz**)

    + Using Answer Set Programming to solve automated planning problems.

      (Using the **Potassco** toolkit for Answer Set Programming, specifically 
      **clingo**, an amalgamation of **gringo** and **clasp**.)

    + Modeling the actions, fluents and the situations of a automated planning 
      problem domain in Situational Calculus and implementation in **GOLOG**, 
      a **Prolog**-based logic programming language based on the situation calculus.

    + Formalizing the game Morra in **Game Description Language (GDL)** to support
      General Game Playing systems.

  * **Assignment 3**

    Modeling and solving complex constraint satisfaction & optimization 
    problems in **MiniZinc**, a medium-level constraint modelling language 
    developed by NICTA. Furthermore, benchmarking performance with respect 
    various utility methods (i.e. objective functions), input sizes, and 
    optimizing models using techniques such as symmetry breaking.

COMP3161: Concepts of Programming Languages 
*******************************************

- Description: [COMP3161]_
- Grade: **High Distinction**
- Assignments: 

  * **Assignment 1**

    Implemented an interpreter for "MinHS", a functional 
    programming language in the spirit of Haskell, 
    fabricated for instructional purposes.

    Interpreter implemented in **Haskell**.

  * **Assignment 2**

    Added type inference for MinHS by implementing 
    Hindley-Milner type inference algorithm (aka "Algorithm W".)
    
    (Implementation in **Haskell**.)

Semester 1 - 2014
-----------------

COMP3891: Extended Operating Systems
************************************

- Description: [COMP3891]_
- Grade: **Distinction** (Mark: 84)
- Assignments:

  * **Assignment 1**

    Solving concurrency and synchronization problems in the 
    **OS/161** instructional Operating System using its 
    synchronization primitives such as locks, semaphores and
    conditional variables and implementation in **C**.

    (Pair project and required distributed revision control
    with **svn**, and debugging using **GDB**) 

  * **Assignment 2**

    Implementing system call signal handlers (i.e. kernel code)
    for file system syscalls: ``open``, ``read``, ``write``, 
    ``lseek``, ``close``, and ``dup2``. In a more concrete sense,
    implementing the data structure and interface for the 
    file descriptor table and open file table, which manipulates 
    the virtual file system (VFS) through its provided interface.

    Advanced assignment component for extended OS students further
    consisted of implementing user-level process management system 
    calls: ``fork``, ``getpid``, ``execv``, ``waitpid``, ``_exit``,
    ``kill_curthread``.

    (Pair project and required distributed revision control
    with **svn**, and debugging using **GDB**) 

  * **Assignment 3**

    Implementing the virtual memory subsystem of **OS/161** to
    take full advantage of its emulated hardware:

    + manipulation of the **MIPS** software-managed Translation Lookaside 
      Buffer (TLB)
    + implement data structure and interface for the frame table
      (also known as coremap) to manage the physical memory, 
      to support kernel-level memory allocation
    + implement a data structure and interface for a two-level
      hierarchical page table for virtual address translation
    + implement the TLB refill signal handler, which will allocate the
      hierarchical page table and physical pages on-demand as required,
      or otherwise lookup the page table and refill the TLB. 
    + implement OS/161's interface for virtual address space management
      abstraction to interact with the virtual memory implementation.
      E.g. methods for defining regions (text, data, stack) in the 
      virtual address space, methods for copying the virtual address 
      space (to support forking processes), etc.

    Advanced assignment component for extended OS students further
    consisted of implementing

    + shared pages and copy-on-write (for optimizing space utilization
      when forking processes.)
    + implement the ``sbrk`` system call to enable the user-level ``malloc``
      function.

COMP4141: Theory of Computation
*******************************

- Description: [COMP4141]_
- Homework Topics:

  * 

ECON1101: Microeconomics 1
**************************

*Not particularly relevant, but included for completeness.*

GENS4010: Science and Religion
*******************************

*Not particularly relevant, but included for completeness.*

Semester 2 - 2013
-----------------

COMP4121: Advanced and Parallel Algorithms
******************************************

COMP4920: Management and Ethics
*******************************

MATH3141: Information, Codes and Ciphers
****************************************

Semester 1 - 2013
-----------------

COMP9417: Machine Learning and Data Mining
******************************************

COMP3411: Artificial Intelligence
*********************************

COMP3821: Extended Algorithms and Programming Techniques
********************************************************

COMP3141: Software System Design and Implementation
***************************************************

Semester 2 - 2012
-----------------

COMP3331: Computer Networks and Applications
********************************************

COMP2911: Engineering Design in Computing
*****************************************

MATH2601: (Higher) Linear Algebra
*********************************

MATH2120: Mathematical Methods for Differential Equations
*********************************************************

MATH2521: Complex Analysis
**************************

Semester 1 - 2012
-----------------

MATH2011: Several Variable Calculus
***********************************

MATH2801: Theory of Statistics
******************************

COMP2121: Microprocessors and Interfacing
*****************************************

COMP2041: Software Construction: Techniques and Tools
*****************************************************

Sumer Term - 2011/2012
----------------------

MATH1231: Mathematics 1B
************************

COMP1927: (Higher) Computing 2
******************************

Semester 2 - 2011
-----------------

MATH1131: Mathematics 1A
************************

MATH1081: Discrete Mathematics
******************************

COMP1917: (Higher) Computing 1
******************************

SENG1031: Software Engineering Workshop 1
*****************************************

.. [Hao1961] http://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1961.tb03975.x/abstract
.. [COMP4418] Knowledge Representation and Reasoning (KRR) is at the core of Artificial Intelligence. It is concerned with the representation of knowledge in symbolic form and the use of this knowledge for reasoning. This course presents current trends and research issues in Knowledge Representation and Reasoning (KRR). It enables students interested in Artificial Intelligence to deepen their knowledge in this important area and gives them a solid background for doing their own work/research in this area. The topics covered may include: Belief revision, Boolean satisfiability, Constraint programming, Description logics and ontologies, Mathematical programming, Planning, Reasoning about action.
.. [COMP3161] Programming language paradigms: imperative, object oriented, declarative (i.e., functional and logic). Theoretical foundations of programming languages: syntax, operatational, axiomatic and denotational semantics. Implementation aspects of central language features, such as dynamic and strong typing, polymorphism, overloading and automatic memory management. Abstracting over programming languages and architectures: byte code approach, component software.
.. [COMP3891] Operating System Organisation and services. Process management: scheduling, synchronisation and communication. Memory management: virtual memory, paging and segmentation. Storage management: disk scheduling, file systems. Protection and security. Distributed operating systems and file systems. Case studies: UNIX & NT.
.. [COMP4141] Computability: formal languages and problems, Turing Machines (TMs), computability, (semi-)decidability, universal TMs, Church-Turing thesis, halting problem, reduction and undecidability proofs, examples; Complexity: run time, space, complexity classes, non-determinism and NP, polynomial reductions and NP completeness, optimisation problems and approximation, randomisation; Languages and Automata: regular expressions and languages, finite automata, determinisation, context-free grammars and languages (CFLs), Chomsky normal form, word problems, pumping lemma, push-down automata, decidability problems for CFLs; Semantics and Correctness: while programs, assertions and program correctness, Hoare logic, loops and loop invariants, relative completeness of Hoare logic (and its role in a proof of Gödel's incompleteness result). [More at http://www.handbook.unsw.edu.au/undergraduate/courses/2014/COMP4141.html]
.. [COMP6741] The course focuses on algorithms for exactly solving NP-hard computational problems. Since no polynomial time algorithm is known for any of these problems, the running time of the algorithms will have a super-polynomial dependence on the input size or some other parameter of the input. 

  The first part presents algorithmic techniques to solve NP-hard problems provably faster than brute-force in the worst case, such as branching algorithms, dynamic programming across subsets, inclusion-exclusion, local search, and measure & conquer. We will also see lower bounds for algorithms and how to rule out certain running times assuming the (Strong) Exponential Time Hypothesis.

  Whereas the first part presents "default" algorithms that one would use without knowing much about the instances one is about to solve, the second part acknowledges that the complexity of an instance does not only depend on its size n. A parameter k is associated with each instance and the parameterized complexity framework aims at designing fixed-parameter algorithms whose running times are f(k)*poly(n) for a computable function f. This gives efficient algorithms for small values of the parameter obtained via techniques such as branching, colour coding, iterative compression, and kernelization (preprocessing). We will also see problems that are not fixed-parameter tractable and not kernelizable to polynomial kernels subject to complexity-theoretic assumptions.
