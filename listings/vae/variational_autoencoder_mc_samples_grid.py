import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from keras import backend as K

from keras.layers import Input, Dense, Lambda, Layer, Add, Multiply
from keras.models import Model, Sequential
from keras.datasets import mnist


original_dim = 784
latent_dim = 2
intermediate_dim = 256
epochs = 5
epsilon_std = 1.0


def nll(y_true, y_pred):
    """ Bernoulli negative log likelihood. """

    # keras.losses.binary_crossentropy gives the mean
    # over the last axis. We require the sum.
    return K.sum(K.binary_crossentropy(y_true, y_pred), axis=-1)


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


def build_vae(mc_samples, original_dim, latent_dim, intermediate_dim):

    x = Input(shape=(original_dim,))
    h = Dense(intermediate_dim, activation='relu')(x)

    z_mu = Dense(latent_dim)(h)
    z_log_var = Dense(latent_dim)(h)

    z_mu, z_log_var = KLDivergenceLayer()([z_mu, z_log_var])
    z_sigma = Lambda(lambda t: K.exp(.5*t))(z_log_var)

    eps = Input(tensor=K.random_normal(stddev=epsilon_std,
                                       shape=(K.shape(x)[0],
                                              mc_samples,
                                              latent_dim)))
    z_eps = Multiply()([z_sigma, eps])
    z = Add()([z_mu, z_eps])

    decoder = Sequential([
        Dense(intermediate_dim, input_dim=latent_dim, activation='relu'),
        Dense(original_dim, activation='sigmoid')
    ])

    x_mean = decoder(z)

    return Model(inputs=[x, eps], outputs=x_mean)


# MNIST digits
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, original_dim) / 255.
x_test = x_test.reshape(-1, original_dim) / 255.


for batch_size in [25, 50, 75, 100]:

    for mc_samples in [1, 10, 25]:

        vae = build_vae(mc_samples, original_dim, latent_dim, intermediate_dim)
        vae.compile(optimizer='rmsprop', loss=nll)

        h = vae.fit(
            x_train,
            np.tile(np.expand_dims(x_train, axis=1), reps=(1, mc_samples, 1)),
            shuffle=True,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(
                x_test,
                np.tile(np.expand_dims(x_test, axis=1),
                        reps=(1, mc_samples, 1))
            )
        )
