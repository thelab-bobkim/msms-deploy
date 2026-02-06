import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

DB = "msms.db"

st.set_page_config(
    layout="wide", 
    page_title="MSMS 2026 - 유지보수 관리 시스템", 
    page_icon="🏢",
    initial_sidebar_state="collapsed"  # 모바일에서 사이드바 기본 접기
)

# 모바일 viewport 메타 태그 추가 (줌 허용)
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
""", unsafe_allow_html=True)

# 사이드바 폭 설정 (반응형)
st.markdown("""
<style>
    /* 데스크톱: 550px */
    @media (min-width: 1025px) {
        [data-testid='stSidebar'] { 
            min-width: 550px !important; 
            max-width: 550px !important; 
        }
        
        [data-testid='stSidebar'] > div:first-child {
            width: 550px !important;
        }
    }
    
    /* 태블릿: 350px */
    @media (min-width: 769px) and (max-width: 1024px) {
        [data-testid='stSidebar'] { 
            min-width: 350px !important; 
            max-width: 350px !important; 
        }
        
        [data-testid='stSidebar'] > div:first-child {
            width: 350px !important;
        }
    }
    
    /* 모바일: 전체 화면 오버레이 */
    @media (max-width: 768px) {
        /* 햄버거 메뉴 버튼 - 극단적으로 눈에 띄게 */
        [data-testid='stSidebarCollapsedControl'] {
            display: block !important;
            position: fixed !important;
            top: 0.5rem !important;
            left: 0.5rem !important;
            z-index: 9999999 !important;
            background: black !important;
            color: white !important;
            border-radius: 8px !important;
            width: 70px !important;
            height: 70px !important;
            padding: 0 !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6) !important;
            border: 5px solid #FFD700 !important;
            animation: pulse 2s infinite !important;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* 햄버거 아이콘 */
        [data-testid='stSidebarCollapsedControl'] svg {
            width: 32px !important;
            height: 32px !important;
            color: #FFD700 !important;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)) !important;
        }
        
        /* 사이드바 배경을 어둡게 */
        [data-testid='stSidebar'][aria-expanded='true'] {
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            width: 100% !important;
            height: 100vh !important;
            z-index: 999998 !important;
            background-color: #2c3e50 !important;
            overflow-y: auto !important;
        }
        
        [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
            width: 100% !important;
            background-color: #2c3e50 !important;
            padding-top: 5rem !important;
        }
        
        /* 사이드바 내부 텍스트와 라벨만 흰색으로 */
        [data-testid='stSidebar'] label,
        [data-testid='stSidebar'] p,
        [data-testid='stSidebar'] h1,
        [data-testid='stSidebar'] h2,
        [data-testid='stSidebar'] h3,
        [data-testid='stSidebar'] span {
            color: white !important;
        }
        
        /* 사이드바 입력 필드 스타일 */
        [data-testid='stSidebar'] input,
        [data-testid='stSidebar'] select {
            background: white !important;
            color: black !important;
        }
        
        /* 사이드바 버튼은 정상 작동하도록 */
        [data-testid='stSidebar'] button {
            cursor: pointer !important;
            pointer-events: auto !important;
        }
        
        /* 사이드바 닫기 버튼 (상단 X 버튼) - 금색으로 */
        [data-testid='stSidebar'] button[kind='header'] {
            background: black !important;
            color: #FFD700 !important;
            border-radius: 8px !important;
            width: 60px !important;
            height: 60px !important;
            padding: 0 !important;
            font-size: 2rem !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
            border: 4px solid #FFD700 !important;
            position: fixed !important;
            top: 0.5rem !important;
            right: 0.5rem !important;
            z-index: 9999999 !important;
        }
        
        /* 메인 컨텐츠 전체 너비 사용 */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 5rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* 앱 헤더 여백 */
        [data-testid='stAppViewContainer'] {
            padding-top: 3rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 커스텀 CSS (반응형 포함)
st.markdown("""
<style>
    /* 메인 헤더 */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    /* 모바일: 헤더 크기 축소 */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        text-align: center;
    }
    
    /* 모바일: 메트릭 카드 패딩 축소 */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem;
        }
    }
    
    /* 수익/손실 색상 */
    .profit { color: #2e7d32; font-weight: 700; }
    .loss { color: #c62828; font-weight: 700; }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        min-height: 44px;
        cursor: pointer !important;
        pointer-events: auto !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 폼 제출 버튼 강화 */
    button[type="submit"],
    button[kind="primary"],
    button[kind="secondary"] {
        cursor: pointer !important;
        pointer-events: auto !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    /* Primary 버튼 추가 스타일 */
    button[kind="primary"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    
    /* 모든 Streamlit 버튼이 클릭 가능하도록 */
    div[data-testid="stButton"] {
        pointer-events: auto !important;
        z-index: 1 !important;
    }
    
    /* 사이드바 스타일 개선 */
    [data-testid='stSidebar'] {
        background-color: #f8f9fa;
    }
    
    /* 셀렉트박스 스타일 */
    .stSelectbox label {
        font-weight: 600;
        color: #333;
    }
    
    /* 모바일: 입력 필드 크기 확대 */
    @media (max-width: 768px) {
        .stSelectbox select,
        .stTextInput input {
            font-size: 16px !important; /* iOS 확대 방지 */
            min-height: 44px !important; /* 터치 친화적 */
        }
    }
    
    /* 데이터프레임 헤더 */
    .stDataFrame thead tr th {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* 모바일: 데이터프레임 폰트 크기 조정 */
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 0.85rem !important;
        }
        
        .stDataFrame thead tr th {
            font-size: 0.9rem !important;
            padding: 0.5rem !important;
        }
    }
    
    /* 필터 섹션 제목 */
    h3 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 1rem;
    }
    
    /* 모바일: 제목 크기 조정 */
    @media (max-width: 768px) {
        h3 {
            font-size: 1.2rem;
        }
    }
    
    /* 프로젝트 카운트 */
    .stAlert {
        border-radius: 0.5rem;
        font-weight: 600;
    }
    
    /* 검색 입력창 */
    .stTextInput input {
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31,119,180,0.25);
    }
    
    /* 모바일: 컨텐츠 여백 조정 */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* 테이블 가로 스크롤 */
        .stDataFrame {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
        
        /* 컬럼 최소 너비 */
        .stDataFrame td, .stDataFrame th {
            white-space: nowrap !important;
            min-width: 80px !important;
        }
        
        /* 메트릭 그리드 2열 */
        [data-testid="column"] {
            min-width: 48% !important;
            flex: 1 1 48% !important;
        }
        
        /* 터치 친화적 크기 */
        a, button, .stButton>button, [data-testid="stCheckbox"] {
            min-height: 44px !important;
        }
        
        /* 입력 필드 터치 최적화 */
        input, select, textarea {
            font-size: 16px !important; /* iOS 확대 방지 */
        }
    }

</style>
""", unsafe_allow_html=True)

# 모바일 사이드바 개선: 닫기 버튼 추가
if 'mobile_script_added' not in st.session_state:
    st.session_state.mobile_script_added = True
    st.markdown("""
    <style>
    /* 모바일 사이드바 하단 닫기 버튼 */
    @media (max-width: 768px) {
        .mobile-close-sidebar {
            position: fixed !important;
            bottom: 1rem !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 9999999 !important;
            background: #1f77b4 !important;
            color: white !important;
            border: none !important;
            border-radius: 0.5rem !important;
            padding: 1rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            cursor: pointer !important;
            min-height: 44px !important;
            width: auto !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def get_db_connection():
    """데이터베이스 연결"""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def load_projects(search="", sales_person="", status="", year_filter=""):
    """프로젝트 목록 로드 (필터링 포함)"""
    conn = get_db_connection()
    
    query = """
    SELECT id, client, customer, name, sales_person, status, 
           contract_start, contract_end
    FROM projects 
    WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND (id LIKE ? OR client LIKE ? OR customer LIKE ? OR name LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term] * 4)
    
    if sales_person and sales_person != "전체":
        query += " AND sales_person = ?"
        params.append(sales_person)
    
    if status and status != "전체":
        query += " AND status = ?"
        params.append(status)
    
    # 연도 필터 추가
    if year_filter and year_filter != "전체":
        query += " AND id LIKE ?"
        params.append(f"%-{year_filter}")
    
    query += " ORDER BY id"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def get_sales_persons():
    """영업담당자 목록 가져오기"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT sales_person FROM projects WHERE sales_person IS NOT NULL ORDER BY sales_person")
    result = [row[0] for row in cursor.fetchall() if row[0]]
    conn.close()
    return result


def get_clients():
    """매출처 목록 가져오기"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT client FROM projects WHERE client IS NOT NULL AND client != '' ORDER BY client")
    result = [row[0] for row in cursor.fetchall() if row[0]]
    conn.close()
    return result


def get_customers():
    """고객사 목록 가져오기"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT customer FROM projects WHERE customer IS NOT NULL AND customer != '' ORDER BY customer")
    result = [row[0] for row in cursor.fetchall() if row[0]]
    conn.close()
    return result


def get_vendors():
    """협력업체 목록 가져오기"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM vendors ORDER BY name")
    result = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return result


