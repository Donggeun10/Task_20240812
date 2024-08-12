import random

from test.train.app.entity import App

def is_sampled(app : App):
    return random.random() > app.nw_sampling_rate

