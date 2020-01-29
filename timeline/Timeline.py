#!/usr/bin/env python3

from timeline.State import State

class Timeline:
    def __init__(self, scenario, vulnerability, event_data):
        """
        Create a new Timeline object.

        Given:
          scenario (str)        the scenario that encompasses this timeline
          vulnerability (str)   the vulnerability that this timeline covers
          event_data (dict)     the event data for this timeline
        """
        self._scenario = scenario
        self._vulnerability = vulnerability
        self._event_data = event_data
        self._states = self._dataToStates()

    def _dataToStates(self):
        """
        Convert the event_data for this timeline into State objects.
        """
        states_list = list()

        last_state = None
        for row in self._event_data:
            if last_state is None:
                last_state = row
                pass
            if row["technique"] != last_state["technique"]:
                last_state["stop_time"] = row["start_time"]
                states_list.append(last_state)
                last_state = row

        states_list.append(last_state)

        states = list()
        for state in states_list:
            s = State(state["start_time"], state["stop_time"],
                      state["tactic"], state["technique"])
            states.append(s)

        return states

    def drawTimeline(self):
        """
        Convert this Timeline into a Graphviz visualization and save to disk.
        """
        pass

    def getScenario(self):
        return self._scenario

    def getVulnerability(self):
        return self._vulnerability

    def getStates(self):
        return self._states
