import pandas as pd
import streamlit as st
from thefuzz import fuzz

# Cài đặt giao diện trang web
st.set_page_config(page_title="Tra Cứu Câu Hỏi", page_icon="🔍", layout="centered")

# --- ĐOẠN CODE DÙNG CSS ĐỂ LÀM ĐẸP GIAO DIỆN TRÊN ĐIỆN THOẠI ---
st.markdown("""
<style>
    /* Ẩn dòng chữ "Press Enter to apply" bên trong ô tìm kiếm */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 Phần Mềm Tìm Kiếm Câu Hỏi")
st.write("Gõ một đoạn câu hỏi vào ô bên dưới, hệ thống sẽ tự động tìm kiếm!")

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Ngan_Hang_Cau_Hoi_Hieu.xlsx", sheet_name='Tổng Hợp Tất Cả Đề', header=2)
        df['Nội dung câu hỏi'] = df['Nội dung câu hỏi'].fillna('')
        df['Các phương án'] = df['Các phương án'].fillna('')
        df['Đáp án đúng'] = df['Đáp án đúng'].fillna('')
        return df
    except Exception as e:
        st.error(f"Lỗi không tìm thấy file Excel: {e}")
        return None

df = load_data()

if df is not None:
    st.success(f"✅ Đã tải thành công {len(df)} câu hỏi!")
    
    # Khởi tạo bộ nhớ tạm để quản lý việc xóa chữ
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
        
    def clear_text():
        st.session_state.search_query = ""

    # Chia bố cục: Ô chữ (chiếm 7 phần), nút Tìm (1.5 phần), nút Xóa (1.5 phần)
    col1, col2, col3 = st.columns([7, 1.5, 1.5])
    
    with col1:
        query = st.text_input("Nhập từ khóa tại đây:", key="search_query")
        
    with col2:
        st.markdown("<br>", unsafe_allow_html=True) # Đẩy nút xuống cho bằng với ô chữ
        search_btn = st.button("🔍", use_container_width=True)
        
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        clear_btn = st.button("❌", on_click=clear_text, use_container_width=True)
    
    if query:
        results = []
        for index, row in df.iterrows():
            question = str(row['Nội dung câu hỏi'])
            score = fuzz.token_set_ratio(query.lower(), question.lower())
            
            if score >= 60 or query.lower() in question.lower():
                results.append({
                    'score': score,
                    'question': question,
                    'options': str(row['Các phương án']),
                    'answer': str(row['Đáp án đúng'])
                })
        
        results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
        
        if not results:
            st.warning("⚠️ Không tìm thấy câu hỏi nào tương tự.")
        else:
            for i, res in enumerate(results, 1):
                # Hiển thị kết quả tối giản, không còn chữ "(Khớp ...%)"
                st.markdown(f"### KẾT QUẢ {i}") 
                st.markdown(f"**❓ Câu hỏi:** {res['question']}")
                st.markdown(f"**📋 Phương án:**\n{res['options']}")
                st.markdown(f"**✅ ĐÁP ÁN ĐÚNG:** <span style='color:red; font-size:18px; font-weight:bold;'>{res['answer']}</span>", unsafe_allow_html=True)
                st.divider()
