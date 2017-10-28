.. title: Implementing Variational Autoencoders in Keras: Beyond the Quickstart Tutorial
.. slug: implementing-variational-autoencoders-in-keras-beyond-the-quickstart-tutorial
.. date: 2017-10-23 01:19:59 UTC+11:00
.. tags: variational inference, keras, tensorflow, python, variational autoencoder, unsupervised learning, deep learning, representation learning, mathjax, draft
.. category: coding
.. link: 
.. description: 
.. type: text

Keras_ is awesome. Its guiding principles ... modularity, extensibility ...

excellent tutorial on `Building Autoencoders in Keras`_ 

while the example demonstrates the power flexibility of Keras, it fails to fully 
take advantage of Keras' beautiful design.

The variational autoencoders is currently one of the mainstay generative models.

inference in deep latent Gaussian models (DLGM) with inference networks and 
stochastic backpropagation, the combination of which is known as amortized 
variational inference. Naturally induces an autoencoder structure.

A number of important shortcomings:

- Number of Monte Carlo samples; explicitly as model input
- Custom layer vs natural use of primitive / building-blocks
- Extensible KL Divergence layer (Adversarial Variational Bayes)
- Easy to extend to Normalizing Flows
- Natural model of loss / likelihood, easily extends to regression, classification, etc.

- https://github.com/fchollet/keras/blob/2.0.8/examples/variational_autoencoder.py

.. _Keras: https://keras.io/
.. _Building Autoencoders in Keras: https://blog.keras.io/building-autoencoders-in-keras.html

Model specification
===================

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
   ] - \mathrm{KL} [q_{\phi}(\mathbf{z} | \mathbf{x}) \| \log p(\mathbf{z}) ]


Encoder
-------

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

   \mathrm{KL} [q_{\phi}(\mathbf{z} | \mathbf{x}) \| \log p(\mathbf{z}) ]
   = - \frac{1}{2} \sum_{k=1}^K \{ 1 + \log \sigma_k^2 - \mu_k^2 - \sigma_k^2 \}

.. code:: python

   class KLDivergenceLayer(Layer):
       """ 
       Identity layer that adds KL divergence to the final model loss. 
       """  

       def __init__(self, *args, **kwargs):
           self.is_placeholder = True
           super(KLDivergenceLayer, self).__init__(*args, **kwargs)   

       def call(self, inputs):  

           mu, log_var = inputs   

           kl = - .5 * K.sum(1 + log_var -
                             K.square(mu) -
                             K.exp(log_var), axis=-1)   

           self.add_loss(kl, inputs=inputs)   

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

.. figure:: ../../images/vae/encoder_full.svg
   :height: 500px
   :align: center

   Full encoder architecture, including auxiliary KL divergence layer.

Decoder
-------

.. code:: python

   decoder = Sequential([
       Dense(intermediate_dim, input_dim=latent_dim, 
             activation='relu'),
       Dense(original_dim, activation='sigmoid')
   ])


.. figure:: ../../images/vae/decoder.svg
   :height: 200px
   :align: center

   Decoder architecture.



Bayesian softmax regression with amortized variational inference

Putting it all together
-----------------------

.. code:: python

   x = Input(shape=(original_dim,))
   h = Dense(intermediate_dim, activation='relu')(x)  

   z_mu = Dense(latent_dim)(h)
   z_log_var = Dense(latent_dim)(h)   

   z_mu, z_log_var = KLDivergenceLayer()([z_mu, z_log_var])
   z_sigma = Lambda(lambda t: K.exp(.5*t))(z_log_var)   

   eps = Input(shape=(latent_dim,))
   z_eps = Multiply()([z_sigma, eps])
   z = Add()([z_mu, z_eps])   

   decoder = Sequential([
       Dense(intermediate_dim, input_dim=latent_dim, 
             activation='relu'),
       Dense(original_dim, activation='sigmoid')
   ])   

   vae = Model(inputs=[x, eps], outputs=decoder(z))
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

   vae.fit(
       [x_train, eps_train],
       x_train,
       shuffle=True,
       epochs=epochs,
       batch_size=batch_size,
       validation_data=(
           [x_test, eps_test],
           x_test
       )
   )

Model evaluation
================

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
This is known as Adversarial Variational Bayes [Mescheder_et_al_2017]_, and is 
an important line of recent research that extends the applicability of
variational inference to arbitrarily expressive implicit probabilistic models 
[Tran_et_al_2017]_.

References
==========

.. [Mescheder_et_al_2017] L. Mescheder, S. Nowozin, and A. Geiger, 
   "Adversarial Variational Bayes: Unifying Variational Autoencoders and 
   Generative Adversarial Networks," in Proceedings of the 34th International 
   Conference on Machine Learning, 2017, vol. 70, pp. 2391–2400.
.. [Tran_et_al_2017] D. Tran, R. Ranganath, and D. Blei, 
   "Hierarchical Implicit Models and Likelihood-Free Variational Inference," 
   *to appear in* Advances in Neural Information Processing Systems 30.

Appendix
========

The accompanying Jupyter Notebook used to generate the diagrams and plots can
be found `here </listings/vae/variational_autoencoder.ipynb.html>`_. 
The fully executable code is reproduced below for completeness.

.. listing:: vae/variational_autoencoder_improved.py python

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
