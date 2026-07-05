class HashTable:
    """
    Implementasi Hash Table manual menggunakan teknik chaining,
    untuk pencarian Task super cepat berdasarkan ID.
    """

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        """
        Fungsi hash sederhana: ubah key (ID/nama) jadi index bucket.
        Pakai modulo supaya hasilnya selalu dalam rentang index yang valid.
        """
        return hash(key) % self.capacity

    def insert(self, key, task):
        """
        Insert task ke hash table dengan key tertentu (biasanya task.id).
        Kompleksitas rata-rata: O(1)
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        # Kalau key sudah ada, update value-nya (bukan duplikat)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, task)
                return

        bucket.append((key, task))
        self.size += 1

        # Resize kalau bucket udah terlalu padat (load factor > 0.75)
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key):
        """Cari task berdasarkan key. Kompleksitas rata-rata: O(1)"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        """Hapus task berdasarkan key. Kompleksitas rata-rata: O(1)"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self):
        """
        Perbesar kapasitas table kalau sudah terlalu penuh,
        supaya performa O(1) tetap terjaga (menghindari banyak collision).
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, task in bucket:
                self.insert(key, task)

    def get_all(self):
        """Ambil semua task yang tersimpan (untuk fitur tampilkan semua). O(n)"""
        result = []
        for bucket in self.buckets:
            for key, task in bucket:
                result.append(task)
        return result

    def __len__(self):
        return self.size