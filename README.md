# MC World Analysis Tools
Small scripts to extract info from Minecraft worlds.

## ChunkList
Lists the chunk coordinates of all generated chunks, stored in specified region files. You can also tell it to list proto-chunks (by default, it only lists fully generated ones), print each chunk's generation status or write to a file. The values are comma-separated, so you can easily manipulate them further, using other tools.

usage: `ChunkList.py [-h] [-s STATUS] [-p] [-o [OUTPUT_FILE]] regionpath`

example: `python3 ChunkList.py ./world/region --output-file ./chunklist.csv`

Notes:
- This is an expensive task! If you have a big world, this might take hours.
- This requires [anvil-parser](https://pypi.org/project/anvil-parser/) to be installed.