def get_vendor_items(vendor_id):
    """특정 협력업체의 항목 목록 가져오기"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, item_name, default_cost 
        FROM vendor_items 
        WHERE vendor_id = ? 
        ORDER BY item_name
    """, (vendor_id,))
    result = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    return result


def search_vendors(query):
    """협력업체 검색 (자동완성용)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name FROM vendors 
        WHERE name LIKE ? 
        ORDER BY name 
        LIMIT 20
    """, (f"%{query}%",))
    result = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return result


def add_vendor(vendor_name):
    """새 협력업체 추가"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO vendors (name) VALUES (?)", (vendor_name,))
        conn.commit()
        vendor_id = cursor.lastrowid
        conn.close()
        return vendor_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def add_vendor_item(vendor_id, item_name, default_cost=0):
    """협력업체 항목 추가"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vendor_items (vendor_id, item_name, default_cost) 
            VALUES (?, ?, ?)
        """, (vendor_id, item_name, default_cost))
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def calculate_split_amounts(total_amount, split_method, start_date, end_date):
    """분할 방식에 따라 월별 금액 계산"""
    amounts = [0.0] * 12
    
    if not start_date or not end_date or total_amount == 0:
        return amounts
    
    start = datetime.strptime(start_date, "%Y-%m-%d") if isinstance(start_date, str) else start_date
    end = datetime.strptime(end_date, "%Y-%m-%d") if isinstance(end_date, str) else end_date
    
    if split_method == "full":  # 전액
        # 시작월에 전액
        month_idx = start.month - 1
        amounts[month_idx] = total_amount
    
    elif split_method == "monthly":  # 월할 (1/12)
        # 계약 기간 내 월수 계산
        months_diff = (end.year - start.year) * 12 + end.month - start.month + 1
        if months_diff > 0:
            monthly_amount = total_amount / months_diff
            current = start
            while current <= end and current.month <= 12:
                month_idx = current.month - 1
                amounts[month_idx] += monthly_amount
                current = current + relativedelta(months=1)
    
    elif split_method == "quarterly":  # 분기할 (1/4)
        quarterly_amount = total_amount / 4
        # 각 분기 시작월 (1, 4, 7, 10월)
        quarters = [0, 3, 6, 9]
        for q in quarters:
            if start.month - 1 <= q <= (end.month - 1 if end.year == start.year else 11):
                amounts[q] = quarterly_amount
    
    elif split_method == "semi_annual":  # 반기할 (1/2)
        semi_annual_amount = total_amount / 2
        # 상반기(1월), 하반기(7월)
        if start.month <= 6:
            amounts[0] = semi_annual_amount
        if end.month >= 7:
            amounts[6] = semi_annual_amount
    
    return amounts


def create_project(project_id, name, client, customer, sales_person, 
                  contract_start, contract_end, contract_amount, split_method, notes=""):
    """새 프로젝트 생성"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 월별 매출 자동 계산
        sales_amounts = calculate_split_amounts(contract_amount, split_method, contract_start, contract_end)
        
        cursor.execute('''
        INSERT INTO projects 
        (id, name, client, customer, sales_person, contract_start, contract_end, 
         contract_amount, split_method, status, notes,
         sales_jan, sales_feb, sales_mar, sales_apr, sales_may, sales_jun,
         sales_jul, sales_aug, sales_sep, sales_oct, sales_nov, sales_dec)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id, name, client, customer, sales_person, 
            contract_start, contract_end, contract_amount, split_method, notes,
            *sales_amounts
        ))
        
        conn.commit()
        return True, "프로젝트가 성공적으로 생성되었습니다!"
    except sqlite3.IntegrityError:
        return False, f"프로젝트 ID '{project_id}'가 이미 존재합니다."
    except Exception as e:
        return False, f"오류 발생: {str(e)}"
    finally:
        conn.close()


def update_project_contract(project_id, contract_start, contract_end, contract_amount, split_method):
    """프로젝트 계약 정보 업데이트 (계약기간 포함)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        sales_amounts = calculate_split_amounts(contract_amount, split_method, contract_start, contract_end)
        
        cursor.execute('''
        UPDATE projects SET
            contract_start = ?,
            contract_end = ?,
            contract_amount = ?,
            split_method = ?,
            sales_jan = ?, sales_feb = ?, sales_mar = ?, sales_apr = ?,
            sales_may = ?, sales_jun = ?, sales_jul = ?, sales_aug = ?,
            sales_sep = ?, sales_oct = ?, sales_nov = ?, sales_dec = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (contract_start, contract_end, contract_amount, split_method, *sales_amounts, project_id))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"업데이트 오류: {e}")
        return False
    finally:
        conn.close()


