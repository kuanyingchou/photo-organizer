# todo:
# - dry run
# - toggle hidden files
# - toggle verbose
# - file creation date might not be way off
# - options
# - global var/constants is a pain

import os
import os.path as p
import sys
import time
import datetime
import exiftool

mkdir_count = 0
mv_count = 0
skip_count = 0

def get_date_from_epoch(epoch):
    dt = datetime.datetime.strptime(time.ctime(epoch) , "%a %b %d %H:%M:%S %Y")
    return dt.date()

def get_date_created(path):
    return get_date_from_epoch(p.getctime(path))

def get_date_taken(path):
    ts = None
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(path)
        # print metadata
        keys = ["EXIF:DateTimeOriginal", "ICC_Profile:ProfileDateTime", "File:FileModifyDate"]
        for k in keys:
            if k in metadata:
                ts = metadata[k]
                break;

    if ts is None:
        # print(path, tags)
        # exit()
        return None

    #[ ref: http://code.activestate.com/recipes/550811-jpg-files-redater-by-exif-data/
    ts = time.strptime(str(ts)[:10], '%Y:%m:%d')
    t = time.mktime(ts)

    return get_date_from_epoch(t)

def get_date(path):
    date = get_date_taken(path)
    # if date is None:
    #     date = get_date_created(path)
    #     print("warning: couldn't find date exif data in '%s'. using file creation date instead" % path)
    return date

def mv_file_under_date(filepath, dest_dir, dry):
    global mkdir_count
    global mv_count
    global skip_count

    if not p.exists(dest_dir):
        exit("error: directory '%s' does not exist!" % dest_dir)
    if not p.exists(filepath):
        exit("error: file '%s' does not exist!" % filepath)

    date = get_date(filepath)
    if date is None:
        print("warning: couldn't find date exif data in '%s'. skipping..." % filepath)
        skip_count += 1
        return # todo

    dest_year_path = p.join(dest_dir, str(date.year))
    if not p.exists(dest_year_path):
        print("mkdir '%s'" % dest_year_path)
        os.mkdir(dest_year_path)
        mkdir_count += 1

    dest_date_path = p.join(dest_year_path, date.isoformat())
    filename = p.basename(filepath)
    if not p.exists(dest_date_path):
        print("mkdir '%s'" % dest_date_path)
        if not dry:
            os.mkdir(dest_date_path)
        mkdir_count += 1

    dest_file_path = p.join(dest_date_path, filename)
    if(p.exists(dest_file_path)):
        print("file '%s' already exists. skipping..." % dest_file_path) # todo: override?
    else:
        print("mv '%s' to '%s'" % (filepath, dest_file_path))
        if not dry:
            os.rename(filepath, dest_file_path)
        mv_count += 1

def mv_under_date(path, dest_dir, dry):
    if not p.exists(dest_dir):
        exit("error: directory '%s' does not exist!" % dest_dir)
    if not p.exists(path):
        exit("error: file '%s' does not exist!" % filepath)

    if p.isfile(path):
        if not p.basename(path).startswith("."):
            mv_file_under_date(path, dest_dir, dry)
    elif p.isdir(path):
        if not path == dest_dir:
            children = os.listdir(path)
            for c in children:
                mv_under_date(p.join(path, c), dest_dir, dry)
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

    dry = False
    for s in sources:
        mv_under_date(s, destination, dry)
    print("%s file(s) moved" % mv_count)
    print("%s dir(s) created" % mkdir_count)
    print("%s file(s) skipped" % skip_count)
    print("done!")

