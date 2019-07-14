from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

from fastai import *
from fastai.text import *
import os

import typing
from typing import Any, Optional, Text, Dict

FASTAI_MODEL_FILE_NAME = "fastai.pkl"

class FastaiIntentClassifier(Component):
    """A custom intent classifier using fast.ai"""
    name = "fastai"
    provides = ["intent"]
    requires = ["tokens"]
    defaults = {}
    language_list = ["en"]
    print('initialised the class')

    def __init__(self, component_config=None):
        super(FastaiIntentClassifier, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Load the sentiment polarity labels from the text
           file, retrieve training tokens and after formatting
           data train the classifier."""


        with open('labels.txt', 'r') as f:
            labels = f.read().splitlines()

        training_data = training_data.training_examples #list of Message objects
        tokens = [list(map(lambda x: x.text, t.get('tokens'))) for t in training_data]
        processed_tokens = [self.preprocessing(t) for t in tokens]
        labeled_data = [(t, x) for t,x in zip(processed_tokens, labels)]
        self.clf = NaiveBayesClassifier.train(labeled_data)



    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        inference = {"name": value,
                  "confidence": confidence,
                  }

        return inference
        

    def preprocessing(self, tokens):
        """Create bag-of-words representation of the training examples."""
        
        return ({word: True for word in tokens})


    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""
        
        if not self.clf:
            # component is either not trained or didn't
            # receive enough training data
            entity = None
        else:
            tokens = [t.text for t in message.get("tokens")]
            tb = self.preprocessing(tokens)
            pred = self.clf.prob_classify(tb)

            sentiment = pred.max()
            confidence = pred.prob(sentiment)

            entity = self.convert_to_rasa(sentiment, confidence)

            message.set("entities", [entity], add_to_output=True)


    def persist(self, file_name, model_dir):
        """Persist this model into the passed directory."""
        classifier_file = os.path.join(model_dir, FASTAI_MODEL_FILE_NAME)
        utils.json_pickle(classifier_file, self)
        return {"classifier_file": FASTAI_MODEL_FILE_NAME}

    @classmethod
    def load(cls,
             meta: Dict[Text, Any],
             model_dir=None,
             model_metadata=None,
             cached_component=None,
             **kwargs):
        file_name = meta.get("classifier_file")
        classifier_file = os.path.join(model_dir, file_name)
        return utils.json_unpickle(classifier_file)

