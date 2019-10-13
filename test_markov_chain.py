#!/usr/bin/env python3

import unittest
from markov_chain.MarkovChain import MarkovChain
from markov_chain.State import State

class TestState(unittest.TestCase):

    def setUp(self):
        self.test_state = State("I am a test state.")

    def test_init(self):
        """
        Test that the constructor raises an AssertionError when the `info`
        argument is not a `dict` type.
        """
        self.assertRaises(AssertionError, State, "", "")
        self.assertRaises(AssertionError, State, "", [])

    def test_getLabel(self):
        """ Test that `getLabel()` returns the correct value. """
        expected = "I am a test state."
        actual = self.test_state.getLabel()
        self.assertEqual(expected, actual)

    def test_getInfo(self):
        """ Test that `getInfo()` returns the correct value. """
        expected = dict()
        actual = self.test_state.getInfo()
        self.assertEqual(expected, actual)

    def test_setInfo(self):
        """
        Test that `setInfo(new_info)` validates the value of `new_info` and
        updates the value of `_info` correctly.
        """
        self.test_state.setInfo({"Key": "Val"})

        expected = {"Key": "Val"}
        actual = self.test_state.getInfo()
        self.assertDictEqual(expected, actual)
        self.assertRaises(AssertionError, self.test_state.setInfo, "")

    def test_dict(self):
        """ Test that `__dict__()` returns the correct value. """
        expected = {
            "label": "I am a test state.",
            "info": {},
        }
        actual = self.test_state.__dict__()
        self.assertDictEqual(expected, actual)

    def test_str(self):
        """ Test that `__str__()` returns the correct value."""
        expected = "{'label': 'I am a test state.', 'info': {}}"
        actual = self.test_state.__str__()
        self.assertEqual(expected, actual)

class TestMarkovChain(unittest.TestCase):

    def setUp(self):
        self.s1 = State("State 1")
        self.s2 = State("State 2")
        self.s3 = State("State 3")
        self.s4 = State("State 4")
        self.valid_trans = {
            self.s1: {self.s1: 0.3, self.s2: 0.4, self.s3: 0.3},
            self.s2: {self.s1: 0.3, self.s2: 0.7, self.s3: 0.0},
            self.s3: {self.s1: 0.1, self.s2: 0.7, self.s3: 0.2}
        }

    def test_init(self):
        """
        Test that the constructor raises an AssertionError when the given
        `transitions` are ill-defined.
        """
        test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)

        invalid_transitions = {
            self.s1: {self.s1: 0.2, self.s2: 0.4, self.s3: 0.3},
            self.s2: {self.s1: 0.3, self.s2: 0.7, self.s3: 0.0},
            self.s3: {self.s1: 0.1, self.s2: 0.7, self.s3: 0.2}
        }
        self.assertRaises(AssertionError, MarkovChain, "", invalid_transitions)

    def test_getLabel(self):
        """ Test that `getLabel()` returns the correct value. """
        test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)

        expected = "Markov Chain 1"
        actual = test_markov_chain.getLabel()
        self.assertEqual(expected, actual)

    def test_getStates(self):
        """ Test that `getStates()` returns the correct value. """
        test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)

        expected = [self.s1, self.s2, self.s3]
        actual = test_markov_chain.getStates()
        self.assertListEqual(expected, actual)

    def test_getTransitions(self):
        """ Test that `getTransitions()` returns the correct value. """
        test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)

        expected = self.valid_trans
        actual = test_markov_chain.getTransitions()
        self.assertDictEqual(expected, actual)

    def test_getNextState(self):
        """
        Test that `getNextState(current_state)` validates the value of
        `current_state` and returns a valid value based on `current_state` and
        `_transitions`.
        """
        test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)

        self.assertRaises(AssertionError, test_markov_chain.getNextState, self.s4)

        for i in range(100):
            expected = [self.s1, self.s2, self.s3]
            actual = test_markov_chain.getNextState(self.s1)
            self.assertIn(actual, expected)

        # With current transition probabilities, `s2` should never get to `s3`
        for i in range(100):
            expected = [self.s1, self.s2]
            actual = test_markov_chain.getNextState(self.s2)
            self.assertIn(actual, expected)

    def test_generateStates(self):
        """
        Test that `generateStates(current_state)` validates the value of
        `current_state` and returns a valid sequence of future states based on
        `current_state` and `_transitions`.
        """
        test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)
        
        self.assertRaises(AssertionError, test_markov_chain.generateStates, self.s4)

        for i in range(100):
            actual = test_markov_chain.generateStates(self.s1, 100)
            prev_state = actual[0].getLabel()
            for curr_state in range(1, len(actual)):
                if prev_state == "State 2":
                    self.assertNotEqual("State 3", curr_state)


if __name__ == "__main__":
    unittest.main()
