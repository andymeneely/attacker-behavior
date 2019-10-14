#!/usr/bin/env python3

import os
import re
import shutil
import unittest
from markov_chain import TEST_DIR
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
        self.test_markov_chain = MarkovChain("Markov Chain 1", self.valid_trans)

    def test_init(self):
        """
        Test that the constructor raises an AssertionError when the given
        `transitions` are ill-defined.
        """
        invalid_transitions = {
            self.s1: {self.s1: 0.2, self.s2: 0.4, self.s3: 0.3},
            self.s2: {self.s1: 0.3, self.s2: 0.7, self.s3: 0.0},
            self.s3: {self.s1: 0.1, self.s2: 0.7, self.s3: 0.2}
        }
        self.assertRaises(AssertionError, MarkovChain, "", invalid_transitions)

    def test_getLabel(self):
        """ Test that `getLabel()` returns the correct value. """
        expected = "Markov Chain 1"
        actual = self.test_markov_chain.getLabel()
        self.assertEqual(expected, actual)

    def test_getStates(self):
        """ Test that `getStates()` returns the correct value. """
        expected = [self.s1, self.s2, self.s3]
        actual = self.test_markov_chain.getStates()
        self.assertListEqual(expected, actual)

    def test_getTransitions(self):
        """ Test that `getTransitions()` returns the correct value. """
        expected = self.valid_trans
        actual = self.test_markov_chain.getTransitions()
        self.assertDictEqual(expected, actual)

    def test_getNextState(self):
        """
        Test that `getNextState(current_state)` validates the value of
        `current_state` and returns a valid value based on `current_state` and
        `_transitions`.
        """
        self.assertRaises(AssertionError, self.test_markov_chain.getNextState, self.s4)

        for i in range(100):
            expected = [self.s1, self.s2, self.s3]
            actual = self.test_markov_chain.getNextState(self.s1)
            self.assertIn(actual, expected)

        # With current transition probabilities, `s2` should never get to `s3`
        for i in range(100):
            expected = [self.s1, self.s2]
            actual = self.test_markov_chain.getNextState(self.s2)
            self.assertIn(actual, expected)

    def test_generateStates(self):
        """
        Test that `generateStates(current_state)` validates the value of
        `current_state` and returns a valid sequence of future states based on
        `current_state` and `_transitions`.
        """
        self.assertRaises(AssertionError, self.test_markov_chain.generateStates, self.s4)

        for i in range(100):
            actual = self.test_markov_chain.generateStates(self.s1, 100)
            prev_state = actual[0].getLabel()
            for curr_state in range(1, len(actual)):
                if prev_state == "State 2":
                    self.assertNotEqual("State 3", curr_state)

    def test_drawVisualization(self):
        """

        """
        # Set Up
        if not os.path.exists(TEST_DIR):
            os.mkdir(TEST_DIR)

        invalid_dir = TEST_DIR[:-1]
        self.assertRaises(AssertionError, self.test_markov_chain.drawVisualization, invalid_dir)

        markov_graph, markov_graph_path = self.test_markov_chain.drawVisualization(TEST_DIR, "blah", view=False)
        self.assertTrue(os.path.exists(markov_graph_path))

        markov_graph, markov_graph_path = self.test_markov_chain.drawVisualization(TEST_DIR)
        self.assertTrue(os.path.exists(markov_graph_path))
        expected = """// Markov Chain 1
                    digraph {
                        node [shape=box]
                        node [style=filled]
                        node [fillcolor="#EEE9E9"]
                        rankdir=LR
                        splines=polyline
                        "State 1" [label="State 1"]
                        "State 2" [label="State 2"]
                        "State 3" [label="State 3"]
                        "State 1" -> "State 1" [label=0.3]
                        "State 1" -> "State 2" [label=0.4]
                        "State 1" -> "State 3" [label=0.3]
                        "State 2" -> "State 1" [label=0.3]
                        "State 2" -> "State 2" [label=0.7]
                        "State 3" -> "State 1" [label=0.1]
                        "State 3" -> "State 2" [label=0.7]
                        "State 3" -> "State 3" [label=0.2]
                    }"""
        expected = re.sub(r" +", " ", re.sub(r"[\n\t]", " ", expected))
        actual = markov_graph.source
        actual = re.sub(r" +", " ", re.sub(r"[\n\t]", " ", actual))
        self.assertEqual(expected, actual)

        # Tear Down
        shutil.rmtree(TEST_DIR)
        


if __name__ == "__main__":
    unittest.main(warnings="ignore")
