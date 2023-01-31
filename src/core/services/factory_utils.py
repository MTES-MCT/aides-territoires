import factory
from factory import fuzzy


class FuzzyMultipleChoice(fuzzy.BaseFuzzyAttribute):
    """Generate a random sub-sample of a list of choices."""

    def __init__(self, choices, **kwargs):
        self.choices = None
        self.choices_generator = choices
        super(FuzzyMultipleChoice, self).__init__(**kwargs)

    def fuzz(self):
        if self.choices is None:
            self.choices = [choice[0] for choice in self.choices_generator]

        sample_size = factory.random.randgen.randint(1, len(self.choices))
        return factory.random.randgen.sample(self.choices, sample_size)
