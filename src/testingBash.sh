for d in */; do
	echo "$d"
	rm $d/*.html
	rm $d/*.py
	unzip scripts.zip -d $d
	cd $d
	python3 generatePage.py
	google-chrome *Py.html &
	cd ..
done

find . -name "*Py.html" | zip filesHTML.zip -@