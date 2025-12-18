import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Perhitungan Kartu 4 Orang",
    layout="wide"
)

st.title("🎴 Perhitungan Permainan Kartu (4 Pemain)")

# ===============================
# INPUT NAMA PEMAIN
# ===============================
st.subheader("👤 Nama Pemain")
col1, col2, col3, col4 = st.columns(4)

with col1:
    p1 = st.text_input("Pemain 1", "Andi")
with col2:
    p2 = st.text_input("Pemain 2", "Budi")
with col3:
    p3 = st.text_input("Pemain 3", "Citra")
with col4:
    p4 = st.text_input("Pemain 4", "Deni")

players = [p1, p2, p3, p4]

# ===============================
# SESSION STATE
# ===============================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Ronde"] + players)
    st.session_state.ronde = 1

# Jika nama pemain berubah → reset kolom
if list(st.session_state.data.columns[1:]) != players:
    st.session_state.data = pd.DataFrame(columns=["Ronde"] + players)
    st.session_state.ronde = 1

# ===============================
# INPUT SKOR
# ===============================
st.subheader(f"📝 Input Skor Ronde {st.session_state.ronde}")
c1, c2, c3, c4 = st.columns(4)

with c1:
    s1 = st.number_input(p1, value=0, key="s1")
with c2:
    s2 = st.number_input(p2, value=0, key="s2")
with c3:
    s3 = st.number_input(p3, value=0, key="s3")
with c4:
    s4 = st.number_input(p4, value=0, key="s4")

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
    st.session_state.ronde += 1
    st.success("Ronde berhasil disimpan!")

# ===============================
# RIWAYAT SKOR
# ===============================
st.subheader("📊 Riwayat Skor")
st.dataframe(st.session_state.data, use_container_width=True)

# ===============================
# TOTAL & RANKING
# ===============================
if not st.session_state.data.empty:
    total = st.session_state.data[players].sum()

    hasil = pd.DataFrame({
        "Pemain": total.index,
        "Total Skor": total.values
    }).sort_values("Total Skor", ascending=False)

    st.subheader("🏆 Peringkat Pemain")
    st.table(hasil)

    # ===============================
    # NOTIF UNTUK PEMAIN TERENDAH
    # ===============================
    pemain_terendah = hasil.iloc[-1]["Pemain"]
    nilai_terendah = hasil.iloc[-1]["Total Skor"]

    st.error(f"😆 Pemain dengan skor terendah adalah **{pemain_terendah}** dengan total skor **{nilai_terendah}**")
    st.warning("🤣 hahaha ngujut")

# ===============================
# RESET
# ===============================
if st.button("🔄 Reset Permainan"):
    st.session_state.data = pd.DataFrame(columns=["Ronde"] + players)
    st.session_state.ronde = 1
    st.warning("Permainan direset!")

# ===============================
# WATERMARK
# ===============================
st.markdown("""
<br><br><br>
<div style='text-align:center; opacity:0.5; font-size:14px;'>
    © 2025 - Dibuat  oleh FUZZY BAYES 
</div>
""", unsafe_allow_html=True)
