import itertools

class Task:
    """
    Representasi satu tugas dalam sistem penjadwalan.
    """
    _id_counter = itertools.count(1)  # auto-increment ID, mulai dari 1

    def __init__(self, nama, deadline, priority, kategori="Umum"):
        """
        nama      : str   -> nama tugas, misal "Tugas Struktur Data"
        deadline  : str   -> format "YYYY-MM-DD HH:MM", misal "2026-07-01 23:59"
        priority  : int   -> 1 (tinggi) - 5 (rendah), kita anggap angka kecil = lebih prioritas
        kategori  : str   -> misal "Kuliah", "Kerja", "Pribadi"
        """
        self.id = next(Task._id_counter)
        self.nama = nama
        self.deadline = deadline
        self.priority = priority
        self.kategori = kategori
        self.status = "Belum Selesai"  # bisa: "Belum Selesai", "Selesai", "Terlambat"

    def tandai_selesai(self):
        self.status = "Selesai"

    def __repr__(self):
        return (f"Task(id={self.id}, nama='{self.nama}', "
                f"deadline='{self.deadline}', priority={self.priority}, "
                f"status='{self.status}')")