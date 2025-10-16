import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import json
import os

# ---------------------------
# Cấu hình lưu/khôi phục JSON
# ---------------------------
SAVE_FILE = "click_data.json"

def default_state():
    return {
        "lich_su_mau": {i: [] for i in range(3, 19)},
        "tong_click": 0,
        "chen_len_tren": False  # mặc định nhảy xuống
    }

def save_state():
    data = {
        "tong_click": st.session_state.tong_click,
        "lich_su_mau": st.session_state.lich_su_mau,
        "chen_len_tren": st.session_state.chen_len_tren
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        st.error(f"Lỗi lưu dữ liệu: {e}")

def load_state():
    # Nếu có file, khôi phục; nếu không, khởi tạo mặc định
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            st.session_state.tong_click = data.get("tong_click", 0)
            st.session_state.lich_su_mau = data.get(
                "lich_su_mau", {i: [] for i in range(3, 19)}
            )
            st.session_state.chen_len_tren = data.get("chen_len_tren", False)
        except Exception as e:
            st.warning(f"Không đọc được file lưu ({SAVE_FILE}). Khởi tạo mới. Chi tiết: {e}")
            init_defaults()
    else:
        init_defaults()

def init_defaults():
    d = default_state()
    st.session_state.lich_su_mau = d["lich_su_mau"]
    st.session_state.tong_click = d["tong_click"]
    st.session_state.chen_len_tren = d["chen_len_tren"]

# ---------------------------
# Khởi tạo session state
# ---------------------------
if "initialized" not in st.session_state:
    # Tải trạng thái đã lưu (nếu có)
    load_state()
    st.session_state.initialized = True

# ---------------------------
# Tạo màu không lặp lại theo ngưỡng 10 click
# ---------------------------
# Danh sách màu cơ bản (20 màu đầu, không lặp lại)
BASE_COLORS = [
    "red", "orange", "green", "blue", "purple",
    "yellow", "pink", "brown", "gray", "cyan",
    "magenta", "lime", "teal", "navy", "gold",
    "violet", "indigo", "salmon", "khaki", "turquoise"
]

def get_color_by_click(n_total_clicks: int) -> str:
    # Mỗi 10 click toàn cục đổi màu
    index = (n_total_clicks - 1) // 10
    if index < len(BASE_COLORS):
        return BASE_COLORS[index]
    # Hết BASE_COLORS thì sinh thêm màu duy nhất từ colormap
    # tab20 có 20 màu cơ bản; dùng sampling theo index để tạo thêm màu mới
    cmap = cm.get_cmap("tab20", 1000)  # sinh 1000 màu khác
    # Chuyển thành mã hex để thống nhất
    return mcolors.to_hex(cmap(index))

# ---------------------------
# Giao diện
# ---------------------------
st.title("Ứng dụng đếm click nhiều màu")
st.caption("Ngưỡng 10 click đổi màu; chế độ nhảy lên/nhảy xuống; tự động lưu khôi phục từ JSON.")

# Hiển thị trạng thái hiện tại
mode_text = "Nhảy lên (màu mới thêm lên trên)" if st.session_state.chen_len_tren \
    else "Nhảy xuống (màu mới chen xuống dưới)"
st.markdown(f"**Chế độ hiện tại:** {mode_text}")
st.markdown(f"**File lưu:** {SAVE_FILE}")

# Nút chuyển chế độ
if st.button("Chuyển chế độ Nhảy lên / Nhảy xuống"):
    st.session_state.chen_len_tren = not st.session_state.chen_len_tren
    save_state()  # lưu lại chế độ
    st.success(f"Đã chuyển chế độ → { 'Nhảy lên' if st.session_state.chen_len_tren else 'Nhảy xuống' }")

# Khu vực nút số
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
        save_state()
        st.toast(f"Đã click {val} → Tổng click: {st.session_state.tong_click}")

# Vẽ stacked bar chart
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

# Thống kê
with st.expander("Thống kê lượt click"):
    if st.session_state.tong_click == 0:
        st.info("Chưa có dữ liệu.")
    else:
        for k in range(3, 19):
            v = len(st.session_state.lich_su_mau[k])
            if v > 0:
                st.write(f"- **Nút {k}:** {v} lần")

# Lịch sử 20 lần gần nhất (theo thứ tự thêm màu vào các cột)
with st.expander("Lịch sử click (20 lần gần nhất)"):
    lich_su = []
    for nut, colors_list in st.session_state.lich_su_mau.items():
        for c in colors_list:
            lich_su.append((nut, c))
    if not lich_su:
        st.info("Chưa có lịch sử.")
    else:
        st.write(" → ".join([f"{nut}({mau})" for nut, mau in lich_su[-20:]]))

# Nút reset
if st.button("Reset dữ liệu", type="primary"):
    init_defaults()
    save_state()
    st.success("Đã reset dữ liệu và lưu vào file.")
