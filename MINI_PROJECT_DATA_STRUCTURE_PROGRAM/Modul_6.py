import streamlit as st
from collections import deque
import time
import random
from html import escape

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Modul 6 - Sistem Queue",
    layout="wide"
)

# =====================================================
# CSS - POPPINS, TANPA EMOJI, DARK FRIENDLY
# =====================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], [class*="st-"], div, p, span, label, input, textarea, select, button {
        font-family: 'Poppins', sans-serif !important;
    }

    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        color: #f8fafc;
        padding: 20px 0 10px 0;
        letter-spacing: 0.2px;
    }

    .main-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 18px;
    }

    .section-note {
        color: #cbd5e1;
        font-size: 0.95rem;
        margin-bottom: 18px;
    }

    .queue-card,
    .served-card,
    .next-card,
    .empty-card,
    .metric-card {
        border-radius: 14px;
        padding: 14px 16px;
        margin: 8px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        overflow-wrap: anywhere;
        word-break: break-word;
        line-height: 1.55;
    }

    .queue-card {
        background: #e0f2fe;
        color: #0f172a !important;
        border-left: 6px solid #0284c7;
    }

    .next-card {
        background: #ede9fe;
        color: #0f172a !important;
        border-left: 6px solid #7c3aed;
    }

    .served-card {
        background: #dcfce7;
        color: #0f172a !important;
        border-left: 6px solid #16a34a;
    }

    .empty-card {
        background: #1e293b;
        color: #e2e8f0 !important;
        border: 1px solid #334155;
    }

    .metric-card {
        background: linear-gradient(135deg, #e0f2fe, #f0fdf4);
        color: #0f172a !important;
        border: 1px solid #bae6fd;
        text-align: center;
    }

    .metric-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a !important;
        margin-top: 4px;
    }

    .small-text {
        font-size: 0.84rem;
        color: #334155 !important;
    }

    .tag-next {
        display: inline-block;
        background: #7c3aed;
        color: #ffffff !important;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-left: 8px;
        letter-spacing: 0.2px;
    }

    .tag-normal {
        display: inline-block;
        background: #0284c7;
        color: #ffffff !important;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-left: 8px;
        letter-spacing: 0.2px;
    }

    .divider-soft {
        height: 1px;
        background: #334155;
        margin: 22px 0;
    }

    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 42px;
    }

    div[data-baseweb="select"] > div,
    textarea,
    input {
        border-radius: 10px !important;
    }

    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 14px 0;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER
# =====================================================

def init_state(key, default_factory):
    if key not in st.session_state:
        st.session_state[key] = default_factory()


def safe(value):
    return escape(str(value))


def rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")


