def countingSort(v: list[int]) -> list[int]:
    if not v:
        return v

    min_val = min(v)
    max_val = max(v)
    offset = min_val
    k = max_val - min_val + 1

    count = [0] * k
    for x in v:
        count[x - offset] += 1

    idx = 0
    for i, c in enumerate(count):
        for _ in range(c):
            v[idx] = i + offset
            idx += 1

    return v
