import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch!                                    #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# 'key': string
# Return value: a hash value
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Make it better!
    hash = 0
    #use the implementation of java hashCode() idea
    #multiply with prime number to make it more spread out
    #now position of character mutters!
    for i in key:
        hash = hash*31 + ord(i)
    return hash


# An item object that represents one key - value pair in the hash table.
class Item:
    # 'key': The key of the item. The key must be a string.
    # 'value': The value of the item.
    # 'next': The next item in the linked list. If this is the last item in the
    #         linked list, 'next' is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return (f"({self.key}, {self.value}, {self.next})")


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# 'self.bucket_size': The bucket size.
# 'self.buckets': An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is 'hash'.
# 'self.item_count': The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # 'key': The key of the item.
    # 'value': The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value, isRehasing = False):
        assert type(key) == str

        #if rehashing, skip checking size to prevent error
        if not isRehasing:
            check_size(self.size(), self.bucket_size)  # Don't remove this code.

        #if count is more than 70% of the bucket size, rehash
        if self.item_count > self.bucket_size*0.7:
            self.rehash(self.bucket_size*2+1)

        #calculate hash
        hash_num = calculate_hash(key)%self.bucket_size

        #when collision
        if self.buckets[hash_num] is not None:
            cur_val = self.buckets[hash_num]
            while cur_val:
                #If the key already exists
                if cur_val.key == key:
                    cur_val.value = value
                    return False
                cur_val = cur_val.next
            #if key doesn't exist already put it in the front
            self.buckets[hash_num] = Item(key, value, self.buckets[hash_num])

        #if no collision
        else:
            self.buckets[hash_num] = Item(key, value, None)

        self.item_count+=1

        return True

    def rehash(self, new_size):
        """
        rehash the self.buckets and change the
        bucket size to the given value
        """
        #add one to make it odd number
        old_bucket = self.buckets
        self.buckets = [None]*new_size
        self.bucket_size = new_size
        self.item_count = 0
        for item_list in old_bucket:
            while item_list:
                self.put(item_list.key, item_list.value, isRehasing=True)
                item_list = item_list.next

    # Get an item from the hash table.
    #
    # 'key': The key.
    # Return value: If the item is found, return (the value of the item, True).
    #               Otherwise, return (None, False).
    def get(self, key):
        assert type(key) == str
        check_size(self.size(), self.bucket_size)  # Don't remove this code.
        hash_code = calculate_hash(key)%self.bucket_size
        cur_val = self.buckets[hash_code]
        while cur_val:
            if cur_val.key == key:
                return (cur_val.value, True)
            cur_val = cur_val.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # 'key': The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str

        hash_code = calculate_hash(key)%self.bucket_size
        cur_val = self.buckets[hash_code]

        result = False

        #if nothing exists in the index
        if cur_val is None:
            return False

        #when that is the only Item class exists in the index
        if cur_val.next is None:
            if cur_val.key == key:
                self.buckets[hash_code] = None
                self.item_count-=1
                result =  True

        #if the first value is what we are looking for
        elif cur_val and cur_val.key == key:
            #set the next to None so that it gets garbege collected
            self.buckets[hash_code] = cur_val.next
            self.item_count-=1
            result = True
        else:
            while cur_val.next:
                #if the key of the next value is what we want to delete
                if cur_val.next.key == key:
                    #set the pointer to the one after
                    cur_val.next = cur_val.next.next
                    self.item_count-=1
                    result = True
                    break
                cur_val = cur_val.next

        if self.item_count < self.bucket_size * 0.3:
            self.rehash(self.bucket_size // 2 + 1)
        return result

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count



# Check that the hash table has a "reasonable" bucket size.
# The bucket size is judged "reasonable" if it is smaller than 100 or
# the buckets are 30% or more used.
#
# Note: Don't change this function.
def check_size(item_count, bucket_size):
    assert (bucket_size < 100 or item_count >= bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4
    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0

    # Test the rehashing.
    for i in range(100):
        hash_table.put(str(i), str(i))
    for i in range(100):
        assert hash_table.get(str(i)) == (str(i), True)
    for i in range(100):
        assert hash_table.delete(str(i)) == True
    hash_table.put("abc", 1)
    hash_table.put("acb", 2)
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
