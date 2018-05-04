counter=1
while [ $counter -le 50 ]
do
echo DOING T = $counter
time python3 tester.py $counter 20
time python3 tester.py $counter 1;
((counter++))
done
