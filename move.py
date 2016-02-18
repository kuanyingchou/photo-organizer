# todo:
# - dry run
# - toggle hidden files

import os
import os.path as p
import sys
import time
import datetime
import exifread

args = sys.argv

if len(args) < 3: # program name is included
    exit("need at least 2 args: src and dest")

sources = args[1:-1]
destination = args[-1]

print("sources: %s" % sources)
print("destination: %s" % destination)

def get_date_from_epoch(epoch):
    dt = datetime.datetime.strptime(time.ctime(epoch) , "%a %b %d %H:%M:%S %Y")
    return dt.date().isoformat()

def get_date_created(path):
    return get_date_from_epoch(p.getctime(path))

def get_date_taken(path):
    f = open(path, 'rb')
    tags = exifread.process_file(f)
    ts = tags["EXIF DateTimeOriginal"] 

    #[ ref: http://code.activestate.com/recipes/550811-jpg-files-redater-by-exif-data/
    ts = time.strptime(str(ts) + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
    t = time.mktime(ts)

    return get_date_from_epoch(t)

def get_date(path):
    date = get_date_taken(path)
    if date is None:
        date = get_date_created(path)
        print("couldn't find date exif data in '%s'" % path)
    return date

def mv_file(filepath, dest_dir):
    if not p.exists(dest_dir):
        print("directory '%s' does not exist!" % dest_dir)
    if not p.exists(filepath):
        print("file '%s' does not exist!" % filepath)

    date = get_date(filepath)
    dest_subdir_path = p.join(dest_dir, date)
    filename = p.basename(filepath)
    if not p.exists(dest_subdir_path):
        print("mkdir %s" % dest_subdir_path)
        os.mkdir(dest_subdir_path)

    dest_file_path = p.join(dest_subdir_path, filename)
    if(p.exists(dest_file_path)):
        print("file %s exists. skipping..." % dest_file_path) # todo: override?
    else:
        print("mv %s to %s" % (filepath, dest_file_path))
        os.rename(filepath, dest_file_path);

def mv(path, dest_dir):
    if p.isfile(path):
        if not p.basename(path).startswith("."):
            mv_file(path, dest_dir)
    elif p.isdir(path):
        if not path == dest_dir:
            children = os.listdir(path)
            for c in children:
                mv(p.join(path, c), dest_dir)
    else:
        # todo: links?
        pass

for s in sources:
    mv(s, destination)


# for f in files:
#     print("created: %s" % time.ctime(os.path.getctime(file)))
# 
#     with open('image.jpg', 'rb') as fh:
#         tags = EXIF.process_file(fh, stop_tag="EXIF DateTimeOriginal")
#         dateTaken = tags["EXIF DateTimeOriginal"]
#         return dateTaken
#     
