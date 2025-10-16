import streamlit as st
import matplotlib.pyplot as plt

# Khởi tạo session state
if "lich_su_mau" not in st.session_state:
    st.session_state.lich_su_mau = {i: [] for i in range(3, 19)}
    st.session_state.tong_click = 0

# Hàm chọn màu theo số thứ tự click toàn cục
def get_color_by_click(n):
    if n <= 2:
        return "red"
    elif n <= 10:
        return "orange"
    elif n <= 20:
        return "green"
    elif n <= 30:
        return "blue"
    else:
        return "purple"

st.title("Ứng dụng đếm click nhiều màu theo từng lượt")

# Tạo các nút từ 3 đến 18
cols = st.columns(4)
for i, val in enumerate(range(3, 19)):
    if cols[i % 4].button(str(val), key=f"btn_{val}"):
        st.session_state.tong_click += 1
        color = get_color_by_click(st.session_state.tong_click)
        st.session_state.lich_su_mau[val].append(color)

# Vẽ stacked bar chart
fig, ax = plt.subplots(figsize=(8, 4))
for i, val in enumerate(range(3, 19)):
    bottom = 0
    for color in st.session_state.lich_su_mau[val]:
        ax.bar(val, 1, bottom=bottom, color=color, edgecolor="black")
        bottom += 1

ax.set_title(f"Tổng số click: {st.session_state.tong_click}")
ax.set_xlabel("Nút")
ax.set_ylabel("Số lần click")
st.pyplot(fig)

# Hiển thị thống kê chi tiết
with st.expander("Thống kê chi tiết"):
    if st.session_state.tong_click == 0:
        st.info("Chưa có dữ liệu.")
    else:
        for k in sorted(st.session_state.lich_su_mau.keys()):
            v = len(st.session_state.lich_su_mau[k])
            if v > 0:
                st.write(f"Nút {k}: {v} lần")

# Hiển thị lịch sử click
with st.expander("Lịch sử click (20 lần gần nhất)"):
    lich_su = []
    for nut, colors in st.session_state.lich_su_mau.items():
        for c in colors:
            lich_su.append((nut, c))
    if not lich_su:
        st.info("Chưa có lịch sử.")
    else:
        # chỉ lấy 20 lần gần nhất
        lich_su_text = " → ".join([f"{nut}({mau})" for nut, mau in lich_su[-20:]])
        st.write(lich_su_text)

# Nút reset
if st.button("Reset dữ liệu", type="primary"):
    st.session_state.lich_su_mau = {i: [] for i in range(3, 19)}
    st.session_state.tong_click = 0
    st.success("Đã reset dữ liệu.")
