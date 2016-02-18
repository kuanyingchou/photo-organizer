# move pictures/videos into directories according to date

Turning:

src
|- img1.jpg
|- img2.jpg
|- img3.jpg
...

into:

dest
|- 2015
    |- 2015-12-31
        |- img1.jpg
   2016
    |- 2016-01-01
        |- img2.jpg
    |- 2016-01-03
        |- img3.jpg
...

Install PyExifTool then run: 

    python app.py src1 src2 ... dest


other tools:
  EXIF.py (exifread) - can't read some files
  Pillow (PIL) -  can't read some files, can't read mov files

  mdls
  exiftool

  find d -name '*.JPG' -exec mv {} s/ \;
