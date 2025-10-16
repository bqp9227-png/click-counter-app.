import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import json, os

SAVE_FILE = "click_data.json"

# ---------------------------
# Lưu / tải trạng thái
# ---------------------------
def default_state():
    return {
        "lich_su_mau": {i: [] for i in range(3, 19)},
        "tong_click": 0,
        "chen_len_tren": False
    }

def save_state():
    data = {
        "tong_click": st.session_state.tong_click,
        "lich_su_mau": st.session_state.lich_su_mau,
        "chen_len_tren": st.session_state.chen_len_tren
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def load_state():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.session_state.tong_click = data.get("tong_click", 0)
        st.session_state.lich_su_mau = data.get("lich_su_mau", {i: [] for i in range(3, 19)})
        st.session_state.chen_len_tren = data.get("chen_len_tren", False)
    else:
        d = default_state()
        st.session_state.tong_click = d["tong_click"]
        st.session_state.lich_su_mau = d["lich_su_mau"]
        st.session_state.chen_len_tren = d["chen_len_tren"]

# ---------------------------
# Khởi tạo
# ---------------------------
if "initialized" not in st.session_state:
    load_state()
    st.session_state.initialized = True

# ---------------------------
# Sinh màu mới (mỗi 10 click)
# ---------------------------
BASE_COLORS = [
    "red", "orange", "green", "blue", "purple",
    "yellow", "pink", "brown", "gray", "cyan",
    "magenta", "lime", "teal", "navy", "gold",
    "violet", "indigo", "salmon", "khaki", "turquoise"
]

def get_color_by_click(n):
    index = (n - 1) // 10
    if index < len(BASE_COLORS):
        return BASE_COLORS[index]
    cmap = cm.get_cmap("tab20", 1000)
    return mcolors.to_hex(cmap(index))

# ---------------------------
# Giao diện
# ---------------------------
st.title("Click Counter App")
st.caption("Mỗi 10 click đổi màu, có chế độ Nhảy lên / Nhảy xuống, lưu trạng thái JSON.")

mode_text = "Nhảy lên (màu mới thêm trên cùng)" if st.session_state.chen_len_tren else "Nhảy xuống (màu mới chen xuống dưới)"
st.markdown(f"**Chế độ hiện tại:** {mode_text}")

if st.button("Chuyển chế độ Nhảy lên / Nhảy xuống"):
    st.session_state.chen_len_tren = not st.session_state.chen_len_tren
    save_state()
    st.success(f"Đã chuyển chế độ → { 'Nhảy lên' if st.session_state.chen_len_tren else 'Nhảy xuống' }")

cols = st.columns(4)
for i, val in enumerate(range(3, 19)):
    if cols[i % 4].button(str(val), key=f"btn_{val}"):
        st.session_state.tong_click += 1
        color = get_color_by_click(st.session_state.tong_click)
        if st.session_state.chen_len_tren:
            st.session_state.lich_su_mau[val].append(color)
        else:
            st.session_state.lich_su_mau[val].insert(0, color)
        save_state()

# ---------------------------
# Vẽ biểu đồ
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
# Thống kê & lịch sử
# ---------------------------
with st.expander("Thống kê lượt click"):
    for k in range(3, 19):
        v = len(st.session_state.lich_su_mau[k])
        if v > 0:
            st.write(f"Nút {k}: {v} lần")

with st.expander("Lịch sử click (20 lần gần nhất)"):
    lich_su = []
    for nut, colors_list in st.session_state.lich_su_mau.items():
        for c in colors_list:
            lich_su.append((nut, c))
    if not lich_su:
        st.info("Chưa có lịch sử.")
    else:
        st.write(" → ".join([f"{nut}({mau})" for nut, mau in lich_su[-20:]]))

# ---------------------------
# Reset
# ---------------------------
if st.button("Reset dữ liệu", type="primary"):
    d = default_state()
    st.session_state.tong_click = d["tong_click"]
    st.session_state.lich_su_mau = d["lich_su_mau"]
    st.session_state.chen_len_tren = d["chen_len_tren"]
    save_state()
    st.success("Đã reset dữ liệu.")
