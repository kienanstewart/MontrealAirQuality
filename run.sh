#!/usr/bin/env bash
export HOME=/Users/rorygeoghegan

. $HOME/.python/bin/activate
cd $HOME/prog/python/MontrealAirQuality
fab --hide=status update_stream
