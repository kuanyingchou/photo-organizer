Move pictures/videos into directories according to capturing date.

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

Install [PyExifTool](https://github.com/smarnach/pyexiftool), then run: 

    python organize.py src1 src2 ... dest

