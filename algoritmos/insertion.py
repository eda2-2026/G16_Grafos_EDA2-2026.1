def insertionSort(v: list[int]) -> int:
    aux = 0
    for i in range(1, len(v)):
        j = i
        while v[j-1] > v[j] and j != 0:
            aux = v[j-1]
            v[j-1] = v[j]
            v[j] = aux
            j = j - 1
    
    return v
