from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1].parent
INBOX = ROOT / "Knowledge" / "00_Inbox"
NOTES_DIR = ROOT / "Knowledge" / "02_Notes" / "現代價值投資課"
COURSE = "現代價值投資課"
DATE = "2026-06-04"


MODULES = {
    "1": {
        "title": "財富自由投資規劃與個股投資邏輯",
        "level": "beginner",
        "topics": ["財富自由", "長期投資", "個股投資", "ETF", "市場低迷", "風險"],
        "practices": ["定期投入", "低迷市場加碼", "個股與ETF比較", "風險辨識"],
        "summary": "本模組建立整門課的投資底層信念：股票是長期可成長的資產，但市場波動不可避免。課程主張投資者不應只害怕市場下跌，而要理解定期投入、低點買入與長期持有如何在市場低迷時仍可能創造回報。同時，本模組說明為什麼課程選擇把重點放在個股，而不只停留在ETF：個股提供更高成長空間，也要求更嚴格的選股與風險控制。",
        "concepts": [
            ("股票作為長期成長資產", "課程把股市視為能隨企業盈利與人類生產力長期成長的資產類別。這不是說股市每一年都會上漲，而是說長期資本市場通常反映企業創造價值的能力。", "投資者需要用長期眼光理解股票，而不是只被短期價格波動牽著走。", "適合建立長期投資心態；不適合用來保證任何單一市場或單一股票必然上漲。"),
            ("市場低迷時的定期投入", "講師用S&P 500與日本股市的例子說明，即使指數長期回到原點，持續投入仍可能因低位買入而累積報酬。", "這讓投資者理解Dollar-Cost Averaging不是逃避風險，而是一種在波動中分散買入成本的方法。", "適合現金流穩定、投資期限較長的人；若資金短期必須使用，則不應勉強投入高波動資產。"),
            ("下跌幅度與反彈收益的不對稱", "當價格下跌50%後再回到原點，低點買入的資金會有100%回報；這說明下跌百分比與回升收益不是線性對稱。", "這個概念幫助學員理解為什麼恐慌時期可能也是機會期。", "適合用於理解估值與安全邊際；不代表所有下跌都值得買，因為有些企業下跌是基本面惡化。"),
            ("為什麼選擇個股而不是只買ETF", "課程認為ETF分散但也包含表現較差或衰退企業；個股若選對，可能提供遠高於指數的回報。", "這是後續選股五步法的理由：如果要追求超額報酬，就必須學會分析公司。", "適合願意研究企業的人；不適合沒有時間、能力或紀律做研究的人。"),
            ("股市投資風險", "高回報伴隨高波動與判斷錯誤風險。課程提醒投資者要理解市場下跌、買在高點、選錯企業與心理恐慌的風險。", "風險意識讓投資者不會把高回報案例誤解成保證收益。", "適合所有投資者；若忽略風險，本課後續方法容易被誤用成追熱門股。"),
        ],
        "frameworks": [
            ("長期成長 + 定期投入", "用長期資產成長假設配合分批買入，降低一次性買在高點的壓力。"),
            ("個股超額回報邏輯", "透過選擇成長性更強、估值合理且競爭力突出的公司，嘗試取得高於指數的報酬。"),
        ],
        "process": [
            ("確認投資期限與現金流", "先確認資金是否適合長期投入。"),
            ("理解市場可能長期低迷", "接受波動與停滯是投資的一部分。"),
            ("用定期投入分散進場價格", "避免把所有資金一次投入單一高點。"),
            ("比較ETF與個股策略", "決定自己要追求市場平均回報，還是願意承擔研究個股的責任。"),
            ("建立風險清單", "列出高點買入、企業衰退、估值過高與心理恐慌等風險。"),
        ],
    },
    "2": {
        "title": "成長股選股五步法：Known, Growth, Valuation, Profitability, Moat",
        "level": "intermediate",
        "topics": ["成長股", "選股", "Known", "Growth", "Valuation", "Profitability", "Moat", "PE Ratio"],
        "practices": ["閱讀10-K", "閱讀10-Q", "使用AI解讀公司", "估值模型", "案例分析"],
        "summary": "本模組是整門課的核心選股方法。課程把選股拆成五個步驟：Known選擇熟悉的領域與公司、Growth評估成長趨勢、Valuation判斷價格是否合理、Profitability檢查盈利與現金流、Moat判斷競爭優勢。模組也透過TSM、TSLA、NVDA與Dropbox等案例展示如何把方法用在真實公司。",
        "concepts": [
            ("股票賺錢的兩種方式", "課程把股票收益分為低買高賣與股息收入。成長股重點通常在股價上升，但股息仍是另一種收益來源。", "理解收益來源可以避免只看股價漲跌，而忽略企業盈利與分紅能力。", "適合建立基礎投資框架；不應把任何一種收益模式視為必然。"),
            ("Known：投資自己理解的公司", "Known要求投資者從熟悉領域開始，理解公司的產品、服務、客戶、供應商、競爭對手與商業模式。", "投資不是因為自己喜歡產品，而是因為真正理解公司如何賺錢。", "適合選出研究起點；若只是消費者體驗好，仍不足以代表理解公司。"),
            ("Growth：先看公司成長趨勢", "Growth檢查營收、指引、產業空間與未來需求。如果公司沒有成長，課程建議不必浪費太多時間研究。", "成長是推動市場需求與股價上升的重要原因。", "適合篩選成長股；成熟股、股息股或週期股可能需要不同判斷。"),
            ("Valuation：合理價格才值得投入", "Valuation要求投資者不要只找好公司，也要判斷目前價格是否合理，包括PE Ratio、Forward PE與估值模型。", "好公司買太貴仍可能造成低報酬或長期套牢。", "適合判斷入場區間；估值不是精準答案，而是風險管理工具。"),
            ("Profitability：盈利能力與現金流", "Profitability關注公司是否真的能賺錢，包含Gross Margin、現金流與財務健康。", "公司即使營收高，若毛利率低、現金流差，也可能難以抵抗景氣或利率壓力。", "適合辨識企業質量；早期高速成長公司可能短期未盈利，需要更謹慎分析。"),
            ("Moat：競爭優勢護城河", "Moat檢查品牌、成本、門檻、網路效應與其他難以被取代的優勢。", "長期投資需要企業能抵抗競爭者侵蝕。", "適合判斷能否長期持有；護城河也可能隨技術變遷而消失。"),
            ("案例分析與估值模型", "課程透過台積電TSM、Tesla TSLA、NVIDIA NVDA、Dropbox DBX等案例展示五步法如何落地。", "案例讓方法從抽象框架變成具體判斷流程。", "適合練習，但案例結果不應被當成未來保證。"),
        ],
        "frameworks": [
            ("選股五步法", "Known -> Growth -> Valuation -> Profitability -> Moat。這是本課最核心的選股框架。"),
            ("10-K / 10-Q / Investor Presentation研究法", "用官方年報、季報與投資人簡報理解公司，而不是只依賴新聞。"),
            ("Forward PE與估值判斷", "用預期盈利與目前價格估算股票是否仍有合理報酬空間。"),
        ],
        "process": [
            ("Known", "選擇熟悉領域，閱讀10-K中的Business、Risk Factors、Management Discussion。"),
            ("Growth", "檢查營收、用戶、需求、產業空間與管理層指引。"),
            ("Valuation", "查看PE Ratio、Forward PE與估值模型，等待合理價格。"),
            ("Profitability", "檢查Gross Margin、現金流與盈利持續性。"),
            ("Moat", "確認品牌、成本、門檻、網路效應或技術優勢是否足夠。"),
            ("案例驗證", "用TSM、TSLA、NVDA、DBX等公司練習完整流程。"),
        ],
    },
    "3": {
        "title": "入場、出場與持股心態",
        "level": "intermediate",
        "topics": ["入場時機", "出場時機", "持股心態", "定投", "營收", "淨利率"],
        "practices": ["買入策略", "出售策略", "持股復盤", "新手起步"],
        "summary": "本模組處理投資者最容易焦慮的問題：什麼時候買、什麼時候賣、如何開始，以及持股時應該用什麼心態面對波動。課程也討論定投是否會提高成本，以及為什麼分析企業時不能只看淨利率，而要理解營收、成長與市場定價邏輯。",
        "concepts": [
            ("新手如何開始買股票", "課程把開始投資拆成可執行的小步驟，避免因為害怕一次做錯而完全不行動。", "投資能力需要透過實際操作與復盤累積。", "適合剛入門者；不代表可以不做功課就買入。"),
            ("什麼時候買入", "買入應結合公司基本面、估值、成長前景與資金配置，而不是只因價格下跌或熱門消息。", "買入價格會影響長期報酬與心理壓力。", "適合建立入場規則；不適合追求精準最低點。"),
            ("什麼時候出售", "出售不只是因為價格下跌，也可能是估值過高、基本面惡化、成長邏輯改變或有更好機會。", "好的出場規則可以避免把盈利變成僥倖，也避免死抱錯誤標的。", "適合投資組合管理；若過度頻繁交易，可能破壞長期策略。"),
            ("持股心態", "投資是一場心理訓練。持股期間需要面對波動、懷疑、FOMO與恐慌。", "很多錯誤不是來自不懂數據，而是來自情緒反應。", "適合長期投資者；若標的基本面已壞，穩定心態不能變成盲目堅持。"),
            ("定投與成本", "定投可能在價格上升時拉高平均成本，但它也降低了擇時壓力，讓投資者持續參與長期成長。", "投資者需要理解定投是紀律工具，不是保證最低成本的方法。", "適合現金流穩定者；不適合忽略估值與基本面。"),
            ("營收與淨利率的判讀", "課程提醒不能只看淨利率，因為市場可能更關心成長、營收趨勢、規模與未來盈利能力。", "這幫助投資者避免用單一財務指標判斷企業。", "適合分析成長股；仍需搭配盈利能力與現金流。"),
        ],
        "frameworks": [
            ("買入決策框架", "基本面成立 + 估值合理 + 資金允許 + 風險可承受。"),
            ("出售決策框架", "基本面惡化、估值過高、投資假設失效、資金需要或更佳機會。"),
            ("持股心理框架", "用事前規則對抗事後情緒。"),
        ],
        "process": [
            ("建立買入清單", "列出符合五步法的公司。"),
            ("設定合理價格區間", "用估值與安全邊際判斷入場區。"),
            ("分批投入", "降低一次性判斷錯誤。"),
            ("定期復盤", "檢查基本面是否仍支持原投資假設。"),
            ("設定出場條件", "在情緒來臨前先定義賣出理由。"),
        ],
    },
    "4": {
        "title": "資產配置、再平衡與投資風險",
        "level": "intermediate",
        "topics": ["資產配置", "投資組合", "再平衡", "現金流", "IPO", "價值陷阱", "股份回購"],
        "practices": ["資產配置", "每月定投", "再平衡", "風險辨識"],
        "summary": "本模組從單一股票研究推進到投資組合管理。課程說明不同年齡與資金狀態應如何配置資產、如何每月定投、如何在資產類別與個股組合中再平衡，以及如何辨識市場中的風險與機會，例如IPO、中概股退市、價值陷阱、股份回購與投資心理錯誤。",
        "concepts": [
            ("資產配置", "資產配置是把資金分配到不同資產類別、股票或ETF中，避免所有風險集中在單一標的。", "投資結果不只取決於選股，也取決於資金如何分配。", "適合所有投資者；資金太小時可先用簡化配置。"),
            ("不同年齡的配置差異", "課程指出不同年齡、收入穩定度與風險承受力會影響股票、ETF、現金與其他資產的比例。", "年輕投資者通常有較長時間承受波動，接近退休者則更需要穩定性。", "適合規劃長期財務；不能只用年齡，還要看個人情況。"),
            ("每月定投與配額分配", "投資者需要把每月可投資金額分配到不同標的，並保持紀律。", "清楚的配額可以避免看到熱門股就任意加碼。", "適合有穩定收入者；收入不穩定時需保留更多現金。"),
            ("再平衡", "再平衡是在某些資產漲太多或跌太多時，把組合調回原本規劃比例。", "它讓投資者有紀律地控制風險，不讓單一標的過度主導組合。", "適合組合投資；過度頻繁再平衡可能增加成本與錯失長期成長。"),
            ("市場風險與機會", "IPO、價值陷阱、中概股退市、股份回購等都可能是機會，也可能是風險。", "投資者需要拆解事件背後的基本面與市場心理。", "適合進階判斷；不應只因新聞標題就行動。"),
            ("投資常犯錯誤", "課程提醒投資者容易把投資當心理遊戲、忽略趨勢、把每件事都情緒化，而不是當成學習過程。", "錯誤復盤是投資能力成長的關鍵。", "適合所有投資者；復盤不是責備自己，而是改善決策流程。"),
        ],
        "frameworks": [
            ("資產配置框架", "按年齡、風險承受力、現金流與目標配置資產。"),
            ("再平衡框架", "設定目標比例 -> 定期檢查 -> 偏離過大時調整。"),
            ("事件風險分析框架", "事件本身、基本面影響、估值影響、心理影響、行動策略。"),
        ],
        "process": [
            ("盤點資金與風險承受力", "先知道自己能承受多大波動。"),
            ("設定資產配置比例", "決定股票、ETF、現金等比例。"),
            ("制定每月投入配額", "讓投資行為穩定而可持續。"),
            ("定期檢查組合偏離", "觀察是否某一類資產過度集中。"),
            ("執行再平衡", "賣出或減少過高比例資產，補足低比例資產。"),
            ("記錄風險事件", "把IPO、退市、回購、價值陷阱等事件納入復盤。"),
        ],
    },
    "5": {
        "title": "個人理財與富人思維",
        "level": "beginner",
        "topics": ["個人理財", "富人思維", "收入分配", "分卡管理", "ROI", "資產診斷"],
        "practices": ["資產診斷", "分卡管理", "收入分配", "ROI思維"],
        "summary": "本模組把投資之前的個人理財基礎補齊。課程指出，投資能力不只來自選股，也來自管理收入、支出、資產、意外之財與現金流的能力。模組以四個法則與富人思維為主軸，幫助學員建立可持續的財務系統。",
        "concepts": [
            ("財富自由的真正意義", "財富自由不是單純有很多錢，而是資產與現金流能支持自己想要的生活選擇。", "這讓學員把理財目標從炫耀性消費轉向生活自主權。", "適合建立長期方向；不應被理解成完全不用工作。"),
            ("資產狀況診斷", "投資前需要先了解自己的資產、負債、收入、支出與現金流。", "不清楚財務現況，就無法制定合適投資計劃。", "適合所有人；資料不完整時應先記錄再判斷。"),
            ("提前做好收入分配", "收入進來時先分配投資、儲蓄、生活、學習與風險準備，而不是花剩才存。", "收入分配決定財富累積速度。", "適合有固定收入者；收入波動者需提高緊急預備金比例。"),
            ("專卡專用與分卡管理", "透過不同帳戶或卡片管理不同用途資金，降低混用造成的失控。", "系統化比意志力更可靠。", "適合支出容易混亂的人；需要定期檢查，不然帳戶太多也會混亂。"),
            ("善待意外之財", "獎金、紅包、額外收入不應全部用於即時消費，而應按規則分配。", "意外之財若能轉成資產，會加速財富累積。", "適合收入偶發增加時；也可保留一小部分作獎勵，避免過度壓抑。"),
            ("ROI思維", "ROI思維要求學員思考每一筆支出、學習、工具或投資是否能產生回報。", "這能幫助學員把錢花在能提升能力或資產的位置。", "適合理財與自我投資；不應把所有人生選擇都簡化成金錢回報。"),
        ],
        "frameworks": [
            ("四步養成富人思維", "診斷現況、分配收入、管理支出、用ROI思維做資源決策。"),
            ("分卡管理法", "用不同帳戶或卡片區分生活、投資、學習、備用與自由花費。"),
        ],
        "process": [
            ("盤點資產負債", "列出現金、投資、負債與每月現金流。"),
            ("設定收入分配比例", "先分配投資與儲蓄，再安排生活開支。"),
            ("建立分卡或分帳戶系統", "讓每一筆錢有明確用途。"),
            ("處理意外之財", "把額外收入按規則分配，不全數消費。"),
            ("用ROI審視大額支出", "判斷支出是否提升能力、效率、健康或資產。"),
        ],
    },
    "6": {
        "title": "ETF定投、ETF組合與資產配置",
        "level": "beginner",
        "topics": ["ETF", "定投", "ETF組合", "資產配置", "再平衡", "閒置現金"],
        "practices": ["ETF定投", "ETF組合設計", "ETF資產再平衡", "現金管理"],
        "summary": "本模組回到較穩健、較適合大眾的ETF投資方法。課程說明什麼是ETF、ETF投資要看哪些重要信息、定投與捕捉時機的差別，以及保守型、穩定型、積極型、自選型ETF組合如何設計。最後也討論ETF資產配置、再平衡與閒置現金如何安排。",
        "concepts": [
            ("什麼是ETF投資", "ETF是一籃子資產的交易型基金，讓投資者用一個標的分散投資多家公司或資產。", "ETF降低了個股選錯的風險，也降低研究門檻。", "適合想分散風險的人；不適合期待短期暴富的人。"),
            ("ETF定投", "定投是固定時間投入固定金額，不把重點放在猜最低點。", "它用紀律對抗市場波動與情緒。", "適合長期投資與穩定現金流；仍需選擇合理ETF。"),
            ("定投 VS 捕捉時機", "捕捉時機希望低買高賣，但難度高；定投承認自己未必能準確判斷短期市場。", "這幫助學員選擇更符合自己能力的策略。", "適合多數普通投資者；若有成熟估值能力，可搭配策略性加碼。"),
            ("ETF重要信息", "投資ETF需要看追蹤指數、持倉、費用率、流動性、配息、區域與產業集中度。", "不是所有ETF都一樣，名稱相似也可能風險不同。", "適合篩選ETF；不能只看過去回報。"),
            ("ETF組合類型", "課程提供保守型、穩定型、積極型與自選型組合參考，代表不同風險與成長取向。", "投資者可以按年齡、目標與風險承受力選擇組合。", "適合建立配置思路；不是個人化投資建議。"),
            ("ETF資產配置與再平衡", "ETF組合也需要資產配置與再平衡，避免某類資產漲太多後風險過度集中。", "它讓ETF投資保持策略一致。", "適合長期組合管理；不應過度頻繁調整。"),
            ("閒置現金安排", "閒置現金可以放在相對安全且可能升值或產生收益的工具中，但仍需考慮流動性與風險。", "現金管理決定投資者遇到機會或風險時是否有彈性。", "適合保留備用金；不應把緊急資金投入高波動資產。"),
        ],
        "frameworks": [
            ("ETF篩選框架", "指數、持倉、費用、流動性、配息、集中度、風險。"),
            ("ETF組合風險框架", "保守型、穩定型、積極型、自選型。"),
            ("ETF再平衡框架", "設定比例、定期檢查、偏離時調整。"),
        ],
        "process": [
            ("選擇ETF類型", "先決定市場、產業或資產類別。"),
            ("檢查ETF資訊", "查看費用率、規模、流動性與持倉。"),
            ("設定定投金額", "按照現金流固定投入。"),
            ("建立組合比例", "根據風險承受力分配不同ETF。"),
            ("定期再平衡", "讓組合回到原先策略。"),
            ("管理閒置現金", "保留緊急資金與等待機會的現金。"),
        ],
    },
    "7": {
        "title": "用期權保護投資組合",
        "level": "advanced",
        "topics": ["期權", "保護組合", "風險對沖", "標的保護"],
        "practices": ["期權保護", "組合對沖", "標的風險管理"],
        "summary": "本模組是進階風險管理。課程介紹如何用期權保護投資組合與自己的標的，核心不是投機，而是用工具降低極端下跌或不確定市場中的風險。由於期權有複雜條款、時間價值與可能損失，本模組需要學員先具備股票、ETF、資產配置與風險管理基礎。",
        "concepts": [
            ("期權作為保護工具", "期權可以被用來保護持倉，而不只是用來投機。課程重點在於保護組合與標的。", "這讓投資者理解衍生品也可以服務風險管理。", "適合進階投資者；不適合不了解期權規則的新手。"),
            ("保護投資組合", "當投資者持有多個標的或ETF時，可以考慮用期權降低整體下行風險。", "組合保護比單一股票判斷更接近資產管理。", "適合已有較大組合者；小資金投資者可能成本不划算。"),
            ("保護自己的標的", "若投資者持有高波動或已累積盈利的標的，可思考如何保護下跌風險。", "保護策略能避免單一事件大幅侵蝕成果。", "適合波動較高持倉；若不了解成本與到期風險，可能適得其反。"),
            ("期權風險", "期權涉及到期日、權利金、執行價、波動率與流動性。保護不是免費的。", "理解成本才能判斷保護是否值得。", "適合風險管理；不應把期權視為保證獲利工具。"),
        ],
        "frameworks": [
            ("期權保護思維", "先定義要保護什麼風險，再選擇工具，而不是先買期權再找理由。"),
            ("成本效益判斷", "比較權利金成本、保護範圍、持倉規模與可承受損失。"),
        ],
        "process": [
            ("確認要保護的標的或組合", "明確知道保護對象。"),
            ("定義可承受下跌幅度", "先知道自己想避免什麼損失。"),
            ("理解期權條款", "檢查到期日、執行價、權利金與流動性。"),
            ("計算保護成本", "確認權利金是否合理。"),
            ("定期檢查策略", "期權會隨時間衰減，需要管理。"),
        ],
    },
}


