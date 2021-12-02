# MC World Analysis Tools
Small scripts to extract info from Minecraft worlds.

## ChunkList
Lists the chunk coordinates of all generated chunks, stored in specified region files. You can also tell it to list proto-chunks (by default, it only lists fully generated ones), print each chunk's generation status or write to a file. The values are comma-separated, so you can easily manipulate them further, using other tools.

usage: `ChunkList.py [-h] [-s STATUS] [-p] [-o [OUTPUT_FILE]] regionpath`

example: `python3 ChunkList.py ./world/region --output-file ./chunklist.csv`

Notes:
- This is an expensive task! If you have a big world, this might take hours.
- This requires [anvil-parser](https://pypi.org/project/anvil-parser/) to be installed.

## PlayerList
List players stored in the files in the playerdata directory. The values are comma-separated, so you can easily manipulate them further, using other tools.

usage: `PlayerList.py [-h] [-u] [-n] [-p] [-o [OUTPUT_FILE]] playerdatapath`

example: `python3 PlayerList.py ./world/playerdata --output-file ./playerlist.csv`

Notes:
- This requires [NBT](https://pypi.org/project/NBT/) to be installed.
