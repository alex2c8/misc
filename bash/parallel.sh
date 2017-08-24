#!/bin/bash

ls -l nan & X=$!
sleep 5 & Y=$!

wait $X
echo "job $X returned $?"
wait $Y
echo "job $Y returned $?"
