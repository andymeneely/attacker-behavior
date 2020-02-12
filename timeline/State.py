#!/usr/bin/env python3

import datetime

from timeline.helpers import strToDatetime, timeDiff

DATETIME_FORMAT = "%m/%d/%Y %I:%M:%S %p %Z"

class State:
    def __init__(self, start_time, stop_time, tactic, technique):
        """
        Create a new attack state.

        Given:
          start_time (str)  state starting time in EDT format
          stop_time (str)   state ending time in EDT format
          tactic (str)      MITRE ATT&CK tactic
          technique (str)   MITRE ATT&CK technique
        """
        self._start_time = strToDatetime(start_time, DATETIME_FORMAT)

        # We need to handle the case where no `stop_time` is given, i.e. the
        # given state is absorbing. In these cases, set the `stop_time` and
        # the duration to "N/A".
        if stop_time != "":
            self._stop_time = strToDatetime(stop_time, DATETIME_FORMAT)
            self._duration = timeDiff(self._start_time, self._stop_time)
        else:
            self._stop_time = "N/A"
            self._duration = "N/A"

        self._tactic = tactic
        self._technique = technique

    def getStartTime(self):
        return self._start_time

    def getStopTime(self):
        return self._stop_time

    def getDuration(self):
        return self._duration

    def getTactic(self):
        return self._tactic

    def getTechnique(self):
        return self._technique

    def isFinal(self):
        return self._duration == "N/A"

    def __dict__(self):
        return {
            "start_time": self.getStartTime(),
            "stop_time": self.getStopTime(),
            "duration": self.getDuration(),
            "tactic": self.getTactic(),
            "technique": self.getTechnique()
            }
