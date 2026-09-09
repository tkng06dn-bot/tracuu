import pandas as pd
import streamlit as st
from thefuzz import fuzz

# Cài đặt giao diện trang web
st.set_page_config(page_title="Tra Cứu Câu Hỏi", page_icon="🔍", layout="centered")

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
    
    # 1. Khởi tạo bộ nhớ tạm để quản lý nội dung ô tìm kiếm
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
        
    # 2. Hàm thực thi khi bấm nút Xóa (làm trống nội dung)
    def clear_text():
        st.session_state.search_query = ""

    # 3. Thiết kế bố cục 3 cột nằm ngang
    col1, col2, col3 = st.columns([6, 2, 2])
    
    with col1:
        # Ô nhập liệu chiếm 6 phần, liên kết với bộ nhớ 'search_query'
        query = st.text_input("🔍 Nhập từ khóa tại đây:", key="search_query")
        
    with col2:
        # Nút tìm kiếm chiếm 2 phần
        st.markdown("<br>", unsafe_allow_html=True) # Căn chỉnh cho bằng với ô chữ
        search_btn = st.button("🔍 Tìm", use_container_width=True)
        
    with col3:
        # Nút xóa chiếm 2 phần
        st.markdown("<br>", unsafe_allow_html=True)
        clear_btn = st.button("❌ Xóa", on_click=clear_text, use_container_width=True)
    
    # Chỉ tiến hành quét dữ liệu khi ô tìm kiếm có chữ
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
                st.markdown(f"### KẾT QUẢ {i} (Khớp {res['score']}%)")
                st.markdown(f"**❓ Câu hỏi:** {res['question']}")
                st.markdown(f"**📋 Phương án:**\n{res['options']}")
                st.markdown(f"**✅ ĐÁP ÁN ĐÚNG:** <span style='color:red; font-size:18px; font-weight:bold;'>{res['answer']}</span>", unsafe_allow_html=True)
                st.divider()