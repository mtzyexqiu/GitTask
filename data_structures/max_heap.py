class MaxHeap:
    """
    Implementasi Max-Heap manual (array-based) untuk menyimpan Task.
    "Max" di sini berarti: priority lebih KECIL = lebih diprioritaskan
    (priority 1 dianggap 'terbesar' nilainya karena paling urgent).
    """

    def __init__(self):
        self.heap = []  # list of Task objects

    def _is_more_urgent(self, task_a, task_b):
        """
        Bandingkan urgensi 2 task.
        Aturan: priority lebih kecil = lebih urgent.
        Kalau priority sama, deadline lebih awal = lebih urgent.
        """
        if task_a.priority != task_b.priority:
            return task_a.priority < task_b.priority
        return task_a.deadline < task_b.deadline

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def insert(self, task):
        """Insert task baru ke heap. Kompleksitas: O(log n)"""
        self.heap.append(task)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        while i > 0:
            parent = self._parent(i)
            if self._is_more_urgent(self.heap[i], self.heap[parent]):
                self._swap(i, parent)
                i = parent
            else:
                break

    def extract_top(self):
        """
        Ambil & hapus task paling urgent (di posisi root).
        Kompleksitas: O(log n)
        """
        if not self.heap:
            return None

        top = self.heap[0]
        last = self.heap.pop()  # ambil elemen terakhir

        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)

        return top

    def _heapify_down(self, i):
        n = len(self.heap)
        while True:
            left = self._left(i)
            right = self._right(i)
            most_urgent = i

            if left < n and self._is_more_urgent(self.heap[left], self.heap[most_urgent]):
                most_urgent = left
            if right < n and self._is_more_urgent(self.heap[right], self.heap[most_urgent]):
                most_urgent = right

            if most_urgent != i:
                self._swap(i, most_urgent)
                i = most_urgent
            else:
                break

    def peek_top(self):
        """Lihat task paling urgent TANPA menghapusnya. O(1)"""
        return self.heap[0] if self.heap else None

    def remove_task_by_id(self, task_id):
        """
        Hapus task tertentu dari heap berdasarkan ID (dipakai saat task
        ditandai selesai/dihapus sebelum jadi top). O(n) karena harus cari dulu.
        """
        for i, task in enumerate(self.heap):
            if task.id == task_id:
                last = self.heap.pop()
                if i < len(self.heap):
                    self.heap[i] = last
                    self._heapify_up(i)
                    self._heapify_down(i)
                return True
        return False

    def is_empty(self):
        return len(self.heap) == 0

    def get_all_sorted(self):
        """
        Ambil SEMUA task urut dari paling urgent, TANPA mengubah heap asli.
        Dipakai buat fitur 'tampilkan semua tugas urut prioritas'.
        """
        import copy
        temp_heap = copy.deepcopy(self)
        result = []
        while not temp_heap.is_empty():
            result.append(temp_heap.extract_top())
        return result