#! /usr/bin/env bash

pip3 install --upgrade setuptools wheel twine
python3 ./setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
