def radixLSD(v: list[int]) -> list[int]:
    if not v:
        return v

    max_val = max(v)
    exp = 1
    while max_val // exp > 0:
        _counting_by_digit(v, exp)
        exp *= 10

    return v


def _counting_by_digit(v: list[int], exp: int) -> None:
    n = len(v)
    output = [0] * n
    count = [0] * 10

    for x in v:
        digit = (x // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (v[i] // exp) % 10
        output[count[digit] - 1] = v[i]
        count[digit] -= 1

    for i in range(n):
        v[i] = output[i]
