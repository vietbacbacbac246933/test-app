import warnings
# Khóa tất cả các cảnh báo hệ thống gây rối Terminal
warnings.filterwarnings("ignore")

import streamlit as st

# Cấu hình giao diện ứng dụng rộng rãi, trực quan
st.set_page_config(page_title="DASS-21 Quiz App", page_icon="📊", layout="centered")

# Dữ liệu 21 câu hỏi từ ảnh của bạn
DASS21_QUESTIONS = {
    1: {"text": "Tôi thấy khó mà thoải mái được", "type": "S"},
    2: {"text": "Tôi bị khô miệng", "type": "A"},
    3: {"text": "Tôi không thấy có chút cảm xúc tích cực nào", "type": "D"},
    4: {"text": "Tôi bị rối loạn nhịp thở (thở gấp, khó thở dù chẳng làm việc gì nặng)", "type": "A"},
    5: {"text": "Tôi thấy khó bắt tay vào công việc", "type": "D"},
    6: {"text": "Tôi đã phản ứng thái quá khi có những sự việc xảy ra", "type": "S"},
    7: {"text": "Tôi bị ra mồ hôi (chẳng hạn như mồ hôi tay...)", "type": "A"},
    8: {"text": "Tôi thấy mình đang suy nghĩ quá nhiều", "type": "S"},
    9: {"text": "Tôi lo lắng về những tình huống có thể khiến tôi hoảng sợ hoặc biến tôi thành trò cười", "type": "A"},
    10: {"text": "Tôi thấy mình chẳng có gì để mong đợi cả", "type": "D"},
    11: {"text": "Tôi thấy bản thân dễ bị kích động", "type": "S"},
    12: {"text": "Tôi thấy khó thư giãn được", "type": "S"},
    13: {"text": "Tôi cảm thấy chán nản, thất vọng", "type": "D"},
    14: {"text": "Tôi không chấp nhận được việc có cái gì đó xen vào cản trở việc tôi đang làm", "type": "S"},
    15: {"text": "Tôi thấy mình gần như hoảng loạn", "type": "A"},
    16: {"text": "Tôi không thấy hăng hái với bất kỳ việc gì nữa", "type": "D"},
    17: {"text": "Tôi cảm thấy mình chẳng đáng làm người", "type": "D"},
    18: {"text": "Tôi thấy mình khá dễ phật ý, tự ái", "type": "S"},
    19: {"text": "Tôi nghe thấy rõ tiếng nhịp tim dù chẳng làm việc gì cả (ví dụ, tiếng nhịp tim tăng, tiếng tim loạn nhịp)", "type": "A"},
    20: {"text": "Tôi hay sợ vô cớ", "type": "A"},
    21: {"text": "Tôi thấy cuộc sống vô nghĩa", "type": "D"}
}

# Định nghĩa các mốc phân loại chuẩn xác theo ảnh thống kê điểm số
def get_status(score, category_type):
    if category_type == "D": # Trầm cảm
        if score <= 9: return "Bình thường (Normal)", "normal"
        if score <= 13: return "Nhẹ (Mild)", "low"
        if score <= 20: return "Vừa phải (Moderate)", "medium"
        if score <= 27: return "Nặng (Severe)", "high"
        return "Rất nặng (Extremely Severe)", "extreme"
        
    elif category_type == "A": # Lo âu
        if score <= 7: return "Bình thường (Normal)", "normal"
        if score <= 9: return "Nhẹ (Mild)", "low"
        if score <= 14: return "Vừa phải (Moderate)", "medium"
        if score <= 19: return "Nặng (Severe)", "high"
        return "Rất nặng (Extremely Severe)", "extreme"
        
    elif category_type == "S": # Căng thẳng
        if score <= 14: return "Bình thường (Normal)", "normal"
        if score <= 18: return "Nhẹ (Mild)", "low"
        if score <= 25: return "Vừa phải (Moderate)", "medium"
        if score <= 33: return "Nặng (Severe)", "high"
        return "Rất nặng (Extremely Severe)", "extreme"

