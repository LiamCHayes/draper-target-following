#!/usr/bin/env python
'''
Finds undefined citations in the LaTeX log, and suggests bib files to include
'''

import os
import re


def citations_read(filename='master.log'):
    '''
    Simple regex-based parser to find undefined citations from the LaTeX log.
    '''
    citation_set = set()

    prefix = r"^.*`"
    suffix = r"'.*$"
    regex_trim = fr"({prefix}|{suffix})"
    regex_match = r"Citation.*undefined"
    with open(filename) as fid:
        for line in fid:
            if re.search(regex_match, line):
                line_new = re.sub(regex_trim, '', line).rstrip()
                citation_set.add(line_new)
    return citation_set


def files_list_ext(ext):
    '''
    Return all the files in the current directory
    '''
    # Source: https://stackoverflow.com/questions/19309667/recursive-os-listdir
    return [
        os.path.join(dp, f) for dp, _, fn in os.walk(".") for f in fn
        if f[-4:] == '.' + ext
    ]


def bib_entries(filename='biblio/consensus.bib'):
    '''
    Very simple regex-based BibTeX parser to extract names of entries

    Uses a regex to detect lines that start with "@" and extract the entry name
    '''
    entries_set = set()
    regex_match = r'@.*{([^,\s]*),'
    with open(filename) as fid:
        for line in fid:
            mtch = re.search(regex_match, line)
            if mtch:
                entries_set.add(mtch.groups()[0])
    return entries_set


def bib_file_list(dirname='./biblio'):
    '''
    Get list of all .bib files
    '''
    file_list = os.listdir(dirname)
    file_list = [x for x in file_list if x[-4:] == '.bib']
    return file_list


def bib_file_dict(dirname='./biblio'):
    '''
    Create a dict mapping each file name to the set of entries in that file
    '''
    file_list = bib_file_list(dirname)
    file_dict = {}
    for filename in file_list:
        filename_full = os.path.join(dirname, filename)
        file_dict[filename] = bib_entries(filename_full)
    return file_dict


def citations_filter_with_entries(citations: set, entries: set):
    '''
    Find the set of citations that match the given entries, and return it
    alongside the original citation set with the matched citations removed
    '''
    citations_matched = [x for x in citations if x in entries]
    citations.difference_update(citations_matched)

    return citations_matched, citations


def bib_included_read(filename='refs.tex', bib_included_files=None):
    '''
    Parse a single .tex files to extract the argument of the \bibliography command
    '''
    if bib_included_files is None:
        bib_included_files = set()

    regex_comments = r'%.*$|'
    regex_list = r'\\bibliography{([^\s}]*)}'
    regex_lstrip = r'(.*/)?'
    with open(filename) as fid:
        line_list = [line.strip() for line in fid]
        line_list = [re.sub(regex_comments, '', line) for line in line_list]
        line_str = ''.join(line_list)
        mtch = re.search(regex_list, line_str)
        if mtch is not None:
            for group in mtch.groups():
                for bib_file in group.split(','):
                    bib_file = re.sub(regex_lstrip, '', bib_file)
                    bib_included_files.add(bib_file)
    return bib_included_files


def bib_included_list(tex_file_list=files_list_ext('tex')):
    '''
    Parse all .tex files to extract the argument of the \bibliography command
    '''
    bib_included_files = set()
    for filename in tex_file_list:
        included_files = bib_included_read(filename)
        bib_included_files = bib_included_files.union(included_files)
    return bib_included_files


def match(log_filename='master.log', bib_dirname='./biblio'):
    '''
    Get set of files that contain citations to find, and set of citations that
    do not appear in any file
    '''
    black_list = {'concat'}
    citations_to_find = citations_read(log_filename)
    files_dict = bib_file_dict(bib_dirname)
    files_to_include = set()
    for filename, entries in files_dict.items():
        if filename not in black_list:
            citations_matched, citations_to_find = citations_filter_with_entries(
                citations_to_find, entries)
            if len(citations_matched) > 0:
                filename = filename[:-4]
                files_to_include.add(filename)

    files_to_include.difference_update(bib_included_list())
    if len(citations_to_find) > 0:
        print(','.join(citations_to_find))

    files_to_include_full = [
        os.path.join(bib_dirname.replace('./', ''), file)
        for file in files_to_include
    ]
    print(','.join(sorted(files_to_include_full)))


if __name__ == '__main__':
    match()
