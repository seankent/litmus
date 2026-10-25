###########
# imports #
###########
import random


################
# Distribution #
################
class Distribution:

    ##########
    # sample #
    ##########
    def sample(self):
        """
        Returns the next sample, overridden by each subclass.
        """
        pass


############
# Constant #
############
class Constant(Distribution):

    ############
    # __init__ #
    ############
    def __init__(self, value):
        """
        Constructs a sampler that always returns the same value.

        Args:
            value (object): The value to return.
        """
        self.value = value

    ##########
    # sample #
    ##########
    def sample(self):
        """
        Returns the next sample.

        Returns:
            object: The value.
        """
        return self.value


###########
# Uniform #
###########
class Uniform(Distribution):

    ############
    # __init__ #
    ############
    def __init__(self, lo, hi):
        """
        Constructs a sampler that returns integers from a range, each equally likely.

        Args:
            lo (int): The smallest value to return.
            hi (int): The largest value to return.
        """
        self.lo = lo
        self.hi = hi

    ##########
    # sample #
    ##########
    def sample(self):
        """
        Returns the next sample.

        Returns:
            int: A value from lo to hi.
        """
        return random.randint(self.lo, self.hi)


##########
# Choice #
##########
class Choice(Distribution):

    ############
    # __init__ #
    ############
    def __init__(self, weights):
        """
        Constructs a sampler that returns values in proportion to their weights.

        Args:
            weights (dict): Value mapped to how often it is chosen, relative to the
                other values.
        """
        self.weights = weights

    ##########
    # sample #
    ##########
    def sample(self):
        """
        Returns the next sample.

        Returns:
            object: One of the values.
        """
        return random.choices(list(self.weights), weights = self.weights.values())[0]
