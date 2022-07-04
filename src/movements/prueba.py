def plus_month(year_month: int, plus: int = 1) -> int:
    year: int = int(str(year_month)[:4])
    month: int = int(str(year_month)[4:])
    month += plus
    if month > 12:
        year += 1
        month = month - 12
    return year * 100 + int(str(month).zfill(2))


def matches_frequency(start: int, current: int, instalments: int) -> bool:
    if current % instalments == 0:
        return True

    return True


def years_between(_from: int, _to: int) -> int:
    if _from > _to:
        _from, _to = _to, _from
    return (_to - _from) // 100


def years_to_cycle(start: int, instalments: int, every: int) -> int:
    current = start
    i = 0
    # and current % every == 0:
    while i < instalments:
        print('current:', current, '- count:', i,
              '- start month:', str(start)[4:],
              '- current month:', str(current)[4:])
        current = plus_month(current, every)
        i += 1
        if str(start)[4:] == str(current)[4:]:
            break
    return years_between(start, current)


def main():
    print('first cycle: %s' % years_to_cycle(202201, 3, 5))
    # print('first cycle: %s' % years_to_cycle(202201, 50, 7))
    # print('first cycle: %s' % years_to_cycle(202201, 50, 8))
    # print('first cycle: %s' % years_to_cycle(202201, 50, 9))
    # print('first cycle: %s' % years_to_cycle(202201, 50, 10))
    # print('first cycle: %s' % years_to_cycle(202201, 50, 11))


if __name__ == '__main__':
    main()
    print('Done')
    exit(0)