def queue_item(title, details="", is_next=False, tag=""):
    cls = "next-card" if is_next else "queue-card"
    badge = "<span class='tag-next'>BERIKUTNYA</span>" if is_next else ""
    extra_tag = f"<span class='tag-normal'>{safe(tag)}</span>" if tag else ""

    st.markdown(
        f"""
        <div class="{cls}">
            <b>{safe(title)}</b>{badge}{extra_tag}<br>
            <span class="small-text">{details}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def served_item(title, details=""):
    st.markdown(
        f"""
        <div class="served-card">
            <b>{safe(title)}</b><br>
            <span class="small-text">{details}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def empty_message(text):
    st.markdown(
        f'<div class="empty-card">{safe(text)}</div>',
        unsafe_allow_html=True
    )


def metric_card(label, number):
    st.markdown(
        f"""
        <div class="metric-card">
            <div>{safe(label)}</div>
            <div class="metric-number">{safe(number)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# SESSION STATE
# =====================================================

# Kasus 1 - Bank
init_state("bank_queue", deque)
init_state("bank_served", list)
init_state("bank_counter", lambda: 1)

# Kasus 2 - Mahasiswa
init_state("mhs_queue", deque)
init_state("mhs_served", list)
init_state("mhs_counter", lambda: 1)

# Kasus 3 - Printer
init_state("printer_queue", deque)
init_state("printer_done", list)
init_state("printer_counter", lambda: 1)

# Kasus 4 - Call Center
init_state("cc_queue", deque)
init_state("cc_served", list)
init_state("cc_counter", lambda: 1)

# Kasus 5 - Buffer Video
init_state("video_buffer", deque)
init_state("video_played", list)
init_state("video_counter", lambda: 1)

# Kasus 6 - Tiket Kereta
init_state("ticket_queue", deque)
init_state("ticket_done", list)
init_state("ticket_counter", lambda: 1)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">Modul 6 - Sistem Antrian Queue</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">Implementasi struktur data Queue menggunakan prinsip FIFO pada enam studi kasus.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

tabs = st.tabs([
    "Antrian Bank",
    "Pendaftaran Mahasiswa",
    "Printer Queue",
    "Call Center",
    "Buffer Streaming",
    "Tiket Kereta"
])


# =====================================================
# KASUS 1 - ANTRIAN BANK
# =====================================================

with tabs[0]:
    st.header("Sistem Antrian Bank")
    st.markdown(
        '<div class="section-note">Nasabah yang masuk lebih awal akan dilayani lebih dahulu menggunakan konsep FIFO.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Tambah Nasabah")

        nama_nasabah = st.text_input(
            "Nama Nasabah",
            key="bank_input",
            placeholder="Contoh: Budi Santoso"
        )

        layanan = st.selectbox(
            "Jenis Layanan",
            ["Setor Tunai", "Tarik Tunai", "Transfer", "Buka Rekening", "KPR"],
            key="bank_layanan"
        )

        if st.button(
            "Ambil Nomor Antrian",
            key="btn_bank_add",
            use_container_width=True
        ):
            if nama_nasabah.strip():
                nomor = f"A{st.session_state.bank_counter:03d}"

                st.session_state.bank_queue.append({
                    "nomor": nomor,
                    "nama": nama_nasabah.strip(),
                    "layanan": layanan,
                    "waktu": time.strftime("%H:%M:%S")
                })

                st.session_state.bank_counter += 1
                st.success(
                    f"Nomor antrian {nomor} diberikan kepada {nama_nasabah}."
                )
            else:
                st.warning("Masukkan nama nasabah terlebih dahulu.")

        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

        if st.button(
            "Panggil dan Layani Nasabah Berikutnya",
            key="btn_bank_serve",
            use_container_width=True
        ):
            if st.session_state.bank_queue:
                nasabah = st.session_state.bank_queue.popleft()
                st.session_state.bank_served.append(nasabah)

                st.success(
                    f"Memanggil {nasabah['nomor']} - {nasabah['nama']} ({nasabah['layanan']})."
                )
            else:
                st.info("Antrian kosong.")

        if st.button(
            "Reset Antrian Bank",
            key="btn_bank_reset",
            use_container_width=True
        ):
            st.session_state.bank_queue = deque()
            st.session_state.bank_served = []
            st.session_state.bank_counter = 1
            st.success("Antrian bank berhasil direset.")

    with col2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            metric_card("Jumlah Antrian", len(st.session_state.bank_queue))
        with col_m2:
            metric_card("Sudah Dilayani", len(st.session_state.bank_served))

        st.subheader("Antrian Saat Ini")

        if st.session_state.bank_queue:
            for i, n in enumerate(st.session_state.bank_queue):
                title = f"{n['nomor']} - {n['nama']}"
                details = (
                    f"Layanan: {safe(n['layanan'])}<br>"
                    f"Waktu masuk: {safe(n['waktu'])}"
                )
                queue_item(title, details, is_next=(i == 0))
        else:
            empty_message("Antrian kosong.")

        st.subheader("Riwayat Pelayanan")

        if st.session_state.bank_served:
            for n in reversed(st.session_state.bank_served[-5:]):
                served_item(
                    f"{n['nomor']} - {n['nama']}",
                    f"Layanan: {safe(n['layanan'])}"
                )
        else:
            empty_message("Belum ada nasabah yang dilayani.")


# =====================================================
# KASUS 2 - PENDAFTARAN MAHASISWA
# =====================================================

with tabs[1]:
    st.header("Sistem Pendaftaran Mahasiswa")
    st.markdown(
        '<div class="section-note">Mahasiswa diproses berdasarkan urutan pendaftaran pertama masuk pertama diproses.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Daftarkan Mahasiswa")

        nama_mhs = st.text_input(
            "Nama Mahasiswa",
            key="mhs_input",
            placeholder="Contoh: Siti Rahayu"
        )

        prodi = st.selectbox(
            "Program Studi",
            [
                "Teknik Informatika",
                "Sistem Informasi",
                "Manajemen",
                "Akuntansi",
                "Hukum"
            ],
            key="mhs_prodi"
        )

        jalur = st.radio(
            "Jalur Masuk",
            ["SNBT", "Mandiri", "Prestasi"],
            key="mhs_jalur",
            horizontal=True
        )

        if st.button(
            "Daftar Sekarang",
            key="btn_mhs_add",
            use_container_width=True
        ):
            if nama_mhs.strip():
                no_reg = f"REG-{st.session_state.mhs_counter:04d}"

                st.session_state.mhs_queue.append({
                    "no_reg": no_reg,
                    "nama": nama_mhs.strip(),
                    "prodi": prodi,
                    "jalur": jalur,
                    "waktu": time.strftime("%H:%M:%S")
                })

                st.session_state.mhs_counter += 1
                st.success(f"No. Registrasi {no_reg} berhasil dibuat untuk {nama_mhs}.")
            else:
                st.warning("Masukkan nama mahasiswa.")

        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

        if st.button(
            "Proses Pendaftaran Berikutnya",
            key="btn_mhs_serve",
            use_container_width=True
        ):
            if st.session_state.mhs_queue:
                mhs = st.session_state.mhs_queue.popleft()
                st.session_state.mhs_served.append(mhs)

                st.success(
                    f"{mhs['no_reg']} - {mhs['nama']} ({mhs['prodi']}) berhasil diproses."
                )
            else:
                st.info("Tidak ada antrian pendaftaran.")

        if st.button(
            "Reset Pendaftaran",
            key="btn_mhs_reset",
            use_container_width=True
        ):
            st.session_state.mhs_queue = deque()
            st.session_state.mhs_served = []
            st.session_state.mhs_counter = 1
            st.success("Data pendaftaran berhasil direset.")

    with col2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            metric_card("Jumlah Antrian", len(st.session_state.mhs_queue))
        with col_m2:
            metric_card("Sudah Diproses", len(st.session_state.mhs_served))

        st.subheader("Antrian Pendaftaran")

        if st.session_state.mhs_queue:
            for i, m in enumerate(st.session_state.mhs_queue):
                queue_item(
                    f"{m['no_reg']} - {m['nama']}",
                    (
                        f"Program studi: {safe(m['prodi'])}<br>"
                        f"Jalur masuk: {safe(m['jalur'])}<br>"
                        f"Waktu daftar: {safe(m['waktu'])}"
                    ),
                    is_next=(i == 0)
                )
        else:
            empty_message("Antrian pendaftaran kosong.")

        st.subheader("Riwayat Pendaftaran Diproses")

        if st.session_state.mhs_served:
            for m in reversed(st.session_state.mhs_served[-5:]):
                served_item(
                    f"{m['no_reg']} - {m['nama']}",
                    f"Program studi: {safe(m['prodi'])} | Jalur: {safe(m['jalur'])}"
                )
        else:
            empty_message("Belum ada pendaftaran yang diproses.")


# =====================================================
# KASUS 3 - PRINTER QUEUE
# =====================================================

with tabs[2]:
    st.header("Printer Queue")
    st.markdown(
        '<div class="section-note">Dokumen dicetak sesuai urutan dokumen masuk ke antrian cetak.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Kirim Dokumen ke Printer")

        nama_doc = st.text_input(
            "Nama Dokumen",
            key="printer_input",
            placeholder="Contoh: Laporan_Keuangan.pdf"
        )

        halaman = st.number_input(
            "Jumlah Halaman",
            min_value=1,
            max_value=500,
            value=10,
            key="printer_halaman"
        )

        prioritas = st.selectbox(
            "Prioritas",
            ["Normal", "Tinggi"],
            key="printer_prio"
        )

        if st.button(
            "Kirim ke Antrian Cetak",
            key="btn_printer_add",
            use_container_width=True
        ):
            if nama_doc.strip():
                job_id = f"JOB-{st.session_state.printer_counter:03d}"

                st.session_state.printer_queue.append({
                    "job_id": job_id,
                    "nama": nama_doc.strip(),
                    "halaman": halaman,
                    "prioritas": prioritas,
                    "waktu": time.strftime("%H:%M:%S")
                })

                st.session_state.printer_counter += 1

                st.success(
                    f"{job_id} - {nama_doc} ({halaman} halaman) masuk antrian cetak."
                )
            else:
                st.warning("Masukkan nama dokumen.")

        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

        if st.button(
            "Cetak Dokumen Berikutnya",
            key="btn_printer_serve",
            use_container_width=True
        ):
            if st.session_state.printer_queue:
                doc = st.session_state.printer_queue.popleft()
                st.session_state.printer_done.append(doc)

                st.success(
                    f"Mencetak {doc['job_id']} - {doc['nama']} ({doc['halaman']} halaman)."
                )
            else:
                st.info("Antrian printer kosong.")

        if st.button(
            "Reset Printer Queue",
            key="btn_printer_reset",
            use_container_width=True
        ):
            st.session_state.printer_queue = deque()
            st.session_state.printer_done = []
            st.session_state.printer_counter = 1
            st.success("Printer queue berhasil direset.")

    with col2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            metric_card("Dokumen Menunggu", len(st.session_state.printer_queue))
        with col_m2:
            metric_card("Selesai Dicetak", len(st.session_state.printer_done))

        st.subheader("Antrian Cetak")

        if st.session_state.printer_queue:
            for i, d in enumerate(st.session_state.printer_queue):
                priority_tag = "PRIORITAS TINGGI" if d["prioritas"] == "Tinggi" else ""

                queue_item(
                    f"{d['job_id']} - {d['nama']}",
                    (
                        f"Jumlah halaman: {safe(d['halaman'])}<br>"
                        f"Prioritas: {safe(d['prioritas'])}<br>"
                        f"Waktu masuk: {safe(d['waktu'])}"
                    ),
                    is_next=(i == 0),
                    tag=priority_tag
                )
        else:
            empty_message("Tidak ada dokumen dalam antrian.")

        st.subheader("Riwayat Dokumen Dicetak")

        if st.session_state.printer_done:
            for d in reversed(st.session_state.printer_done[-5:]):
                served_item(
                    f"{d['job_id']} - {d['nama']}",
                    f"Jumlah halaman: {safe(d['halaman'])} | Prioritas: {safe(d['prioritas'])}"
                )
        else:
            empty_message("Belum ada dokumen yang dicetak.")


# =====================================================
# KASUS 4 - CALL CENTER KOPERASI
# =====================================================

with tabs[3]:
    st.header("Call Center Koperasi")
    st.markdown(
        '<div class="section-note">Panggilan pelanggan diproses berdasarkan urutan panggilan masuk.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Masukkan Panggilan Masuk")

        nama_pelanggan = st.text_input(
            "Nama Pelanggan",
            key="cc_input",
            placeholder="Contoh: Ahmad Fauzi"
        )

        no_anggota = st.text_input(
            "No. Anggota",
            key="cc_anggota",
            placeholder="Contoh: KOP-0012"
        )

        keperluan = st.selectbox(
            "Keperluan",
            [
                "Info Pinjaman",
                "Pembayaran Cicilan",
                "Simpanan",
                "Pengaduan",
                "Lainnya"
            ],
            key="cc_keperluan"
        )

        if st.button(
            "Masukkan ke Antrian Call",
            key="btn_cc_add",
            use_container_width=True
        ):
            if nama_pelanggan.strip():
                ticket = f"CALL-{st.session_state.cc_counter:03d}"

                st.session_state.cc_queue.append({
                    "ticket": ticket,
                    "nama": nama_pelanggan.strip(),
                    "no_anggota": no_anggota.strip() or "-",
                    "keperluan": keperluan,
                    "waktu": time.strftime("%H:%M:%S")
                })

                st.session_state.cc_counter += 1

                st.success(f"Tiket {ticket} dibuat untuk {nama_pelanggan}.")
            else:
                st.warning("Masukkan nama pelanggan.")

        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

        if st.button(
            "Layani Panggilan Berikutnya",
            key="btn_cc_serve",
            use_container_width=True
        ):
            if st.session_state.cc_queue:
                pelanggan = st.session_state.cc_queue.popleft()
                st.session_state.cc_served.append(pelanggan)

                st.success(
                    f"Melayani {pelanggan['ticket']} - {pelanggan['nama']} | {pelanggan['keperluan']}."
                )
            else:
                st.info("Tidak ada panggilan masuk.")

        if st.button(
            "Reset Call Center",
            key="btn_cc_reset",
            use_container_width=True
        ):
            st.session_state.cc_queue = deque()
            st.session_state.cc_served = []
            st.session_state.cc_counter = 1
            st.success("Data call center berhasil direset.")

    with col2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            metric_card("Panggilan Menunggu", len(st.session_state.cc_queue))
        with col_m2:
            metric_card("Sudah Dilayani", len(st.session_state.cc_served))

        st.subheader("Antrian Panggilan")

        if st.session_state.cc_queue:
            for i, p in enumerate(st.session_state.cc_queue):
                queue_item(
                    f"{p['ticket']} - {p['nama']}",
                    (
                        f"No. anggota: {safe(p['no_anggota'])}<br>"
                        f"Keperluan: {safe(p['keperluan'])}<br>"
                        f"Waktu masuk: {safe(p['waktu'])}"
                    ),
                    is_next=(i == 0)
                )
        else:
            empty_message("Tidak ada panggilan masuk.")

        st.subheader("Riwayat Panggilan Dilayani")

        if st.session_state.cc_served:
            for p in reversed(st.session_state.cc_served[-5:]):
                served_item(
                    f"{p['ticket']} - {p['nama']}",
                    f"No. anggota: {safe(p['no_anggota'])} | Keperluan: {safe(p['keperluan'])}"
                )
        else:
            empty_message("Belum ada panggilan yang dilayani.")


# =====================================================
# KASUS 5 - BUFFER STREAMING VIDEO
# =====================================================

with tabs[4]:
    st.header("Buffer Streaming Video")
    st.markdown(
        '<div class="section-note">Segmen video dimuat ke buffer dan diputar sesuai urutan masuk.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Muat Segmen Video")

        nama_video = st.text_input(
            "Nama Video",
            key="video_input",
            placeholder="Contoh: Tutorial Python Episode 3"
        )

        durasi_seg = st.slider(
            "Durasi Segmen dalam Detik",
            5,
            60,
            10,
            key="video_durasi"
        )

        resolusi = st.selectbox(
            "Resolusi",
            ["360p", "480p", "720p", "1080p", "4K"],
            key="video_res"
        )

        jumlah_seg = st.number_input(
            "Jumlah Segmen Dimuat",
            min_value=1,
            max_value=20,
            value=3,
            key="video_jml"
        )

        if st.button(
            "Muat ke Buffer",
            key="btn_video_add",
            use_container_width=True
        ):
            if nama_video.strip():
                for _ in range(jumlah_seg):
                    seg_id = f"SEG-{st.session_state.video_counter:04d}"
                    ukuran = round(random.uniform(2.5, 15.0), 2)

                    st.session_state.video_buffer.append({
                        "seg_id": seg_id,
                        "video": nama_video.strip(),
                        "durasi": durasi_seg,
                        "resolusi": resolusi,
                        "ukuran_mb": ukuran,
                        "waktu": time.strftime("%H:%M:%S")
                    })

                    st.session_state.video_counter += 1

                st.success(
                    f"{jumlah_seg} segmen video {nama_video} berhasil dimuat ke buffer."
                )
            else:
                st.warning("Masukkan nama video.")

        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

        if st.button(
            "Putar Segmen Berikutnya",
            key="btn_video_play",
            use_container_width=True
        ):
            if st.session_state.video_buffer:
                seg = st.session_state.video_buffer.popleft()
                st.session_state.video_played.append(seg)

                st.success(
                    f"Memutar {seg['seg_id']} - {seg['video']} ({seg['resolusi']}, {seg['durasi']} detik, {seg['ukuran_mb']} MB)."
                )
            else:
                st.info("Buffer kosong. Muat video terlebih dahulu.")

        if st.button(
            "Bersihkan Buffer",
            key="btn_video_reset",
            use_container_width=True
        ):
            st.session_state.video_buffer = deque()
            st.session_state.video_played = []
            st.session_state.video_counter = 1
            st.success("Buffer berhasil dibersihkan.")

    with col2:
        buffer_size = len(st.session_state.video_buffer)
        max_buffer = 20
        percent = min(buffer_size / max_buffer, 1.0)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            metric_card("Segmen Buffer", buffer_size)
        with col_m2:
            metric_card("Sudah Diputar", len(st.session_state.video_played))

        st.subheader("Status Buffer")
        st.progress(percent, text=f"Buffer terisi: {buffer_size}/{max_buffer}")

        if st.session_state.video_buffer:
            for i, s in enumerate(list(st.session_state.video_buffer)[:6]):
                queue_item(
                    f"{s['seg_id']} - {s['video']}",
                    (
                        f"Resolusi: {safe(s['resolusi'])}<br>"
                        f"Durasi: {safe(s['durasi'])} detik<br>"
                        f"Ukuran: {safe(s['ukuran_mb'])} MB<br>"
                        f"Waktu masuk: {safe(s['waktu'])}"
                    ),
                    is_next=(i == 0)
                )

            if buffer_size > 6:
                st.caption(f"Terdapat {buffer_size - 6} segmen lain yang belum ditampilkan.")
        else:
            empty_message("Buffer kosong.")

        st.subheader("Riwayat Segmen Diputar")

        if st.session_state.video_played:
            for s in reversed(st.session_state.video_played[-5:]):
                served_item(
                    f"{s['seg_id']} - {s['video']}",
                    f"Resolusi: {safe(s['resolusi'])} | Durasi: {safe(s['durasi'])} detik"
                )
        else:
            empty_message("Belum ada segmen yang diputar.")


# =====================================================
# KASUS 6 - TIKET KERETA API ONLINE
# =====================================================

with tabs[5]:
    st.header("Sistem Tiket Kereta Api Online")
    st.markdown(
        '<div class="section-note">Pesanan tiket diproses berdasarkan urutan transaksi masuk.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Pesan Tiket")

        nama_pemesan = st.text_input(
            "Nama Pemesan",
            key="ticket_input",
            placeholder="Contoh: Dewi Lestari"
        )

        rute = st.selectbox(
            "Rute",
            [
                "Jakarta ke Bandung",
                "Bandung ke Yogyakarta",
                "Yogyakarta ke Surabaya",
                "Surabaya ke Malang",
                "Jakarta ke Semarang",
                "Semarang ke Solo"
            ],
            key="ticket_rute"
        )

        kelas = st.radio(
            "Kelas",
            ["Ekonomi", "Bisnis", "Eksekutif"],
            key="ticket_kelas",
            horizontal=True
        )

        jumlah_tiket = st.number_input(
            "Jumlah Tiket",
            min_value=1,
            max_value=10,
            value=1,
            key="ticket_jml"
        )

        if st.button(
            "Pesan Tiket",
            key="btn_ticket_add",
            use_container_width=True
        ):
            if nama_pemesan.strip():
                order_id = f"TRX-{st.session_state.ticket_counter:05d}"

                harga = {
                    "Ekonomi": 150_000,
                    "Bisnis": 300_000,
                    "Eksekutif": 500_000
                }

                total = harga[kelas] * jumlah_tiket

                st.session_state.ticket_queue.append({
                    "order_id": order_id,
                    "nama": nama_pemesan.strip(),
                    "rute": rute,
                    "kelas": kelas,
                    "jumlah": jumlah_tiket,
                    "total": total,
                    "waktu": time.strftime("%H:%M:%S")
                })

                st.session_state.ticket_counter += 1

                st.success(
                    f"{order_id} - {nama_pemesan} | {rute} | Total: {rupiah(total)}."
                )
            else:
                st.warning("Masukkan nama pemesan.")

        st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

        if st.button(
            "Proses Pesanan Berikutnya",
            key="btn_ticket_serve",
            use_container_width=True
        ):
            if st.session_state.ticket_queue:
                order = st.session_state.ticket_queue.popleft()
                st.session_state.ticket_done.append(order)

                st.success(
                    f"{order['order_id']} - {order['nama']} | {order['rute']} | {rupiah(order['total'])} terkonfirmasi."
                )
            else:
                st.info("Tidak ada pesanan dalam antrian.")

        if st.button(
            "Reset Sistem Tiket",
            key="btn_ticket_reset",
            use_container_width=True
        ):
            st.session_state.ticket_queue = deque()
            st.session_state.ticket_done = []
            st.session_state.ticket_counter = 1
            st.success("Sistem tiket berhasil direset.")

    with col2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            metric_card("Pesanan Menunggu", len(st.session_state.ticket_queue))
        with col_m2:
            metric_card("Terkonfirmasi", len(st.session_state.ticket_done))

        st.subheader("Antrian Pesanan")

        if st.session_state.ticket_queue:
            for i, o in enumerate(st.session_state.ticket_queue):
                queue_item(
                    f"{o['order_id']} - {o['nama']}",
                    (
                        f"Rute: {safe(o['rute'])}<br>"
                        f"Kelas: {safe(o['kelas'])}<br>"
                        f"Jumlah tiket: {safe(o['jumlah'])}<br>"
                        f"Total: {rupiah(o['total'])}<br>"
                        f"Waktu pesan: {safe(o['waktu'])}"
                    ),
                    is_next=(i == 0)
                )
        else:
            empty_message("Tidak ada pesanan dalam antrian.")

        st.subheader("Riwayat Pesanan Terkonfirmasi")

        if st.session_state.ticket_done:
            for o in reversed(st.session_state.ticket_done[-5:]):
                served_item(
                    f"{o['order_id']} - {o['nama']}",
                    f"Rute: {safe(o['rute'])} | Total: {rupiah(o['total'])}"
                )
        else:
            empty_message("Belum ada pesanan yang dikonfirmasi.")


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    '<div class="footer-text">6 Studi Kasus Struktur Data Queue - Python dan Streamlit</div>',
    unsafe_allow_html=True
)
