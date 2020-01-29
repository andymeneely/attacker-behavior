#!/bin/sh

coverage run --source=timeline test_timeline.py;
coverage report -m;
