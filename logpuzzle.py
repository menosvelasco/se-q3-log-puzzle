#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # (r'_(\S*)\W', filename)
    host_name = filename.split('_')
    host_name = host_name[1]
    with open(filename, 'r') as f:

        print(f)
        em_list = []
        for value in f:
            get_space = re.search(r'GET (\S*)', value)
            group_get = get_space.group(1)

            if group_get:
                if 'puzzle' in group_get:
                    url_list = f'http://{host_name}{group_get}'
                    print(url_list)
                    em_list.append(url_list)

        return sorted(list(set(em_list)), key=lambda url_w: url_w[-8:-4])


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    with open('index.html', 'w') as f:
        f.write('<html><body>')

        image_count = 0
        for i in img_urls:
            print(i)
            image = f'img{str(image_count)}.jpg'

            file_name = os.path.join(dest_dir, image)
            urllib.request.urlretrieve(i, file_name)
            print('retrieve')
            f.write(f'<img src="{file_name}"/>')
            image_count += 1
        f.write('</body></html>')


# http: // code.google.com/edu/languages/google-python-class/images/puzzle/a-baaa.jpg

def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
