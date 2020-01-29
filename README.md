# attacker-behavior
Scripts to analyze penetration testing timelines to understand attacker behavior

# Modules

## timeline

Automation scripts for converting our research timeline spreadsheets into graphical timelines.

### Design Decision

There are Python libraries that allow you to download a Google Sheet using Google API Keys, but these keys are unique to a specific Google Account (or Business Account) -- rather than the headache of everyone who wants to use these scripts having to set up an API key and then having to store it in an ignored file within this repository, I chose to implement this code to work with CSV exports of Google Sheets. This means that anyone with access to the attack timelines can download any timeline as a CSV and get to work. CSV files are also significantly easier to parse than XLSX files.

### Prerequisite

To use these scripts, you need to open one of the timeline spreadsheets ([example]
(https://docs.google.com/spreadsheets/d/1Q6w5TAvlZszQL71pNK2QKzBs_p1MdE4kCId1kXIdAOk/edit#gid=0)) in Google Drive.

Then use `File-->Download-->Comma-separated values (.csv, current sheet)` on the default sheet. Save this file to the `data/` directory in this module.

### Testing

To test, run `./run_tests.sh`.
