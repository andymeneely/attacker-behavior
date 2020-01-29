#!/usr/bin/env python3

import datetime
import os
import unittest

from timeline import DATA_DIR
from timeline.State import State
from timeline.Team import Team
from timeline.Timeline import Timeline
from timeline.helpers import strToDatetime, timeDiff

class TestTeam(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        year = 2018
        competition = "regionals"
        team = 2
        data_csv = os.path.join(DATA_DIR, "2018_regionals_team2.csv")

        self.test_team = Team(year, competition, team, data_csv)

        expected_year = year
        actual_year = self.test_team.getYear()
        self.assertEqual(expected_year, actual_year)

        expected_competition = competition
        actual_competition = self.test_team.getCompetition()
        self.assertEqual(expected_competition, actual_competition)

        expected_team = team
        actual_team = self.test_team.getTeam()
        self.assertEqual(expected_team, actual_team)

        expected_length = 10
        actual_length = len(self.test_team.getTimelines())
        self.assertEqual(expected_length, actual_length)

class TestTimeline(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        scenario = "Initial Access to Company Credentials and Information"
        vulnerability = "Clear Text Credentials in Chat History"
        event_data = [
            {'start_time': '11/03/2018 09:59:13 AM EDT',
             'stop_time': '',
             'tactic': 'Discovery',
             'technique': 'Network Service Scanning'},
            {'start_time': '11/03/2018 10:02:26 AM EDT',
             'stop_time': '',
             'tactic': 'Discovery',
             'technique': 'Network Service Scanning'},
            {'start_time': '11/03/2018 11:03:52 AM EDT',
             'stop_time': '',
             'tactic': 'Credential Access, Lateral Movement, Lateral Movement',
             'technique': 'Brute Force, Valid Accounts, Remote Services'},
            {'start_time': '11/03/2018 11:06:09 AM EDT',
             'stop_time': '',
             'tactic': 'Credential Access, Lateral Movement, Lateral Movement',
             'technique': 'Brute Force, Valid Accounts, Remote Services'}
        ]

        self.test_timeline = Timeline(scenario, vulnerability, event_data)

        expected_states = [
            {'start_time': datetime.datetime(2018, 11, 3, 9, 59, 13),
             'stop_time': datetime.datetime(2018, 11, 3, 11, 3, 52),
             'duration': 3879.0,
             'tactic': 'Discovery',
             'technique': 'Network Service Scanning'},
            {'start_time': datetime.datetime(2018, 11, 3, 11, 3, 52),
             'stop_time': 'N/A',
             'duration': 'N/A',
             'tactic': 'Credential Access, Lateral Movement, Lateral Movement',
             'technique': 'Brute Force, Valid Accounts, Remote Services'}
        ]
        actual_states = self.test_timeline.getStates()
        for i in range(len(expected_states)):
            self.assertDictEqual(expected_states[i], actual_states[i].__dict__())

        expected_scenario = scenario
        actual_scenario = self.test_timeline.getScenario()
        self.assertEqual(expected_scenario, actual_scenario)

        expected_vulnerability = vulnerability
        actual_vulnerability = self.test_timeline.getVulnerability()
        self.assertEqual(expected_vulnerability, actual_vulnerability)

class TestState(unittest.TestCase):
    def setUp(self):
        self.datetime_format = "%m/%d/%Y %H:%M:%S %p %Z"
        pass

    def test_init(self):
        start_time = "11/03/2018 09:59:13 AM EDT"
        stop_time = "11/03/2018 11:03:52 AM EDT"
        tactic = "Discovery"
        technique = "Network Service Scanning"
        self.test_state = State(start_time, stop_time, tactic, technique)

        expected_start = strToDatetime(start_time, self.datetime_format)
        actual_start = self.test_state.getStartTime()
        self.assertEqual(expected_start, actual_start)

        expected_stop = strToDatetime(stop_time, self.datetime_format)
        actual_stop = self.test_state.getStopTime()
        self.assertEqual(expected_stop, actual_stop)

        expected_duration = timeDiff(expected_start, expected_stop)
        actual_duration = self.test_state.getDuration()
        self.assertEqual(expected_duration, actual_duration)

        expected_tactic = tactic
        actual_tactic = self.test_state.getTactic()
        self.assertEqual(expected_tactic, actual_tactic)

        expected_technique = technique
        actual_technique = self.test_state.getTechnique()
        self.assertEqual(expected_technique, actual_technique)

        expected_dict = {
            'start_time': datetime.datetime(2018, 11, 3, 9, 59, 13),
            'stop_time': datetime.datetime(2018, 11, 3, 11, 3, 52),
            'duration': 3879.0,
            'tactic': 'Discovery',
            'technique': 'Network Service Scanning'
        }
        actual_dict = self.test_state.__dict__()
        self.assertDictEqual(expected_dict, actual_dict)

if __name__ == "__main__":
    unittest.main(warnings="ignore")
