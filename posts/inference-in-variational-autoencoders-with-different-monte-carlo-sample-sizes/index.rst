.. title: Inference in Variational Autoencoders with Different Monte Carlo Sample Sizes
.. slug: inference-in-variational-autoencoders-with-different-monte-carlo-sample-sizes
.. date: 2017-11-20 23:51:24 UTC+11:00
.. tags: bayesian, variational inference, keras, tensorflow, python, variational autoencoder, unsupervised learning, deep learning, representation learning, mathjax
.. category: coding
.. link: 
.. description: 
.. type: text

.. admonition:: Draft

   Please do not share or link.

In a :doc:`previous post 
<implementing-variational-autoencoders-in-keras-beyond-the-quickstart-tutorial>`, 
I demonstrated how to use leverage Keras' modular design to implement variational
inference in a way that makes it easy to tweak hyperparameters, adapt to related
models, and extend to the more sophisticated methods in the current research.

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
