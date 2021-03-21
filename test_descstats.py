#!/usr/bin/env python3

import io
import pytest


def test_is_batches_number(script_runner):
    inp = io.StringIO("QQ\n")
    scrret = script_runner.run("descstats.py", "x", stdin=inp)
    assert scrret.success
    assert (
        scrret.stdout
        == "Number of batches must be a number - setting default value for batches - 1\n"
    )


def test_is_input_number(script_runner):
    inp = io.StringIO("Z\nQQ\n")
    scrret = script_runner.run("descstats.py", "10", stdin=inp)
    assert scrret.success
    assert scrret.stderr == "Skipping - not a number\n"


def test_single_line_number(script_runner):
    inp = io.StringIO("5\nQQ\n")
    scrret = script_runner.run("descstats.py", "1", stdin=inp)
    assert scrret.success
    assert scrret.stdout == "5.0,0.0,5.0\n"


def test_sample_line_number(script_runner):
    inp = io.StringIO("1\n2\n3\n137.036\nQQ\n")
    scrret = script_runner.run("descstats.py", "1", stdin=inp)
    assert scrret.success
    assert (
        scrret.stdout == "1.0,0.0,1.0\n1.5,0.5,1.5\n2.0,0.816,2.0\n35.759,58.477,2.5\n"
    )


def test_batch5_line_number(script_runner):
    inp = io.StringIO("1\n2\n3\n4\n5\nQQ\n")
    scrret = script_runner.run("descstats.py", "5", stdin=inp)
    assert scrret.success
    assert scrret.stdout == "3.0,1.414,3.0\n"


def test_sample2_line_number(script_runner):
    inp = io.StringIO("1\n2\n3\n137.036\nQQ\n")
    scrret = script_runner.run("descstats.py", "2", stdin=inp)
    assert scrret.success
    assert scrret.stdout == "1.5,0.5,1.5\n35.759,47.39,3.0\n"
