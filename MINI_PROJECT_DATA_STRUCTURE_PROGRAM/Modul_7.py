import streamlit as st
from collections import deque
import time

st.set_page_config(page_title="Sistem Linked List - 6 Studi Kasus", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a1a2e;
        padding: 20px 0;
    }
    .node-item {
        background: #f0f4ff;
        border-left: 5px solid #4f46e5;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
        font-weight: 500;
    }
    .node-head {
        background: #ede9fe;
        border-left: 5px solid #7c3aed;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
        font-weight: 700;
    }
    .node-tail {
        background: #fef3c7;
        border-left: 5px solid #d97706;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .deleted-item {
        background: #fff1f2;
        border-left: 5px solid #f43f5e;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
        text-decoration: line-through;
        color: #9ca3af;
    }
    .undo-item {
        background: #fef9ec;
        border-left: 5px solid #f59e0b;
        padding: 8px 14px;
        margin: 4px 0;
        border-radius: 5px;
    }
    .redo-item {
        background: #ecfdf5;
        border-left: 5px solid #10b981;
        padding: 8px 14px;
        margin: 4px 0;
        border-radius: 5px;
    }
    .current-text {
        background: #1e1e2e;
        color: #cdd6f4;
        padding: 15px 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
        min-height: 80px;
        white-space: pre-wrap;
    }
    .arrow {
        text-align: center;
        font-size: 1.2rem;
        color: #6366f1;
        margin: 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NODE CLASSES
# ─────────────────────────────────────────────
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self._size += 1

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def delete(self, data_key, key_field=None):
        cur = self.head
        prev = None
        while cur:
            val = cur.data.get(key_field, "") if key_field else cur.data
            if val == data_key:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self._size -= 1
                return True
            prev = cur
            cur = cur.next
        return False

    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def size(self):
        return self._size

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        new_node = DoublyNode(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def pop_tail(self):
        if not self.tail:
            return None
        data = self.tail.data
        if self.tail.prev:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.head = self.tail = None
        self._size -= 1
        return data

    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def size(self):
        return self._size

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init(key, factory):
    if key not in st.session_state:
        st.session_state[key] = factory()

# Kasus 1 - Playlist
init("playlist_ll", LinkedList)
init("playlist_counter", lambda: 1)
init("playlist_now_playing", lambda: None)

# Kasus 2 - Browser History
init("browser_ll", LinkedList)
init("browser_counter", lambda: 1)

# Kasus 3 - Anggota Koperasi
init("koperasi_ll", LinkedList)
init("koperasi_counter", lambda: 1)
init("koperasi_deleted", list)

# Kasus 4 - Reservasi Hotel
init("hotel_ll", LinkedList)
init("hotel_counter", lambda: 1)
init("hotel_deleted", list)

# Kasus 5 - RS Antrian
init("rs_ll", LinkedList)
init("rs_counter", lambda: 1)
init("rs_served", list)

# Kasus 6 - Undo Redo
init("editor_dll", DoublyLinkedList)
init("editor_redo_stack", list)
init("editor_current", lambda: "")

# ─────────────────────────────────────────────
st.markdown('<div class="main-title">🔗 Sistem Linked List — 6 Studi Kasus</div>', unsafe_allow_html=True)
st.markdown("---")

tabs = st.tabs([
    "🎵 Playlist Musik",
    "🌐 Browser History",
    "🤝 Anggota Koperasi",
    "🏨 Reservasi Hotel",
    "🏥 Antrian RS",
    "✏️ Undo & Redo Editor"
])

# ══════════════════════════════════════════════
# KASUS 1 — PLAYLIST MUSIK DIGITAL
# ══════════════════════════════════════════════
with tabs[0]:
    st.header("🎵 Playlist Musik Digital")
    st.write("Linked List memungkinkan penambahan lagu baru secara **dinamis** di posisi mana saja.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("➕ Tambah Lagu")
        judul = st.text_input("Judul Lagu", key="pl_judul", placeholder="Contoh: Bohemian Rhapsody")
        artis = st.text_input("Artis", key="pl_artis", placeholder="Contoh: Queen")
        durasi = st.text_input("Durasi (mm:ss)", key="pl_durasi", placeholder="Contoh: 05:54")
        posisi = st.radio("Tambah di", ["Akhir Playlist", "Awal Playlist"], key="pl_posisi", horizontal=True)

        if st.button("🎵 Tambah Lagu", key="btn_pl_add", use_container_width=True):
            if judul.strip() and artis.strip():
                data = {
                    "id": f"SONG-{st.session_state.playlist_counter:03d}",
                    "judul": judul.strip(),
                    "artis": artis.strip(),
                    "durasi": durasi.strip() or "03:30"
                }
                if posisi == "Akhir Playlist":
                    st.session_state.playlist_ll.append(data)
                else:
                    st.session_state.playlist_ll.prepend(data)
                st.session_state.playlist_counter += 1
                st.success(f"✅ **{judul}** — {artis} ditambahkan ke {'akhir' if posisi == 'Akhir Playlist' else 'awal'}.")
            else:
                st.warning("⚠️ Isi judul dan artis.")

        st.markdown("---")
        songs = st.session_state.playlist_ll.to_list()
        if songs:
            pilih = st.selectbox("🎧 Pilih Lagu untuk Diputar / Hapus",
                                 [f"{s['id']} — {s['judul']} ({s['artis']})" for s in songs], key="pl_select")
            idx = [f"{s['id']} — {s['judul']} ({s['artis']})" for s in songs].index(pilih)

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("▶️ Putar", key="btn_pl_play", use_container_width=True):
                    st.session_state.playlist_now_playing = songs[idx]
                    st.success(f"▶️ Memutar: **{songs[idx]['judul']}**")
            with col_b:
                if st.button("🗑️ Hapus", key="btn_pl_del", use_container_width=True):
                    st.session_state.playlist_ll.delete(songs[idx]["id"], "id")
                    st.success(f"🗑️ **{songs[idx]['judul']}** dihapus.")
                    st.rerun()

        if st.button("🔄 Reset Playlist", key="btn_pl_reset", use_container_width=True):
            st.session_state.playlist_ll = LinkedList()
            st.session_state.playlist_counter = 1
            st.session_state.playlist_now_playing = None
            st.rerun()

    with col2:
        now = st.session_state.playlist_now_playing
        if now:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#667eea,#764ba2);border-radius:15px;padding:20px;color:white;margin-bottom:15px;'>
                <div style='font-size:2rem;text-align:center;'>▶️</div>
                <div style='font-size:1.3rem;font-weight:bold;text-align:center;'>{now['judul']}</div>
                <div style='text-align:center;opacity:0.85;'>{now['artis']} · {now['durasi']}</div>
            </div>
            """, unsafe_allow_html=True)

        songs = st.session_state.playlist_ll.to_list()
        st.subheader(f"📋 Playlist ({len(songs)} lagu)")
        if songs:
            for i, s in enumerate(songs):
                is_now = now and now["id"] == s["id"]
                if i == 0:
                    st.markdown(f'<div class="node-head">{"▶️ " if is_now else "🔵 "}<b>[HEAD]</b> {s["id"]} — {s["judul"]} · {s["artis"]} · {s["durasi"]}</div>', unsafe_allow_html=True)
                elif i == len(songs) - 1:
                    st.markdown(f'<div class="node-tail">{"▶️ " if is_now else "🟡 "}<b>[TAIL]</b> {s["id"]} — {s["judul"]} · {s["artis"]} · {s["durasi"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="node-item">{"▶️ " if is_now else "⚪ "}{s["id"]} — {s["judul"]} · {s["artis"]} · {s["durasi"]}</div>', unsafe_allow_html=True)
                if i < len(songs) - 1:
                    st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)
        else:
            st.info("Playlist kosong.")

# ══════════════════════════════════════════════
# KASUS 2 — BROWSER HISTORY
# ══════════════════════════════════════════════
with tabs[1]:
    st.header("🌐 Browser History")
    st.write("Setiap halaman dikunjungi disimpan sebagai node dalam Linked List.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("🔗 Kunjungi Halaman")
        url = st.text_input("URL", key="brow_url", placeholder="Contoh: https://google.com")
        judul_page = st.text_input("Judul Halaman", key="brow_title", placeholder="Contoh: Google Search")
        kategori = st.selectbox("Kategori", ["Berita", "Sosial Media", "E-Commerce", "Edukasi", "Hiburan", "Lainnya"], key="brow_kat")

        if st.button("🌐 Kunjungi", key="btn_brow_add", use_container_width=True):
            if url.strip():
                data = {
                    "id": f"PAGE-{st.session_state.browser_counter:03d}",
                    "url": url.strip(),
                    "judul": judul_page.strip() or url.strip(),
                    "kategori": kategori,
                    "waktu": time.strftime("%H:%M:%S")
                }
                st.session_state.browser_ll.prepend(data)
                st.session_state.browser_counter += 1
                st.success(f"✅ Mengunjungi: **{data['judul']}**")
            else:
                st.warning("⚠️ Masukkan URL.")

        st.markdown("---")
        history = st.session_state.browser_ll.to_list()
        if history:
            pilih_page = st.selectbox("🗑️ Hapus dari History",
                                      [f"{p['id']} — {p['judul']}" for p in history], key="brow_del_sel")
            if st.button("🗑️ Hapus Halaman Ini", key="btn_brow_del", use_container_width=True):
                idx_p = [f"{p['id']} — {p['judul']}" for p in history].index(pilih_page)
                st.session_state.browser_ll.delete(history[idx_p]["id"], "id")
                st.success(f"Dihapus dari riwayat.")
                st.rerun()

        if st.button("🧹 Hapus Semua Riwayat", key="btn_brow_clear", use_container_width=True):
            st.session_state.browser_ll = LinkedList()
            st.session_state.browser_counter = 1
            st.rerun()

    with col2:
        history = st.session_state.browser_ll.to_list()
        st.subheader(f"📋 Riwayat Kunjungan ({len(history)} halaman)")
        st.caption("Node terbaru ada di HEAD (atas)")
        if history:
            for i, p in enumerate(history):
                icon = "🟣" if i == 0 else ("🟡" if i == len(history)-1 else "⚪")
                label = " [HEAD — Terbaru]" if i == 0 else (" [TAIL — Terlama]" if i == len(history)-1 else "")
                st.markdown(f'<div class="{"node-head" if i==0 else ("node-tail" if i==len(history)-1 else "node-item")}">{icon}<b>{label}</b> {p["id"]}<br><small>🔗 {p["url"]}<br>📁 {p["kategori"]} · ⏰ {p["waktu"]}</small></div>', unsafe_allow_html=True)
                if i < len(history) - 1:
                    st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)
        else:
            st.info("Belum ada riwayat.")

# ══════════════════════════════════════════════
# KASUS 3 — DAFTAR ANGGOTA KOPERASI
# ══════════════════════════════════════════════
with tabs[2]:
    st.header("🤝 Daftar Anggota Koperasi")
    st.write("Data anggota dapat **ditambah dan dihapus kapan saja** menggunakan Linked List.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("➕ Tambah Anggota")
        nama_ang = st.text_input("Nama Anggota", key="kop_nama", placeholder="Contoh: Rina Marlina")
        no_ktp = st.text_input("No. KTP", key="kop_ktp", placeholder="32xxxxxxxxxxxxxxx")
        simpanan = st.number_input("Simpanan Pokok (Rp)", min_value=0, value=500000, step=50000, key="kop_simpanan")
        jenis = st.selectbox("Jenis Keanggotaan", ["Biasa", "Luar Biasa", "Kehormatan"], key="kop_jenis")

        if st.button("➕ Daftarkan Anggota", key="btn_kop_add", use_container_width=True):
            if nama_ang.strip():
                data = {
                    "id": f"ANG-{st.session_state.koperasi_counter:04d}",
                    "nama": nama_ang.strip(),
                    "no_ktp": no_ktp.strip() or "-",
                    "simpanan": simpanan,
                    "jenis": jenis
                }
                st.session_state.koperasi_ll.append(data)
                st.session_state.koperasi_counter += 1
                st.success(f"✅ **{data['id']}** — {nama_ang} terdaftar.")
            else:
                st.warning("⚠️ Masukkan nama anggota.")

        st.markdown("---")
        anggota_list = st.session_state.koperasi_ll.to_list()
        if anggota_list:
            pilih_ang = st.selectbox("Pilih Anggota untuk Dihapus",
                                     [f"{a['id']} — {a['nama']}" for a in anggota_list], key="kop_del_sel")
            if st.button("🗑️ Hapus Anggota", key="btn_kop_del", use_container_width=True):
                idx_a = [f"{a['id']} — {a['nama']}" for a in anggota_list].index(pilih_ang)
                target = anggota_list[idx_a]
                st.session_state.koperasi_deleted.append(target)
                st.session_state.koperasi_ll.delete(target["id"], "id")
                st.success(f"🗑️ **{target['nama']}** dihapus dari keanggotaan.")
                st.rerun()

        if st.button("🔄 Reset", key="btn_kop_reset", use_container_width=True):
            st.session_state.koperasi_ll = LinkedList()
            st.session_state.koperasi_counter = 1
            st.session_state.koperasi_deleted = []
            st.rerun()

    with col2:
        anggota_list = st.session_state.koperasi_ll.to_list()
        st.subheader(f"📋 Daftar Anggota Aktif ({len(anggota_list)})")
        if anggota_list:
            for i, a in enumerate(anggota_list):
                label = " [HEAD]" if i == 0 else (" [TAIL]" if i == len(anggota_list)-1 else "")
                cls = "node-head" if i == 0 else ("node-tail" if i == len(anggota_list)-1 else "node-item")
                st.markdown(f'<div class="{cls}">👤 <b>{a["id"]}{label}</b> — {a["nama"]}<br><small>KTP: {a["no_ktp"]} | {a["jenis"]} | Simpanan: Rp {a["simpanan"]:,.0f}</small></div>', unsafe_allow_html=True)
                if i < len(anggota_list) - 1:
                    st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)
        else:
            st.info("Belum ada anggota terdaftar.")

        if st.session_state.koperasi_deleted:
            st.subheader(f"❌ Anggota Dikeluarkan ({len(st.session_state.koperasi_deleted)})")
            for a in reversed(st.session_state.koperasi_deleted[-3:]):
                st.markdown(f'<div class="deleted-item">🚫 {a["id"]} — {a["nama"]}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# KASUS 4 — SISTEM RESERVASI HOTEL
# ══════════════════════════════════════════════
with tabs[3]:
    st.header("🏨 Sistem Reservasi Hotel")
    st.write("Data reservasi tersimpan secara **dinamis** dalam Linked List.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📋 Buat Reservasi")
        nama_tamu = st.text_input("Nama Tamu", key="htl_nama", placeholder="Contoh: Budi Santoso")
        tipe_kamar = st.selectbox("Tipe Kamar", ["Standard", "Deluxe", "Suite", "Executive Suite"], key="htl_tipe")
        checkin = st.date_input("Check-in", key="htl_checkin")
        checkout = st.date_input("Check-out", key="htl_checkout")
        jumlah_tamu = st.number_input("Jumlah Tamu", min_value=1, max_value=10, value=2, key="htl_jml")

        harga = {"Standard": 350000, "Deluxe": 600000, "Suite": 1200000, "Executive Suite": 2500000}

        if st.button("🏨 Buat Reservasi", key="btn_htl_add", use_container_width=True):
            if nama_tamu.strip():
                malam = max((checkout - checkin).days, 1)
                total = harga[tipe_kamar] * malam
                data = {
                    "id": f"RES-{st.session_state.hotel_counter:04d}",
                    "nama": nama_tamu.strip(),
                    "tipe": tipe_kamar,
                    "checkin": str(checkin),
                    "checkout": str(checkout),
                    "malam": malam,
                    "tamu": jumlah_tamu,
                    "total": total
                }
                st.session_state.hotel_ll.append(data)
                st.session_state.hotel_counter += 1
                st.success(f"✅ **{data['id']}** — {nama_tamu} | {tipe_kamar} | {malam} malam | Rp {total:,.0f}")
            else:
                st.warning("⚠️ Masukkan nama tamu.")

        st.markdown("---")
        reservasi_list = st.session_state.hotel_ll.to_list()
        if reservasi_list:
            pilih_res = st.selectbox("Pilih Reservasi untuk Dibatalkan",
                                     [f"{r['id']} — {r['nama']} ({r['tipe']})" for r in reservasi_list], key="htl_del_sel")
            if st.button("❌ Batalkan Reservasi", key="btn_htl_del", use_container_width=True):
                idx_r = [f"{r['id']} — {r['nama']} ({r['tipe']})" for r in reservasi_list].index(pilih_res)
                target = reservasi_list[idx_r]
                st.session_state.hotel_deleted.append(target)
                st.session_state.hotel_ll.delete(target["id"], "id")
                st.success(f"❌ Reservasi **{target['id']}** dibatalkan.")
                st.rerun()

        if st.button("🔄 Reset Reservasi", key="btn_htl_reset", use_container_width=True):
            st.session_state.hotel_ll = LinkedList()
            st.session_state.hotel_counter = 1
            st.session_state.hotel_deleted = []
            st.rerun()

    with col2:
        reservasi_list = st.session_state.hotel_ll.to_list()
        st.subheader(f"📋 Daftar Reservasi Aktif ({len(reservasi_list)})")
        if reservasi_list:
            for i, r in enumerate(reservasi_list):
                label = " [HEAD]" if i == 0 else (" [TAIL]" if i == len(reservasi_list)-1 else "")
                cls = "node-head" if i == 0 else ("node-tail" if i == len(reservasi_list)-1 else "node-item")
                st.markdown(f'<div class="{cls}">🏨 <b>{r["id"]}{label}</b> — {r["nama"]}<br><small>{r["tipe"]} | {r["checkin"]} → {r["checkout"]} ({r["malam"]} malam) | {r["tamu"]} tamu | Rp {r["total"]:,.0f}</small></div>', unsafe_allow_html=True)
                if i < len(reservasi_list) - 1:
                    st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)
        else:
            st.info("Belum ada reservasi.")

        if st.session_state.hotel_deleted:
            st.subheader("❌ Reservasi Dibatalkan")
            for r in reversed(st.session_state.hotel_deleted[-3:]):
                st.markdown(f'<div class="deleted-item">🚫 {r["id"]} — {r["nama"]} | {r["tipe"]}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# KASUS 5 — SISTEM ANTRIAN RUMAH SAKIT
# ══════════════════════════════════════════════
with tabs[4]:
    st.header("🏥 Sistem Antrian Rumah Sakit")
    st.write("Pasien baru ditambahkan secara **dinamis**. Pasien darurat dapat disisipkan di awal.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("➕ Daftarkan Pasien")
        nama_pasien = st.text_input("Nama Pasien", key="rs_nama", placeholder="Contoh: Andi Wijaya")
        keluhan = st.text_input("Keluhan", key="rs_keluhan", placeholder="Contoh: Demam tinggi")
        poli = st.selectbox("Poli Tujuan", ["Umum", "Anak", "Jantung", "Ortopedi", "Gigi", "Kandungan"], key="rs_poli")
        prioritas = st.radio("Prioritas", ["Normal", "Darurat (UGD)"], key="rs_prio", horizontal=True)

        if st.button("🏥 Daftarkan Pasien", key="btn_rs_add", use_container_width=True):
            if nama_pasien.strip():
                data = {
                    "id": f"PS-{st.session_state.rs_counter:04d}",
                    "nama": nama_pasien.strip(),
                    "keluhan": keluhan.strip() or "-",
                    "poli": poli,
                    "prioritas": prioritas,
                    "waktu": time.strftime("%H:%M:%S")
                }
                if prioritas == "Darurat (UGD)":
                    st.session_state.rs_ll.prepend(data)
                    st.success(f"🚨 **{data['id']}** — {nama_pasien} (DARURAT) langsung ke HEAD antrian!")
                else:
                    st.session_state.rs_ll.append(data)
                    st.success(f"✅ **{data['id']}** — {nama_pasien} ditambahkan.")
                st.session_state.rs_counter += 1
            else:
                st.warning("⚠️ Masukkan nama pasien.")

        st.markdown("---")
        if st.button("👨‍⚕️ Panggil Pasien Berikutnya", key="btn_rs_serve", use_container_width=True):
            pasien_list = st.session_state.rs_ll.to_list()
            if pasien_list:
                p = pasien_list[0]
                st.session_state.rs_ll.delete(p["id"], "id")
                st.session_state.rs_served.append(p)
                st.success(f"🔔 Memanggil: **{p['id']}** — {p['nama']} | Poli {p['poli']}")
                st.rerun()
            else:
                st.info("Antrian kosong.")

        if st.button("🔄 Reset", key="btn_rs_reset", use_container_width=True):
            st.session_state.rs_ll = LinkedList()
            st.session_state.rs_counter = 1
            st.session_state.rs_served = []
            st.rerun()

    with col2:
        pasien_list = st.session_state.rs_ll.to_list()
        st.subheader(f"📋 Antrian Pasien ({len(pasien_list)})")
        if pasien_list:
            for i, p in enumerate(pasien_list):
                icon = "🚨" if p["prioritas"] == "Darurat (UGD)" else ("🟣" if i == 0 else ("🟡" if i == len(pasien_list)-1 else "⚪"))
                label = " [HEAD — Dipanggil Berikutnya]" if i == 0 else (" [TAIL]" if i == len(pasien_list)-1 else "")
                cls = "node-head" if i == 0 else ("node-tail" if i == len(pasien_list)-1 else "node-item")
                st.markdown(f'<div class="{cls}">{icon} <b>{p["id"]}{label}</b> — {p["nama"]}<br><small>Poli {p["poli"]} | {p["keluhan"]} | {p["prioritas"]} | ⏰ {p["waktu"]}</small></div>', unsafe_allow_html=True)
                if i < len(pasien_list) - 1:
                    st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)
        else:
            st.info("Antrian kosong.")

        st.subheader(f"✅ Sudah Dilayani ({len(st.session_state.rs_served)})")
        for p in reversed(st.session_state.rs_served[-4:]):
            st.markdown(f'<div class="served-item" style="background:#f0fff4;border-left:5px solid #48bb78;padding:10px;margin:4px 0;border-radius:5px;">✔️ <b>{p["id"]}</b> — {p["nama"]} | Poli {p["poli"]}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# KASUS 6 — UNDO & REDO EDITOR TEKS
# ══════════════════════════════════════════════
with tabs[5]:
    st.header("✏️ Undo & Redo Editor Teks")
    st.write("Menggunakan **Doubly Linked List** — setiap perubahan bisa di-undo (mundur) dan di-redo (maju).")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("⌨️ Editor")
        teks_baru = st.text_area("Ketik / Edit Teks", key="editor_input",
                                  value=st.session_state.editor_current,
                                  height=120,
                                  placeholder="Mulai mengetik di sini...")

        colA, colB, colC = st.columns(3)
        with colA:
            if st.button("💾 Simpan Perubahan", key="btn_ed_save", use_container_width=True):
                if teks_baru != st.session_state.editor_current:
                    st.session_state.editor_dll.append(teks_baru)
                    st.session_state.editor_current = teks_baru
                    st.session_state.editor_redo_stack = []
                    st.success("✅ Perubahan disimpan.")
                    st.rerun()
                else:
                    st.info("Tidak ada perubahan.")

        with colB:
            if st.button("↩️ Undo", key="btn_ed_undo", use_container_width=True):
                dll = st.session_state.editor_dll
                if dll.size() > 0:
                    popped = dll.pop_tail()
                    st.session_state.editor_redo_stack.append(popped)
                    items = dll.to_list()
                    st.session_state.editor_current = items[-1] if items else ""
                    st.success(f"↩️ Undo berhasil.")
                    st.rerun()
                else:
                    st.info("Tidak ada yang bisa di-undo.")

        with colC:
            if st.button("↪️ Redo", key="btn_ed_redo", use_container_width=True):
                if st.session_state.editor_redo_stack:
                    redo_val = st.session_state.editor_redo_stack.pop()
                    st.session_state.editor_dll.append(redo_val)
                    st.session_state.editor_current = redo_val
                    st.success(f"↪️ Redo berhasil.")
                    st.rerun()
                else:
                    st.info("Tidak ada yang bisa di-redo.")

        if st.button("🗑️ Hapus Semua & Reset", key="btn_ed_reset", use_container_width=True):
            st.session_state.editor_dll = DoublyLinkedList()
            st.session_state.editor_redo_stack = []
            st.session_state.editor_current = ""
            st.rerun()

        st.markdown("---")
        st.subheader("📄 Teks Saat Ini")
        cur_text = st.session_state.editor_current
        st.markdown(f'<div class="current-text">{cur_text if cur_text else "[ kosong ]"}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("🔗 Doubly Linked List — Riwayat Perubahan")
        history_items = st.session_state.editor_dll.to_list()

        if history_items:
            for i, h in enumerate(history_items):
                is_current = (i == len(history_items) - 1)
                is_head = (i == 0)
                label = " ← CURRENT (TAIL)" if is_current else (" [HEAD]" if is_head else "")
                cls = "node-head" if is_head and not is_current else ("node-tail" if is_current else "node-item")
                preview = h[:60] + "..." if len(h) > 60 else (h if h else '[ kosong ]')

                if i > 0:
                    st.markdown('<div style="text-align:center;color:#4f46e5;font-size:1rem;">⬆️⬇️</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="{cls}">{"✏️" if is_current else "📝"} <b>v{i+1}{label}</b><br><small style="font-family:monospace;">{preview}</small></div>', unsafe_allow_html=True)
        else:
            st.info("Belum ada perubahan tersimpan.")

        if st.session_state.editor_redo_stack:
            st.markdown("---")
            st.subheader(f"↪️ Redo Stack ({len(st.session_state.editor_redo_stack)})")
            for i, r in enumerate(reversed(st.session_state.editor_redo_stack)):
                preview = r[:50] + "..." if len(r) > 50 else (r if r else "[ kosong ]")
                st.markdown(f'<div class="redo-item">↪️ <b>Redo {i+1}</b>: <small style="font-family:monospace;">{preview}</small></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div style='background:#f8f9ff;border:1px solid #e2e8f0;border-radius:10px;padding:15px;'>
            <b>📊 Statistik Editor</b><br>
            🔵 Versi tersimpan: <b>{st.session_state.editor_dll.size()}</b><br>
            🟢 Redo tersedia: <b>{len(st.session_state.editor_redo_stack)}</b><br>
            📝 Karakter saat ini: <b>{len(st.session_state.editor_current)}</b>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center><small>📚 6 Studi Kasus Struktur Data Linked List — Python & Streamlit</small></center>", unsafe_allow_html=True)