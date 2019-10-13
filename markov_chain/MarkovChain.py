#!/usr/bin/env python3

import numpy as np

class MarkovChain():
    """ A `MarkovChain` object represents a Markov chain. """

    def __init__(self, label="", transitions=dict()):
        """
        Constructor. Create a `MarkovChain` object.

        Arguments:
        label           a label or name for the `MarkovChain`
        transitions     a dictionary representing transition probabilities in
                        the Markov chain. Should be of the form:
                            {`S1`: {`S1`: 0.3, `S2`: 0.4, `S3`: 0.3},
                             `S2`: {`S1`: 0.3, `S2`: 0.7, `S3`: 0.0},
                             `S3`: {`S1`: 0.1, `S2`: 0.7, `S3`: 0.2}}
        """
        assert self._checkTransitionIntegrity(transitions)
        self._label = label
        self._transitions = transitions
        self._states = list(transitions.keys())

    def _checkTransitionIntegrity(self, transitions):
        """
        Return `True` if the transition probabilities are valid (if the
        probabilities for each state add up to 1). Return `False` otherwise.
        """
        for state, trans in transitions.items():
            if sum(list(trans.values())) != 1:
                return False

        return True

    def getLabel(self):
        """ Return `self._label`. """
        return self._label

    def getStates(self):
        """ Return `self._states`. """
        return self._states

    def getTransitions(self):
        """ Return `self._transitions`. """
        return self._transitions

    def getNextState(self, current_state):
        """
        Return the state of the random variable at the next time instance.

        Arguments:
        current_state   a `State` object that exists within the `MarkovChain`
        """
        assert current_state in self._states
        return np.random.choice(
            self.getStates(),
            p = [self.getTransitions()[current_state][next_state]
                 for next_state in self.getStates()]
        )

    def generateStates(self, current_state, num_states=10):
        """
        Generate the next `num_states` states of the `MarkovChain`.

        Arguments:
        current_state   a `State object that exists within the `MarkovChain`
        num_states      the number of future states to generate
        """
        assert current_state in self.getStates()
        future_states = list()
        for i in range(num_states):
            next_state = self.getNextState(current_state)
            future_states.append(next_state)
            current_state = next_state
        return future_states

