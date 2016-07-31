#!/bin/sh

. env/bin/activate

# exec here to trick supervisor into killing the right process
exec ./server.py
