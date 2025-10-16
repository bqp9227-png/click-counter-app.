import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ---------------------------
# Khởi tạo session state
# ---------------------------
if "lich_su_mau" not in st.session_state:
    st.session_state.lich_su_mau = {i: [] for i in range(3, 19)}
if "tong_click" not in st.session_state:
    st.session_state.tong_click = 0
if "chen_len_tren" not in st.session_state:
    st.session_state.chen_len_tren = False  # False: nhảy xuống, True: nhảy lên
if "mau_toan_cuc" not in st.session_state:
    st.session_state.mau_toan_cuc = []  # lưu màu cho cột 19
if "nguong_mau" not in st.session_state:
    st.session_state.nguong_mau = 0  # ngưỡng màu hiện tại

# ---------------------------
# Cấu hình màu: đổi mỗi 10 click
# ---------------------------
BASE_COLORS = [
    "red", "orange", "green", "blue", "purple",
    "yellow", "pink", "brown", "gray", "cyan",
    "magenta", "lime", "teal", "navy", "gold",
    "violet", "indigo", "salmon", "khaki", "turquoise"
]

def get_color_by_click(n_total_clicks: int) -> str:
    index = (n_total_clicks - 1) // 10
    if index < len(BASE_COLORS):
        return BASE_COLORS[index]
    cmap = cm.get_cmap("tab20", 1000)
    return mcolors.to_hex(cmap(index % 1000))

# ---------------------------
# Giao diện
# ---------------------------
st.title("Click Counter App (cột 19 đổi màu ngay khi đổi)")
st.caption("Cột 3–18: mỗi click đều thêm màu. Cột 19: thêm màu ngay khi màu đổi (mỗi 10 click).")

# Hiển thị chế độ hiện tại
mode_text = "Nhảy lên (màu mới thêm trên cùng)" if st.session_state.chen_len_tren else "Nhảy xuống (màu mới chen xuống dưới)"
st.markdown(f"**Chế độ hiện tại:** {mode_text}")

# Nút chuyển chế độ
if st.button("Chuyển chế độ Nhảy lên / Nhảy xuống"):
    st.session_state.chen_len_tren = not st.session_state.chen_len_tren
    st.success(f"Đã chuyển → {'Nhảy lên' if st.session_state.chen_len_tren else 'Nhảy xuống'}")

# Các nút từ 3 → 18
cols = st.columns(4)
for i, val in enumerate(range(3, 19)):
    if cols[i % 4].button(str(val), key=f"btn_{val}"):
        st.session_state.tong_click += 1
        color = get_color_by_click(st.session_state.tong_click)

        # luôn thêm màu cho cột riêng (3–18)
        if st.session_state.chen_len_tren:
            st.session_state.lich_su_mau[val].append(color)
        else:
            st.session_state.lich_su_mau[val].insert(0, color)

        # kiểm tra ngưỡng màu bằng chia thực
        muc_mau = int(st.session_state.tong_click / 10)
        if muc_mau > st.session_state.nguong_mau:
            st.session_state.nguong_mau = muc_mau
            if st.session_state.chen_len_tren:
                st.session_state.mau_toan_cuc.append(color)
            else:
                st.session_state.mau_toan_cuc.insert(0, color)

        st.toast(f"Click {val} → Tổng: {st.session_state.tong_click}")

# ---------------------------
# Vẽ biểu đồ stacked bar
# ---------------------------
fig, ax = plt.subplots(figsize=(10, 4.8))
for val in range(3, 19):
    bottom = 0
    for color in st.session_state.lich_su_mau[val]:
        ax.bar(val, 1, bottom=bottom, color=color, edgecolor="black")
        bottom += 1

# vẽ thêm cột toàn cục ở vị trí 19
bottom = 0
for color in st.session_state.mau_toan_cuc:
    ax.bar(19, 1, bottom=bottom, color=color, edgecolor="black")
    bottom += 1

ax.set_title(f"Tổng số click: {st.session_state.tong_click}")
ax.set_xlabel("Nút (19 = toàn cục)")
ax.set_ylabel("Số lần click")
ax.set_xticks(list(range(3, 20)))
st.pyplot(fig)

# ---------------------------
# Thống kê
# ---------------------------
with st.expander("Thống kê lượt click"):
    if st.session_state.tong_click == 0:
        st.info("Chưa có dữ liệu.")
    else:
        for k in range(3, 19):
            v = len(st.session_state.lich_su_mau[k])
            if v > 0:
                st.write(f"- **Nút {k}:** {v} lần")
        st.write(f"**Cột toàn cục (19):** {len(st.session_state.mau_toan_cuc)} màu đã ghi")

# ---------------------------
# Reset
# ---------------------------
if st.button("Reset phiên", type="primary"):
    st.session_state.lich_su_mau = {i: [] for i in range(3, 19)}
    st.session_state.tong_click = 0
    st.session_state.chen_len_tren = False
    st.session_state.mau_toan_cuc = []
    st.session_state.nguong_mau = 0
    st.success("Đã reset phiên (không lưu).")
