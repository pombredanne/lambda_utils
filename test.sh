#!/bin/bash -e

coverage run test.py
coverage report -m
coverage erase
