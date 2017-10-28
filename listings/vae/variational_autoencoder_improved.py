import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from keras.layers import Input, Dense, Lambda, Layer, Add, Multiply
from keras.models import Model, Sequential
from keras import backend as K
from keras.datasets import mnist

batch_size = 100
original_dim = 784
latent_dim = 2
intermediate_dim = 256
epochs = 50
epsilon_std = 1.0


def nll(y_true, y_pred):
    """ Negative log likelihood. """

    # keras.losses.binary_crossentropy gives the mean
    # over the last axis. We require the sum.
    return K.sum(K.binary_crossentropy(y_true, y_pred), axis=-1)


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

        self.add_loss(K.mean(kl), inputs=inputs)

        return inputs

x = Input(shape=(original_dim,))
h = Dense(intermediate_dim, activation='relu')(x)

z_mu = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)

z_mu, z_log_var = KLDivergenceLayer()([z_mu, z_log_var])
z_sigma = Lambda(lambda t: K.exp(.5*t))(z_log_var)

eps = Input(shape=(latent_dim,))
z_eps = Multiply()([z_sigma, eps])
z = Add()([z_mu, z_eps])

encoder = Model(x, z_mu)

decoder = Sequential([
    Dense(intermediate_dim, input_dim=latent_dim, 
          activation='relu'),
    Dense(original_dim, activation='sigmoid')
])

vae = Model(inputs=[x, eps], outputs=decoder(z))
vae.compile(optimizer='rmsprop', loss=nll)

# train the VAE on MNIST digits
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, original_dim) / 255.
x_test = x_test.reshape(-1, original_dim) / 255.

eps_train = np.random.randn(len(x_train), latent_dim)
eps_test = np.random.randn(len(x_test), latent_dim)

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

# display a 2D plot of the digit classes in the latent space
x_test_encoded = encoder.predict(x_test, batch_size=batch_size)
plt.figure(figsize=(6, 6))
plt.scatter(x_test_encoded[:, 0], x_test_encoded[:, 1],
            c=y_test, alpha=.4, s=3**2, cmap='viridis')
plt.colorbar()
plt.show()

# display a 2D manifold of the digits
n = 15  # figure with 15x15 digits
digit_size = 28

# linearly spaced coordinates on the unit square were transformed 
# through the inverse CDF (ppf) of the Gaussian to produce values 
# of the latent variables z, since the prior of the latent space 
# is Gaussian
u_grid = np.dstack(np.meshgrid(np.linspace(0.05, 0.95, n),
                               np.linspace(0.05, 0.95, n)))
z_grid = norm.ppf(u_grid)
x_decoded = decoder.predict(z_grid.reshape(n*n, 2))
x_decoded = x_decoded.reshape(n, n, digit_size, digit_size)

plt.figure(figsize=(10, 10))
plt.imshow(np.block(list(map(list, x_decoded))), cmap='gray')
plt.show()
