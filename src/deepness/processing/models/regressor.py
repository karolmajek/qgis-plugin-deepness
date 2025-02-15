""" Module including Regression model definition
"""
from typing import List

import numpy as np

from deepness.processing.models.model_base import ModelBase


class Regressor(ModelBase):
    """ Class implements regression model.

    Regression model is used to predict metric per pixel of the image.
    """

    def __init__(self, model_file_path: str):
        """

        Parameters
        ----------
        model_file_path : str
            Path to the model file
        """
        super(Regressor, self).__init__(model_file_path)

    def postprocessing(self, model_output: List) -> np.ndarray:
        """ Postprocess the model output.

        Parameters
        ----------
        model_output : List
            Output from the (Regression) model

        Returns
        -------
        np.ndarray
            Postprocessed batch of masks (N,H,W,C), 0-1 (one output channel)

        """
        return model_output[0]

    def get_number_of_output_channels(self) -> int:
        """ Returns number of channels in the output layer

        Returns
        -------
        int
            Number of channels in the output layer
        """
        if len(self.outputs_layers) == 1:
            return self.outputs_layers[0].shape[-3]
        else:
            raise NotImplementedError("Model with multiple output layers is not supported! Use only one output layer.")

    @classmethod
    def get_class_display_name(cls) -> str:
        """ Returns display name of the model class

        Returns
        -------
        str
            Display name of the model class
        """
        return cls.__name__

    def check_loaded_model_outputs(self):
        """ Check if the model has correct output layers

        Correct means that:
        - there is only one output layer
        - output layer has 1 channel
        - batch size is 1
        - output resolution is square
        """
        if len(self.outputs_layers) == 1:
            shape = self.outputs_layers[0].shape

            if len(shape) != 4:
                raise Exception(f'Regression model output should have 4 dimensions: (Batch_size, Channels, H, W). \n'
                                f'Actually has: {shape}')

            if shape[2] != shape[3]:
                raise Exception(f'Regression model can handle only square outputs masks. Has: {shape}')

        else:
            raise NotImplementedError("Model with multiple output layers is not supported! Use only one output layer.")
