from pathlib import Path
from time import localtime, strftime

import tensorflow as tf
import tensorflow.keras as keras


class MusicModel:
    """
    LSTM-based model for music generation.
    """

    def __init__(self,
                 vocab_size: int,
                 embed_dims: int,
                 rnn_size: int,
                 layers: int,
                 dropout_rate: float,
                 ckpt_dir: str = './training_checkpoints',
                 ckpt_prefix: str = 'ckpt_{epoch'):
        """
        Initialize parameters for model.
        :param vocab_size: the number of classes for the model to learn/predict
        :param embed_dims: embedding layer dimensions
        :param rnn_size: lstm layer dimensions
        :param layers: number of (lstm, dropout, batch_normalization) layers
        :param dropout_rate: lstm-layer dropout rate
        """
        # initialize parameters
        self.vocab_size = vocab_size
        self.embed_dims = embed_dims
        self.rnn_size = rnn_size
        self.layers = layers
        self.dropout_rate = dropout_rate
        self.ckpt_path = Path(ckpt_dir) / Path(ckpt_prefix)
        self.log_dir = Path('/logs') / Path(strftime("%Y-%m-%d-%H%M", localtime()))
        self.model = None
        self.callbacks = list()

    def build_model(self):
        """
        Build and compile model.
        """
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Embedding(self.vocab_size, self.embed_dims, batch_input_shape=[None, None]))
        for _ in range(self.layers - 1):
            self.model.add(keras.layers.LSTM(self.rnn_size, return_sequences=True))
            self.model.add(keras.layers.Dropout(self.dropout_rate))
            self.model.add(keras.layers.BatchNormalization())
        self.model.add(keras.layers.LSTM(self.rnn_size))
        self.model.add(keras.layers.Dropout(self.dropout_rate))
        self.model.add(keras.layers.BatchNormalization())
        self.model.add(keras.layers.Dense(units=self.vocab_size, activation='softmax'))

        # compile model
        # TODO: learning rate scheduling
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # callbacks
        ckpt_callback = tf.keras.callbacks.ModelCheckpoint(filepath=ckpt_path, save_weights_only=True)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
        self.callbacks = [ckpt_callback, tensorboard_callback]

    def train(self, data, val_data, epochs: int, batch_size: int, verbose: int = 0):
        """
        Train model on dataset.
        :param data: dataset of event sequences
        :param val_data: validation data
        :param epochs: number of epochs to train
        :param batch_size: batch size
        :param verbose: verbosity
        :return:
        """
        history = self.model.fit(data,
                                 epochs=epochs,
                                 batch_size=batch_size,
                                 validation_data=val_data,
                                 verbose=verbose,
                                 callbacks=self.callbacks)
        return history

    def load_checkpoint(self):
        # TODO: implement load_checkpoint
        pass

    def finetune(self):
        # TODO: implement finetune
        pass

    def generate_sequence(self):
        # TODO: implement generate_sequence
        pass