#!/bin/sh

#TXT_FILE="data/big.txt"
#TXT_FILE="data/0643/combined"
#TXT_FILE="data/google-books-common-words-no-cnt.txt"
D_BASE="data/big_english_word_lists"
D_FILE="1 2 3 4 5 6 7 8 9 10";
#D_FILE="10";
BUF_DIR="/tmp/mdbsc"

####################################
for d in $D_FILE; do
rm -rf $BUF_DIR
TXT_FILE="$D_BASE/wlist_match$d.txt"
#echo "Basic"
B=`python impl1.py $TXT_FILE`
#echo "LMDB"
L=`python impl2.py $TXT_FILE $BUF_DIR`
echo "$B\t$L"
done;

