# Naive TTL Dictionary

This is a naive implementation of a dict-like interface with key expiration and optionally, persistence.

## Install


```
pip install nttldict
```

## Usage

```
import nttldict
from time import sleep

ttldict = NaiveTTLDict(default_ttl=1)

ttldict['a'] = 'x'

sleep(1)
instance.get('a')

```
it should return `None`

To persist the dict on disk, useful for CLI tools, use `NaiveTTLDictDisk` class

## Why is it naive?

It contains some gotchas:
- Is not thread-safe
- It checks expiration on access
- Is not optimized, most operations are `O(n)` or worse
- Persistence uses writeback, which is not bad, but current `shelve` implementation duplicates memory

## How is this useful?

You can store arbitrary objects (anything that `pickle` can handle). Current use case is to store different kind of credentials in CLI tools.
