import React, { useState, useEffect } from 'react';
import { Calendar, Search, FileText, Download, Table, Settings, Activity, ExternalLink, RefreshCw, Globe, Zap, Languages, ChevronRight, Edit2, X, Tag, Menu, Printer } from 'lucide-react';

const App = () => {
  // --- 狀態管理 ---
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [isLoading, setIsLoading] = useState(true);
  const [hasRun, setHasRun] = useState(false);
  const [activeTab, setActiveTab] = useState('preview');
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  
  // 預設關鍵字
  const [keywords, setKeywords] = useState({
    company: "MGCooling, 元鈦科技, 緯創 水冷, 陳茂欽",
    competitor: "雙鴻, 奇鋐, 台達電 CDU, CoolIT, Vertiv, 高力, 勤誠",
    trend: "AI 伺服器 水冷, 液冷散熱, CDU 市場, NVIDIA GB200 液冷",
    tech: "兩相浸沒式, 介電液, 漏液偵測, Manifold, 冷卻液認證, Quick Disconnect"
  });

  const [newsData, setNewsData] = useState({});

  // --- 模擬數據 (連結已修正為 Google 搜尋，確保可點擊) ---
  const MOCK_NEWS_DATA = {
    company: {
      label: "MGCooling 公司動態",
      color: "from-blue-500 to-blue-600",
      items: [
        {
          title: "緯創加碼佈局液冷，MGCooling 扮演關鍵角色",
          source: "數位時代",
          published: "2025-12-02",
          link: "https://www.google.com/search?q=緯創+液冷+MGCooling+元鈦科技",
          summary: "緯創資通看好AI算力帶動的散熱需求，強調與 MGCooling (元鈦) 的技術整合將是明年GB200出貨的關鍵優勢...",
          isTranslated: false
        },
        {
          title: "MGCooling 攜手光寶科技，展示 Coolite 整合方案",
          source: "Yahoo奇摩新聞",
          published: "2025-12-01",
          link: "https://www.google.com/search?q=元鈦科技+光寶+Coolite+液冷",
          summary: "在最新展覽中，MGCooling 的液冷配管與光寶電源系統完美結合，不僅 PUE 顯著降低，更展現了一條龍服務的實力...",
          isTranslated: false
        }
      ]
    },
    technology: {
      label: "技術前沿與研發 (R&D)",
      color: "from-violet-500 to-purple-600",
      items: [
        {
          title: "3M Exit Sparks Race for New Two-Phase Immersion Coolants",
          source: "HPCwire (Global)",
          published: "2025-12-03",
          link: "https://www.google.com/search?q=3M+exit+two-phase+immersion+cooling+fluids+development",
          summary: "【AI 摘要翻譯】隨著 3M 退出冷卻液市場，各大化工廠正競相開發新型 PFAS-free 的兩相浸沒式冷卻液。新一代介電液在沸點控制與環保標準上取得了突破性進展。",
          isTranslated: true
        },
        {
          title: "新一代 CDU 智慧漏液偵測技術解析",
          source: "電子時報 (Digitimes)",
          published: "2025-12-02",
          link: "https://www.google.com/search?q=CDU+leak+detection+technology+AI+server",
          summary: "為解決水冷系統最讓人擔憂的漏液風險，業界推出結合 AI 壓力感測的負壓偵測系統，能在微量洩漏發生前即時阻斷水路...",
          isTranslated: false
        }
      ]
    },
    competitor: {
      label: "競品與全球供應鏈",
      color: "from-rose-500 to-rose-600",
      items: [
        {
          title: "Vertiv Announces New High-Density Cooling Solutions", 
          source: "Data Center Dynamics (US)",
          published: "2025-12-03",
          link: "https://www.google.com/search?q=Vertiv+high+density+cooling+solutions+AI+data+center",
          summary: "【AI 摘要翻譯】Vertiv 宣布推出針對 AI 資料中心的新型高密度冷卻解決方案。該方案旨在解決高達 100kW 機櫃熱負荷，並整合了最新的 CDU 技術以提高能源效率。",
          isTranslated: true
        },
        {
          title: "雙鴻、奇鋐擴產應對 NVIDIA GB200 需求",
          source: "自由財經",
          published: "2025-12-03",
          link: "https://www.google.com/search?q=雙鴻+奇鋐+GB200+水冷板+擴產",
          summary: "隨著GB200即將放量，台灣散熱大廠雙鴻與奇鋐正積極擴充水冷板產能，預計明年Q1放量...",
          isTranslated: false
        }
      ]
    },
    trend: {
      label: "產業趨勢觀測",
      color: "from-emerald-500 to-emerald-600",
      items: [
        {
          title: "TrendForce: 2025年 AI 晶片液冷滲透率將突破 20%",
          source: "TrendForce",
          published: "2025-12-03",
          link: "https://www.google.com/search?q=TrendForce+AI+server+liquid+cooling+penetration+rate+2025",
          summary: "氣冷散熱面臨瓶頸，液冷將成為高階 AI 伺服器標配。分析師指出 CDU 市場規模將在未來三年翻倍...",
          isTranslated: false
        }
      ]
    }
  };

  const handleKeywordChange = (category, value) => {
    setKeywords(prev => ({ ...prev, [category]: value }));
  };

  const runSearch = (isInitial = false) => {
    setIsLoading(true);
    setHasRun(false);
    setShowMobileMenu(false);
    
    // 模擬載入時間，初次快一點，手動慢一點
    setTimeout(() => {
      setNewsData(MOCK_NEWS_DATA);
      setHasRun(true);
      setIsLoading(false);
    }, isInitial ? 800 : 1800);
  };

  // 自動執行
  useEffect(() => {
    runSearch(true);
  }, []);

  const generateMarkdown = () => {
    let md = `# 🌊 MGCooling 市場情報日報\n\n`;
    md += `**日期**: ${date}\n`;
    md += `**整理單位**: 行銷部自動化系統\n\n---\n\n`;
    md += `## 📊 重點摘要\n> 本日市場重點關注於 NVIDIA GB200 帶動的液冷滲透率提升，以及國際市場對液冷規模的預測。系統已自動將英文外電翻譯為中文摘要。\n\n`;

    Object.entries(newsData).forEach(([category, items]) => {
      md += `## ${items.label}\n\n`;
      items.items.forEach((item, index) => {
        const titlePrefix = item.isTranslated ? "[AI 翻譯] " : "";
        md += `### ${index + 1}. ${titlePrefix}${item.title}\n`;
        md += `- **來源**: ${item.source} | ${item.published}\n`;
        md += `- **連結**: [點擊閱讀全文](${item.link})\n`;
        if (item.isTranslated) {
            md += `- **摘要 (已翻譯)**: ${item.summary}\n\n`;
        } else {
             md += `\n`;
        }
      });
    });
    
    md += `---\n*本報告由 AI 情報系統自動生成，決策前請查證原始來源。*`;
    return md;
  };

  const downloadReport = () => {
    const element = document.createElement("a");
    const file = new Blob([generateMarkdown()], {type: 'text/markdown'});
    element.href = URL.createObjectURL(file);
    element.download = `MGCooling_DailyReport_${date.replace(/-/g, '')}.md`;
    document.body.appendChild(element);
    element.click();
  };

  const handlePrint = () => {
    window.print();
  };

  // 獨立出報表內容渲染函數，供預覽和列印共用
  const renderDailyReport = () => (
    <div className="bg-white rounded-xl md:rounded-2xl shadow-xl shadow-gray-200/50 overflow-hidden ring-1 ring-black/5 print:shadow-none print:border-none print:rounded-none">
        {/* Header */}
        <div className="bg-gray-50 border-b border-gray-100 p-6 md:p-10 text-center relative overflow-hidden print:bg-white print:border-b-2 print:border-black">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 print:hidden"></div>
            <p className="text-[10px] md:text-xs font-bold tracking-[0.2em] text-gray-400 uppercase mb-2 md:mb-3">Daily Intelligence Report</p>
            <h1 className="text-2xl md:text-4xl font-extrabold text-gray-900 mb-3 md:mb-4 font-serif tracking-tight leading-tight">MGCooling<br className="md:hidden" /> 市場情報日報</h1>
            <div className="inline-flex items-center gap-2 md:gap-3 px-3 py-1 md:px-4 md:py-1.5 rounded-full border border-gray-200 bg-white shadow-sm text-xs md:text-sm font-medium text-gray-600 print:border-black print:shadow-none">
            <Calendar size={12} className="md:w-3.5 md:h-3.5" />
            {date}
            </div>
        </div>

        <div className="p-4 md:p-10 space-y-8 md:space-y-10 print:p-0 print:pt-6">
            {/* Summary */}
            <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-100 p-5 md:p-6 relative shadow-sm print:bg-white print:border print:border-gray-300 print:shadow-none">
                <div className="mb-3 flex items-center justify-center md:absolute md:top-0 md:left-6 md:-translate-y-1/2">
                    <div className="bg-white px-3 py-1 rounded-full border border-gray-100 shadow-sm flex items-center gap-2 text-[10px] md:text-xs font-bold text-gray-800 uppercase tracking-wide print:border-gray-300 print:shadow-none">
                        <Activity size={12} className="text-blue-500 print:text-black"/>
                        Executive Summary
                    </div>
                </div>
                <p className="text-gray-600 leading-relaxed font-serif text-base md:text-lg italic text-center print:text-black">
                    "本日焦點：新型 PFAS-free 冷卻液引發 R&D 關注，漏液偵測技術成為 CDU 採購重點。MGCooling 需持續深化與 ODM 夥伴之整合優勢。"
                </p>
            </div>

            {/* News Blocks */}
            {Object.entries(newsData).map(([key, section]) => (
                <div key={key} className="space-y-4 md:space-y-5 print:break-inside-avoid">
                <div className={`bg-gradient-to-r ${section.color} px-4 py-2.5 md:px-5 md:py-3 rounded-lg md:rounded-xl shadow-lg shadow-gray-200 flex items-center justify-between text-white transform hover:scale-[1.01] transition-transform print:shadow-none print:transform-none`}>
                    <h2 className="text-base md:text-lg font-bold tracking-wide flex items-center gap-2 print:text-white">
                    {section.label}
                    </h2>
                    <span className="bg-white/20 px-2 py-0.5 rounded text-[10px] md:text-xs font-medium backdrop-blur-sm print:hidden">
                    {section.items.length} 則
                    </span>
                </div>

                <div className="grid gap-3 md:gap-4">
                    {section.items.map((item, i) => (
                    <div key={i} className="group bg-white rounded-lg md:rounded-xl border border-gray-100 p-4 md:p-5 hover:border-gray-300 hover:shadow-md transition-all duration-200 print:shadow-none print:border-gray-300 print:break-inside-avoid">
                        <div className="flex flex-col md:flex-row md:items-start justify-between gap-2 md:gap-4 mb-2 md:mb-3">
                        <h3 className="font-bold text-gray-900 text-base md:text-lg leading-snug group-hover:text-blue-600 transition-colors print:text-black">
                            {item.isTranslated && (
                                <span className="inline-block align-middle mr-2 bg-indigo-50 text-indigo-600 text-[10px] px-1.5 py-0.5 rounded border border-indigo-100 font-bold tracking-wider print:border-gray-400 print:text-black">
                                AI 譯
                                </span>
                            )}
                            {item.title}
                        </h3>
                        </div>
                        
                        <div className="flex items-center gap-3 text-[10px] md:text-xs text-gray-400 font-medium uppercase tracking-wide mb-2 md:mb-3 print:text-gray-600">
                        <span className="truncate max-w-[150px]">{item.source}</span>
                        <span className="w-1 h-1 rounded-full bg-gray-300 shrink-0 print:bg-gray-400"></span>
                        <span>{item.published}</span>
                        </div>

                        <p className={`text-sm leading-relaxed ${item.isTranslated ? 'text-gray-700 bg-gray-50 p-3 rounded-lg border border-gray-100 print:bg-white print:border-gray-200' : 'text-gray-500 print:text-black'}`}>
                        {item.summary}
                        </p>
                        
                        <div className="mt-3 md:mt-4 flex justify-end print:hidden">
                            <a 
                            href={item.link} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-xs font-bold text-blue-600 hover:text-blue-800 transition-colors active:text-blue-400"
                            >
                                閱讀全文 <ChevronRight size={12} strokeWidth={3} />
                            </a>
                        </div>
                    </div>
                    ))}
                </div>
                </div>
            ))}
        </div>
        
        <div className="bg-gray-50 border-t border-gray-100 p-6 text-center print:hidden">
            <p className="text-[10px] md:text-xs text-gray-400 font-medium">Generated by MGCooling AI Intelligence System</p>
        </div>
    </div>
  );

  const SettingsPanel = () => (
    <div className="space-y-6">
      <div className="bg-white/60 p-4 rounded-2xl border border-gray-100 shadow-sm">
        <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">DATE SELECTION</label>
        <div className="relative group">
          <input 
            type="date" 
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="w-full pl-10 pr-3 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all shadow-sm group-hover:shadow appearance-none"
          />
          <Calendar className="absolute left-3.5 top-3 text-gray-400 group-hover:text-blue-500 transition-colors" size={16} />
        </div>
      </div>

      <div className="flex-1">
         <div className="flex items-center justify-between px-2 mb-3">
           <h2 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Target Keywords</h2>
           <Settings size={12} className="text-gray-400" />
         </div>
         <div className="space-y-4">
          <KeywordCard 
            label="MGCooling 公司" 
            value={keywords.company} 
            onChange={(v) => handleKeywordChange('company', v)} 
            color="blue"
            icon={<Activity size={12}/>}
          />
          <KeywordCard 
            label="技術前沿 (Tech)" 
            value={keywords.tech} 
            onChange={(v) => handleKeywordChange('tech', v)} 
            color="violet"
            icon={<Zap size={12}/>}
          />
          <KeywordCard 
            label="競品與供應鏈" 
            value={keywords.competitor} 
            onChange={(v) => handleKeywordChange('competitor', v)} 
            color="rose"
            icon={<Globe size={12}/>}
          />
          <KeywordCard 
            label="市場趨勢" 
            value={keywords.trend} 
            onChange={(v) => handleKeywordChange('trend', v)} 
            color="emerald"
            icon={<Activity size={12}/>}
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#F5F5F7] flex flex-col font-sans text-gray-900 selection:bg-blue-200">
       {/* Print Styles */}
       <style>{`
        @media print {
            @page { margin: 1cm; size: A4; }
            body { 
                -webkit-print-color-adjust: exact !important; 
                print-color-adjust: exact !important; 
                background: white !important;
            }
            .print\\:hidden { display: none !important; }
            .print\\:block { display: block !important; }
            .print\\:w-full { width: 100% !important; }
            main { padding: 0 !important; margin: 0 !important; overflow: visible !important; height: auto !important; }
            /* Hide URL on print */
            a[href]:after { content: none !important; }
        }
      `}</style>

      {/* Screen Layout - Wrapped for Print Hiding */}
      <div className="print:hidden flex flex-col h-screen">
        <header className="bg-white/80 backdrop-blur-md border-b border-gray-200/50 px-4 md:px-6 py-4 flex items-center justify-between sticky top-0 z-50 transition-all duration-300">
            <div className="flex items-center gap-3">
            <button 
                onClick={() => setShowMobileMenu(true)}
                className="md:hidden p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
                <Menu size={24} />
            </button>

            <div className="w-9 h-9 md:w-10 md:h-10 bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-xl shadow-lg shadow-blue-500/20 flex items-center justify-center shrink-0">
                <Activity size={20} strokeWidth={2.5} />
            </div>
            <div>
                <h1 className="text-base md:text-lg font-bold tracking-tight text-gray-900">MGCooling</h1>
                <p className="text-[10px] md:text-[11px] font-medium text-gray-500 uppercase tracking-widest leading-none">Market Intelligence</p>
            </div>
            </div>
            
            <div className="flex items-center gap-2 md:gap-3">
                <button 
                    onClick={() => runSearch(false)}
                    disabled={isLoading}
                    className={`flex items-center gap-2 px-3 py-2 md:px-4 rounded-full text-xs md:text-sm font-medium transition-all duration-200 ${
                        isLoading 
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200 shadow-sm hover:shadow active:scale-95'
                    }`}
                >
                    <RefreshCw size={14} className={isLoading ? "animate-spin" : ""} />
                    <span className="hidden md:inline">{isLoading ? "Updating..." : "一鍵更新"}</span>
                    <span className="md:hidden">{isLoading ? "更新中" : "更新"}</span>
                </button>
                
                <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-green-50/50 border border-green-100 rounded-full">
                    <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></div>
                    <span className="text-xs font-medium text-green-700">Online</span>
                </div>
            </div>
        </header>

        <div className="flex flex-1 overflow-hidden relative">
            {/* Desktop Sidebar */}
            <aside className="w-80 bg-white/50 backdrop-blur-xl border-r border-gray-200 flex flex-col gap-6 overflow-y-auto z-0 hidden md:flex pt-6 px-4 pb-6 sticky top-0 h-[calc(100vh-73px)]">
            <SettingsPanel />
            </aside>

            {/* Mobile Menu */}
            {showMobileMenu && (
            <div className="fixed inset-0 z-[60] md:hidden">
                <div className="absolute inset-0 bg-black/20 backdrop-blur-sm" onClick={() => setShowMobileMenu(false)}></div>
                <div className="absolute top-0 left-0 bottom-0 w-4/5 max-w-xs bg-white shadow-2xl flex flex-col p-6 overflow-y-auto animate-in slide-in-from-left duration-300">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-bold text-gray-900">設定與關鍵字</h2>
                    <button onClick={() => setShowMobileMenu(false)} className="p-2 bg-gray-100 rounded-full text-gray-600">
                    <X size={20} />
                    </button>
                </div>
                <SettingsPanel />
                <button 
                    onClick={() => runSearch(false)}
                    className="mt-6 w-full py-3.5 rounded-xl flex items-center justify-center gap-2 font-semibold text-white bg-gray-900 hover:bg-black"
                    >
                    <RefreshCw size={18} /> 立即更新情報
                </button>
                </div>
            </div>
            )}

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto relative p-3 md:p-8">
            <div className="max-w-4xl mx-auto pb-20 md:pb-10">
                {isLoading && !hasRun ? (
                <div className="flex flex-col items-center justify-center py-20 md:py-32 animate-pulse space-y-6">
                    <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    <div className="text-center">
                    <h3 className="text-lg font-bold text-gray-900">MGCooling Intelligence</h3>
                    <p className="text-sm text-gray-500 mt-1">正在為您彙整今日全球情報...</p>
                    </div>
                </div>
                ) : (
                <>
                    {/* Segment Control */}
                    <div className="flex justify-center mb-6 md:mb-8 sticky top-0 z-10 pt-2 pb-2 bg-[#F5F5F7]/95 backdrop-blur">
                    <div className="bg-gray-200/80 p-1 rounded-lg md:rounded-full flex w-full max-w-sm md:w-auto shadow-inner">
                        <SegmentButton 
                        active={activeTab === 'preview'} 
                        onClick={() => setActiveTab('preview')} 
                        label="預覽" 
                        icon={<FileText size={14}/>}
                        />
                        <SegmentButton 
                        active={activeTab === 'list'} 
                        onClick={() => setActiveTab('list')} 
                        label="清單" 
                        icon={<Table size={14}/>}
                        />
                        <SegmentButton 
                        active={activeTab === 'export'} 
                        onClick={() => setActiveTab('export')} 
                        label="匯出" 
                        icon={<Download size={14}/>}
                        />
                    </div>
                    </div>

                    {/* Content */}
                    <div className="animate-in slide-in-from-bottom-4 duration-500 ease-out">
                    {activeTab === 'preview' && renderDailyReport()}

                    {activeTab === 'list' && (
                        <div className="bg-white rounded-xl md:rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                            <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-gray-50 text-gray-500 font-semibold border-b border-gray-200">
                                <tr>
                                    <th className="px-4 py-3 md:px-6 md:py-4 whitespace-nowrap">Title</th>
                                    <th className="px-4 py-3 md:px-6 md:py-4 w-32 whitespace-nowrap">Source</th>
                                    <th className="px-4 py-3 md:px-6 md:py-4 w-24 whitespace-nowrap">Lang</th>
                                    <th className="px-4 py-3 md:px-6 md:py-4 w-16">Link</th>
                                </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                {Object.values(newsData).flatMap(s => s.items).map((item, i) => (
                                    <tr key={i} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-4 py-3 md:px-6 md:py-4">
                                        <div className="font-medium text-gray-900 line-clamp-2 md:line-clamp-none">{item.title}</div>
                                    </td>
                                    <td className="px-4 py-3 md:px-6 md:py-4 text-gray-500 text-xs md:text-sm whitespace-nowrap">{item.source}</td>
                                    <td className="px-4 py-3 md:px-6 md:py-4">
                                        {item.isTranslated ? (
                                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-600 text-[10px] md:text-xs font-bold border border-indigo-100 whitespace-nowrap">
                                                EN→TW
                                            </span>
                                        ) : (
                                            <span className="text-gray-400 text-[10px] md:text-xs font-medium whitespace-nowrap">中文</span>
                                        )}
                                    </td>
                                    <td className="px-4 py-3 md:px-6 md:py-4">
                                        <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-blue-600 transition-colors p-2 -m-2 block">
                                        <ExternalLink size={16} />
                                        </a>
                                    </td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                            </div>
                        </div>
                    )}
                    
                    {activeTab === 'export' && (
                        <div className="bg-white rounded-xl md:rounded-2xl shadow-sm border border-gray-200 p-8 md:p-12 text-center h-[50vh] flex flex-col justify-center items-center">
                            <div className="w-16 h-16 md:w-20 md:h-20 bg-green-50 text-green-600 rounded-3xl flex items-center justify-center mb-6 shadow-sm">
                                <Download size={32} />
                            </div>
                            <h2 className="text-xl font-bold text-gray-900 mb-2">Ready to Export</h2>
                            <p className="text-gray-500 mb-8 max-w-xs mx-auto text-sm">Download as Markdown or Print as PDF for distribution.</p>
                            
                            <div className="flex flex-col gap-3 w-full max-w-xs">
                                <button 
                                    onClick={handlePrint}
                                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all transform active:scale-95 flex items-center justify-center gap-2"
                                >
                                    <Printer size={18} /> 列印 / 另存 PDF
                                </button>
                                
                                <button 
                                    onClick={downloadReport}
                                    className="w-full bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 font-bold py-3 px-8 rounded-xl shadow-sm hover:shadow transition-all transform active:scale-95 flex items-center justify-center gap-2"
                                >
                                    <FileText size={18} /> 下載 Markdown
                                </button>
                            </div>
                        </div>
                    )}
                    </div>
                </>
                )}
            </div>
            </main>
        </div>
      </div>

      {/* Print Layout - Hidden on Screen */}
      <div className="hidden print:block print:w-full">
         {!isLoading && hasRun && renderDailyReport()}
      </div>
    </div>
  );
};

// --- styled Components with Better UI ---

const KeywordCard = ({ label, value, onChange, color, icon }) => {
    const [isEditing, setIsEditing] = useState(false);
    
    const colorMap = {
        blue: { bg: "bg-blue-50", text: "text-blue-700", border: "border-blue-100", tagBg: "bg-blue-100", tagText: "text-blue-800" },
        rose: { bg: "bg-rose-50", text: "text-rose-700", border: "border-rose-100", tagBg: "bg-rose-100", tagText: "text-rose-800" },
        emerald: { bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-100", tagBg: "bg-emerald-100", tagText: "text-emerald-800" },
        violet: { bg: "bg-violet-50", text: "text-violet-700", border: "border-violet-100", tagBg: "bg-violet-100", tagText: "text-violet-800" }
    };
    
    const style = colorMap[color];
    const tags = value.split(',').map(s => s.trim()).filter(s => s);

    return (
        <div className={`bg-white rounded-xl border ${isEditing ? 'border-blue-400 ring-2 ring-blue-100' : 'border-gray-200'} p-3 shadow-sm hover:shadow-md transition-all duration-200 group`}>
            <div 
                className={`text-xs font-bold uppercase tracking-wider mb-2 flex justify-between items-center ${style.text} cursor-pointer`}
                onClick={() => setIsEditing(!isEditing)}
            >
                <div className="flex items-center gap-1.5">
                    {icon} {label}
                </div>
                {isEditing ? (
                     <div className="p-1 rounded bg-white text-gray-400 hover:text-red-500">
                        <X size={12} />
                     </div>
                ) : (
                    <div className="opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded bg-white text-gray-400 hover:text-blue-500">
                        <Edit2 size={10} />
                    </div>
                )}
            </div>
            
            {isEditing ? (
                <textarea 
                  autoFocus
                  value={value}
                  onChange={(e) => onChange(e.target.value)}
                  onBlur={() => setIsEditing(false)}
                  className="w-full text-xs text-gray-700 leading-relaxed bg-gray-50 border border-gray-200 rounded p-2 focus:ring-0 resize-none outline-none h-20"
                />
            ) : (
                <div 
                    className="flex flex-wrap gap-1.5 cursor-pointer min-h-[40px] content-start"
                    onClick={() => setIsEditing(true)}
                >
                    {tags.map((tag, i) => (
                        <span key={i} className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium ${style.tagBg} ${style.tagText}`}>
                            {tag}
                        </span>
                    ))}
                    {tags.length === 0 && <span className="text-xs text-gray-300 italic">Click to add keywords...</span>}
                </div>
            )}
        </div>
    );
};

const SegmentButton = ({ active, onClick, label, icon }) => (
    <button
        onClick={onClick}
        className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg md:rounded-full text-xs md:text-sm font-semibold transition-all duration-200 ${
            active 
            ? 'bg-white text-gray-900 shadow-sm' 
            : 'text-gray-500 hover:text-gray-700'
        }`}
    >
        {icon} {label}
    </button>
);

export default App;
