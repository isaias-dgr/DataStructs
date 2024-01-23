from random import randint
from typing import List

def binary_search(target: int, set_data:  List[int] ) -> bool:
    low = 0
    middle = 0
    higth = len(set_data)-1
  
    while set_data[low] <= target <= set_data[higth] :
        middle = low + int((higth - low) / 2)
        if set_data[middle] == target:
            return True, (target, middle)
        if target > set_data[middle]:
            low = middle + 1
        if target < set_data[middle]:
            higth = middle - 1       
    return False, (None, None)


if __name__=='__main__':
    set_test = list(range(0,10))
    target_value = randint(1,200)
    # target_value = 7

    print(f"target: {target_value} set_test: {set_test}")
    print(binary_search(target_value, set_test))