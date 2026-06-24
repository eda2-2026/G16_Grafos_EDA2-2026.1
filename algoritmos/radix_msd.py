def radixMSD(v: list[int]) -> list[int]:
    if not v:
        return v

    max_val = max(v)
    digits = len(str(max_val))
    exp = 10 ** (digits - 1)

    result = _msd_sort(v, exp)
    for i in range(len(v)):
        v[i] = result[i]

    return v


def _msd_sort(v: list[int], exp: int) -> list[int]:
    if len(v) <= 1 or exp == 0:
        return v

    buckets: list[list[int]] = [[] for _ in range(10)]
    for x in v:
        digit = (x // exp) % 10
        buckets[digit].append(x)

    result = []
    for bucket in buckets:
        result.extend(_msd_sort(bucket, exp // 10))

    return result
