.. title: Estimating the KL Divergence (and any f-Divergence) Between Implicit Distributions
.. slug: estimating-the-kl-divergence-and-any-f-divergence-between-implicit-distributions
.. date: 2018-04-26 01:10:03 UTC+10:00
.. tags: mathjax, draft
.. category: 
.. link: 
.. description: 
.. type: text

The Kullback-Leibler (KL) Divergence between distributions $p$ and $q$ is 
defined as

.. math::

   \mathrm{KL}[p(x) \| q(x)] = 
   \mathbb{E}_{p(x)} \left [ \log \left ( \frac{p(x)}{q(x)} \right ) \right ].

Let $r(x)$ be the ratio of between the densities $p(x)$ and $q(x)$,

.. math::
   
   r(x) := \frac{p(x)}{q(x)}.

The KL divergence can be more succinctly expressed as

.. math::

   \mathrm{KL}[p(x) \| q(x)] = \mathbb{E}_{p(x)} [ \log r(x) ].

This density ratio is central to ... and we shall see it appear frequently 
thoughout this post.

.. topic:: Example: Univariate Gaussians

   We will use the following univariate Gaussian distributions as the running 
   example throughout the remainder of this post,   

   .. math::    

      p(x) &= \mathcal{N}(x \mid 1, 1^2), \\
      q(x) &= \mathcal{N}(x \mid 0, 2^2).   

   .. code:: python   

      p = tf.distributions.Normal(loc=1., scale=1.)
      q = tf.distributions.Normal(loc=0., scale=2.)   

   .. figure:: ../../images/dre/pdfs.png
      :align: center

   .. figure:: ../../images/dre/density_ratio.png
      :align: center

Analytical Form
---------------

.. code:: python

   def kl_divergence_gaussians(p, q):
       
       r = p.loc - q.loc
      
       return (K.log(q.scale) - K.log(p.scale) 
               - .5 * (1. - (p.scale**2 + r**2) / q.scale**2))

.. code:: pycon

   >>> kl_divergence_gaussians(p, q).eval()
   0.44314718

Equivalently, we can also use `kl_divergence`_ from TensorFlow Distributions, 
which computes the KL divergence between distributions where the analytical 
closed-form expression is available.

.. code:: pycon

   >>> tf.distributions.kl_divergence(p, q).eval()
   0.44314718

Monte Carlo Estimation
----------------------

For distributions where their KL divergence is not available in an analytical 
closed-form expression, we can nonetheless estimate it accurately using Monte 
Carlo (MC) estimation, provided that both the probability density functions, 
$p(x)$ and $q(x)$, that constitute the density ratio $r(x)$ are accessible.

.. math::
 
   \mathrm{KL}[p(x) \| q(x)] 
   & \approx
   \frac{1}{M} \sum_{i=1}^{M} \log r(x_p^{(i)}) \\
   & = 
   \frac{1}{M} \sum_{i=1}^{M} \log \left [ \frac{p(x_p^{(i)})}{q(x_p^{(i)})} \right ], 
   \quad x_p^{(i)} \sim p(x).

We can do this using the `monte_carlo_csiszar_f_divergence`_ convenience function.

.. code:: pycon

   >>> M = 5000
   >>> csiszar_divergence.monte_carlo_csiszar_f_divergence(
   ...     f=csiszar_divergence.kl_forward,
   ...     p_log_prob=p.log_prob,
   ...     q=q,
   ...     num_draws=M
   ... ).eval()
   0.4469335

When either $p(x)$ or $q(x)$ is unavailable, it poses significant problems for
performing Monte Carlo estimation.

.. _kl_divergence: #
.. _monte_carlo_csiszar_f_divergence: #