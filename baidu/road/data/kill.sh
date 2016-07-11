#!/bin/bash
ps -ef | grep yncongestion | grep -v grep | cut -c 9-15 | xargs kill -s 9;
ps -ef | grep phantomjs | grep -v grep | cut -c 9-15 | xargs kill -s 9
