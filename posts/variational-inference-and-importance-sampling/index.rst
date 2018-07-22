.. title: Variational Inference and Importance Sampling
.. slug: variational-inference-and-importance-sampling
.. date: 2018-04-12 10:00:34 UTC+10:00
.. tags: mathjax, draft
.. category: 
.. link: 
.. description: 
.. type: text

In this short note, we motivate variational inference from an importance 
sampling perspective.

Let :math:`\mathbf{x}` be a set of observed variables and :math:`\mathbf{z}` a 
set of hidden variables whose joint distribution factorizes as
:math:`p(\mathbf{x}, \mathbf{z}) = p(\mathbf{x} | \mathbf{z}) p(\mathbf{z})`.
We marginalize out the latent variables :math:`\mathbf{z}` to obtain the 
*evidence*

.. math::

   p(\mathbf{x}) 
   &= \int p(\mathbf{x} | \mathbf{z}) p(\mathbf{z}) d\mathbf{z} \\
   &= \mathbb{E}_{p(\mathbf{z})} [p(\mathbf{x} | \mathbf{z})]

We define function :math:`r` to be the *density ratio*

.. math::

   r(\mathbf{z}) := \frac{p(\mathbf{z})}{p(\mathbf{z}|\mathbf{x})}

Then, we can re-write the *evidence* as 

.. math::

   p(\mathbf{x}) 
   &= \int p(\mathbf{x} | \mathbf{z}) p(\mathbf{z}|\mathbf{x}) r(\mathbf{z}) d\mathbf{z} \\
   &= \mathbb{E}_{p(\mathbf{z}|\mathbf{x})} [r(\mathbf{z}) p(\mathbf{x} | \mathbf{z})]

Test

.. math::

   p(\mathbf{x}) 
   &= \mathbb{E}_{p(\mathbf{z}|\mathbf{x})} 
   [  \frac{p(\mathbf{z})}{p(\mathbf{z} | \mathbf{x})} 
      p(\mathbf{x} | \mathbf{z}) ] \\
   &= \mathbb{E}_{q(\mathbf{z}|\mathbf{x})} 
   [ \frac{p(\mathbf{z} | \mathbf{x})}{q(\mathbf{z}|\mathbf{x})} 
     \frac{p(\mathbf{z})}{p(\mathbf{z} | \mathbf{x})} 
     p(\mathbf{x} | \mathbf{z}) ] 

Evaluating this integral using Monte Carlo sampling is problematic since

need to sample from more interesting and important regions

having oversampled the important region, we have to adjust our estimate to 

account for having sampled from this other distribution.

Importance sampling allows us to study one distribution while sampling from another.

Ideally, we would be able to sample from the exact posterior distribution 
:math:`p(\mathbf{z} | \mathbf{x})`. However this is intractable and why we in 
the first place. We approximate this using a variational distribution 
:math:`q(\mathbf{z}) \approx p(\mathbf{z} | \mathbf{x})`. 




We define function 
:math:`r` to be the *density ratio*

.. math::

   r(\mathbf{z}) := \frac{p(\mathbf{z})}{q(\mathbf{z})}


:math:`p(\mathbf{x} | \mathbf{z})` is the nominal distribution
:math:`q(\mathbf{z})` is the importance distribution
:math:`r(\mathbf{z})` is the importance weight

Intuitively, this ratio indicates the adjustment factor required for the 
approximate posterior :math:`q(\mathbf{z})` to be equal to prior 
:math:`p(\mathbf{z})`, since :math:`r(\mathbf{z}) q(\mathbf{z}) = p(\mathbf{z})`.

Taking the logarithm of both sides and by applying Jensen's inequality, we have

.. math::
   
   \log p(\mathbf{x}) 
   & = \log \mathbb{E}_{q(\mathbf{z})} [r(\mathbf{z}) p(\mathbf{x} | \mathbf{z})] \\
   & \geq \mathbb{E}_{q(\mathbf{z})} \log [r(\mathbf{z}) p(\mathbf{x} | \mathbf{z})] \\
   & = \mathbb{E}_{q(\mathbf{z})} [ \log r(\mathbf{z}) + \log p(\mathbf{x} | \mathbf{z}) ] \\
   & = \mathbb{E}_{q(\mathbf{z})} [ \log p(\mathbf{z}) - \log q(\mathbf{z}) + \log p(\mathbf{x} | \mathbf{z}) ]

Hence, we arrive at exactly the *evidence lower bound* (ELBO). Importantly, the
tightness of the bound is determined by KL divergence between the approximate
and exact posterior, and maximizing the former is equivalent to minimizing the
latter. We have equality exactly when the KL divergence is zero, which occurs
iff :math:`q(\mathbf{z}) = p(\mathbf{z})`.

Density Ratio Estimation
------------------------

References
----------

* https://statweb.stanford.edu/~owen/mc/Ch-var-is.pdf
* http://blog.shakirm.com/2018/01/machine-learning-trick-of-the-day-7-density-ratio-trick/