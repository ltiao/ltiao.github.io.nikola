.. title: A Probabilistic Interpretation of CycleGAN as Approximate Bayesian Inference with Implicit Distributions
.. slug: a-probabilistic-interpretation-of-cyclegan-as-approximate-bayesian-inference-with-implicit-distributions
.. date: 2017-12-01 13:15:43 UTC+11:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

.. admonition:: Draft

   Please do not share or link.

Sketch
======

1. Revisit Probabilistic PCA [#tipping1998]_, Factor Analysis.
2. Generalize to deep latent Gaussian models (DLGMs) [#rezende2014]_ and 
   describe how inference is done: amortized variational inference / stochastic 
   backpropagation with inference networks.
3. Generalize amortized variational inference to implicit distributions:
   Adversarial autoencoders, BiGAN/ALIGAN, AVB [#mescheder2017]_ [#tran2017]_.
4. Formulate CycleGAN [#zhu2017]_ as a deep latent Gaussian model with a 
   implicit prior distribution, where inference is done using amortized 
   variational inference with an implicit approximate posterior distribution. 

References
==========

.. [#tipping1998] M. E. Tipping and C. M. Bishop, 
   "Probabilistic Principal Component Analysis," 
   Journal of the Royal Statistical Society. Series B (Statistical Methodology), 
   vol. 61. WileyRoyal Statistical Society, pp. 611–622, 1999.   
.. [#rezende2014] D. J. Rezende, S. Mohamed, and D. Wierstra,
   "Stochastic backpropagation and approximate inference in deep generative 
   models," in Proceedings of The 31st Conference on Machine Learning, 
   Beijing, China, 2014, vol. 32, no. 2, pp. 1278–1286.
.. [#zhu2017] J.-Y. Zhu, T. Park, P. Isola, and A. A. Efros, 
   "Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial 
   Networks," Mar. 2017.
.. [#hu2017] Z. Hu, Z. Yang, R. Salakhutdinov, and E. P. Xing, 
   "On Unifying Deep Generative Models," Jun. 2017.
.. [#mescheder2017] L. Mescheder, S. Nowozin, and A. Geiger, 
   "Adversarial Variational Bayes: Unifying Variational Autoencoders and 
   Generative Adversarial Networks," 
   in Proceedings of the 34th International Conference on Machine Learning, 2017, 
   vol. 70, pp. 2391–2400.
.. [#tran2017] D. Tran, R. Ranganath, and D. Blei, 
   "Hierarchical Implicit Models and Likelihood-Free Variational Inference," 
   *to appear in* Advances in Neural Information Processing Systems 30, 2017.
