#!/usr/bin/env python3

import datetime
import os
import re
import shutil
import unittest

from timeline import DATA_DIR, TEST_DIR
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

class TestDrawTimelines(unittest.TestCase):
    def setUp(self):
        self.year = 2018
        self.competition = "regionals"
        self.team = 2
        self.data_csv = os.path.join(DATA_DIR, "2018_regionals_team2.csv")
        self.test_team = Team(self.year, self.competition, self.team, self.data_csv)
        pass

    def test_drawTimelines(self):
        # Set Up
        if not os.path.exists(TEST_DIR):
            os.mkdir(TEST_DIR)

        expected_timelines = [
            """// 2018 regionals, Team 2: Clear Text Credentials in Chat History
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Brute Force, Valid Accounts, Remote Services" [label="Brute Force, Valid Accounts, Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Brute Force, Valid Accounts, Remote Services" [label="2018-11-03 11:03:52 AM"]
            }""",

            """// 2018 regionals, Team 2: Unauthenticated MongoDB Remote Access
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Brute Force, Remote Services" [label="Brute Force, Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Brute Force, Remote Services" [label="2018-11-03 11:10:18 AM"]
            }""",

            """// 2018 regionals, Team 2: No SSL on Sensitive Web Apps
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            }""",

            """// 2018 regionals, Team 2: OpenAudit Default Credentials
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Pre-Attack" [label="Pre-Attack"]
            	"Account Manipulation" [label="Account Manipulation"]
            	"Exploitation of Remote Services / Execution for client exploitation" [label="Exploitation of Remote Services / Execution for client exploitation"]
            	"Remote File Copy" [label="Remote File Copy" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Pre-Attack" [label="2018-11-03 10:00:24 AM"]
            	"Pre-Attack" -> "Account Manipulation" [label="2018-11-03 10:00:31 AM"]
            	"Account Manipulation" -> "Exploitation of Remote Services / Execution for client exploitation" [label="2018-11-03 10:34:04 AM"]
            	"Exploitation of Remote Services / Execution for client exploitation" -> "Remote File Copy" [label="2018-11-03 10:34:01 AM"]
            }""",

            """// 2018 regionals, Team 2: Command Injection in API
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Pre-Attack" [label="Pre-Attack"]
            	"Exploitation of Remote Services" [label="Exploitation of Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Pre-Attack" [label="2018-11-03 07:08:23 AM"]
            	"Pre-Attack" -> "Exploitation of Remote Services" [label="2018-11-03 08:05:46 AM"]
            }""",

            """// 2018 regionals, Team 2: Web App Runs as Privleged User
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"System Service Discovery" [label="System Service Discovery" fillcolor="#A2E8E8"]
            }""",

            """// 2018 regionals, Team 2: Default Traccar Admin Credentials
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Pre-Attack" [label="Pre-Attack"]
            	"Network Service Scanning" [label="Network Service Scanning"]
            	"File and Directory Discovery" [label="File and Directory Discovery"]
            	"Brute Force, Valid Accounts, Remote Services" [label="Brute Force, Valid Accounts, Remote Services"]
            	"Pre-Attack" [label="Pre-Attack"]
            	"Valid Accounts, Remote Services" [label="Valid Accounts, Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Pre-Attack" [label="2018-11-03 10:52:54 AM"]
            	"Pre-Attack" -> "Network Service Scanning" [label="2018-11-03 05:16:22 PM"]
            	"Network Service Scanning" -> "File and Directory Discovery" [label="2018-11-03 02:49:17 PM"]
            	"File and Directory Discovery" -> "Brute Force, Valid Accounts, Remote Services" [label="2018-11-03 01:47:32 PM"]
            	"Brute Force, Valid Accounts, Remote Services" -> "Pre-Attack" [label="2018-11-03 04:12:24 PM"]
            	"Pre-Attack" -> "Valid Accounts, Remote Services" [label="2018-11-03 04:17:25 PM"]
            }""",

            """// 2018 regionals, Team 2: Unauthenticated Postgres remote Access
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Pre-Attack" [label="Pre-Attack"]
            	"Brute Force, Valid Accounts, Remote Services" [label="Brute Force, Valid Accounts, Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Pre-Attack" [label="2018-11-03 05:47:53 PM"]
            	"Pre-Attack" -> "Brute Force, Valid Accounts, Remote Services" [label="2018-11-03 05:49:59 PM"]
            }""",

            """// 2018 regionals, Team 2: MongoDB Listening on 0.0.0.0
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Brute Force, Valid Accounts, Remote Services" [label="Brute Force, Valid Accounts, Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Brute Force, Valid Accounts, Remote Services" [label="2018-11-03 02:46:22 PM"]
            }""",

            """// 2018 regionals, Team 2: Database Stores Plantext Credentials
            digraph {
            	node [shape=box]
            	node [style=filled]
            	node [fillcolor="#EEE9E9"]
            	rankdir=LR
            	splines=polyline
            	"Network Service Scanning" [label="Network Service Scanning" fillcolor="#A2E8E8"]
            	"Pre-Attack" [label="Pre-Attack"]
            	"Brute Force, Valid Accounts, Remote Services" [label="Brute Force, Valid Accounts, Remote Services" fillcolor="#FF9E9E"]
            	"Network Service Scanning" -> "Pre-Attack" [label="2018-11-03 05:47:53 PM"]
            	"Pre-Attack" -> "Brute Force, Valid Accounts, Remote Services" [label="2018-11-03 05:49:59 PM"]
            }"""
        ]

        expected = list()
        actual = list()
        for exp in expected_timelines:
            expected.append(re.sub(r" +", " ", re.sub(r"[\n\t]", " ", exp)))

        actual_timelines, actual_paths = self.test_team.drawTimelines(TEST_DIR, view=False)
        for i in range(len(actual_timelines)):
            self.assertTrue(os.path.exists(actual_paths[i]))
            #print(actual_timelines[i].source)
            actual.append(re.sub(r" +", " ", re.sub(r"[\n\t]", " ", actual_timelines[i].source)))

        expected = sorted(expected)
        actual = sorted(actual)
        for i in range(len(expected)):
            self.assertEqual(expected[i], actual[i])

        # Tear Down
        shutil.rmtree(TEST_DIR)

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
        self.datetime_format = "%m/%d/%Y %I:%M:%S %p %Z"
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
