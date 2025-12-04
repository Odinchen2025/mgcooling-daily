import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import urllib.parse
import time

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="MGCooling 市場情報日報",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS 美化 (Apple 風格移植版) ---
st.markdown("""
<style>
    /* 全局設定 */
    .stApp {
        background-color: #F5F5F7;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 標題樣式 */
    h1 {
        color: #1D1D1F;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }
    h3, h4 {
        color: #1D1D1F;
        font-weight: 600 !important;
    }
    
    /* 連結樣式 */
    a {
        text-decoration: none !important;
        color: #0066CC !important;
        font-weight: 500;
        transition: opacity 0.2s;
    }
    a:hover {
        opacity: 0.7;
    }

    /* 新聞卡片設計 */
    .news-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    }
    
    /* 分類標籤 Header */
    .category-header {
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        font-size: 0.95rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 側邊欄美化 */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-right: 1px solid #E5E5E5;
    }

    /* --- 列印模式 (Print/PDF) --- */
    @media print {
        /* 隱藏非內容元素 */
        section[data-testid="stSidebar"], 
        header, 
        .stButton, 
        footer, 
        #MainMenu, 
        .print-hide {
            display: none !important;
        }
        
        /* 調整版面 */
        .stApp {
            background-color: white !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* 確保背景色塊被列印 */
        .category-header {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        
        /* 防止卡片被切斷 */
        .news-card {
            break-inside: avoid;
            box-shadow: none;
            border: 1px solid #ccc;
        }
        
        /* 隱藏連結網址顯示 */
        a[href]:after {
            content: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 核心邏輯 (真正抓取 Google News) ---

# 預設關鍵字設定
DEFAULT_KEYWORDS = {
    "company": {
        "label": "MGCooling 公司動態",
        "color": "linear-gradient(135deg, #0061ff 0%, #60efff 100%)",
        "terms": "元鈦科技, MGCooling, 緯創 水冷, 陳茂欽"
    },
    "tech": {
        "label": "技術前沿 (R&D)",
        "color": "linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%)",
        "terms": "兩相浸沒式, 介電液, 漏液偵測, Manifold, 冷卻液認證"
    },
    "competitor": {
        "label": "競品與全球供應鏈",
        "color": "linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%)",
        "terms": "雙鴻, 奇鋐, 台達電 CDU, CoolIT, Vertiv, 高力, 勤誠"
    },
    "trend": {
        "label": "市場趨勢觀測",
        "color": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
        "terms": "AI 伺服器 水冷, 液冷散熱, CDU 市場, NVIDIA GB200 液冷"
    }
}

def get_google_news_rss(query):
    """抓取真實 Google News RSS (台灣繁體中文)"""
    encoded_query = urllib.parse.quote(query)
    # 使用 Google News RSS 服務
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    try:
        feed = feedparser.parse(rss_url)
        return feed.entries[:3] # 每個關鍵字取前 3 則，確保版面整潔
    except Exception as e:
        return []

def run_analysis(keywords_config):
    """執行搜尋並整理資料"""
    results = {}
    progress_bar = st.progress(0)
    
    # 計算進度條總數
    all_terms = []
    for cat in keywords_config.values():
        all_terms.extend([t.strip() for t in cat["terms"].split(",") if t.strip()])
    total_steps = len(all_terms)
    current_step = 0
    
    for cat_key, config in keywords_config.items():
        cat_news = []
        terms = [t.strip() for t in config["terms"].split(",") if t.strip()]
        
        for term in terms:
            news_items = get_google_news_rss(term)
            for item in news_items:
                cat_news.append({
                    "title": item.title,
                    "link": item.link,
                    "published": item.get('published', '未知日期'),
                    "source": item.get('source', {}).get('title', 'Google News'),
                    "keyword": term
                })
            current_step += 1
            if total_steps > 0:
                progress_bar.progress(min(current_step / total_steps, 1.0))
            time.sleep(0.1) # 避免請求過快被 Google 擋
            
        # 去重 (依據連結)
        seen_links = set()
        unique_news = []
        for news in cat_news:
            if news['link'] not in seen_links:
                unique_news.append(news)
                seen_links.add(news['link'])
        
        # 按日期排序 (嘗試解析，若失敗則保留原順序)
        try:
            unique_news.sort(key=lambda x: pd.to_datetime(x['published']).tz_localize(None), reverse=True)
        except:
            pass
            
        results[cat_key] = unique_news
    
    progress_bar.empty()
    return results

# --- 4. 側邊欄 UI ---
with st.sidebar:
    st.title("⚙️ 設定面板")
    st.info("💡 這裡可以調整想要追蹤的關鍵字")
    
    user_keywords = {}
    for key, config in DEFAULT_KEYWORDS.items():
        st.subheader(f"{config['label'].split(' ')[0]}") # 簡化標題
        val = st.text_area(
            label=config['label'], 
            value=config['terms'], 
            height=70,
            key=key,
            label_visibility="collapsed"
        )
        user_keywords[key] = {
            "label": config["label"],
            "color": config["color"],
            "terms": val
        }
    
    st.markdown("---")
    if st.button("🔄 手動刷新情報", type="primary", use_container_width=True):
        st.session_state.run_search = True
    st.caption("Powered by Streamlit Cloud")

# --- 5. 主畫面 UI ---

# Header 區塊
today_str = datetime.now().strftime("%Y-%m-%d")
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"#### 📅 {today_str}")
    st.markdown("# 🌊 MGCooling 市場情報日報")

with col2:
    # 列印按鈕 (使用 JS 呼叫瀏覽器列印)
    st.markdown("""
        <div style="text-align: right; padding-top: 20px;">
            <button onclick="window.print()" class="print-hide" style="
                background-color: #000; color: white; border: none; 
                padding: 10px 20px; border-radius: 20px; cursor: pointer; 
                font-weight: 600; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                🖨️ 匯出 PDF / 列印
            </button>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Executive Summary
st.markdown("""
<div class="news-card" style="border-left: 5px solid #0066CC; background: linear-gradient(to right, #f8f9fa, #ffffff);">
    <h4 style="margin:0; color: #0066CC;">📊 Executive Summary</h4>
    <p style="margin-top: 10px; color: #555; line-height: 1.6;">
        本系統自動彙整今日網路關於 <b>水冷散熱、元鈦科技(MGCooling)</b> 及 <b>AI 伺服器供應鏈</b> 之最新動態。<br>
        重點關注：<b>NVIDIA GB200 液冷滲透率</b>、<b>CDU 技術革新</b> 以及 <b>競爭對手擴產動向</b>。
    </p>
</div>
""", unsafe_allow_html=True)

# 執行自動搜尋 (預設自動執行)
if 'run_search' not in st.session_state:
    st.session_state.run_search = True 

# 如果觸發搜尋
if st.session_state.run_search:
    with st.spinner('🚀 正在搜集全球情報...'):
        data = run_analysis(user_keywords)

        if not any(data.values()):
            st.warning("⚠️ 今日暫無相關新聞，請嘗試在側邊欄調整關鍵字範圍。")
        
        for cat_key, news_list in data.items():
            if not news_list:
                continue
            
            config = user_keywords[cat_key]
            
            # 顯示分類標題 (帶色塊)
            st.markdown(f"""
            <div class="category-header" style="background: {config['color']};">
                {config['label']} ({len(news_list)})
            </div>
            """, unsafe_allow_html=True)
            
            # 顯示新聞卡片
            for idx, item in enumerate(news_list[:5], 1): # 每類最多顯示 5 則
                # 處理日期格式
                pub_date = item['published']
                if len(pub_date) > 16:
                    pub_date = pub_date[:16]

                st.markdown(f"""
                <div class="news-card">
                    <div style="display:flex; justify-content:space-between; align-items:start; gap: 15px;">
                        <a href="{item['link']}" target="_blank" style="font-size: 1.1rem; flex:1; line-height: 1.4;">
                            {idx}. {item['title']}
                        </a>
                        <span style="background:#f1f3f5; padding:4px 10px; border-radius:6px; font-size:0.8rem; color:#555; white-space:nowrap; font-weight: 600;">
                            {item['source']}
                        </span>
                    </div>
                    <div style="margin-top:12px; font-size:0.85rem; color:#888; display: flex; gap: 15px;">
                        <span>📅 {pub_date}</span>
                        <span style="color:#0066CC; background: rgba(0,102,204,0.1); padding: 0 6px; border-radius: 4px;">
                            #{item['keyword']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="print-hide" style="text-align: center; color: #aaa; font-size: 0.8rem; margin-top: 50px; padding-bottom: 20px;">
    Generated by MGCooling AI Intelligence System • Confidential
</div>
""", unsafe_allow_html=True)
