import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Modul 5 - Stack",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#1e3a8a;
}

.stack-box{
    background-color:#f8fafc;
    color:black;
    padding:12px;
    border-radius:10px;
    border-left:5px solid #2563eb;
    margin:5px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "buku_stack" not in st.session_state:
    st.session_state.buku_stack = []

if "history_stack" not in st.session_state:
    st.session_state.history_stack = []

if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []

if "redo_stack" not in st.session_state:
    st.session_state.redo_stack = []

if "saldo" not in st.session_state:
    st.session_state.saldo = 0

if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">📚 MODUL 5 - STRUKTUR DATA STACK</div>',
    unsafe_allow_html=True
)

st.write(
    "Implementasi Struktur Data Stack menggunakan 5 Studi Kasus."
)

st.divider()

tabs = st.tabs([
    "📚 Tumpukan Buku",
    "🌐 Browser History",
    "📝 Undo Editor",
    "🧮 Validasi Kurung",
    "🏦 ATM Undo"
])

# =====================================================
# KASUS 1
# =====================================================

with tabs[0]:

    st.header("📚 Tumpukan Buku")

    buku = st.text_input(
        "Masukkan Judul Buku"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "➕ Tambah Buku",
            key="tambah_buku",
            width="stretch"
        ):

            if buku:

                st.session_state.buku_stack.append(
                    buku
                )

                st.success(
                    f"{buku} berhasil ditambahkan"
                )

    with col2:

        if st.button(
            "📤 Ambil Buku",
            key="ambil_buku",
            width="stretch"
        ):

            if st.session_state.buku_stack:

                keluar = st.session_state.buku_stack.pop()

                st.warning(
                    f"Buku keluar: {keluar}"
                )

    with col3:

        if st.button(
            "🗑 Reset",
            key="reset_buku",
            width="stretch"
        ):

            st.session_state.buku_stack = []

    st.subheader("Isi Stack Buku")

    if st.session_state.buku_stack:

        for item in reversed(
            st.session_state.buku_stack
        ):

            st.markdown(
                f"""
                <div class='stack-box'>
                📖 {item}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.info(
            f"Buku Teratas : {st.session_state.buku_stack[-1]}"
        )

    else:

        st.info("Belum ada buku.")

# =====================================================
# KASUS 2
# =====================================================

with tabs[1]:

    st.header("🌐 Browser History")

    url = st.text_input(
        "Masukkan URL",
        placeholder="https://google.com"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🌐 Kunjungi",
            key="visit",
            width="stretch"
        ):

            if url:

                st.session_state.history_stack.append(
                    url
                )

                st.success(
                    "Website ditambahkan."
                )

    with col2:

        if st.button(
            "⬅ Back",
            key="back",
            width="stretch"
        ):

            if st.session_state.history_stack:

                keluar = st.session_state.history_stack.pop()

                st.warning(
                    f"Kembali dari {keluar}"
                )

    with col3:

        if st.button(
            "🗑 Reset",
            key="reset_history",
            width="stretch"
        ):

            st.session_state.history_stack = []

    st.subheader("Riwayat Browser")

    if st.session_state.history_stack:

        for item in reversed(
            st.session_state.history_stack
        ):

            st.link_button(
                item,
                item
            )

    else:

        st.info("Belum ada riwayat.")

# =====================================================
# KASUS 3
# =====================================================

with tabs[2]:

    st.header("📝 Undo Redo Editor")

    teks = st.text_area(
        "Tulis Dokumen"
    )

    if st.button(
        "💾 Simpan Versi",
        key="simpan_versi",
        width="stretch"
    ):

        st.session_state.undo_stack.append({
            "Waktu":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            "Teks": teks
        })

        st.session_state.redo_stack.clear()

        st.success("Versi disimpan.")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "↩ Undo",
            key="undo_btn",
            width="stretch"
        ):

            if st.session_state.undo_stack:

                data = st.session_state.undo_stack.pop()

                st.session_state.redo_stack.append(
                    data
                )

    with col2:

        if st.button(
            "↪ Redo",
            key="redo_btn",
            width="stretch"
        ):

            if st.session_state.redo_stack:

                data = st.session_state.redo_stack.pop()

                st.session_state.undo_stack.append(
                    data
                )

    st.subheader("Dokumen Aktif")

    if st.session_state.undo_stack:

        st.code(
            st.session_state.undo_stack[-1]["Teks"]
        )

    st.subheader("Undo Stack")

    if st.session_state.undo_stack:

        st.dataframe(
            pd.DataFrame(
                st.session_state.undo_stack
            ),
            width="stretch"
        )

    st.subheader("Redo Stack")

    if st.session_state.redo_stack:

        st.dataframe(
            pd.DataFrame(
                st.session_state.redo_stack
            ),
            width="stretch"
        )

# =====================================================
# KASUS 4
# =====================================================

with tabs[3]:

    st.header("🧮 Validasi Kurung")

    ekspresi = st.text_input(
        "Masukkan Ekspresi",
        "((a+b)*(c+d))"
    )

    if st.button(
        "Validasi",
        key="validasi",
        width="stretch"
    ):

        stack = []

        proses = []

        pasangan = {
            ")":"(",
            "]":"[",
            "}":"{"
        }

        valid = True

        for char in ekspresi:

            if char in "([{":

                stack.append(char)

                proses.append([
                    char,
                    "PUSH",
                    str(stack)
                ])

            elif char in ")]}":

                if not stack:

                    valid = False
                    break

                atas = stack.pop()

                proses.append([
                    char,
                    "POP",
                    str(stack)
                ])

                if atas != pasangan[char]:

                    valid = False
                    break

        if stack:
            valid = False

        st.subheader(
            "Proses Stack"
        )

        df = pd.DataFrame(
            proses,
            columns=[
                "Karakter",
                "Operasi",
                "Isi Stack"
            ]
        )

        st.dataframe(
            df,
            width="stretch"
        )

        if valid:

            st.success(
                "✅ Ekspresi VALID"
            )

            st.info("""
            Semua kurung buka memiliki
            pasangan kurung tutup yang sesuai.
            Stack berhasil kosong di akhir proses.
            """)

        else:

            st.error(
                "❌ Ekspresi TIDAK VALID"
            )

            st.warning("""
            Terdapat kurung yang tidak memiliki pasangan
            atau urutan kurung tidak sesuai.
            """)

# =====================================================
# KASUS 5
# =====================================================

with tabs[4]:

    st.header("🏦 ATM Undo Transaksi")

    jenis = st.selectbox(
        "Jenis Transaksi",
        ["Setor", "Tarik"]
    )

    nominal = st.number_input(
        "Nominal",
        min_value=1000,
        step=1000
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💳 Proses",
            key="proses_atm",
            width="stretch"
        ):

            if jenis == "Setor":

                st.session_state.saldo += nominal

                st.session_state.transaksi.append({
                    "Jenis": jenis,
                    "Nominal": nominal
                })

            else:

                if nominal <= st.session_state.saldo:

                    st.session_state.saldo -= nominal

                    st.session_state.transaksi.append({
                        "Jenis": jenis,
                        "Nominal": nominal
                    })

                else:

                    st.error(
                        "Saldo tidak cukup"
                    )

    with col2:

        if st.button(
            "↩ Undo Transaksi",
            key="undo_atm",
            width="stretch"
        ):

            if st.session_state.transaksi:

                trx = st.session_state.transaksi.pop()

                if trx["Jenis"] == "Setor":

                    st.session_state.saldo -= trx["Nominal"]

                else:

                    st.session_state.saldo += trx["Nominal"]

                st.warning(
                    "Transaksi terakhir dibatalkan"
                )

    st.metric(
        "Saldo Saat Ini",
        f"Rp {st.session_state.saldo:,.0f}"
    )

    st.subheader(
        "Riwayat Transaksi"
    )

    if st.session_state.transaksi:

        st.dataframe(
            pd.DataFrame(
                st.session_state.transaksi
            ),
            width="stretch"
        )

    else:

        st.info(
            "Belum ada transaksi."
        )