#!/usr/bin/env python3

from uuid import UUID

def ints_to_uuid(nums):
    to_bytes = lambda x: x.to_bytes(int(16 / len(nums)), byteorder='big', signed=True)
    bytes = b''
    for i in nums:
        bytes += to_bytes(i)
    return UUID(bytes=bytes)
