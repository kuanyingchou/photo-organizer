# todo:
# - dry run
# - toggle hidden files
# - toggle verbose

import os
import os.path as p
import sys
import time
import datetime
import exifread

mkdir_count = 0
mv_count = 0


def get_date_from_epoch(epoch):
    dt = datetime.datetime.strptime(time.ctime(epoch) , "%a %b %d %H:%M:%S %Y")
    return dt.date().isoformat()

def get_date_created(path):
    return get_date_from_epoch(p.getctime(path))

def get_date_taken(path):
    f = open(path, 'rb')
    tags = exifread.process_file(f)
    key = "EXIF DateTimeOriginal"
    if key in tags:
        ts = tags[key] 
    else:
        return None

    #[ ref: http://code.activestate.com/recipes/550811-jpg-files-redater-by-exif-data/
    ts = time.strptime(str(ts) + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
    t = time.mktime(ts)

    return get_date_from_epoch(t)

def get_date(path):
    date = get_date_taken(path)
    if date is None:
        date = get_date_created(path)
        print("warning: couldn't find date exif data in '%s'. using file creation date instead" % path)
    return date

def mv_file_under_date(filepath, dest_dir):
    global mkdir_count
    global mv_count

    if not p.exists(dest_dir):
        exit("error: directory '%s' does not exist!" % dest_dir)
    if not p.exists(filepath):
        exit("error: file '%s' does not exist!" % filepath)

    date = get_date(filepath)
    dest_subdir_path = p.join(dest_dir, date)
    filename = p.basename(filepath)
    if not p.exists(dest_subdir_path):
        print("mkdir '%s'" % dest_subdir_path)
        os.mkdir(dest_subdir_path)
        mkdir_count += 1

    dest_file_path = p.join(dest_subdir_path, filename)
    if(p.exists(dest_file_path)):
        print("file '%s' already exists. skipping..." % dest_file_path) # todo: override?
    else:
        print("mv '%s' to '%s'" % (filepath, dest_file_path))
        os.rename(filepath, dest_file_path);
        mv_count += 1

def mv_under_date(path, dest_dir):
    if not p.exists(dest_dir):
        exit("error: directory '%s' does not exist!" % dest_dir)
    if not p.exists(path):
        exit("error: file '%s' does not exist!" % filepath)

    if p.isfile(path):
        if not p.basename(path).startswith("."):
            mv_file_under_date(path, dest_dir)
    elif p.isdir(path):
        if not path == dest_dir:
            children = os.listdir(path)
            for c in children:
                mv_under_date(p.join(path, c), dest_dir)
    else:
        # todo: links?
        pass

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 3: # program name is included
        exit("need at least 2 args: src and dest")

    sources = args[1:-1]
    destination = args[-1]

    if len(sources) > 1:
        src_str = ", ".join(["'" + s + "'" for s in sources[:-1]]) + " and " + sources[-1]
    else:
        src_str = "'"+sources[0]+"'"


    print("moving files from %s to '%s'..." % (src_str, destination))

    for s in sources:
        mv_under_date(s, destination)
    print("%s file(s) moved" % mv_count)
    print("%s dir(s) created" % mkdir_count)
    print("done!")

