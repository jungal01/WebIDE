#cm=$(`stat -c %y hello.c` -gt `stat -c %y cclang`)
#echo $cm
MODDATE=$(stat -c %Y hello.c)
MODDATE=${MODDATE% *}
comDate=$(stat -c %Y cclang)
comDate=${comDate% *}
if [ "$MODDATE" -gt "$comDate" ]; then
  echo "need to recompile"
else
  echo "read from current binary"
fi
