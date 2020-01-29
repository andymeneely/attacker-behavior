#!/usr/bin/env python3

import json
import pandas

from timeline.Timeline import Timeline

class Team:
    def __init__(self, year, competition, team, data_csv):
        """
        Create a new Team object, which represents a single CPTC Team for a
        single competition in the given year.

        Given:
          year (int)          the year for this team
          competition (str)   one of ['regionals', 'nationals']
          team (int)          the team number for this team
          data_csv (str)      the location on disk of the CSV dataset
        """
        self._year = year
        self._competition = competition
        self._team = team
        self._data_csv = data_csv
        self._json = self._csvToJSON()
        self._timelines = self._jsonToTimelines()

    def _cleanCSV(self):
        """
        Read in a CSV file as a pandas dataframe and clean up NA cells by 
        filling them in with the value of the previous row in the same column.
        """
        data = pandas.read_csv(self._data_csv, sep=",")
        data.fillna(method="ffill", inplace=True)
        
        return data

    def _csvToJSON(self):
        """
        Convert this team's CSV data to a JSON object. Each row in the JSON
        dictionary list will represent a Splunk event as a dictionary with the
        following keys:

          Scenario:           real world scenario for the given vulnerability
          Vulnerability:      name of the given vulnerability
          Evidence:           the source of the evidence for this event
          Time (EDT):         the date-time stamp of this event in EDT
          Unix Time:          the data-time stamp of this event in Unix time
          Host:               the host that logged this event
          Source Type:        the Splunk source type for this event
          Notes:              human annotations for this event
          Event:              the actual logged event
          Format:             the format of the logged event
          ATT&CK Tactic(s):   mapping to relevant MITRE ATT&CK tactic
          ATT&CK Techique(s): mapping to relevant MITRE ATT&CK technique
        """
        clean_csv = self._cleanCSV()
        raw_json = clean_csv.to_json(orient="records")
        raw_json = json.loads(raw_json)

        return raw_json

    def _jsonToTimelines(self):
        """
        Convert the team's JSON dictionary into a list of Timeline objects.
        """
       
        # Remove rows from the JSON where the "Evidence" is "Report" -- these
        # events cannot be automatically converted to timelines as they do not
        # have timestamps associated with them.
        clean_json = list()
        vuln_list = list()
        for row in self._json:
            if row["Evidence"] != "Report":
                clean_json.append(row)
                vuln_list.append(row["Vulnerability"])

        # Create a dictionary for each vulnerability and its associated events
        vuln_list = set(vuln_list)
        vulnerabilities = dict()
        for vuln in vuln_list:
            vulnerabilities[vuln] = list()

        # Collect events for each vulnerability
        for row in clean_json:
            curr_vulnerability = row["Vulnerability"]
            event = {
                "scenario": row["Scenario"],
                "start_time": row["Time (EDT)"],
                "stop_time": "",
                "tactic": row["ATT&CK Tactic(s)"],
                "technique": row["ATT&CK Technique(s)"]
            }
            vulnerabilities[curr_vulnerability].append(event)

        # Create Timeline objects for each vulnerability
        timelines = list()
        for vuln, events in vulnerabilities.items():
            scenario = events[0]["scenario"]
            for event in events:
                del event["scenario"]

            timeline = Timeline(scenario, vuln, events)
            timelines.append(timeline)

        return timelines

    def getYear(self):
        return self._year

    def getCompetition(self):
        return self._competition

    def getTeam(self):
        return self._team

    def getTimelines(self):
        return self._timelines
