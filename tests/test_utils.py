from hackytools.utils import ftime_ns

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
        (68546438444, '1m', '8s'),
        (979779441123, '16m', '19s'),
        (7977941341123, '2h, 12m', '57s'),
        (97977941341123, '1d, 3h, 12m', '57s'),
    )

    for n, pre, after in data:
        res = ftime_ns(n)
        print(res)
        print(pre)
        print(after)
        assert res.startswith(pre)
        assert res.endswith(after)
