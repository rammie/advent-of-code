import copy

dense_map = open("input9.txt").read()
# dense_map = open("input9-ex.txt").read()


class FreeSpace:
    def __init__(self):
        self._free_space = {}
        self._free_space_heap = []

    def reserve(self, index, size):
        self._free_space[index] = size
        self._free_space_heap.append((index, size))
        self._free_space_heap.sort()

    def _find(self, size):
        for heap_index, (_, free_size) in enumerate(self._free_space_heap):
            if free_size >= size:
                return heap_index
        return None

    def claim(self, size):
        heap_index = self._find(size)
        if heap_index is None:
            return False

        index, free_size = self._free_space_heap[heap_index]
        del self._free_space_heap[heap_index]
        del self._free_space[index]
        remaining = free_size - size
        if remaining:
            self.reserve(index + size, remaining)

        self._free_space_heap.sort()
        return index


def create_disk_map(dense_map):
    free_space = FreeSpace()
    files = []

    file_id = 0
    disk_map = []
    for c, char in enumerate(dense_map):
        count = int(char)
        disk_index = len(disk_map)
        if c % 2 == 0:
            disk_map.extend([file_id] * count)
            files.append((disk_index, count, file_id))
            file_id += 1
        else:
            disk_map.extend(["."] * count)
            free_space.reserve(disk_index, count)

    files.sort(reverse=True)
    return disk_map, free_space, files


def pack_disk(disk_map):
    c = 0
    disk_len = len(disk_map)
    for b in range(disk_len - 1, -1, -1):
        while disk_map[c] != ".":
            c += 1
            if c >= b or c == len(disk_map):
                return disk_map
        disk_map[b], disk_map[c] = disk_map[c], disk_map[b]
    return disk_map


def pack_disk2(disk_map, free_space, files):
    for file_index, (file_start, file_size, file_id) in enumerate(files):
        free_index = free_space.claim(file_size)
        if free_index is False or free_index > file_start:
            continue

        for i in range(file_size):
            disk_map[free_index:free_index + file_size] = [file_id] * file_size
            disk_map[file_start:file_start + file_size] = ["."] * file_size

        files[file_index] = (free_index, file_size, file_id)

    files.sort(reverse=True)
    return disk_map


def checksum(disk_map):
    result = 0
    for c, char in enumerate(disk_map):
        if char == ".":
            continue
        result += c * int(char)
    return result


def print_disk(disk_map):
    for char in disk_map:
        print(char, end="")
    print()


disk_map, free_space, files = create_disk_map(dense_map)
# Part 1
# packed = pack_disk(disk_map)

# Part 2
while True:
    disk_copy = disk_map.copy()
    print_disk(disk_copy)
    packed = pack_disk2(disk_map, free_space, files)
    if disk_copy == packed:
        break

print_disk(packed)
print(files)
print(free_space._free_space_heap)
print(checksum(packed))