from core.scheduler import TaskScheduler

scheduler = TaskScheduler()


def tampilkan_menu():
    print("\n" + "=" * 50)
    print("   SISTEM PENJADWALAN TUGAS - KELOMPOK 12")
    print("=" * 50)
    print("1. Tambah Tugas")
    print("2. Lihat Tugas Paling Urgent")
    print("3. Lihat Semua Tugas (urut Prioritas)")
    print("4. Lihat Semua Tugas (urut Timeline/Deadline)")
    print("5. Cari Tugas (by ID)")
    print("6. Tandai Tugas Selesai")
    print("7. Hapus Tugas")
    print("8. Deteksi Konflik Jadwal")
    print("9. Filter Tugas")
    print("0. Keluar")
    print("=" * 50)


def input_tugas_baru():
    print("\n--- Tambah Tugas Baru ---")
    nama = input("Nama tugas: ")
    deadline = input("Deadline (format: YYYY-MM-DD HH:MM, contoh 2026-07-01 23:59): ")
    priority = int(input("Priority (1=tertinggi, 5=terendah): "))
    kategori = input("Kategori (Kuliah/Kerja/Pribadi): ")

    task = scheduler.tambah_tugas(nama, deadline, priority, kategori)
    print(f"\n✅ Tugas berhasil ditambahkan dengan ID: {task.id}")


def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-9): ").strip()

        if pilihan == "1":
            input_tugas_baru()

        elif pilihan == "2":
            task = scheduler.tugas_paling_urgent()
            print("\n--- Tugas Paling Urgent ---")
            print(task if task else "Tidak ada tugas.")

        elif pilihan == "3":
            print("\n--- Semua Tugas (urut Prioritas) ---")
            tugas_list = scheduler.semua_tugas_by_priority()
            if not tugas_list:
                print("Belum ada tugas.")
            for t in tugas_list:
                print(t)

        elif pilihan == "4":
            print("\n--- Semua Tugas (urut Timeline) ---")
            tugas_list = scheduler.semua_tugas_by_timeline()
            if not tugas_list:
                print("Belum ada tugas.")
            for t in tugas_list:
                print(t)

        elif pilihan == "5":
            task_id = int(input("Masukkan ID tugas: "))
            task = scheduler.cari_tugas(task_id)
            print("\n--- Hasil Pencarian ---")
            print(task if task else "Tugas tidak ditemukan.")

        elif pilihan == "6":
            task_id = int(input("Masukkan ID tugas yang sudah selesai: "))
            berhasil = scheduler.tandai_selesai(task_id)
            print("✅ Berhasil ditandai selesai." if berhasil else "❌ Tugas tidak ditemukan.")

        elif pilihan == "7":
            task_id = int(input("Masukkan ID tugas yang ingin dihapus: "))
            berhasil = scheduler.hapus_tugas(task_id)
            print("✅ Tugas berhasil dihapus." if berhasil else "❌ Tugas tidak ditemukan.")

        elif pilihan == "8":
            print("\n--- Deteksi Konflik Jadwal ---")
            toleransi = int(input("Toleransi konflik (menit, default 60): ") or "60")
            konflik_list = scheduler.deteksi_konflik_jadwal(toleransi_menit=toleransi)
            if konflik_list:
                for t1, t2, selisih in konflik_list:
                    print(f"⚠️  KONFLIK: '{t1.nama}' <-> '{t2.nama}' | selisih {selisih:.0f} menit")
            else:
                print("✅ Tidak ada konflik jadwal.")

        elif pilihan == "9":
            print("\nMode filter: hari_ini / minggu_ini / selesai / terlambat")
            mode = input("Pilih mode filter: ").strip()
            hasil = scheduler.filter_tugas(mode)
            print(f"\n--- Hasil Filter: {mode} ---")
            if not hasil:
                print("Tidak ada tugas yang cocok.")
            for t in hasil:
                print(t)

        elif pilihan == "0":
            print("\nTerima kasih! Sampai jumpa 👋")
            break

        else:
            print("\n❌ Pilihan tidak valid, coba lagi.")

        input("\nTekan Enter untuk lanjut...")


if __name__ == "__main__":
    main()