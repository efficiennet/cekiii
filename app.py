import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Perhitungan Kartu 4 Orang",
    layout="wide"
)

st.title("🎴 Perhitungan Permainan Kartu")

# =====================================
# LOAD CSV JIKA ADA (AGAR DATA TIDAK HILANG)
# =====================================
if "data" not in st.session_state:
    if os.path.exists("data_kartu.csv"):
        st.session_state.data = pd.read_csv("data_kartu.csv")
    else:
        st.session_state.data = pd.DataFrame()

if "ronde" not in st.session_state:
    if not st.session_state.data.empty:
        st.session_state.ronde = st.session_state.data["Ronde"].max() + 1
    else:
        st.session_state.ronde = 1

# =====================================
# INPUT NAMA HANYA SEKALI
# =====================================
if "nama_fixed" not in st.session_state:
    st.session_state.nama_fixed = False

st.subheader("👤 Nama Pemain")

if not st.session_state.nama_fixed:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        p1 = st.text_input("Pemain 1", "tomi")
    with col2:
        p2 = st.text_input("Pemain 2", "erwin")
    with col3:
        p3 = st.text_input("Pemain 3", "fajar")
    with col4:
        p4 = st.text_input("Pemain 4", "ega")

    # Simpan nama ke session_state
    if st.button("🔒 Simpan Nama Pemain"):
        st.session_state.p1 = p1
        st.session_state.p2 = p2
        st.session_state.p3 = p3
        st.session_state.p4 = p4
        st.session_state.nama_fixed = True
        st.rerun()

else:
    # Nama sudah tersimpan
    p1 = st.session_state.p1
    p2 = st.session_state.p2
    p3 = st.session_state.p3
    p4 = st.session_state.p4

    st.info(f"Nama pemain: **{p1}, {p2}, {p3}, {p4}**")

players = [p1, p2, p3, p4]

# Jika data kosong → buat kolom awal
if st.session_state.data.empty:
    st.session_state.data = pd.DataFrame(columns=["Ronde"] + players)

# =====================================
# INPUT SKOR RONDE
# =====================================
st.subheader(f"📝 Input Skor Ronde {st.session_state.ronde}")

c1, c2, c3, c4 = st.columns(4)
with c1:
    s1 = st.number_input(p1, value=0)
with c2:
    s2 = st.number_input(p2, value=0)
with c3:
    s3 = st.number_input(p3, value=0)
with c4:
    s4 = st.number_input(p4, value=0)

if st.button("➕ Simpan Ronde"):
    new_row = {
        "Ronde": st.session_state.ronde,
        p1: s1,
        p2: s2,
        p3: s3,
        p4: s4
    }

    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )

    # Simpan ke CSV agar tidak hilang saat refresh
    st.session_state.data.to_csv("data_kartu.csv", index=False)

    st.session_state.ronde += 1
    st.success("Ronde berhasil disimpan!")

# =====================================
# RIWAYAT SKOR
# =====================================
st.subheader("📊 Riwayat Skor")
st.dataframe(st.session_state.data, use_container_width=True)

# =====================================
# TOTAL & PERINGKAT
# =====================================
if not st.session_state.data.empty:

    total = st.session_state.data[players].sum()

    hasil = pd.DataFrame({
        "Pemain": total.index,
        "Total Skor": total.values
    }).sort_values("Total Skor", ascending=False)

    st.subheader("🏆 Peringkat Pemain")
    st.table(hasil)

    # Pemain Terendah
    pemain_terendah = hasil.iloc[-1]["Pemain"]
    nilai_terendah = hasil.iloc[-1]["Total Skor"]

    st.error(f"😆 Pemain skor terendah: **{pemain_terendah}** ({nilai_terendah} poin)")
    st.warning("🤣 hahaha ngujut")

# =====================================
# RESET
# =====================================
if st.button("🔄 Reset Permainan"):
    st.session_state.data = pd.DataFrame(columns=["Ronde"] + players)
    st.session_state.ronde = 1

    if os.path.exists("data_kartu.csv"):
        os.remove("data_kartu.csv")

    st.warning("Permainan direset!")
    st.rerun()

# =====================================
# WATERMARK
# =====================================
st.markdown("""
<br><br>
<div style='text-align:center; opacity:0.5; font-size:14px;'>
    © 2025 - FUZZY BAYESSS
</div>
""", unsafe_allow_html=True)