# --- GIAO DIỆN CHÍNH ---
st.title("🧠 Bài Kiểm Tra Sức Khỏe Tâm Lý (DASS-21)")
st.caption("Thang đo mức độ Trầm cảm, Lo âu và Căng thẳng trong vòng 1 tuần qua.")
st.info("💡 Hướng dẫn: Hãy chọn mức độ phù hợp nhất với tình trạng thực tế của bạn.")
st.write("---")

# Bản đồ điểm số tương ứng các lựa chọn
options_dict = {
    "Không bao giờ": 0,
    "Vài lần": 1,
    "Thường xuyên": 2,
    "Gần như mọi ngày": 3
}

# Khởi tạo form nhập liệu tập trung để không bị re-run liên tục khi bấm chọn câu hỏi
with st.form("dass21_quiz_form"):
    user_answers = {}
    
    # Vòng lặp hiển thị 21 câu hỏi gọn gàng
    for q_id, q_data in DASS21_QUESTIONS.items():
        st.markdown(f"##### Câu {q_id}: {q_data['text']}")
        choice = st.radio(
            f"Chọn mức độ cho câu {q_id}", 
            options=list(options_dict.keys()), 
            index=0, 
            key=f"q_{q_id}",
            label_visibility="collapsed" # Ẩn nhãn phụ để giao diện sạch sẽ
        )
        user_answers[q_id] = options_dict[choice]
        st.write("") # Tạo khoảng cách nhỏ giữa các câu

    st.write("---")
    # Nút bấm submit form
    submit_button = st.form_submit_button(label="📊 XEM KẾT QUẢ ĐÁNH GIÁ", type="primary")

# --- XỬ LÝ DỮ LIỆU KHI BẤM SUBMIT ---
if submit_button:
    # 1. Tính toán điểm gốc của từng nhóm
    scores = {"D": 0, "A": 0, "S": 0}
    for q_id, ans_value in user_answers.items():
        q_type = DASS21_QUESTIONS[q_id]["type"]
        scores[q_type] += ans_value
        
    # 2. Nhân hệ số 2 theo tiêu chuẩn quy đổi
    final_D = scores["D"] * 2
    final_A = scores["A"] * 2
    final_S = scores["S"] * 2

    # Lấy nhãn phân loại
    label_D, status_D = get_status(final_D, "D")
    label_A, status_A = get_status(final_A, "A")
    label_S, status_S = get_status(final_S, "S")

    # 3. Hiển thị kết quả ra màn hình bằng Dashboard trực quan
    st.success("🎉 Đã tính toán kết quả thành công! Dưới đây là thống kê của bạn:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="📉 Nhóm 1: TRẦM CẢM", value=f"{final_D} điểm", delta=label_D, delta_color="inverse")
    with col2:
        st.metric(label="⚡ Nhóm 2: LO ÂU", value=f"{final_A} điểm", delta=label_A, delta_color="inverse")
    with col3:
        st.metric(label="🔥 Nhóm 3: CĂNG THẲNG", value=f"{final_S} điểm", delta=label_S, delta_color="inverse")

    # Hiển thị thêm các hộp cảnh báo chi tiết theo mức độ để tăng trải nghiệm người dùng
    st.write("---")
    st.markdown("### 📋 Đánh giá chi tiết:")
    
    # Định dạng màu cho từng phân loại dựa trên mức độ nghiêm trọng
    for name, score, label, status in [("Trầm cảm", final_D, label_D, status_D), 
                                      ("Lo âu", final_A, label_A, status_A), 
                                      ("Căng thẳng", final_S, label_S, status_S)]:
        if "Bình thường" in label:
            st.success(f"**{name}**: {score} điểm $\rightarrow$ {label}")
        elif "Nhẹ" in label or "Vừa phải" in label:
            st.warning(f"**{name}**: {score} điểm $\rightarrow$ {label}")
        else:
            st.error(f"**{name}**: {score} điểm $\rightarrow$ {label}")
