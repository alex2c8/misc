ts=1504981429
off=200000

for i in `seq $(($ts-$off)) $(($ts))`;
do
	./solve secret.enc ./out/_$i $i
	grep -i OWASP ./out/_$i

	# printf $(($i))
	# printf "\n"

	if [ $? != 0 ]; then
		rm -f ./out/_$i
	else
		echo out_$i
	fi
done