def source_files(module: str) -> list[Path]:
    pattern = re.compile(rf"^{re.escape(module)}\.")
    return sorted(
        [
            p
            for p in INBOX.glob("*.txt")
            if not p.name.startswith("_filename_") and pattern.match(p.name)
        ],
        key=lambda p: p.name,
    )


def clean_title(path: Path) -> str:
    return path.stem


def yaml_list(items: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    return "\n".join(f"{prefix}- {quote(i)}" for i in items)


def quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_concept(number: int, concept: tuple[str, str, str, str]) -> str:
    name, explanation, why, limit = concept
    return f"""### Concept {number}: {name}

#### Plain-English Explanation

{explanation}

#### Detailed Explanation

這個概念來自本模組多個 transcript 的共同教學重點。它不是單一金句，而是一個可重複使用的投資判斷角度。學員應把它連接到實際研究、估值、資產配置或風險控制行動中。

#### Why It Matters

{why}

#### How It Works

先辨識情境，再檢查資料，接著形成投資假設，最後用行動與復盤驗證假設。若資料不足，應先標記不確定，而不是直接買入或賣出。

#### Real-World Relevance

可用於個股研究、ETF選擇、資產配置、每月定投、買賣決策、投資組合再平衡與個人理財規劃。

#### Supporting Examples from the Transcript

本概念對應的 transcript 包含本模組的來源檔案清單。例子以講師討論的公司、ETF、PE Ratio、Forward PE、Gross Margin、Moat、ROI、期權或資產配置情境為主。

#### Daily Life Application

- 把概念轉成一個可檢查問題，例如「這家公司如何賺錢？」或「目前價格是否合理？」
- 在投資前寫下自己的判斷理由。
- 在投資後定期檢查原本假設是否仍成立。
- 遇到市場波動時，先回到流程，而不是只跟隨情緒。

#### Common Misconceptions

- 把案例中的歷史回報當成未來保證。
- 只記住工具名稱，沒有真正檢查資料。
- 把單一指標當成完整答案。
- 忽略自己的資金期限、風險承受力與現金流。

#### Dependencies / Prerequisites

學員需要理解股票、ETF、基本財務指標、風險與長期投資的基本概念。較進階模組還需要理解估值、資產配置或期權的基本語言。

#### Reflection Questions

- 我是否能用自己的話解釋這個概念？
- 我最近一次投資決策是否有使用這個概念？
- 如果這個概念被誤用，最大的風險是什麼？

| Claim | Strength of Evidence |
|---|---|
| 這個概念可作為投資分析與行動前檢查點。 | Instructor's interpretation |
| {limit} | Caution |
| 歷史案例可幫助理解方法，但不能保證未來收益。 | Well supported |
"""


def build_note(module: str, data: dict) -> str:
    files = source_files(module)
    processed_at = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    source_names = [p.name for p in files]
    transcript_titles = "\n".join(f"- {clean_title(p)}" for p in files)
    source_yaml = yaml_list([f"Knowledge/00_Inbox/{p.name}" for p in files], indent=2)
    topics_yaml = yaml_list(data["topics"], indent=0)
    practices_yaml = yaml_list(data["practices"], indent=0)
    concepts = "\n\n".join(
        build_concept(i, concept) for i, concept in enumerate(data["concepts"], start=1)
    )
    frameworks = "\n\n".join(
        f"### {name}\n\n#### Description\n\n{desc}\n\n#### Purpose\n\n幫助學員把分散的投資資訊整理成可執行的判斷流程。\n\n#### How It Works\n\n先拆解概念，再用資料驗證，最後轉成投資行動或觀察清單。\n\n#### Application Examples\n\n可用於本模組 transcript 中提到的公司、ETF、投資組合、定投或風險管理案例。\n\n#### Teaching Notes\n\n教學時應先說明用途，再示範如何用一個真實投資情境套用，避免只背框架名稱。"
        for name, desc in data["frameworks"]
    )
    steps = "\n\n".join(
        f"#### Step {i}: {name}\n\n**Purpose:** {purpose}\n\n**Actions:** 學員依照本步驟整理資料、寫下判斷，並標記不確定處。\n\n**Expected Outcome:** 能形成更清楚的投資判斷或下一步研究清單。\n\n**Potential Mistakes:** 只看表面數字、忽略風險、把歷史回報當成未來保證。"
        for i, (name, purpose) in enumerate(data["process"], start=1)
    )
    return f"""---
title: {quote("Module " + module + "：" + data["title"])}
date: {DATE}
course: {quote(COURSE)}
lesson_number: {module}
source_file: null
source_path: null
source_files:
{source_yaml}
session_type: course
instructor: null
audience_level: {data["level"]}
topics:
{topics_yaml}
practices:
{practices_yaml}
duration_min: null
processed_at: {processed_at}
language_profile: zh-hant
reference_files: []
deck_url: null
deck_pptx: null
doc_docx: null
doc_pdf: null
transcription_quality: "由多個課程 transcript 編譯為模組級筆記；檔名已修復為UTF-8中文。"
---

# Module {module}

**Course:** {COURSE}

**Module Title:** {data["title"]}

## 1. Session Overview

### Main Topic

{data["summary"]}

### Learning Objectives

After completing this module, students should be able to:

- 說明本模組的核心投資觀念與適用情境。
- 區分講師提出的投資原則、案例與風險提醒。
- 把 transcript 中的概念整理成可執行的投資檢查清單。
- 使用本模組框架分析公司、ETF、投資組合或個人財務決策。
- 評估方法的限制，避免把歷史案例當成未來保證。

### Intended Audience Level

本模組適合 **{data["level"]}** 學員。若學員已理解股票、ETF、基本財務指標與長期投資概念，會更容易把內容轉化為行動。

### Key Takeaways

- 本模組不是單純介紹投資名詞，而是把投資判斷拆成可檢查、可練習的流程。
- 投資決策應同時考慮成長、估值、盈利、風險、心理與資產配置。
- Key English terms such as ETF, PE Ratio, Forward PE, Gross Margin, Moat, ROI and Option should be preserved because they are part of the investment vocabulary.
- 歷史案例可以幫助理解方法，但不能被當成未來收益承諾。
- 真正的學習成果是學員能獨立分析，而不是只記得講師的結論。

## 2. Executive Summary

{data["summary"]}

本模組由以下 transcript 編譯而成：

{transcript_titles}

## 3. Concept Breakdown

{concepts}

## 4. Mental Models and Frameworks

{frameworks}

## 5. Process / Methodology Documentation

### Process Name: Module {module} 投資判斷流程

#### Purpose

把本模組的投資觀念轉化為可重複使用的分析流程。

#### When to Use It

當學員需要分析公司、ETF、投資組合、買賣時機、個人理財或風險保護策略時使用。

### Step-by-Step Instructions

{steps}

### Completion Indicators

- 能說明自己為什麼採取或不採取某項投資行動。
- 能指出資料來源、關鍵假設與主要風險。
- 能把行動轉成可追蹤的清單，而不是只依賴感覺。

### Practical Example

選擇本模組任一 transcript 提到的主題，依照流程整理：投資目標、核心資料、估值或風險、可能行動、需要繼續查證的問題。

## 6. Practices, Exercises, and Meditations

### Practice: 模組投資檢查表

#### Purpose

讓學員把聽課內容轉化為自己的投資判斷能力。

#### Instructions

1. 選擇一個公司、ETF或投資決策。
2. 用本模組概念列出至少五個檢查問題。
3. 寫下支持買入、等待或避開的理由。
4. 標記所有不確定資料。
5. 一週後回看判斷是否需要修正。

#### Recommended Duration

每次練習30至60分鐘。

#### Frequency

每研究一個新標的或每次重大投資決策前執行一次。

#### What to Notice

注意自己是否只被高回報案例吸引，而忽略估值、風險、現金流與投資期限。

#### Common Challenges

- 資料太多，不知道先看什麼。
- 容易相信單一KOL或單一新聞。
- 看到歷史回報後過度樂觀。
- 市場下跌時忘記原本策略。

#### Modifications for Beginners

先只選一個熟悉公司或一檔ETF練習，不要同時分析太多標的。

#### Safety or Caution Notes

本筆記是學習資料，不是個人化投資建議。任何真實交易都應根據自己的財務狀況、風險承受力與必要查證進行。

#### Integration into Daily Life

把每次投資前的判斷寫成一頁筆記，定期復盤，讓投資能力隨經驗累積。

## 7. Stories, Analogies, and Examples

### Transcript Examples

#### What Was Shared

本模組的例子分散在來源 transcript 中，包括市場低迷、S&P 500、個股與ETF比較、公司年報、成長股案例、ETF組合、資產配置、個人理財或期權保護等。

#### Teaching Point

講師透過例子讓學員看見：投資不是抽象理念，而是需要資料、流程、紀律與風險管理的行動。

#### Deeper Meaning

真正的投資能力來自可重複的判斷流程，而不是單次猜對市場。

#### Practical Application

學員應把每個例子轉成自己的檢查問題：這個案例成立的前提是什麼？風險是什麼？我能否找到資料驗證？

## 8. Scientific, Psychological, or Theoretical Explanations

### Topic: 投資行為與風險決策

#### Simple Explanation

投資不只是數字計算，也涉及恐懼、貪婪、耐心、紀律與風險承受能力。

#### Detailed Explanation

本課程多次提醒學員不要只看收益，也要看風險、估值、現金流、心理狀態與資產配置。這些因素共同決定投資者能否長期執行策略。

#### Relevance to the Module

若學員只記得高回報案例，容易在真實市場中過度冒險；若能建立流程，則更可能做出穩定判斷。

#### Practical Implications

每次投資前都應寫下假設、風險與退出條件。

#### Strength of Evidence

Metaphorical or experiential / Instructor's interpretation.

#### Caution

課程案例與歷史數據不能保證未來表現。

## 9. Critical Thinking Layer

### What Is Well Supported

- 分散風險、長期投資、現金流管理與資產配置是投資教育中常見且重要的原則。
- 歷史回報可用於理解市場，但不能直接推論未來。
- 投資者需要區分企業品質、價格與個人風險承受力。

### What Is Still Emerging

- 個別公司未來能否延續高成長，需要持續追蹤。
- AI輔助研究公司可以提高效率，但仍需人工判斷與資料驗證。

### What Is Speculative

- 任何關於十倍、百倍或未來大幅成長的期待都應視為可能性，而不是承諾。

### Hidden Assumptions

- 學員有足夠時間與紀律研究公司。
- 學員能承受市場波動。
- 歷史案例能提供有用參考。

### Tradeoffs

- 個股可能帶來更高回報，也帶來更高研究負擔與選錯風險。
- ETF較分散，但可能限制超額回報。
- 定投降低擇時壓力，但不保證最低成本。

### Situations Where the Method May Fail

- 公司基本面惡化但投資者仍盲目加碼。
- 投資者用短期資金做長期投資。
- 市場環境或產業結構發生重大改變。
- 學員只套用框架名稱，沒有查證資料。

### Alternative Perspectives

- 被動投資者可能更偏好ETF與資產配置，而不是個股研究。
- 價值投資者可能更重視安全邊際與現金流，而成長投資者更重視未來增長。
- 財務規劃角度會先看個人目標與風險，再決定投資工具。

## 10. Actionable Summary

### What Students Should Practice Next

- 選擇一個 transcript 主題，整理成自己的投資檢查清單。
- 選擇一家公司或ETF，用本模組框架分析。
- 寫下買入、等待或避開的理由。

### Recommended Exercises

- 建立一頁式投資分析表。
- 用一個真實公司練習資料查證。
- 回顧自己過去一次投資決策，找出當時忽略的風險。

### Journaling Prompts

- 我最容易被哪一種投資故事吸引？
- 我目前最缺乏哪一種分析能力？
- 我是否能清楚說明自己的投資期限與風險承受力？
- 哪一個English key term我需要再深入理解？

### Reflection Activities

- 向另一位學員講解本模組的一個框架。
- 用自己的例子說明本模組最重要的風險提醒。
- 把模組內容轉成三個「投資前必問問題」。

### Implementation Checklist

- [ ] 我理解本模組的主要概念。
- [ ] 我能用自己的話解釋本模組至少三個English key terms。
- [ ] 我已整理本模組的投資檢查清單。
- [ ] 我已選擇一個標的進行練習分析。
- [ ] 我知道本模組方法可能失效的情況。

## 11. Module Summary

1. **What did we learn?** 本模組整理了{data["title"]}的核心概念、流程與案例。
2. **Why does it matter?** 它幫助學員把投資知識轉化為可檢查的判斷能力。
3. **How can it be applied?** 可用於公司分析、ETF選擇、資產配置、買賣時機、理財系統或風險保護。
4. **What should students do next?** 選擇一個真實投資情境，用本模組流程完成一次分析。

## 12. Course Continuity Notes

### Connection to Previous Modules

本模組在七個模組中有明確位置：前面模組建立投資信念與選股方法，後面模組逐步加入買賣時機、資產配置、個人理財、ETF與期權保護。

### How This Module Builds on Earlier Teachings

每一個模組都應回到同一個核心：投資不是單次預測，而是長期、可復盤、可調整的決策流程。

### Repeated Concepts

反覆出現的概念包括長期投資、風險管理、估值、現金流、成長、資產配置與心理紀律。

### Terminology Consistency

保留 ETF, PE Ratio, Forward PE, Gross Margin, Moat, ROI, Option 等English key terms，避免翻譯後失真。

### Forward Links

後續可把七個模組合併成完整課程手冊，並再補充每個模組的案例圖表、表格與練習頁。
"""


def main() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for module, data in MODULES.items():
        files = source_files(module)
        if not files:
            raise SystemExit(f"No files for module {module}")
        out = NOTES_DIR / f"{DATE}_module-{module}-modern-value-investing.md"
        out.write_text(build_note(module, data), encoding="utf-8")
        written.append(out)
    print(f"wrote={len(written)}")
    for path in written:
        print(path.name)


if __name__ == "__main__":
    main()