def update_project_sales(project_id, contract_amount, split_method, contract_start, contract_end):
    """프로젝트 매출 업데이트 (기존 호환용)"""
    return update_project_contract(project_id, contract_start, contract_end, contract_amount, split_method)


def load_project_detail(project_id):
    """프로젝트 상세 정보 로드"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    
    if not project:
        conn.close()
        return None, []
    
    cursor.execute("SELECT * FROM purchases WHERE project_id = ? ORDER BY id", (project_id,))
    purchases = cursor.fetchall()
    
    conn.close()
    return dict(project), [dict(p) for p in purchases]


def update_project_purchases(project_id, purchases_data):
    """프로젝트 구매 데이터 업데이트"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 기존 구매 삭제
        cursor.execute("DELETE FROM purchases WHERE project_id = ?", (project_id,))
        
        # 새 구매 데이터 삽입
        for purchase in purchases_data:
            cursor.execute('''
            INSERT INTO purchases 
            (project_id, vendor, item, is_bundle,
             cost_jan, cost_feb, cost_mar, cost_apr, cost_may, cost_jun,
             cost_jul, cost_aug, cost_sep, cost_oct, cost_nov, cost_dec)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                purchase['vendor'],
                purchase['item'],
                1 if purchase['is_bundle'] else 0,
                *([purchase['cost']] * 12)
            ))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"구매 데이터 업데이트 오류: {e}")
        return False
    finally:
        conn.close()


# ====== 사이드바 ======
with st.sidebar:
    st.markdown("## 🏢 프로젝트 포트폴리오")
    
    # 프로젝트 추가 버튼
    if st.button("➕ 새 프로젝트 등록", type="primary", use_container_width=True):
        st.session_state['show_create_form'] = True
        st.session_state['selected_project'] = None
    
    st.markdown("---")
    
    # 필터
    st.markdown("### 🔍 필터")
    
    # 연도 필터 (상단에 강조)
    year_options = ["전체", "2024", "2025", "2026"]
    filter_year = st.selectbox(
        "📅 연도",
        year_options,
        key="filter_year",
        help="프로젝트 ID에서 연도를 추출합니다 (예: M032-2025 → 2025년)"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        sales_persons = ["전체"] + get_sales_persons()
        filter_sales = st.selectbox("👤 영업담당자", sales_persons, key="filter_sales")
    
    with col2:
        filter_status = st.selectbox(
            "📊 상태",
            ["전체", "active", "completed", "cancelled"],
            format_func=lambda x: {
                "전체": "전체", 
                "active": "진행중", 
                "completed": "완료", 
                "cancelled": "취소"
            }.get(x, x),
            key="filter_status"
        )
    
    # 검색
    search_term = st.text_input("🔍 검색", placeholder="프로젝트, 클라이언트, 고객사...")
    
    # 프로젝트 목록 로드
    projects_df = load_projects(
        search_term, 
        filter_sales if filter_sales != "전체" else "",
        filter_status if filter_status != "전체" else "",
        filter_year if filter_year != "전체" else ""
    )
    
    st.info(f"📁 총 {len(projects_df)}개 프로젝트")
    
    if not projects_df.empty:
        # 한글 컬럼명으로 변경
        display_df = projects_df.copy()
        display_df['상태'] = display_df['status'].map({
            'active': '✅ 진행중',
            'completed': '✔️ 완료', 
            'cancelled': '❌ 취소'
        })
        
        display_df = display_df[['id', 'sales_person', 'client', 'customer', 'name', '상태']].rename(columns={
            'id': 'ID',
            'sales_person': '영업담당자',
            'client': '매출처',
            'customer': '고객사',
            'name': '프로젝트명'
        })
        
        # 데이터프레임 표시 (클릭 가능)
        event = st.dataframe(
            display_df,
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
            use_container_width=True,
            height=600
        )
        
        # 프로젝트 선택 처리
        sel_id = None
        if event.selection and event.selection.rows:
            selected_row_idx = event.selection.rows[0]
            sel_id = projects_df.iloc[selected_row_idx]["id"]
            st.session_state['selected_project'] = sel_id
            st.session_state['show_create_form'] = False
    else:
        st.warning("프로젝트가 없습니다")
        sel_id = None
    
    # 모바일 사이드바 하단 닫기 버튼 (모바일에서만 표시)
    st.markdown("---")
    
    # 모바일에서만 표시되는 닫기 버튼
    st.markdown("""
    <style>
    /* 데스크톱에서는 닫기 버튼 숨김 */
    .mobile-close-button {
        display: none;
    }
    
    /* 모바일에서만 표시 */
    @media (max-width: 768px) {
        .mobile-close-button {
            display: block !important;
        }
    }
    </style>
    
    <div class='mobile-close-button' style='margin: 2rem 0; text-align: center;'>
        <h3 style='color: #FFD700; text-align: center; margin-bottom: 1rem;'>👇 여기를 눌러 닫기</h3>
        <button 
            id='closeSidebarBtn'
            style='
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                color: black;
                border: 5px solid black;
                border-radius: 15px;
                padding: 2rem;
                font-size: 1.5rem;
                font-weight: 900;
                width: 100%;
                min-height: 80px;
                cursor: pointer;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
                text-transform: uppercase;
                letter-spacing: 2px;
            '
        >
            ✕ 필터 닫기 ✕
        </button>
    </div>
    
    <script>
    // 닫기 버튼 클릭 이벤트
    (function() {
        const btn = document.getElementById('closeSidebarBtn');
        if (btn) {
            btn.onclick = function() {
                const hamburger = document.querySelector('[data-testid="stSidebarCollapsedControl"]');
                if (hamburger) {
                    hamburger.click();
                }
            };
        }
    })();
    </script>
    """, unsafe_allow_html=True)


# ====== 메인 영역 ======

# 프로젝트 등록 폼
if st.session_state.get('show_create_form', False):
    st.markdown("<div class='main-header'>📝 새 프로젝트 등록</div>", unsafe_allow_html=True)
    
    with st.form("create_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. ID
            new_id = st.text_input("*프로젝트 ID", placeholder="예: PROJ001")
            
            # 2. 영업담당자 (드롭다운 + 직접 입력)
            existing_sales_persons = get_sales_persons()
            if existing_sales_persons:
                sales_option = st.radio(
                    "*영업담당자",
                    ["기존 선택", "새로 입력"],
                    horizontal=True,
                    key="sales_option"
                )
                
                if sales_option == "기존 선택":
                    new_sales_person = st.selectbox(
                        "담당자 선택",
                        existing_sales_persons,
                        key="sales_select"
                    )
                else:
                    new_sales_person = st.text_input("담당자 입력", placeholder="예: 홍길동", key="sales_input")
            else:
                new_sales_person = st.text_input("*영업담당자", placeholder="예: 홍길동")
            
            # 3. 매출처 (DB에서 드롭다운)
            existing_clients = get_clients()
            if existing_clients:
                client_option = st.radio(
                    "*매출처",
                    ["DB에서 선택", "새로 입력"],
                    horizontal=True,
                    key="client_option"
                )
                
                if client_option == "DB에서 선택":
                    new_client = st.selectbox(
                        "매출처 선택",
                        existing_clients,
                        key="client_select"
                    )
                else:
                    new_client = st.text_input("매출처 입력", placeholder="예: ㈜바인스랩", key="client_input")
            else:
                new_client = st.text_input("*매출처", placeholder="예: ㈜바인스랩")
            
            # 4. 고객사 (DB에서 드롭다운)
            existing_customers = get_customers()
            if existing_customers:
                customer_option = st.radio(
                    "고객사",
                    ["DB에서 선택", "새로 입력"],
                    horizontal=True,
                    key="customer_option"
                )
                
                if customer_option == "DB에서 선택":
                    new_customer = st.selectbox(
                        "고객사 선택",
                        existing_customers,
                        key="customer_select"
                    )
                else:
                    new_customer = st.text_input("고객사 입력", placeholder="예: 한일병원", key="customer_input")
            else:
                new_customer = st.text_input("고객사", placeholder="예: 한일병원")
            
            # 5. 프로젝트명
            new_name = st.text_input("*프로젝트명", placeholder="예: XX시스템 유지보수")
        
        with col2:
            new_contract_start = st.date_input("*계약 시작일", value=datetime.now())
            new_contract_end = st.date_input("*계약 종료일", value=datetime.now() + timedelta(days=365))
            new_contract_amount = st.number_input("*계약 금액 (원)", min_value=0.0, step=1000000.0, format="%.0f")
            new_split_method = st.selectbox(
                "*분할 방식",
                ["monthly", "quarterly", "semi_annual", "full"],
                format_func=lambda x: {
                    "monthly": "월할 (1/12)",
                    "quarterly": "분기할 (1/4)",
                    "semi_annual": "반기할 (1/2)",
                    "full": "전액"
                }[x]
            )
            new_notes = st.text_area("비고", placeholder="추가 메모...")
        
        col_btn1, col_btn2 = st.columns([1, 5])
        
        with col_btn1:
            submit = st.form_submit_button("✅ 등록", type="primary")
        
        with col_btn2:
            cancel = st.form_submit_button("❌ 취소")
        
        if submit:
            if not all([new_id, new_name, new_client, new_sales_person]):
                st.error("필수 항목(*) 을 모두 입력해주세요!")
            else:
                success, message = create_project(
                    new_id, new_name, new_client, new_customer, new_sales_person,
                    new_contract_start.strftime("%Y-%m-%d"),
                    new_contract_end.strftime("%Y-%m-%d"),
                    new_contract_amount, new_split_method, new_notes
                )
                
                if success:
                    st.success(message)
                    st.session_state['show_create_form'] = False
                    st.session_state['selected_project'] = new_id
                    st.rerun()
                else:
                    st.error(message)
        
        if cancel:
            st.session_state['show_create_form'] = False
            st.rerun()

# 프로젝트 상세
elif st.session_state.get('selected_project'):
    sel_id = st.session_state['selected_project']
    project, purchases = load_project_detail(sel_id)
    
    if project:
        # 헤더
        col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
        
        with col_h1:
            status_emoji = {'active': '✅', 'completed': '✔️', 'cancelled': '❌'}
            st.markdown(f"<div class='main-header'>{status_emoji.get(project.get('status', 'active'), '')} {project['name']}</div>", unsafe_allow_html=True)
        
        with col_h2:
            st.markdown(f"**👤 담당자:** {project.get('sales_person', '-')}")
        
        with col_h3:
            st.markdown(f"**📅 계약기간:** {project.get('contract_start', '-')[:7] if project.get('contract_start') else '-'} ~ {project.get('contract_end', '-')[:7] if project.get('contract_end') else '-'}")
        
        st.markdown("---")
        
        # 월 컬럼
        month_names = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
        month_fields = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        
        # 매출 데이터
        sales_values = [project[f'sales_{m}'] for m in month_fields]
        
        # 비용 데이터 계산
        total_costs = np.zeros(12)
        cost_rows = []
        cost_idx = []
        
        for purchase in purchases:
            cost_values = [purchase[f'cost_{m}'] for m in month_fields]
            is_bundle = purchase['is_bundle']
            
            if not is_bundle:
                total_costs += np.array(cost_values)
            
            cost_rows.append(cost_values)
            bundle_mark = '[일괄적용] ' if is_bundle else ''
            cost_idx.append(f"{bundle_mark}{purchase['vendor']} - {purchase['item']}")
        
        # 순이익 계산
        profit = np.array(sales_values) - total_costs
        margin = (profit.sum() / sum(sales_values) * 100) if sum(sales_values) > 0 else 0
        
        # 연간 요약
        st.markdown("### 📈 연간 요약")
        c1, c2, c3, c4 = st.columns(4)
        
        c1.metric("💰 연간 매출", f"₩{sum(sales_values):,.0f}")
        c2.metric("🛒 연간 매입 (순수)", f"₩{total_costs.sum():,.0f}")
        c3.metric(
            f"💵 순이익 (마진 {margin:.1f}%)",
            f"₩{profit.sum():,.0f}",
            delta_color="normal" if profit.sum() >= 0 else "inverse"
        )
        c4.metric("📊 프로젝트 상태", 
                 {"active": "진행중", "completed": "완료", "cancelled": "취소"}.get(project.get('status', 'active'), '알수없음'))
        
        st.markdown("---")
        
        # 탭으로 구성 (프로젝트 계약기간 탭 추가)
        tab1, tab2, tab_contract, tab3, tab4 = st.tabs(["📊 월별 상세", "📅 분기별 요약", "📅 프로젝트 계약기간", "⚙️ 관리 콘솔", "ℹ️ 프로젝트 정보"])
        
        with tab1:
            # 월별 매출
            st.markdown("#### 💰 월별 매출")
            st.dataframe(
                pd.DataFrame([sales_values], columns=month_names, index=["매출"]).style.format("₩{:,.0f}"),
                use_container_width=True
            )
            
            # 월별 매입
            st.markdown("#### 🛒 월별 매입")
            if cost_rows:
                # 매입 데이터프레임 생성
                purchase_df = pd.DataFrame(cost_rows, columns=month_names, index=cost_idx)
                
                # 매입처와 품목을 분리하여 더 명확하게 표시
                st.markdown("**매입처별 상세:**")
                for i, (idx_label, cost_row) in enumerate(zip(cost_idx, cost_rows)):
                    with st.expander(f"📦 {idx_label}", expanded=False):
                        # 월별 매입 금액 표시
                        purchase_detail_df = pd.DataFrame([cost_row], columns=month_names, index=["매입 금액"])
                        st.dataframe(
                            purchase_detail_df.style.format("₩{:,.0f}"),
                            use_container_width=True
                        )
                        # 합계 표시
                        total = sum(cost_row)
                        st.markdown(f"**연간 합계:** ₩{total:,.0f}")
                
                # 전체 매입 합계 테이블
                st.markdown("---")
                st.markdown("**📊 전체 매입 요약 (일괄적용 제외):**")
                total_purchase_row = [total_costs[i] for i in range(12)]
                total_df = pd.DataFrame([total_purchase_row], columns=month_names, index=["총 매입"])
                st.dataframe(
                    total_df.style.format("₩{:,.0f}"),
                    use_container_width=True
                )
            else:
                st.info("매입 데이터가 없습니다")
            
            # 월별 순이익
            st.markdown("#### 💵 월별 순이익")
            
            def color_profit(val):
                try:
                    v = float(str(val).replace('₩', '').replace(',', ''))
                    return 'color: #2e7d32; font-weight: 700' if v >= 0 else 'color: #c62828; font-weight: 700'
                except:
                    return ''
            
            profit_df = pd.DataFrame([list(profit)], columns=month_names, index=["순이익"])
            st.dataframe(
                profit_df.style.format("₩{:,.0f}").map(color_profit),
                use_container_width=True
            )
        
        with tab2:
            st.markdown("#### 📅 분기별 요약")
            q_vals = [
                profit[0:3].sum(),
                profit[3:6].sum(),
                profit[6:9].sum(),
                profit[9:12].sum()
            ]
            qc1, qc2, qc3, qc4, qc5 = st.columns(5)
            qc1.metric("1분기", f"₩{q_vals[0]:,.0f}")
            qc2.metric("2분기", f"₩{q_vals[1]:,.0f}")
            qc3.metric("3분기", f"₩{q_vals[2]:,.0f}")
            qc4.metric("4분기", f"₩{q_vals[3]:,.0f}")
            qc5.metric("연간 합계", f"₩{profit.sum():,.0f}")
        
        # 새로운 프로젝트 계약기간 탭
        with tab_contract:
            st.markdown("### 📅 프로젝트 계약기간 관리")
            st.info("💡 계약 시작일, 종료일, 금액, 분할 방식을 수정하면 월별 매출이 자동으로 재계산됩니다.")
            
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                # 계약 시작일
                current_start = project.get('contract_start', '')
                if current_start:
                    from datetime import datetime as dt
                    current_start_date = dt.strptime(current_start, "%Y-%m-%d").date()
                else:
                    current_start_date = datetime.now().date()
                
                edit_contract_start = st.date_input(
                    "*계약 시작일",
                    value=current_start_date,
                    key="edit_contract_start",
                    help="계약 시작 날짜를 선택하세요"
                )
                
                # 계약 금액
                edit_amount = st.number_input(
                    "*계약 금액 (원)",
                    value=float(project.get('contract_amount', sum(sales_values))),
                    step=1000000.0,
                    format="%.0f",
                    key="edit_amount",
                    help="총 계약 금액을 입력하세요"
                )
            
            with col_c2:
                # 계약 종료일
                current_end = project.get('contract_end', '')
                if current_end:
                    from datetime import datetime as dt
                    current_end_date = dt.strptime(current_end, "%Y-%m-%d").date()
                else:
                    current_end_date = (datetime.now() + timedelta(days=365)).date()
                
                edit_contract_end = st.date_input(
                    "*계약 종료일",
                    value=current_end_date,
                    key="edit_contract_end",
                    help="계약 종료 날짜를 선택하세요"
                )
                
                # 분할 방식
                edit_split = st.selectbox(
                    "*분할 방식",
                    ["monthly", "quarterly", "semi_annual", "full"],
                    index=["monthly", "quarterly", "semi_annual", "full"].index(project.get('split_method', 'monthly')),
                    format_func=lambda x: {
                        "monthly": "월할 (1/12)",
                        "quarterly": "분기할 (1/4)",
                        "semi_annual": "반기할 (1/2)",
                        "full": "전액"
                    }[x],
                    key="edit_split",
                    help="매출 분할 방식을 선택하세요"
                )
            
            # 계약 기간 정보 표시
            st.markdown("---")
            st.markdown("#### 📋 현재 계약 정보")
            
            info_col1, info_col2, info_col3 = st.columns(3)
            info_col1.metric("계약 시작일", edit_contract_start.strftime("%Y년 %m월 %d일"))
            info_col2.metric("계약 종료일", edit_contract_end.strftime("%Y년 %m월 %d일"))
            
            # 계약 기간 계산
            contract_days = (edit_contract_end - edit_contract_start).days
            contract_months = contract_days / 30.44  # 평균 월 일수
            info_col3.metric("계약 기간", f"{int(contract_months)}개월 ({contract_days}일)")
            
            st.markdown("---")
            
            # 저장 버튼
            col_btn1, col_btn2 = st.columns([3, 1])
            
            with col_btn1:
                if st.button("💾 계약 정보 저장 및 매출 재계산", type="primary", use_container_width=True):
                    if update_project_contract(
                        sel_id,
                        edit_contract_start.strftime("%Y-%m-%d"),
                        edit_contract_end.strftime("%Y-%m-%d"),
                        edit_amount,
                        edit_split
                    ):
                        st.success("✅ 계약 정보가 저장되고 매출이 재계산되었습니다!")
                        st.rerun()
            
            with col_btn2:
                if st.button("🔄 초기화", use_container_width=True):
                    st.rerun()
        
        with tab3:
            st.warning("⚠️ 변경사항은 저장 버튼을 눌러야 적용됩니다")
            
            st.markdown("---")
            
            # 구매 항목 관리
            st.markdown("#### 🛒 구매 항목 관리")
            
            if purchases:
                st.info("💡 삭제하려는 항목을 체크하고 '🗑️ 선택 항목 삭제' 버튼을 클릭하세요")
            
            # 협력업체 목록 로드
            vendors_list = get_vendors()  # [(id, name), ...]
            vendors_dict = {name: vid for vid, name in vendors_list}
            vendor_names = [name for _, name in vendors_list]
            
            # 삭제할 항목 추적
            items_to_delete = []
            updated_purchases = []
            
            for i, purchase in enumerate(purchases):
                # 체크박스를 포함한 expander
                col_check, col_expand = st.columns([0.5, 9.5])
                
                with col_check:
                    delete_check = st.checkbox("", key=f"delete_{i}", label_visibility="collapsed")
                    if delete_check:
                        items_to_delete.append(i)
                
                with col_expand:
                    with st.expander(f"📦 {purchase['vendor']} - {purchase['item']}"):
                        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                        
                        # 협력업체 선택/입력
                        current_vendor = purchase['vendor']
                        if current_vendor in vendor_names:
                            vendor_idx = vendor_names.index(current_vendor)
                        else:
                            vendor_idx = 0
                        
                        with col1:
                            vendor_option = st.radio(
                                "협력업체 선택 방식",
                                ["DB에서 선택", "직접 입력"],
                                horizontal=True,
                                key=f"vendor_opt_{i}"
                            )
                            
                            if vendor_option == "DB에서 선택":
                                vn = st.selectbox(
                                    "협력업체",
                                    vendor_names,
                                    index=vendor_idx,
                                    key=f"v{i}"
                                )
                            else:
                                vn = st.text_input(
                                    "협력업체 (직접 입력)",
                                    current_vendor,
                                    key=f"v_text_{i}"
                                )
                        
                        with col2:
                            # 선택한 협력업체의 항목 로드
                            if vendor_option == "DB에서 선택" and vn in vendors_dict:
                                vendor_id = vendors_dict[vn]
                                items_list = get_vendor_items(vendor_id)  # [(id, name, cost), ...]
                                item_names = [name for _, name, _ in items_list]
                                
                                if item_names:
                                    current_item = purchase['item']
                                    if current_item in item_names:
                                        item_idx = item_names.index(current_item)
                                    else:
                                        item_idx = 0
                                    
                                    vi = st.selectbox(
                                        "항목",
                                        item_names,
                                        index=item_idx,
                                        key=f"i{i}"
                                    )
                                    
                                    # 선택한 항목의 기본 비용 가져오기
                                    selected_item_data = next((item for item in items_list if item[1] == vi), None)
                                    if selected_item_data:
                                        default_cost = selected_item_data[2]
                                    else:
                                        default_cost = float(purchase[f'cost_jan'])
                                else:
                                    vi = st.text_input("항목 (직접 입력)", purchase['item'], key=f"i_text_{i}")
                                    default_cost = float(purchase[f'cost_jan'])
                            else:
                                vi = st.text_input("항목", purchase['item'], key=f"i{i}")
                                default_cost = float(purchase[f'cost_jan'])
                        
                        vp = col3.number_input(
                            "월 비용",
                            value=float(purchase[f'cost_jan']),
                            key=f"p{i}",
                            step=100000.0,
                            format="%.0f"
                        )
                        isb = col4.checkbox("일괄적용", value=bool(purchase['is_bundle']), key=f"b{i}")
                        
                        # 삭제 체크되지 않은 항목만 추가
                        if i not in items_to_delete:
                            updated_purchases.append({
                                'vendor': vn,
                                'item': vi,
                                'cost': vp,
                                'is_bundle': isb
                            })
            
            # 새 구매 항목 추가
            st.markdown("**➕ 새 구매 항목 추가**")
            
            # 협력업체 목록 (새 항목용)
            vendors_list = get_vendors()
            vendors_dict = {name: vid for vid, name in vendors_list}
            vendor_names = [name for _, name in vendors_list]
            
            new_col1, new_col2, new_col3, new_col4 = st.columns([2, 2, 1, 1])
            
            with new_col1:
                new_vendor_option = st.radio(
                    "협력업체 선택",
                    ["DB에서 선택", "새로 입력"],
                    horizontal=True,
                    key="new_vendor_opt"
                )
                
                if new_vendor_option == "DB에서 선택":
                    if vendor_names:
                        new_vendor = st.selectbox(
                            "협력업체",
                            vendor_names,
                            key="new_v"
                        )
                    else:
                        st.warning("DB에 협력업체가 없습니다. 새로 입력해주세요.")
                        new_vendor = st.text_input("협력업체 (직접 입력)", key="new_v_text", placeholder="예: ㈜공급업체")
                else:
                    new_vendor = st.text_input("협력업체 (새로 입력)", key="new_v_text2", placeholder="예: ㈜공급업체")
            
            with new_col2:
                # 선택한 협력업체의 항목 로드
                if new_vendor_option == "DB에서 선택" and vendor_names and new_vendor in vendors_dict:
                    vendor_id = vendors_dict[new_vendor]
                    items_list = get_vendor_items(vendor_id)
                    item_names = [name for _, name, _ in items_list]
                    
                    if item_names:
                        item_option = st.radio(
                            "항목 선택",
                            ["DB에서 선택", "새로 입력"],
                            horizontal=True,
                            key="new_item_opt"
                        )
                        
                        if item_option == "DB에서 선택":
                            selected_item_name = st.selectbox(
                                "항목",
                                item_names,
                                key="new_i"
                            )
                            # 선택한 항목의 기본 비용 가져오기
                            selected_item = next((item for item in items_list if item[1] == selected_item_name), None)
                            default_new_cost = float(selected_item[2]) if selected_item else 0.0
                            new_item = selected_item_name
                        else:
                            new_item = st.text_input("항목 (새로 입력)", key="new_i_text", placeholder="예: 서버 호스팅")
                            default_new_cost = 0.0
                    else:
                        new_item = st.text_input("항목 (직접 입력)", key="new_i_text2", placeholder="예: 서버 호스팅")
                        default_new_cost = 0.0
                else:
                    new_item = st.text_input("항목", key="new_i_fallback", placeholder="예: 서버 호스팅")
                    default_new_cost = 0.0
            
            new_cost = new_col3.number_input(
                "월 비용",
                value=default_new_cost,
                key="new_p",
                step=100000.0,
                format="%.0f"
            )
            new_bundle = new_col4.checkbox("일괄적용", key="new_b")
            
            col_save1, col_save2, col_save3 = st.columns([1, 1, 2])
            
            with col_save1:
                if st.button("➕ 추가 후 저장", type="primary"):
                    if new_vendor and new_item and new_cost > 0:
                        updated_purchases.append({
                            'vendor': new_vendor,
                            'item': new_item,
                            'cost': new_cost,
                            'is_bundle': new_bundle
                        })
                    
                    if update_project_purchases(sel_id, updated_purchases):
                        st.success("✅ 저장 완료!")
                        st.rerun()
            
            with col_save2:
                if st.button("💾 현재 항목만 저장"):
                    if update_project_purchases(sel_id, updated_purchases):
                        st.success("✅ 저장 완료!")
                        st.rerun()
            
            with col_save3:
                if items_to_delete:
                    if st.button(f"🗑️ 선택 항목 삭제 ({len(items_to_delete)}개)", type="secondary", use_container_width=True):
                        # 삭제할 항목을 제외한 나머지만 저장
                        if update_project_purchases(sel_id, updated_purchases):
                            st.success(f"✅ {len(items_to_delete)}개 항목이 삭제되었습니다!")
                            st.rerun()
        
        with tab4:
            st.markdown("#### ℹ️ 프로젝트 기본 정보")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"**프로젝트 ID:** {project['id']}")
                st.markdown(f"**프로젝트명:** {project['name']}")
                st.markdown(f"**클라이언트:** {project.get('client', '-')}")
                st.markdown(f"**고객사:** {project.get('customer', '-')}")
                st.markdown(f"**영업담당자:** {project.get('sales_person', '-')}")
            
            with info_col2:
                st.markdown(f"**계약 시작일:** {project.get('contract_start', '-')}")
                st.markdown(f"**계약 종료일:** {project.get('contract_end', '-')}")
                st.markdown(f"**계약 금액:** ₩{project.get('contract_amount', 0):,.0f}")
                split_methods = {'monthly': '월할 (1/12)', 'quarterly': '분기할 (1/4)', 'semi_annual': '반기할 (1/2)', 'full': '전액'}
                st.markdown(f"**분할 방식:** {split_methods.get(project.get('split_method', 'monthly'), '-')}")
                status_map = {'active': '진행중', 'completed': '완료', 'cancelled': '취소'}
                st.markdown(f"**상태:** {status_map.get(project.get('status', 'active'), '알수없음')}")
            
            if project.get('notes'):
                st.markdown("**📝 비고:**")
                st.info(project['notes'])

# 홈 화면 - 전체 통계
else:
    st.markdown("<div class='main-header'>🏢 MSMS 2026 - 유지보수 서비스 관리 시스템</div>", unsafe_allow_html=True)
    st.markdown("### SQLite Edition - 향상된 성능 및 안정성")
    
    conn = get_db_connection()
    
    # 전체 통계
    col1, col2, col3, col4 = st.columns(4)
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'active'")
    active_projects = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT SUM(sales_jan + sales_feb + sales_mar + sales_apr + 
                   sales_may + sales_jun + sales_jul + sales_aug + 
                   sales_sep + sales_oct + sales_nov + sales_dec) 
        FROM projects
    """)
    total_revenue = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT SUM(cost_jan + cost_feb + cost_mar + cost_apr + 
                   cost_may + cost_jun + cost_jul + cost_aug + 
                   cost_sep + cost_oct + cost_nov + cost_dec) 
        FROM purchases WHERE is_bundle = 0
    """)
    total_cost = cursor.fetchone()[0] or 0
    
    conn.close()
    
    col1.metric("📁 전체 프로젝트", f"{total_projects:,}개")
    col2.metric("✅ 진행중", f"{active_projects:,}개")
    col3.metric("💰 총 매출", f"₩{total_revenue:,.0f}")
    col4.metric("💸 총 비용", f"₩{total_cost:,.0f}")
    
    st.markdown("---")
    st.info("👈 **왼쪽 사이드바에서 프로젝트를 선택하거나 새 프로젝트를 등록하세요**")
    
    st.markdown("### 🎯 주요 기능")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **✅ 데이터 관리**
        - SQLite 데이터베이스 - 빠르고 안정적
        - 실시간 업데이트 - 변경사항 즉시 반영
        - 자동 백업 - JSON 백업 자동 생성
        
        **✅ 프로젝트 관리**
        - 프로젝트 생성 및 수정
        - 계약 기간 및 금액 관리
        - 자동 분할 계산 (월할/분기할/반기할/전액)
        """)
    
    with feature_col2:
        st.markdown("""
        **✅ 원가 관리**
        - 구매 항목 등록 및 관리
        - 일괄적용 항목 구분
        - 월별 순이익 자동 계산
        
        **✅ 검색 및 필터**
        - 통합 검색 기능
        - 영업담당자별 필터링
        - 프로젝트 상태별 조회
        """)
    
    st.markdown("---")
    
    # 엑셀 Import 기능
    st.markdown("### 📄 일괄 등록 (엑셀 Import)")
    st.info("💡 **일괄 등록 기능이란?** 엑셀 파일에서 여러 프로젝트를 한 번에 등록하는 기능입니다. 수동 입력 대신 엑셀 파일을 업로드하면 자동으로 DB에 저장됩니다.")
    
    with st.expander("📂 엑셀 파일 업로드", expanded=False):
        st.markdown("""
        **엑셀 파일 형식 요구사항:**
        - 시트명: `계약 현황`
        - 필수 컬럼: `코드번호`, `매출처`, `사업명`, `총 계약금액(매출)`, `계약시작일`, `계약만료일`
        - 선택 컬럼: `영업대표`, `청구형태`, `월별 매출 데이터`
        
        **주요 기능:**
        - 프로젝트 자동 등록
        - 월별 매출 데이터 반영
        - 2026년 연장 프로젝트 자동 표시
        - 기존 프로젝트 데이터 업데이트
        """)
        
        uploaded_file = st.file_uploader(
            "엑셀 파일 선택 (.xlsx)",
            type=['xlsx'],
            help="2025_data1.xlsx 형식의 파일을 업로드하세요"
        )
        
        if uploaded_file:
            st.success(f"✅ 파일 선택: {uploaded_file.name}")
            
            col_import1, col_import2 = st.columns([1, 3])
            
            with col_import1:
                if st.button("🚀 Import 실행", type="primary", use_container_width=True):
                    # Import 함수 호출
                    from excel_import import import_excel_to_db
                    
                    progress_placeholder = st.empty()
                    message_placeholder = st.empty()
                    
                    def show_progress(msg):
                        progress_placeholder.info(f"🔄 {msg}")
                    
                    # Import 실행
                    results = import_excel_to_db(uploaded_file, show_progress)
                    
                    # 결과 표시
                    progress_placeholder.empty()
                    
                    if results['success'] > 0:
                        st.success(f"✅ Import 완료: {results['success']}개 프로젝트 처리")
                    
                    if results['messages']:
                        with st.expander("📊 상세 결과", expanded=True):
                            for msg in results['messages']:
                                st.write(msg)
                    
                    # 새로고침
                    st.rerun()
            
            with col_import2:
                st.warning("⚠️ 기존 데이터와 코드번호가 같으면 덮어쓰기됩니다.")
    
    st.markdown("---")
    st.success("💡 **처음 사용하시나요?** '➕ 새 프로젝트 등록' 버튼을 누르거나, 엑셀 파일을 업로드하여 일괄 등록하세요!")
