from algoritmos.insertion import insertionSort
from algoritmos.selection import selectionSort
from algoritmos.counting import countingSort
from algoritmos.quick import quickSort
from algoritmos.radix_lsd import radixLSD
from algoritmos.radix_msd import radixMSD

ALGORITMOS = {
    "insertion": insertionSort,
    "selection": selectionSort,
    "counting":  countingSort,
    "quick":     quickSort,
    "radix_lsd": radixLSD,
    "radix_msd": radixMSD,
}
