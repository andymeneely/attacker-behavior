#!/usr/bin/env python3

import numpy as np
import os
from graphviz import Digraph
from markov_chain import SVG_DIR

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

    def drawVisualization(self, out_dir=SVG_DIR, out_name=None, view=True):
        """
        Generate a the DOT Graphviz representation of the `MarkovChain` with
        states and transitions.

        Arguments:
        out_dir     directory to save the generated `.dot` and `.svg` files to
        out_name    name to use when saving generated `.dot` and `.svg`
        view        whether or not to save and open the rendered graph (True)
                    or to just save the rendered graph (False)
        """
        assert os.path.exists(out_dir)
        markov_graph = Digraph(comment = self.getLabel(), format="svg")
        markov_graph.attr("node", shape="box")
        markov_graph.attr("node", style="filled")
        markov_graph.attr("node", fillcolor="#EEE9E9")
        markov_graph.attr(rankdir="LR")
        markov_graph.attr(splines="polyline")

        for state in self.getStates():
            markov_graph.node(state.getLabel(), state.getLabel())

        for start_state, probs in self.getTransitions().items():
            for end_state, prob in probs.items():
                if prob != 0:
                    markov_graph.edge(
                        start_state.getLabel(),
                        end_state.getLabel(),
                        label=str(prob)
                    )

        if out_name is None:
            out_name = "_".join(self.getLabel().lower().split(" ")) + ".dot"
        out_path = os.path.join(out_dir, out_name)
        markov_graph.render(out_path, view=view)
        return markov_graph, out_path


