from unittest import TestCase
import time

import pytest

from nttldict import NaiveTTLDict, NaiveTTLDictDisk


DEFAULT_TTL = 0.04


def sleep():
    return time.sleep(DEFAULT_TTL)

class TestCase:
    def test_create(self):
        cache = NaiveTTLDictDisk(filename='whatever', default_ttl=DEFAULT_TTL)
        
        for k,v in zip(range(10), range(10)):
            # Keys must be str as values!
            cache[str(k)] = v

        assert len(cache) == 10


    def test_persisted(self):
        cache = NaiveTTLDictDisk(filename='whatever', default_ttl=DEFAULT_TTL)

        assert len(cache) == 10
        for key in cache:
            assert key == str(cache[key])

    def test_expired(self):
        cache = NaiveTTLDictDisk(filename='whatever', default_ttl=DEFAULT_TTL)
        assert len(cache) == 10
        sleep()
        assert len(cache) == 0
