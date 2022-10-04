unzip Art_Assets.zip
folder="Frames_EPS/"
files=`ls $folder`

for file in $files
do
	echo "${file##*/}"
	new_file="${file%.jgr}".eps
	jgraph $folder$file > $folder$new_file
done

