import streamlit as st
import heapq

st.set_page_config(
    page_title="Modul 10 - Heap & Priority Queue",
    page_icon="⭐",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:2.5rem;
    font-weight:bold;
    color:#1a1a2e;
    padding:20px;
}
.queue-item{
    background:white;
    color:black;
    padding:12px;
    border-radius:10px;
    border-left:5px solid #667eea;
    margin:5px 0;
}
.done-item{
    background:#f0fff4;
    color:black;
    padding:12px;
    border-radius:10px;
    border-left:5px solid green;
    margin:5px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">⭐ Heap & Priority Queue - 6 Studi Kasus</div>',
    unsafe_allow_html=True
)

# =========================
# SESSION STATE
# =========================
def init_state(key):
    if key not in st.session_state:
        st.session_state[key] = []

for key in [
    "rs_heap","rs_done",
    "cpu_heap","cpu_done",
    "tiket_heap","tiket_done",
    "market_heap","market_done",
    "driver_heap","driver_done",
    "kdkmp_heap","kdkmp_done"
]:
    init_state(key)

# =========================
# TABS
# =========================
tabs = st.tabs([
    "🏥 Rumah Sakit",
    "💻 CPU",
    "🎫 Tiket",
    "🛒 Marketplace",
    "🚗 Driver",
    "💰 KDKMP"
])

# =====================================================
# KASUS 1
# =====================================================
with tabs[0]:

    st.header("🏥 Sistem Antrian Rumah Sakit")

    col1,col2 = st.columns(2)

    with col1:

        nama = st.text_input("Nama Pasien")

        status = st.selectbox(
            "Tingkat Kegawatan",
            [
                "🔴 Gawat Darurat",
                "🟡 Sedang",
                "🟢 Ringan"
            ]
        )

        prioritas_map = {
            "🔴 Gawat Darurat":1,
            "🟡 Sedang":2,
            "🟢 Ringan":3
        }

        if st.button("➕ Tambah Pasien", width="stretch"):

            heapq.heappush(
                st.session_state.rs_heap,
                (
                    prioritas_map[status],
                    nama,
                    status
                )
            )

        if st.button("📢 Panggil Pasien", width="stretch"):

            if st.session_state.rs_heap:

                pasien = heapq.heappop(
                    st.session_state.rs_heap
                )

                st.session_state.rs_done.append(
                    pasien
                )

                st.success(
                    f"{pasien[1]} dipanggil"
                )

    with col2:

        st.metric(
            "Pasien Menunggu",
            len(st.session_state.rs_heap)
        )

        st.subheader("Priority Queue")

        for p in sorted(st.session_state.rs_heap):

            st.markdown(
                f"""
                <div class='queue-item'>
                {p[2]}<br>
                {p[1]}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("Sudah Dilayani")

        for p in reversed(st.session_state.rs_done):

            st.markdown(
                f"""
                <div class='done-item'>
                ✔️ {p[1]}
                </div>
                """,
                unsafe_allow_html=True
            )

# =====================================================
# KASUS 2
# =====================================================
with tabs[1]:

    st.header("💻 CPU Scheduling")

    proses = st.text_input("Nama Proses")

    prioritas = st.slider(
        "Prioritas",
        1,
        10,
        5
    )

    if st.button("Tambah Proses"):

        heapq.heappush(
            st.session_state.cpu_heap,
            (
                -prioritas,
                proses
            )
        )

    if st.button("Jalankan Proses"):

        if st.session_state.cpu_heap:

            p = heapq.heappop(
                st.session_state.cpu_heap
            )

            st.session_state.cpu_done.append(p)

            st.success(
                f"Menjalankan {p[1]}"
            )

    st.write(sorted(st.session_state.cpu_heap))

# =====================================================
# KASUS 3
# =====================================================
with tabs[2]:

    st.header("🎫 Sistem Pemesanan Tiket")

    nama = st.text_input("Nama Pelanggan")

    jenis = st.selectbox(
        "Kategori",
        ["VIP","Regular"]
    )

    prioritas = 1 if jenis=="VIP" else 2

    if st.button("Tambah Pelanggan"):

        heapq.heappush(
            st.session_state.tiket_heap,
            (
                prioritas,
                nama,
                jenis
            )
        )

    st.write(sorted(
        st.session_state.tiket_heap
    ))

# =====================================================
# KASUS 4
# =====================================================
with tabs[3]:

    st.header("🛒 Marketplace")

    produk = st.text_input("Nama Produk")

    rating = st.slider(
        "Rating",
        1.0,
        5.0,
        4.0
    )

    if st.button("Tambah Produk"):

        heapq.heappush(
            st.session_state.market_heap,
            (
                -rating,
                produk
            )
        )

    st.write(
        sorted(
            st.session_state.market_heap
        )
    )

# =====================================================
# KASUS 5
# =====================================================
with tabs[4]:

    st.header("🚗 Driver Online")

    driver = st.text_input("Nama Driver")

    jarak = st.number_input(
        "Jarak (KM)",
        min_value=0.1
    )

    if st.button("Tambah Driver"):

        heapq.heappush(
            st.session_state.driver_heap,
            (
                jarak,
                driver
            )
        )

    st.write(
        sorted(
            st.session_state.driver_heap
        )
    )

# =====================================================
# KASUS 6
# =====================================================
with tabs[5]:

    st.header("💰 Pembiayaan KDKMP")

    nama = st.text_input("Nama Peminjam")

    skor = st.slider(
        "Skor Kelayakan",
        0,
        100,
        50
    )

    if st.button("Tambah Calon"):

        heapq.heappush(
            st.session_state.kdkmp_heap,
            (
                -skor,
                nama
            )
        )

    st.write(
        sorted(
            st.session_state.kdkmp_heap
        )
    )

st.divider()

if st.button("🗑️ Reset Semua Data"):

    for key in st.session_state.keys():
        del st.session_state[key]

    st.rerun()