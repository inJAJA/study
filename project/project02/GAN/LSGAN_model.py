from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout
from tensorflow.keras.layers import BatchNormalization, Activation, ZeroPadding2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import UpSampling2D, Conv2D, Conv2DTranspose
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam

#-------------------------------------
from Image_load import load_image
#-------------------------------------


import matplotlib.pyplot as plt

import sys

import numpy as np

class DCGAN():
    def __init__(self, rows, cols, channels):
        # Input shape
        self.img_rows = rows
        self.img_cols = cols
        self.channels = channels
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = self.img_rows*self.img_cols*self.channels
        self.noise_shape = (self.latent_dim, )

        optimizer = Adam(2e-5, 0.5)

        # Build and compile the discriminator
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy'])

        # Build the generator
        self.generator = self.build_generator()

        # The generator takes noise as input and generates imgs
        z = Input(shape=(self.noise_shape))
        img = self.generator(z)

        # For the combined model we will only train the generator
        self.discriminator.trainable = False

        # The discriminator takes generated images as input and determines validity
        valid = self.discriminator(img)

        # The combined model  (stacked generator and discriminator)
        # Trains the generator to fool the discriminator
        self.combined = Model(z, valid)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_generator(self):
    
        model = Sequential()

        model.add(Dense(256, input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(np.prod(self.img_shape), activation='tanh'))
        model.add(Reshape(self.img_shape))

        model.summary()

        noise = Input(shape=(self.latent_dim,))
        img = model(noise)

        return Model(noise, img)

    def build_discriminator(self):

        model = Sequential()

        model.add(Flatten(input_shape=self.img_shape))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        # (!!!) No softmax
        model.add(Dense(1))
        model.summary()

        img = Input(shape=self.img_shape)
        validity = model(img)

        return Model(img, validity)

    def train(self, epochs, batch_size=256, save_interval=50):

        # Load the dataset
        X_train = load_image('D:/data/Gan/Dog', self.img_rows, self.img_cols)
        noise = load_image('D:/data/Gan/Human', self.img_rows, self.img_cols)

        # Rescale -1 to 1
        X_train = X_train / 127.5 - 1.
        # X_train = np.expand_dims(X_train, axis=3)
        noise = noise / 127.5 - 1.

        # Adversarial ground truths
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))

        for epoch in range(epochs):

            # ---------------------
            #  Train Discriminator
            # ---------------------

            # Select a random half of images
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]

            # Sample noise and generate a batch of new images
            # noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            imgs_n = noise[idx]
            imgs_n = imgs_n.reshape(-1, self.latent_dim)
            gen_imgs = self.generator.predict(imgs_n)

            # Train the discriminator (real classified as ones and generated as zeros)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            # ---------------------
            #  Train Generator
            # ---------------------

            # Train the generator (wants discriminator to mistake images as real)
            g_loss = self.combined.train_on_batch(imgs_n, valid)

            # Plot the progress
            print ("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))

            # If at save interval => save generated image samples
            if (epoch % save_interval == 0) or epoch == epochs:
                self.save_imgs(epoch)

    def save_imgs(self, epoch):
        r, c = 3, 5

        human = load_image('D:/data/Gan/predict/Human', self.img_rows, self.img_cols)
        dog = load_image('D:/data/Gan/predict/Dog', self.img_rows, self.img_cols)

        x_pred = human / 127.5 -1.
        dog = dog / 127.5 - 1.

        x_pred = x_pred.reshape(-1, self.latent_dim)
        print(x_pred.shape)

        gen_imgs = self.generator.predict(x_pred)

        # Rescale images 0 - 1
        gen_imgs = 0.5 * gen_imgs + 0.5

        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(c):
            axs[0,i].imshow(human[i, :,:,:])
            axs[0,i].axis('off')
            if i ==0:
                axs[0, i].set_ylabel('HUMAN', size = 20)

        for j in range(c):
            axs[1,j].imshow(dog[j, :,:,:])
            axs[1,j].axis('off')
            if j ==0:
                axs[1,j].set_ylabel('DOG', size = 20)

        for k in range(c):
            axs[2,k].imshow(gen_imgs[k, :,:,:])
            axs[2,k].axis('off')
            if k ==0:
                axs[2, k].set_ylabel('OUTPUT', size = 20)
            
        fig.savefig("./project/GAN/result/lsgan/lsgan_%d.png" % epoch)
        plt.close()

dcgan = DCGAN(64, 64, 3)
dcgan.train(epochs=50000, batch_size=64, save_interval=200)