.. title: Serious shortcomings of n-gram feature spaces in text classification
.. slug: serious-shortcomings-of-n-gram-feature-spaces-in-text-classification
.. date: 2014-01-15 11:44:00 UTC+11:00
.. tags: n-gram, classification, natural language processing, machine learning, mathjax
.. category:
.. link: 
.. description: 
.. type: text

The major drawback of feature spaces represented by :math:`n`-gram models is 
extreme sparcity. 

But what makes me really uncomfortable is that it can only interpret unseen 
instances with respect to learned training data. What I mean by this is if a 
classifier learned from the instances *'today was a good day'* and *'that is a 
ridiculous thing to say'*, it is unable to say much about the instance *'i love 
this song!'* since the features are *'today', 'was', 'a', 'good', 'day', 'that', 
'is', 'ridiculous', 'thing', 'to', 'say'*. 

It is impossible to classify this new instance because it is entirely 
meaningless to the classifier - it cannot be represented. So no matter how 
many millions of instances the classifier learns from, by knowing the feature 
space, one can always artificially construct "hard" examples by using words 
not in the feature space. 

So we see this model is only well-suited for extremely large amounts of 
training data [1]_ - but even then, there is no guarantee that it is able to 
represent *all* unseen instances in its feature space. 

The Iris flower data set is a very typical test case for many statistical 
classification techniques. An interesting observation is that for an English
sentence to be valid, it need not necessarily contain specific words, say, 
*'was'* or *'good'*, in the same way that for an iris flower to *be an iris 
flower*, it necessarily has sepal and petal widths and lengths.

.. [1] Halevy, Alon, Peter Norvig, and Fernando Pereira. "The unreasonable 
       effectiveness of data." Intelligent Systems, IEEE 24.2 (2009): 8-12.