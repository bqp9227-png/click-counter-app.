import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ---------------------------
# Khởi tạo session state
# ---------------------------
def init_defaults():
    if "lich_su_mau" not in st.session_state:
        st.session_state.lich_su_mau = {i: [] for i in range(3, 19)}  # lịch sử màu theo từng nút
    if "tong_click" not in st.session_state:
        st.session_state.tong_click = 0  # tổng số click toàn cục
    if "chen_len_tren" not in st.session_state:
        st.session_state.chen_len_tren = False  # False: nhảy xuống, True: nhảy lên

init_defaults()

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
    # nếu vượt quá BASE_COLORS, sinh thêm từ colormap
    cmap = cm.get_cmap("tab20", 1000)
    return mcolors.to_hex(cmap(index % 1000))

# ---------------------------
# Giao diện và điều khiển
# ---------------------------
st.title("Click Counter App (không lưu trạng thái)")
st.caption("Mỗi 10 click đổi màu. Chế độ Nhảy lên/Nhảy xuống điều khiển vị trí thêm màu trong cột.")

mode_text = "Nhảy lên (màu mới thêm trên cùng)" if st.session_state.chen_len_tren else "Nhảy xuống (màu mới chen xuống dưới)"
st.markdown(f"**Chế độ hiện tại:** {mode_text}")

if st.button("Chuyển chế độ Nhảy lên / Nhảy xuống"):
    st.session_state.chen_len_tren = not st.session_state.chen_len_tren
    st.success(f"Đã chuyển → {'Nhảy lên' if st.session_state.chen_len_tren else 'Nhảy xuống'}")

# Lưới nút 3 → 18
cols = st.columns(4)
for i, val in enumerate(range(3, 19)):
    if cols[i % 4].button(str(val), key=f"btn_{val}"):
        st.session_state.tong_click += 1
        color = get_color_by_click(st.session_state.tong_click)
        if st.session_state.chen_len_tren:
            # Nhảy lên: thêm màu mới lên trên cùng
            st.session_state.lich_su_mau[val].append(color)
        else:
            # Nhảy xuống: chen màu mới xuống đáy
            st.session_state.lich_su_mau[val].insert(0, color)
        st.toast(f"Click {val} → Tổng: {st.session_state.tong_click}")

# ---------------------------
# Vẽ biểu đồ stacked bar
# ---------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
for val in range(3, 19):
    bottom = 0
    for color in st.session_state.lich_su_mau[val]:
        ax.bar(val, 1, bottom=bottom, color=color, edgecolor="black")
        bottom += 1

ax.set_title(f"Tổng số click: {st.session_state.tong_click}")
ax.set_xlabel("Nút")
ax.set_ylabel("Số lần click")
ax.set_xticks(list(range(3, 19)))
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

# ---------------------------
# Reset
# ---------------------------
if st.button("Reset phiên", type="primary"):
    st.session_state.lich_su_mau = {i: [] for i in range(3, 19)}
    st.session_state.tong_click = 0
    st.session_state.chen_len_tren = False
    st.success("Đã reset phiên (không lưu).")
