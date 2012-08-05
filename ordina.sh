#!/bin/bash
DIR='manga/archivio'
#FILES=`find ${DIR} -name \*.cbz`
for FILE in `ls -1 $DIR`;
do
	BASENAME=`basename $FILE`
	DIRNAME=${DIR}/${BASENAME::-8}
	[ -d $DIRNAME ] || mkdir $DIRNAME || exit
	mv -v ${DIR}/${FILE} ${DIRNAME}/
done

