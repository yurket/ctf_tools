#!/bin/bash

BINDIR=/usr/local/bin

sudo install -v -m 0755 create_new_src.py $BINDIR/create_new_src
sudo install -v -m 0755 text_stat.py $BINDIR/text_stat
