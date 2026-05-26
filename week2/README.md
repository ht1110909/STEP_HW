## Overview
Implemented a hash table from scratch where each key gets a hash code and based on that hash code the (key, value) item is stored in a list. Each element of the list either containes None or Item object where Item object is consists of (key, value, next). Next is pointing to the next Item object if applicable, else None.

Insertion is done by almost O(1) as it gets the hash code and insert the Item object in the list.
Deletion is done by almost O(1) as it finds the hash code of the key and delete the corresponding Item object by skipping that object
Get is done by almost O(1) as it finds the hash code of the key and return the corresponding Itme object

Note that when rehash, it takes O(N) since all the elements in the list needs to be inserted again

## Design decision
- Used a prime number multiplier when compute a hash code in order to reduce collision
- Rehash the entire bucket when the number of objects in the list if either less than 30% of the bucket size or more than 70% of the bucket size

## Homework 2
**The complexity of searching / adding / removing an element is mostly O(1) with a hash table, whereas the complexity is O(log N) with a tree. This means that a hash table is more efficient than a tree. However, real-world large-scale database systems tend to prefer a tree to a hash table. Why? List as many reasons as possible.**

One reason can be that when rehashing, it takes O(N) which takes way longer than O(log N). When there are a lot of data, it is more likely to rehash multiple times. It is better to take O(log N) all the time than having to rehash that takes O(N) multiple times.
Another reason can be a hash table takes more memory space than a tree. While a tree always has a size that corresponds to the amount of element in the tree, a hash table size can be larger than it needs to be, taking more space than neccesary.

## Homework 3
**Design a cache that achieves the following operations with mostly O(1)**
- When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
- If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair

The algorithm can have both a hash table and a list that works as a queue structure (FIFO). The queue has a size of number of pairs we want to hold in a cashe. When a pair is added, it checks if it is already in the cashe using a hash table (O(1)). If not, it gets the first element of the queue and delete that element from both the queue and the hash table (both O(1)). Then, add the new pair in the hash table and the queue (O(1)). 
