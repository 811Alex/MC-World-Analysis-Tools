#!/usr/bin/env python3

from Util.Print import *
from Util.UUID import *
from nbt import nbt
from time import sleep
from requests import get
from json import loads as parse_json
from sys import stdout, stderr
from pathlib import Path
from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType

ENDPOINT_UUID_TO_NAME = 'https://sessionserver.mojang.com/session/minecraft/profile/'
API_REQUEST_DELAY = .5
total_playerdata_files = 0
processed_playerdata_files = 0

def parse_args():
    parser = ArgumentParser(description='List players stored in the files in the playerdata directory.', formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('playerdatapath', type=Path, help='The playerdata directory to read (or a single playerdata file).')
    parser.add_argument('-u', '--no-uuid', action='store_true', default=False, help='Don\'t print UUIDs.')
    parser.add_argument('-n', '--name', action='store_true', default=False, help='Print player names (needs internet connectivity, much slower). If a name was not found or the UUID was made by Floodgate, it\'ll skip it when only printing names, or print <unknown> or <floodgate> when printing other info too.')
    parser.add_argument('-p', '--position', action='store_true', default=False, help='Print player positions.')
    parser.add_argument('-o', '--output-file', nargs='?', type=FileType('w'), default=stdout, help='Output data to a file instead of stdout.')
    args = parser.parse_args()
    return args

def with_playerdata(playerdatafile, consumer):
    if playerdatafile.suffix == '.dat':
        try:
            consumer(nbt.NBTFile(playerdatafile,'rb'), playerdatafile.name)
        except Exception as ex:
            raise Exception('Failed at playerdata file "' + playerdatafile.name + '"!')
        return True
    return False

def for_each_playerdata(playerdatadir, consumer, slow_down = False):
    global total_playerdata_files, processed_playerdata_files
    total_playerdata_files = len(list(playerdatadir.glob('*.dat')))
    if total_playerdata_files > 0:
        for f in playerdatadir.glob('*.dat'):
            processed_playerdata_files += 1
            with_playerdata(f, consumer)
            if slow_down and processed_playerdata_files != total_playerdata_files:
                sleep(API_REQUEST_DELAY)   # to take it easy on the API
        return True
    return False

def get_uuid(player):
    if player:
        if 'UUID' in player:
            return ints_to_uuid(player['UUID'])
        if 'UUIDLeast' in player and 'UUIDMost' in player:
            return ints_to_uuid([int(str(player['UUIDLeast'])), int(str(player['UUIDMost']))])
        raise KeyError('Can\'t find UUID key(s) in player data!')
    return None

def get_name(uuid):
    if is_xuid(uuid):
        return '<floodgate>', False
    else:
        resp = get(ENDPOINT_UUID_TO_NAME + uuid.hex)
        if resp.status_code == 200:
            return parse_json(resp.text)['name'], True
        else:
            return '<unknown>', False

def print_player(player, output_file, output_is_file, print_uuid, print_name, print_pos, playerdata_filename):
    global total_playerdata_files, processed_playerdata_files
    if player:
        uuid = get_uuid(player)
        info = []
        if print_uuid:
            info.append(str(uuid))
        if print_name:
            name, found = get_name(uuid)
            if found or print_uuid or print_pos:
                info.append(name)
        if print_pos:
            info.append(','.join(map(str, player['Pos'])))
        if len(info) > 0:
            print(','.join(info), file=output_file)
        if output_is_file:
            if total_playerdata_files > 0:
                reprint('Processed: ' + str(processed_playerdata_files) + '/' + str(total_playerdata_files) + '  |  Current: ' + playerdata_filename)
            else:
                reprint('Processing: ' + playerdata_filename)

def main():
    args = parse_args()
    if args.no_uuid and not args.name and not args.position:
        error('Nothing to print, change arguments.')
        return
    playerdatapath = args.playerdatapath
    output_file = args.output_file
    output_is_file = output_file and output_file != stdout
    if output_is_file:
        print('Writting to file: ' + output_file.name)
    consumer = lambda player, playerdata_filename: print_player(player, output_file, output_is_file, not args.no_uuid, args.name, args.position, playerdata_filename)
    if playerdatapath.is_dir():
        if not for_each_playerdata(playerdatapath, consumer, args.name):
            error('No .dat files found in this directory.')
    elif playerdatapath.is_file():
        if not with_playerdata(playerdatapath, consumer):
            error('The file is not .dat')
    else:
        error('Unknown playerdata path.')
    if output_is_file:
        output_file.close()
        print('\nDone!')

if __name__ == '__main__':
    main()
