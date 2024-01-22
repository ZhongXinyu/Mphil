#!/usr/bin/env bash

echo "**** Variables ****"
var1=1
echo "var1 = $var1"
echo 'var1 = $var1'

str1="Hello"
echo "str1 = $str1"
echo 'str1 = $str1'

echo ""
echo "**** Strings ****"
test_string1='abcdefghijklm'
test_string2='nopqrstuvwxyz'
echo ${#test_string1}   #string length
echo "** Substrings"
echo ${test_string1:7} #substring from position 7
echo ${test_string1:7:4} #substring from position 7, for 4 characters
echo "** Substring Removal"
echo ${test_string1#'abc'} #shortest substring removed from front
echo ${test_string1##'abc'} #longest substring removed from front
echo ${test_string1%'klm'} #shortest substring removed from back
echo ${test_string1%%'klm'} #longest substring removed from back
echo "** Replacement"
echo ${test_string1/efg/567} #replacement first match
echo ${test_string1//efg/567} #replacement all matches
echo "** note: to make match at front or back add # or %"
echo "** if no replacement is supplied does deletion"
echo ${test_string1/efg} #deletion
echo "** Joining"
echo $test_string1$test_string2 #joining strings, += also works

echo ""
echo "**** Loops ****"

for i in {1..10}; # {1..10} expands to "1 2 3 4 5 6 7 8 9 10"
do 
    echo "List form:    The iteration number is $i"
done

for (( i = 0; i < 10; i++ )) #C style loop
do
    echo "C style form: The iteration number is $i"
done

i=0
while [ $i -lt 5 ] #Executes until false
do
    echo "while: i is currently $i"
    i=$[$i+1] #Not the lack of spaces around the brackets. This makes it a not a test expression
done

i=5
until [[ $i -eq 10 ]]; #Executes until true
do
    echo "until: i is currently $i"
    i=$((i+1))
done

echo ""
echo "**** Conditionals ****"
num=5
if [ "$num" -eq 1 ]; then
    echo "the number is 1"
elif [ "$num" -gt 2 ]; then
    echo "the number is greater than 2"
else
    echo "The number was not 1 and is not more than 2."
fi

echo ""
echo "**** Functions ****"
function_greet() {
    echo "This script is called $0"
    echo "Hello $1"
}

function_greet "James"

# Global variable return
function_add1 () {
    wrong=$1+$2
    sum=$(($1+$2))
}
function_add1 6 7
echo $wrong
echo $sum

# Local variable return
function_add2 () {
    local sum=$(($1+$2))
    echo $sum
}

#