#!/usr/bin/env python3

import os

from graphviz import Digraph
from timeline.State import State

from timeline import SVG_DIR

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

    def drawTimeline(self, year="", team="", competition="", out_dir=SVG_DIR, view=True):
        """
        Convert this Timeline into a Graphviz visualization and save to disk.
        """
        out_name = str(year) + "_" + competition + "_t" + str(team) + "_" + "_".join(self._vulnerability.split(" ")) + ".dot"
        comment = str(year) + " " + competition + ", Team " + str(team) + ": " + self._vulnerability
        timeline = Digraph(comment=comment, format="svg")
        timeline.attr("node", shape="box")
        timeline.attr("node", style="filled")
        timeline.attr("node", fillcolor="#EEE9E9")
        timeline.attr(rankdir="LR")
        timeline.attr(splines="polyline")

        initial = True
        for state in self.getStates():
            state_label = state.getTechnique()
            if initial == True:
                timeline.node(state_label, state_label, fillcolor="#A2E8E8")
                initial = False
            elif state.isFinal():
                timeline.node(state_label, state_label, fillcolor="#FF9E9E")
            else:
                timeline.node(state_label, state_label)

        time_format = "%Y-%m-%d %I:%M:%S %p"
        prev_state = None
        for state in self.getStates():
            if prev_state is not None:
                prev_label = prev_state.getTechnique()
                curr_label = state.getTechnique()
                timeline.edge(prev_label, curr_label, state.getStartTime().strftime(time_format))
                prev_state = state
            else:
                prev_state = state

        out_path = os.path.join(out_dir, out_name)
        timeline.render(out_path, view=view)

        return timeline, out_path

    def getScenario(self):
        return self._scenario

    def getVulnerability(self):
        return self._vulnerability

    def getStates(self):
        return self._states
