FILES="*[^clean_br.sh]*"

for f in $FILES
do
	sed -e 's/<br>/ /g; s/<br >/ /g; s/<br \/>/ /g; s/<br\/>/ /g' $f > "new_"$f
done