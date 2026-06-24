def quickSort(v: list[int]) -> list[int]:
    _quick(v, 0, len(v) - 1)
    return v


def _quick(v: list[int], low: int, high: int) -> None:
    if low < high:
        pivot_idx = _partition(v, low, high)
        _quick(v, low, pivot_idx - 1)
        _quick(v, pivot_idx + 1, high)


def _partition(v: list[int], low: int, high: int) -> int:
    pivot = v[high]
    i = low - 1
    for j in range(low, high):
        if v[j] <= pivot:
            i += 1
            v[i], v[j] = v[j], v[i]
    v[i + 1], v[high] = v[high], v[i + 1]
    return i + 1
