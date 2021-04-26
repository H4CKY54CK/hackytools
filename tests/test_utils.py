from hackytools.utils import *

def test_ftime_ns():
    data = (
        (0, '0', 'ns'),
        (10, '10', 'ns'),
        (371, '371', 'ns'),
        (5150, '5', '\u00b5s'),
        (58715, '58', '\u00b5s'),
        (987465, '987', '\u00b5s'),
        (3167431, '3', 'ms'),
        (64744741, '64', 'ms'),
        (943167497, '943', 'ms'),
        (6468541351, '6', 's'),
    )

    for n, pre, after in data:
        res = ftime_ns(n)
        assert res.startswith(pre), "Expected: %s | Got: %s" % (pre + ' ' + after, res)
        assert res.endswith(after), "Expected: %s | Got: %s" % (pre + ' ' + after, res)


def test_ftime():
    data = (
        (68546438444, '1m', '8s'),
        (979779441123, '16m', '19s'),
        (7977941341123, '2h, 12m', '57s'),
        (97977941341123, '1d, 3h, 12m', '57s'),
    )

    for n, pre, after in data:
        n /= 1000000000
        res = ftime(n, 'macro')
        assert res.startswith(pre), "Expected: %s | Got: %s" % (pre + ' ' + after, res)
        assert res.endswith(after), "Expected: %s | Got: %s" % (pre + ' ' + after, res)


def test_ftime_seconds():
    data = (
        (68546438444, '1m', '8s'),
        (979779441123, '16m', '19s'),
        (7977941341123, '2h, 12m', '57s'),
        (97977941341123, '1d, 3h, 12m', '57s'),
    )

    for n, pre, after in data:
        n /= 1000000000
        res = ftime_seconds(n)
        assert res.startswith(pre), "Expected: %s | Got: %s" % (pre + ' ' + after, res)
        assert res.endswith(after), "Expected: %s | Got: %s" % (pre + ' ' + after, res)


def test_flatten():
    data = [1, [2, [3, [[[4,5,6,7,8,9]]]]]]
    assert flatten(data) == list(range(1,10))


def test_smiter():
    data = range(500)
    for i in smiter(data):
        if i.value == 0:
            assert i.first is True and i.last is False
        elif i.value == 499:
            assert i.last is True and i.first is False
        else:
            assert i.first is not True and i.last is not True

    data = [13]
    for i in smiter(data):
        assert i.last is True and i.first is True and i.value == 13


def test_splitint():
    for i in range(1,307):
        n = 10 ** i
        nums = list(map(int,str(n)))
        assert splitint(n) == nums