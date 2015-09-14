gender="male"; wc -l ${gender}.txt; ./whittle.py ${gender}; cat ${gender}.txt.out | sort > ${gender}.txt
gender="female"; wc -l ${gender}.txt; ./whittle.py ${gender}; cat ${gender}.txt.out | sort > ${gender}.txt
