import streamlit as st
import matplotlib.pyplot as plt

if "counts" not in st.session_state:
    st.session_state.counts = {i: 0 for i in range(3, 19)}
    st.session_state.tong_click = 0
    st.session_state.lich_su = []

def get_color(n):
    if 1 <= n <= 10:
        return "skyblue"
    elif 11 <= n <= 20:
        return "orange"
    elif 21 <= n <= 30:
        return "green"
    elif 31 <= n <= 40:
        return "red"
    else:
        return "purple"

st.title("Ứng dụng đếm click và biểu đồ (Streamlit)")

cols = st.columns(4)
for i, val in enumerate(range(3, 19)):
    if cols[i % 4].button(str(val), key=f"btn_{val}"):
        st.session_state.counts[val] += 1
        st.session_state.tong_click += 1
        st.session_state.lich_su.append(val)

st.subheader(f"Tổng số click: {st.session_state.tong_click}")

fig, ax = plt.subplots(figsize=(8, 4))
x = list(st.session_state.counts.keys())
y = list(st.session_state.counts.values())
color = get_color(st.session_state.tong_click)
bars = ax.bar(x, y, color=color, alpha=0.8, edgecolor="black")

for bar, v in zip(bars, y):
    if v > 0:
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f"{v}", ha="center", va="bottom")

ax.set_title(f"Biểu đồ số lần click - Tổng: {st.session_state.tong_click}")
ax.set_xlabel("Giá trị nút")
ax.set_ylabel("Số lần click")
ax.grid(True, alpha=0.3)

st.pyplot(fig)

with st.expander("Thống kê chi tiết"):
    if st.session_state.tong_click == 0:
        st.info("Chưa có dữ liệu.")
    else:
        counts = st.session_state.counts
        nut_nhieu_nhat = max(counts.items(), key=lambda x: x[1])
        nut_it_nhat = next((item for item in sorted(counts.items(), key=lambda x: x[1]) if item[1] > 0), ("Không có", 0))

        st.write(f"- Nút được click nhiều nhất: {nut_nhieu_nhat[0]} ({nut_nhieu_nhat[1]} lần)")
        st.write(f"- Nút được click ít nhất: {nut_it_nhat[0]} ({nut_it_nhat[1]} lần)")
        st.write("Chi tiết từng nút:")
        for k in sorted(counts.keys()):
            v = counts[k]
            if v > 0:
                st.write(f"Nút {k}: {v} lần ({(v / st.session_state.tong_click) * 100:.1f}%)")

with st.expander("Lịch sử click (20 lần gần nhất)"):
    lich_su = st.session_state.lich_su
    if not lich_su:
        st.info("Chưa có lịch sử.")
    else:
        st.write(" → ".join(map(str, lich_su[-20:])))

if st.button("Reset dữ liệu", type="primary"):
    st.session_state.counts = {i: 0 for i in range(3, 19)}
    st.session_state.tong_click = 0
    st.session_state.lich_su = []
    st.success("Đã reset dữ liệu.")
