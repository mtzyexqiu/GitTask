from flask import Flask, render_template, request, redirect, url_for
from core.scheduler import TaskScheduler

app = Flask(__name__)
scheduler = TaskScheduler()


@app.route("/")
def index():
    urgent = scheduler.tugas_paling_urgent()
    konflik = scheduler.deteksi_konflik_jadwal(toleransi_menit=60)
    terlambat = scheduler.filter_tugas("terlambat")
    selesai = scheduler.filter_tugas("selesai")

    return render_template(
        "index.html",
        jumlah_tugas=scheduler.jumlah_tugas(),
        urgent=urgent,
        jumlah_konflik=len(konflik),
        jumlah_terlambat=len(terlambat),
        jumlah_selesai=len(selesai),
    )


@app.route("/tambah", methods=["GET", "POST"])
def tambah_tugas():
    if request.method == "POST":
        nama = request.form["nama"]
        deadline = request.form["deadline"]
        priority = int(request.form["priority"])
        kategori = request.form["kategori"]

        scheduler.tambah_tugas(nama, deadline, priority, kategori)
        return redirect(url_for("index"))

    return render_template("tambah_tugas.html")


@app.route("/urgent")
def tugas_urgent():
    task = scheduler.tugas_paling_urgent()
    return render_template("detail_tugas.html", task=task, judul="Tugas Paling Urgent")


@app.route("/semua/<urut>")
def semua_tugas(urut):
    if urut == "priority":
        tugas_list = scheduler.semua_tugas_by_priority()
        judul = "Semua Tugas - Urut Prioritas (Max-Heap)"
    else:
        tugas_list = scheduler.semua_tugas_by_timeline()
        judul = "Semua Tugas - Urut Timeline (DLL)"

    return render_template("semua_tugas.html", tugas_list=tugas_list, judul=judul)


@app.route("/cari", methods=["GET", "POST"])
def cari_tugas():
    task = None
    sudah_cari = False

    if request.method == "POST":
        sudah_cari = True
        task_id = int(request.form["task_id"])
        task = scheduler.cari_tugas(task_id)

    return render_template("cari_tugas.html", task=task, sudah_cari=sudah_cari)


@app.route("/konflik", methods=["GET", "POST"])
def konflik_jadwal():
    konflik_list = []
    sudah_cek = False

    if request.method == "POST":
        sudah_cek = True
        toleransi = int(request.form.get("toleransi", 60))
        konflik_list = scheduler.deteksi_konflik_jadwal(toleransi_menit=toleransi)

    return render_template("konflik_jadwal.html", konflik_list=konflik_list, sudah_cek=sudah_cek)


@app.route("/filter", methods=["GET", "POST"])
def filter_tugas():
    hasil = []
    mode = None

    if request.method == "POST":
        mode = request.form["mode"]
        hasil = scheduler.filter_tugas(mode)

    return render_template("filter_tugas.html", hasil=hasil, mode=mode)


@app.route("/selesai/<int:task_id>")
def tandai_selesai(task_id):
    scheduler.tandai_selesai(task_id)
    return redirect(url_for("semua_tugas", urut="timeline"))


@app.route("/hapus/<int:task_id>")
def hapus_tugas(task_id):
    scheduler.hapus_tugas(task_id)
    return redirect(url_for("semua_tugas", urut="timeline"))


if __name__ == "__main__":
    app.run(debug=True)