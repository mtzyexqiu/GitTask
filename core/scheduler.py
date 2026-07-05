from datetime import datetime
from models.task import Task
from data_structures.max_heap import MaxHeap
from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.hash_table import HashTable


class TaskScheduler:
    """
    Class utama yang menggabungkan Max-Heap, Doubly Linked List,
    dan Hash Table menjadi satu sistem penjadwalan tugas yang utuh.
    """

    def __init__(self):
        self.heap = MaxHeap()              # untuk urutan prioritas
        self.timeline = DoublyLinkedList()  # untuk urutan kronologis (deadline)
        self.lookup = HashTable()           # untuk pencarian cepat by ID

    def tambah_tugas(self, nama, deadline, priority, kategori="Umum"):
        """
        Tambah tugas baru ke SEMUA struktur data sekaligus.
        """
        task = Task(nama, deadline, priority, kategori)

        self.heap.insert(task)
        self.timeline.insert_sorted_by_deadline(task)
        self.lookup.insert(task.id, task)

        return task

    def cari_tugas(self, task_id):
        """Cari tugas berdasarkan ID. O(1) pakai Hash Table."""
        return self.lookup.get(task_id)

    def hapus_tugas(self, task_id):
        """
        Hapus tugas dari SEMUA struktur data sekaligus.
        """
        task = self.lookup.get(task_id)
        if task is None:
            return False

        self.lookup.remove(task_id)
        self.timeline.remove_by_id(task_id)
        self.heap.remove_task_by_id(task_id)
        return True

    def tandai_selesai(self, task_id):
        """Tandai tugas sebagai selesai."""
        task = self.lookup.get(task_id)
        if task is None:
            return False
        task.tandai_selesai()
        return True

    def tugas_paling_urgent(self):
        """Lihat tugas paling urgent saat ini (dari Max-Heap)."""
        return self.heap.peek_top()

    def semua_tugas_by_priority(self):
        """Semua tugas urut berdasarkan prioritas (dari Max-Heap)."""
        return self.heap.get_all_sorted()

    def semua_tugas_by_timeline(self):
        """Semua tugas urut berdasarkan deadline/kronologis (dari DLL)."""
        return self.timeline.traverse_forward()

    def deteksi_konflik_jadwal(self, toleransi_menit=60):
        """
        Deteksi tugas-tugas yang deadline-nya berdekatan (dalam rentang
        toleransi_menit), karena berpotensi tidak bisa dikerjakan keduanya
        tepat waktu. Memanfaatkan DLL yang sudah terurut -> O(n).
        """
        konflik = []
        tugas_terurut = self.timeline.traverse_forward()

        for i in range(len(tugas_terurut) - 1):
            t1 = tugas_terurut[i]
            t2 = tugas_terurut[i + 1]

            d1 = datetime.strptime(t1.deadline, "%Y-%m-%d %H:%M")
            d2 = datetime.strptime(t2.deadline, "%Y-%m-%d %H:%M")

            selisih_menit = (d2 - d1).total_seconds() / 60

            if selisih_menit <= toleransi_menit:
                konflik.append((t1, t2, selisih_menit))

        return konflik

    def filter_tugas(self, mode):
        """
        Filter tugas berdasarkan mode: 'hari_ini', 'minggu_ini',
        'selesai', 'terlambat'.
        """
        semua_tugas = self.timeline.traverse_forward()
        sekarang = datetime.now()
        hasil = []

        for task in semua_tugas:
            deadline_dt = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M")

            if mode == "selesai":
                if task.status == "Selesai":
                    hasil.append(task)

            elif mode == "terlambat":
                if task.status != "Selesai" and deadline_dt < sekarang:
                    hasil.append(task)

            elif mode == "hari_ini":
                if deadline_dt.date() == sekarang.date():
                    hasil.append(task)

            elif mode == "minggu_ini":
                selisih_hari = (deadline_dt.date() - sekarang.date()).days
                if 0 <= selisih_hari <= 7:
                    hasil.append(task)

        return hasil

    def jumlah_tugas(self):
        return len(self.lookup)