.. title: Implementing Variational Autoencoders in Keras: Beyond the Quickstart Tutorial
.. slug: implementing-variational-autoencoders-in-keras-beyond-the-quickstart-tutorial
.. date: 2017-10-23 01:19:59 UTC+11:00
.. tags: variational inference, keras, tensorflow, python, variational autoencoder, unsupervised learning, deep learning, representation learning, mathjax
.. category: coding
.. link: 
.. description: 
.. type: text

.. admonition:: Draft

   Do not share or link to.

Keras_ is awesome. It is a very well-designed library that clearly abides by to 
its `guiding principles`_ of modularity and extensibility and thereby allows us 
to easily assemble powerful complex models from primitive building blocks. 
This has been demonstrated by many blog posts and tutorials, such as the 
excellent tutorial on `Building Autoencoders in Keras`_. 
As the name suggests, that tutorial provides examples of how to implement 
various kinds of autoencoders in Keras, including the variational autoencoder 
(VAE) [#kingma2014]_. 

Like all autoencoders, the variational autoencoder are primarily used for 
unsupervised learning of hidden representations. 
However, variational autoencoders are fundamentally different to your standard 
neural network-based autoencoder in that they tackle the problem with a 
probabilistic approach: by specifying distributions over the observed and 
latent variables, and approximating the intractable posterior over the latter
using variational inference with an *inference network* 
[#inference1]_ [#inference2]_.

.. TEASER_END

While the examples in the aforementioned tutorial do well to showcase the 
versatility of Keras on a wide range of autoencoder model architectures, 
`its implementation of the variational autoencoder`_ doesn't properly take 
advantage of Keras' modular design, making it difficult to generalize and 
extend in important ways. As we will see, it relies on implementing custom 
layers and constructs that are restricted to a specific instance of 
variational autoencoders. This is a shame, because when combined, Keras' 
building blocks are powerful enough to encapsulate most variants of the 
variational autoencoder and more generally, a large family of 
*deep latent variable models* combined with inference networks.

The goal of this post is to propose a clean and elegant alternative 
implementation that takes better advantage of Keras' modular design. 
It is not a tutorial on variational autoencoders [*]_. 
Rather, we study variational autoencoders as a specific case of variational 
inference in deep latent variable models with inference networks, and 
demonstrate how we can use Keras to implement them in a modular fashion such 
that they can be easily adapted to various common problems with different 
(non-Gaussian) likelihoods, such as classification with Bayesian logistic / 
softmax regression. 
This first post will lay the groundwork for a series of future posts that 
explore how we can trivially extend this basic modular framework to the more
powerful methods proposed in the latest research, such as the normalizing flows 
for building richer posterior approximations [#rezende2015]_, the Gumbel-softmax 
trick for inference in discrete latent variables, and even the most recent 
GAN-related density-ratio estimation techniques for likelihood-free inference 
[#mescheder2017]_ [#tran2017]_.

.. _Keras: https://keras.io/
.. _guiding principles: https://keras.io/#guiding-principles
.. _Building Autoencoders in Keras: https://blog.keras.io/building-autoencoders-in-keras.html
.. _is not a way to train generative models: http://dustintran.com/blog/variational-auto-encoders-do-not-train-complex-generative-models
.. _its implementation of the variational autoencoder: https://github.com/fchollet/keras/blob/2.0.8/examples/variational_autoencoder.py

Model specification
===================

Firstly, it is important to understand that the variational autoencoder 
`is not a way to train generative models`_. 
Rather, the generative model is a component of the variational autoencoder and
is, in general, a deep latent variable model (usually a deep latent Gaussian 
model).
Learning in the generative model is done using variational inference, with an 
*inference network* to amortize the cost of inference by sharing statistical 
strength and generalization across observed data-points. We first specify the 
generative model component, the *probabilistic decoder*.

latent variables are Gaussian a priori

Decoder
-------

In this example, we let the decoder model 
:math:`p_{\theta}(\mathbf{x}_i | \mathbf{z}_i )` be a multivariate Bernoulli 
whose probabilities are computed from :math:`\mathbf{z}` using a fully-connected 
neural network with a single hidden layer.

.. math:: 

   p(\mathbf{z}_i) & = \mathcal{N}(\mathbf{0}, \mathbf{I}), \\
   \mathbf{h}_i & = h(\mathbf{W}_1 \mathbf{z}_i + \mathbf{b}_1), \\
   p_{\theta}(\mathbf{x}_i | \mathbf{z}_i)
     & = \mathrm{Bern}( \sigma( \mathbf{W}_2 \mathbf{h}_i + \mathbf{b}_2 ) )

.. code:: python

   decoder = Sequential([
     Dense(intermediate_dim, input_dim=latent_dim, activation='relu'),
     Dense(original_dim, activation='sigmoid')
   ])

.. figure:: ../../images/vae/decoder.svg
   :height: 200px
   :align: center

   Decoder architecture.


We could, for example, adapt this to solve multi-class classification with
Bayesian softmax regression by swapping the final layer for 

.. code:: python

   Dense(10, activation='softmax')


with amortized variational inference

Bayesian modelling assumes observed variables are fully governed by latent 
variables and related through the likelihood / generative model.

Intractable, resort to variational inference.

When combined end-to-end, the inference network and the deep latent variable 
model can be seen as having an autoencoder structure. 
Indeed, this general structure contains the variational autoencoder as a special 
case, and more traditionally, the Helmholtz machine. 
Even more generally, we can use this structure to perform amortized variational 
inference in complex generative models for a wide array of supervised, 
unsupervised and semi-supervised tasks.

The loss we wish to minimize is the *negative* of the *evidence lower bound* 
(ELBO), which is expressed as

.. math::

   \mathrm{ELBO}(q) 
   &= 
   \mathbb{E}_{q_{\phi}(\mathbf{z} | \mathbf{x})} [
     \log p_{\theta}(\mathbf{x} | \mathbf{z}) + 
     \log p(\mathbf{z}) -
     \log q_{\phi}(\mathbf{z} | \mathbf{x})
   ] \\
   &= 
   \mathbb{E}_{q_{\phi}(\mathbf{z} | \mathbf{x})} [
     \log p_{\theta}(\mathbf{x} | \mathbf{z})
   ] - \mathrm{KL} [q_{\phi}(\mathbf{z} | \mathbf{x}) \| p(\mathbf{z}) ].


* minimizes the KL
* approximately maximizes the log marginal likelihood

Encoder
-------

In the specific case of autoencoders, the network that maps latent code

More the general case of amortized variational inference, this is known as a
recognition model, or an inference network.


.. math::

   q_{\phi}(\mathbf{z} | \mathbf{x}) 
   = 
   \mathcal{N}(
     \mathbf{z} | 
     \mathbf{\mu}_{\phi}(\mathbf{x}), 
     \mathrm{diag}(\mathbf{\sigma}_{\phi}^2(\mathbf{x}))
   )



Reparameterization using Keras Layers
#####################################

.. math::

   \nabla_{\phi} 
   \mathbb{E}_{q_{\phi}(\mathbf{z} | \mathbf{x})} [ f(\mathbf{x}, \mathbf{z}) ]
   &= \nabla_{\phi} \mathbb{E}_{p(\mathbf{\epsilon})} [ 
      f(\mathbf{x}, 
        g_{\phi}(\mathbf{x}, \mathbf{\epsilon})) 
   ] \\
   &= \mathbb{E}_{p(\mathbf{\epsilon})} [ 
    \nabla_{\phi}
    f(\mathbf{x}, 
      g_{\phi}(\mathbf{x}, \mathbf{\epsilon})) 
   ] \\

Specifying :math:`f(\mathbf{x}, \mathbf{z}) = \log p_{\theta}(\mathbf{x} , \mathbf{z}) - \log q_{\phi}(\mathbf{z} | \mathbf{x})` gives us the gradient of the ELBO above.

.. math::

   z = g_{\phi}(\mathbf{x}, \mathbf{\epsilon}), \quad 
     \mathbf{\epsilon} \sim p(\mathbf{\epsilon})

.. math::

   g_{\phi}(\mathbf{x}, \mathbf{\epsilon}) = 
     \mathbf{\mu}_{\phi}(\mathbf{x}) + 
     \mathbf{\sigma}_{\phi}(\mathbf{x}) \odot 
     \mathbf{\epsilon}, \quad 
     \mathbf{\epsilon} \sim 
     \mathcal{N}(\mathbf{0}, \mathbf{I})
   
Assume ``z_mu`` and ``z_sigma`` are the outputs of some layers. Then, using  
`Merge Layers <https://keras.io/layers/merge/>`_, ``Add`` and ``Multiply``:

.. code:: python

   eps = Input(shape=(latent_dim,))
   z_eps = Multiply()([z_sigma, eps])   

   z = Add()([z_mu, z_eps])

.. figure:: ../../images/vae/reparameterization.svg
   :height: 300px
   :align: center

   Reparameterization with simple location-scale transformation using Keras 
   merge layers.

Lambda layer, which simultaneously draws samples from a hard-coded base 
distribution and performs reparameterization. This implementation achieves a 
more appropriate level of modularity and abstraction. It's makes it clear that
each of these atomic building blocks are themselves deterministic 
transformations which together make up a deterministic transformation. 
The source of stochasticity comes from the input, which we are able to tweak at
test time. Gumbel-softmax trick.

For the sake of illustration, we've fixed ``sigma`` and ``mu`` as ``Input`` 
layers. That's why it says ``InputLayer`` next to it. In reality, it will be 
the output layer of a network. We specify :math:`\mathbf{\mu}_{\phi}(\mathbf{x})` 
and :math:`\mathbf{\sigma}_{\phi}(\mathbf{x})` now.

.. code:: python

   x = Input(shape=(original_dim,))
   h = Dense(intermediate_dim, activation='relu')(x)  

   z_mu = Dense(latent_dim)(h)
   z_log_var = Dense(latent_dim)(h)
   z_sigma = Lambda(lambda t: K.exp(.5*t))(z_log_var)

.. figure:: ../../images/vae/encoder.svg
   :height: 500px
   :align: center

   Encoder architecture.

KL Divergence
#############

We choose prior :math:`p(\mathbf{z})` to be 

.. math:: p(\mathbf{z}) = \mathcal{N}(\mathbf{0}, \mathbf{I}).



latent space regularization

.. math:: 

   \mathrm{KL} [q_{\phi}(\mathbf{z} | \mathbf{x}) \| p(\mathbf{z}) ]
   = - \frac{1}{2} \sum_{k=1}^K \{ 1 + \log \sigma_k^2 - \mu_k^2 - \sigma_k^2 \}

.. code:: python

   class KLDivergenceLayer(Layer):  

       """ Identity transform layer that adds KL divergence
       to the final model loss.
       """  

       def __init__(self, *args, **kwargs):
           self.is_placeholder = True
           super(KLDivergenceLayer, self).__init__(*args, **kwargs)   

       def call(self, inputs):  

           mu, log_var = inputs   

           kl_batch = - .5 * K.sum(1 + log_var -
                                   K.square(mu) -
                                   K.exp(log_var), axis=-1)   

           self.add_loss(K.mean(kl_batch), inputs=inputs)   

           return inputs

.. code:: python

   z_mu, z_log_var = KLDivergenceLayer()([z_mu, z_log_var])

by itself, it will learn to ignore the input and map all outputs to 0.
It is only when we tack on the decoder that the reconstruction likelihood
is introduced. Only then will we reconcile the likelihood / observed data with 
our prior to form the posterior over latent codes.

At this stage we could specify 
``prob_encoder = Model(inputs=x, outputs=[z_mu, z_sigma])``
and compile it with something like 
``prob_encoder.compile(optimizer='rmsprop`, loss=None)``. 
When we fit it, it would trivially map all inputs to 0 and 1, thus learning the
prior distribution.

inputs mu and log_var are of shape (batch_size, latent_dim)
the loss we add should be scalar. this is unlike loss 
function specified in model compile which should returns 
loss vector of shape (batch_size,) since it requires 
loss for each datapoint in the batch for sample 
weighting.

.. figure:: ../../images/vae/encoder_full.svg
   :height: 500px
   :align: center

   Full encoder architecture, including auxiliary KL divergence layer.

Putting it all together
-----------------------

.. code:: python

   x = Input(shape=(original_dim,))
   h = Dense(intermediate_dim, activation='relu')(x) 

   z_mu = Dense(latent_dim)(h)
   z_log_var = Dense(latent_dim)(h) 

   z_mu, z_log_var = KLDivergenceLayer()([z_mu, z_log_var])
   z_sigma = Lambda(lambda t: K.exp(.5*t))(z_log_var) 

   eps = Input(tensor=K.random_normal(shape=(K.shape(x)[0], latent_dim)))
   z_eps = Multiply()([z_sigma, eps])
   z = Add()([z_mu, z_eps]) 

   decoder = Sequential([
       Dense(intermediate_dim, input_dim=latent_dim, activation='relu'),
       Dense(original_dim, activation='sigmoid')
   ]) 

   x_mean = decoder(z)

.. code:: python

   vae = Model(inputs=[x, eps], outputs=x_mean)
   vae.compile(optimizer='rmsprop', loss=nll)

.. figure:: ../../images/vae/vae_full_shapes.svg
   :height: 500px
   :align: center

   Variational autoencoder architecture.


The point of this tutorial is to illustrate the general framework for performing
amortized variational inference using Keras, treating the inference network 
(approximate posterior) and the generative network (likelihood) as black-boxes.
What we've used for the encoder and decoder each with a single hidden 
full-connected layer is perhaps the minimal viable architecture. 
In the examples directory, Keras provides a more sophisticated variational 
autoencoder with deconvolutional layers. The architecture definitions can be
trivially copy-pasted here without need to modify anything else.


Model fitting
=============

We load the training data as usual. Now the ``vae`` is explicitly specified with
random noise source as an auxiliary input. This allows to easily control the 
base distribution :math:`p(\mathbf{\epsilon})` and also how we draw Monte Carlo
samples of :math:`\mathbf{z}` for each datapoint :math:`\mathbf{x}`. Usually
we just stick with a simple isotropic Gaussian distribution and draw a different
MC sample for each datapoint.

.. code:: python

   (x_train, y_train), (x_test, y_test) = mnist.load_data()
   x_train = x_train.reshape(-1, original_dim) / 255.
   x_test = x_test.reshape(-1, original_dim) / 255.   

   eps_train = np.random.randn(len(x_train), latent_dim)
   eps_test = np.random.randn(len(x_test), latent_dim)  

Model fitting feels less intuitive. The ``vae`` is compiled with ``loss=None``
explicitly specified which raises a warning. When fit is called, the targets 
argument is left unspecified, and the reconstruction loss is optimized through
the `CustomLayer`. This mapping from mathematical problem formulation to code
implementation appears more natural and straightforward. It's easy to understand
at a glance from our call to the ``fit`` method that we're training a
probabilistic auto-encoder.


.. code:: python

   vae.fit(x_train,
           x_train,
           shuffle=True,
           epochs=epochs,
           batch_size=batch_size,
           validation_data=(x_test, x_test))

Personally, I prefer this view since the all sources of stochasticity emanate
from the inputs to the model. 

Recap
=====

- Demonstration of Sequential and functional Model API
- Custom auxiliary layers that augments the model loss
- Fixing input to source of stochasticity
- Reparameterization using Merge layers

What's next
===========

Normalizing flows

We illustrate how to employ the simple Gumbel-Softmax reparameterization to 
build a Categorical VAE with discrete latent variables.

We can easily extend ``KLDivergenceLayer`` to use an auxiliary density ratio 
estimator function, instead of evaluating the KL divergence in closed-form. 
This relaxes the requirement on approximate posterior 
:math:`q(\mathbf{z}|\mathbf{x})` (and incidentally prior :math:`p(\mathbf{z})`) 
to yield tractable densities, at the cost of maximizing a cruder estimate of the 
ELBO. 
This is known as Adversarial Variational Bayes [#mescheder2017]_, and is an 
important line of recent research that extends the applicability of variational 
inference to arbitrarily expressive implicit probabilistic models [#tran2017]_.

Footnotes
=========

.. [*] For a complete tutorial on variational autoencoders, I highly recommend:

   * `What is a variational autoencoder? 
     <https://jaan.io/what-is-variational-autoencoder-vae-tutorial/>`_ by Jaan 
     Altosaar.
   * `Tutorial on Variational Autoencoders <https://arxiv.org/abs/1606.05908>`_ 
     by Carl Doersch.


References
==========

.. [#kingma2014] D. P. Kingma and M. Welling, "Auto-Encoding Variational Bayes," 
   in Proceedings of the 2nd International Conference on Learning Representations 
   (ICLR), 2014.
.. [#inference1] `Edward tutorial on Inference Networks 
   <http://edwardlib.org/tutorials/inference-networks>`_ 
.. [#inference2] Section "Recognition models and amortised inference" in 
   `Shakir's blog post 
   <http://blog.shakirm.com/2015/01/variational-inference-tricks-of-the-trade/>`_.
.. [#rezende2015] D. Rezende and S. Mohamed, "Variational Inference with 
   Normalizing Flows," in Proceedings of the 32nd International Conference on 
   Machine Learning, 2015, vol. 37, pp. 1530–1538.
.. [#mescheder2017] L. Mescheder, S. Nowozin, and A. Geiger, 
   "Adversarial Variational Bayes: Unifying Variational Autoencoders and 
   Generative Adversarial Networks," in Proceedings of the 34th International 
   Conference on Machine Learning, 2017, vol. 70, pp. 2391–2400.
.. [#tran2017] D. Tran, R. Ranganath, and D. Blei, "Hierarchical Implicit Models 
   and Likelihood-Free Variational Inference," *to appear in* Advances in Neural 
   Information Processing Systems 30, 2017.



Appendix
========

Below, you can find:

* The `accompanying Jupyter Notebook`_ used to generate the diagrams and plots 
  in this post.
* The above snippets combined in a single executable Python file:

.. listing:: vae/variational_autoencoder_improved.py python

.. _accompanying Jupyter Notebook: /listings/vae/variational_autoencoder.ipynb.html

Number of Monte Carlo samples
-----------------------------

.. code:: python

   eps = Input(shape=(mc_samples, latent_dim))

Everything else remains exactly the same. The ``Multiply`` layer will 
automatically broadcast ``eps`` which has shape 
``(batch_size, mc_samples, latent_dim)`` with ``sigma`` which has shape 
``(batch_size, latent_dim)`` and output shape 
``(batch_size, mc_samples, latent_dim)``. Since the subsequent layers do not 
operate on the which will then be propagated to the 
final output. 

diagram here

We expand the targets to 3d a array ``np.expand_dims(x_train, axis=1)`` to be
of shape ``(batch_size, 1, original_dim)`` so that the loss function can 
broadcast with the output with shape ``(batch_size, mc_samples, original_dim)``.
It is important to make the distinction between the log likelihood of the mean 
over outputs, versus the mean of the log likelihood over the outputs. Since we 
require the expected log likelihood, we are interested in the latter.

.. code:: python

   eps_train = np.random.randn(len(x_train), mc_samples, latent_dim)
   eps_test = np.random.randn(len(x_test), mc_samples, latent_dim)  

   vae.fit(
       [x_train, eps_train],
       np.expand_dims(x_train, axis=1),
       shuffle=True,
       epochs=epochs,
       batch_size=batch_size,
       validation_data=(
           [x_test, eps_test],
           np.expand_dims(x_test, axis=1)
       )
   )

For every data point, there are ``mc_samples`` reconstructions. 

.. code:: python

   recons = vae.predict([x_test[:1], eps_test[:1]]).squeeze()

   plt.figure(figsize=(10, 10))
   plt.imshow(np.block(list(map(list, recons.reshape(5, 5, 28, 28)))), 
              cmap='gray')
   plt.show()

plot here
