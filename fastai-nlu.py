from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

from fastai import *
from fastai.text import *
import os

import typing
from typing import Any, Optional, Text, Dict

ass FastaiClassifier(Component):
        """A pre-trained fastai classifier component"""

            name = "fastai-nlu"
                provides = ["intent"]
                    requires = []
                        defaults = {}
                            language_list = ["en"]

                                def __init__(self, component_config=None):
                                            print("init for fastaiclassifier!!")
                                                    super(FastaiClassifier, self).__init__(component_config)

                                                        def train(self, training_data, cfg, **kwargs):
                                                                    """Not needed, because the the model is pretrained"""
                                                                            pass



                                                                            def convert_to_rasa(self, value, confidence):
                                                                                        """Convert model output into the Rasa NLU compatible output format."""
                                                                                                
                                                                                                        inference = {"name": value,
                                                                                                                                  "confidence": confidence,
                                                                                                                                                    }

                                                                                                                return inference


                                                                                                                def process(self, message, **kwargs):
                                                                                                                            """Retrieve the text message, pass it to the classifier
                                                                                                                                        and append the prediction results to the message class."""

                                                                                                                                        #         FIX THIS
                                                                                                                                        #         sid = FastaiClassifier()
                                                                                                                                        #         res = sid.polarity_scores(message.text)
                                                                                                                                        #         key, value = max(res.items(), key=lambda x: x[1])

                                                                                                                                        #         entity = self.convert_to_rasa(key, value)
                                                                                                                                                intent_to_send = self.convert_to_rasa("happy", 5)
                                                                                                                                                        print("fastai processing!!, message: ", message)
                                                                                                                                                                message.set("intent", [entity], add_to_output=True)
                                                                                                                                                                #         message.set("entities", [entity], add_to_output=True)

                                                                                                                                                                    def persist(self, model_dir):
                                                                                                                                                                                """Pass because a pre-trained model is already persisted"""

                                                                                                                                                                                        pass
