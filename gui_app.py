import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime
from core.scheduler import TaskScheduler

scheduler = TaskScheduler()


class TaskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Sistem Penjadwalan Tugas - Kelompok 12")
        root.geometry("850x600")
        root.configure(bg="#1e1e2f")

        # ===== SIDEBAR MENU (angka 1-9 & 0, sama seperti CLI) =====
        sidebar = tk.Frame(root, bg="#2b2b3d", width=240)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="MENU UTAMA", bg="#2b2b3d", fg="white",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        menu_items = [
            ("1. Tambah Tugas", self.tambah_tugas),
            ("2. Tugas Paling Urgent", self.tugas_urgent),
            ("3. Urut Prioritas (Heap)", self.lihat_priority),
            ("4. Urut Timeline (DLL)", self.lihat_timeline),
            ("5. Cari Tugas by ID", self.cari_tugas),
            ("6. Tandai Selesai", self.tandai_selesai),
            ("7. Hapus Tugas", self.hapus_tugas),
            ("8. Deteksi Konflik Jadwal", self.deteksi_konflik),
            ("9. Filter Tugas", self.filter_tugas),
            ("0. Keluar", root.quit),
        ]

        for text, cmd in menu_items:
            tk.Button(sidebar, text=text, anchor="w", bg="#3b3b55", fg="white",
                       activebackground="#52527a", relief="flat",
                       font=("Segoe UI", 10), command=cmd, padx=10, pady=8
                       ).pack(fill="x", padx=10, pady=3)

        # ===== AREA OUTPUT =====
        main_frame = tk.Frame(root, bg="#1e1e2f")
        main_frame.pack(side="right", fill="both", expand=True)

        tk.Label(main_frame, text="Hasil / Output", bg="#1e1e2f", fg="white",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 5))

        self.output = scrolledtext.ScrolledText(main_frame, bg="#12121c", fg="#00ff88",
                                                  font=("Consolas", 10), wrap="word")
        self.output.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tampilkan_output("Selamat datang di Sistem Penjadwalan Tugas!\n"
                               "Pilih menu di sebelah kiri untuk mulai (1-9), atau 0 untuk keluar.")

    def tampilkan_output(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    # ---------- 1. Tambah Tugas ----------
    def tambah_tugas(self):
        nama = simpledialog.askstring("Tambah Tugas", "Nama tugas:")
        if not nama:
            return
        deadline = simpledialog.askstring("Tambah Tugas", "Deadline (YYYY-MM-DD HH:MM):")
        if not deadline:
            return
        try:
            datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Format deadline salah!\nGunakan: YYYY-MM-DD HH:MM")
            return
        priority = simpledialog.askinteger("Tambah Tugas", "Priority (1=tertinggi, 5=terendah):",
                                             minvalue=1, maxvalue=5)
        if priority is None:
            return
        kategori = simpledialog.askstring("Tambah Tugas", "Kategori (Kuliah/Kerja/Pribadi):") or "Umum"

        task = scheduler.tambah_tugas(nama, deadline, priority, kategori)
        self.tampilkan_output(f"✅ Tugas berhasil ditambahkan!\n\n{task}")

    # ---------- 2. Tugas Paling Urgent ----------
    def tugas_urgent(self):
        task = scheduler.tugas_paling_urgent()
        self.tampilkan_output(str(task) if task else "Belum ada tugas.")

    # ---------- 3. Urut Prioritas ----------
    def lihat_priority(self):
        tugas_list = scheduler.semua_tugas_by_priority()
        if not tugas_list:
            self.tampilkan_output("Belum ada tugas.")
            return
        text = "=== Tugas urut Prioritas (Max-Heap) ===\n\n"
        for t in tugas_list:
            text += f"{t}\n"
        self.tampilkan_output(text)

    # ---------- 4. Urut Timeline ----------
    def lihat_timeline(self):
        tugas_list = scheduler.semua_tugas_by_timeline()
        if not tugas_list:
            self.tampilkan_output("Belum ada tugas.")
            return
        text = "=== Tugas urut Timeline (DLL) ===\n\n"
        for t in tugas_list:
            text += f"{t}\n"
        self.tampilkan_output(text)

    # ---------- 5. Cari Tugas ----------
    def cari_tugas(self):
        task_id = simpledialog.askinteger("Cari Tugas", "Masukkan ID tugas:")
        if task_id is None:
            return
        task = scheduler.cari_tugas(task_id)
        self.tampilkan_output(str(task) if task else "Tugas tidak ditemukan.")

    # ---------- 6. Tandai Selesai ----------
    def tandai_selesai(self):
        task_id = simpledialog.askinteger("Tandai Selesai", "Masukkan ID tugas:")
        if task_id is None:
            return
        berhasil = scheduler.tandai_selesai(task_id)
        self.tampilkan_output("✅ Tugas ditandai selesai." if berhasil else "❌ Tugas tidak ditemukan.")

    # ---------- 7. Hapus Tugas ----------
    def hapus_tugas(self):
        task_id = simpledialog.askinteger("Hapus Tugas", "Masukkan ID tugas:")
        if task_id is None:
            return
        berhasil = scheduler.hapus_tugas(task_id)
        self.tampilkan_output("✅ Tugas berhasil dihapus." if berhasil else "❌ Tugas tidak ditemukan.")

    # ---------- 8. Deteksi Konflik ----------
    def deteksi_konflik(self):
        toleransi = simpledialog.askinteger("Deteksi Konflik", "Toleransi (menit):", initialvalue=60) or 60
        konflik_list = scheduler.deteksi_konflik_jadwal(toleransi_menit=toleransi)
        if not konflik_list:
            self.tampilkan_output("✅ Tidak ada konflik jadwal.")
            return
        text = "=== Konflik Jadwal Ditemukan ===\n\n"
        for t1, t2, selisih in konflik_list:
            text += f"⚠️  '{t1.nama}' <-> '{t2.nama}' | selisih {selisih:.0f} menit\n"
        self.tampilkan_output(text)

    # ---------- 9. Filter Tugas ----------
    def filter_tugas(self):
        mode = simpledialog.askstring(
            "Filter Tugas",
            "Mode filter:\nhari_ini / minggu_ini / selesai / terlambat"
        )
        if not mode:
            return
        hasil = scheduler.filter_tugas(mode.strip())
        if not hasil:
            self.tampilkan_output(f"Tidak ada tugas untuk filter '{mode}'.")
            return
        text = f"=== Hasil Filter: {mode} ===\n\n"
        for t in hasil:
            text += f"{t}\n"
        self.tampilkan_output(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerGUI(root)
    root.mainloop()