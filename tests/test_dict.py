from unittest import TestCase
import time

import pytest

from nttldict import NaiveTTLDict, NaiveTTLDictDisk


DEFAULT_TTL = 0.03

ttldict = NaiveTTLDict(default_ttl=DEFAULT_TTL)
ttlcache = NaiveTTLDictDisk(filename='.foo.bar', default_ttl=DEFAULT_TTL)

INSTANCES = [ttldict, ttlcache]

def sleep():
    return time.sleep(DEFAULT_TTL)

@pytest.mark.parametrize('instance', INSTANCES)
class TestCase:
    
    def test_empty(self, instance):
        assert len(instance) == 0

    def test_basics(self, instance):
        assert instance.get('a') is None
        instance['a'] = 'x'
        assert instance.get('a') == 'x'
        instance['a'] = 'y'
        assert instance.get('a') == 'y'

        sleep()
        assert instance.get('a') is None

        instance['a'] = 'x'
        assert instance.get('a') == 'x'

        # every item must be expired
        sleep()
        assert len(instance) == 0


    def test_len(self, instance):
        assert len(instance) == 0

        instance['a'] = 1
        instance['b'] = 2
        assert len(instance) == 2
        sleep()
        assert len(instance) == 0

    def test_contains(self, instance):
        assert 'b' not in instance
        instance['b'] = 'y'
        assert 'b' in instance

        sleep()
        assert 'b' not in instance

    def test_get(self, instance):
        instance['a'] = 1
        assert instance.get('a') == 1
        assert instance.get('b', "default") == "default"
        sleep()
        assert instance.get('a', "default") == "default"
    
    def test_set(self, instance):
        # With param
        instance.set('a', 'y', DEFAULT_TTL + 0.01)
        assert instance['a'] == 'y'
        sleep()
        assert instance['a'] == 'y'
        sleep()
        assert instance.get('a') is None

        # Without param
        instance.set('a', 'y')
        assert instance['a'] == 'y'
        sleep()
        assert instance.get('a') is None

    def test_pop(self, instance):
        instance['a'] = 'x'
        assert instance.pop('a') == 'x'
        sleep()
        assert instance.pop('a') is None

    def test_iter_empty(self, instance):
        for key in instance:
            pytest.fail(f"Iterating empty dictionary gave a key {key}")

        assert [k for k in instance] == []

    def test_iter(self, instance):
        instance['a'] = 'x'
        instance['b'] = 'y'
        instance['c'] = 'z'
        assert sorted([k for k in instance]) == sorted(['a', 'b', 'c'])

        assert sorted([k for k in instance.values()]) == sorted(['x', 'y', 'z'])
        sleep()
        assert [k for k in instance] == []

        for k in range(10):
            # Keys must be str as values!
            instance[str(k)] = k
        
        assert len(instance) == 10
        
        for key in instance:
            assert key == str(instance[key])
        
        sleep()
        assert len(instance) == 0

    def test_values(self, instance):
        assert len(instance.values()) == 0

        for k in range(10):
            # Keys must be str as values!
            instance[str(k)] = k
        
        assert len(instance) == 10
        assert len(instance.values()) == 10
        
        for v in instance.values():
            assert v == instance[str(v)]

        sleep()
        assert len(instance) == 0

    def test_items(self, instance):
        assert len(instance.items()) == 0

        for k in range(10):
            # Keys must be str as values!
            instance[str(k)] = k
        
        assert len(instance) == 10
        assert len(instance.items()) == 10
        
        for k, v in instance.items():
            assert k == str(v)

        sleep()
        assert len(instance) == 0

    def test_objects(self, instance):
        d = dict(foo="bar",b= 2)
        instance['a'] = range(10)
        instance['b'] = d
        instance['c'] = object()

        assert len(instance) == 3
        assert instance.get('a') == range(10)
        assert instance.get('b') == d
        assert type(instance.get('c')) == type(object())

        sleep()
        assert len(instance) == 0