#!/bin/sh

coverage run --source=markov_chain test_markov_chain.py;
coverage report -m;
