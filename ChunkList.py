#!/usr/bin/env python3

from Util.Print import *
from anvil import Region
from re import search
from sys import stdout
from pathlib import Path
from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType

total_region_files = 0
processed_region_files = 0

def parse_args():
    parser = ArgumentParser(description='List chunks stored in the region (Anvil) files that exist in a directory.\nBy default, it lists fully generated chunks.', formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('regionpath', type=Path, help='Directory containing the region files to read (or a single region file).')
    parser.add_argument('-s', '--status', type=str, default='full', help='Chunk status filter (RegEx), by default "full".')
    parser.add_argument('-p', '--print-status', action='store_true', default=False, help='Also print each chunk\'s status.')
    parser.add_argument('-o', '--output-file', nargs='?', type=FileType('w'), default=stdout, help='Output data to a file instead of stdout.')
    args = parser.parse_args()
    return args

def for_each_chunk_in_region(regionfile, consumer, nbt_data=False):
    """
    Calls consumer with each chunk stored in the regionfile.

    Parameters
    ----------
    regiondir
        Region file (Path) to read (files that don't have the .mca suffix get ignored)
    consumer
        The consumer to call for each chunk
    nbt_data
        If true, the consumer will recieve the chunk's NBT data instead

    Returns
    -------
    boolean
        False if the file suffix was not .mca, otherwise True
    """
    if regionfile.suffix == '.mca':
        region = Region.from_file(str(regionfile))
        if region.data: # region file not empty
            chunk_func = region.chunk_data if nbt_data else region.get_chunk
            for x in range(32):
                for z in range(32):
                    try:
                        consumer(chunk_func(x, z), regionfile.name)
                    except Exception as ex:
                        raise Exception('Failed at region "' + regionfile.name + '", chunk (' + str(x) + ',' + str(z) + ')!')
        return True
    return False

def for_each_chunk(regiondir, consumer, nbt_data=False):
    """
    Calls consumer with each chunk stored in the regiondir (all region files).

    Parameters
    ----------
    regiondir
        Directory (Path) containing the region files to read (will only look for files with the .mca suffix)
    consumer
        The consumer to call for each chunk
    nbt_data
        If true, the consumer will recieve the chunk's NBT data instead

    Returns
    -------
    boolean
        True if at least one file was read, otherwise False
    """
    global total_region_files, processed_region_files
    total_region_files = len(list(regiondir.glob('*.mca')))
    if total_region_files > 0:
        for f in regiondir.glob('*.mca'):
            processed_region_files += 1
            for_each_chunk_in_region(f, consumer, nbt_data)
        return True
    return False

def get_level(chunk):  # compat
    if chunk:
        if (not 'Status' in chunk) and ('Level' in chunk):
            chunk = chunk['Level']
            if not 'Status' in chunk:
                raise KeyError('No "Status" key in the level!')
        return chunk
    return None

def print_valid_chunk(chunk, output_file, output_is_file, status, print_status, region_filename):
    global total_region_files, processed_region_files
    level = get_level(chunk)
    if level and search(status, level['Status'].value):
        print(level['xPos'].valuestr() + ',' + level['zPos'].valuestr() + (',' + level['Status'].value if print_status else ''), file=output_file)
        if output_is_file:
            if total_region_files > 0:
                reprint('Processed: ' + str(processed_region_files) + '/' + str(total_region_files) + '  |  Current: ' + region_filename)
            else:
                reprint('Processing: ' + region_filename)

def main():
    args = parse_args()
    regionpath = args.regionpath
    output_file = args.output_file
    output_is_file = output_file and output_file != stdout
    if output_is_file:
        print('Writting to file: ' + output_file.name)
    consumer = lambda chunk, region_filename: print_valid_chunk(chunk, output_file, output_is_file, args.status, args.print_status, region_filename)
    if regionpath.is_dir():
        if not for_each_chunk(regionpath, consumer, True):
            error('No .mca files found in this directory.')
    elif regionpath.is_file():
        if not for_each_chunk_in_region(regionpath, consumer, True):
            error('The file is not .mca')
    else:
        error('Unknown region path.')
    if output_is_file:
        output_file.close()
        print('\nDone!')

if __name__ == '__main__':
    main()
