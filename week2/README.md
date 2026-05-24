## Overview
Implemented a hash table from scratch where each key gets a hash code and based on that hash code the (key, value) item is stored in a list. Each element of the list either containes None or Item object where Item object is consists of (key, value, next). Next is pointing to the next Item object if applicable, else None.

## Design decision
- Used a prime number multiplier when compute a hash code in order to reduce collision
- Rehash the entire bucket when the number of objects in the list if either less than 30% of the bucket size or more than 70% of the bucket size
