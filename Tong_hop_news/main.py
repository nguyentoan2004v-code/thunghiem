from datetime import datetime
from scrapers.vnexpress_scraper import get_articles as vne
from scrapers.haituh_scraper import get_articles as haitu
from scrapers.tuoitre_scraper import get_articles as tt
from db import save_article, get_conn, get_category_id_by_name, add_article_category

# --- BỘ TỪ KHÓA ĐÃ TỐI ƯU (Thể thao ưu tiên cao nhất) ---
KEYWORDS = {
    "Thể thao": [
        # Bóng đá
        "bóng đá", "v-league", "hlv", "huấn luyện viên", "cầu thủ", "đội tuyển", "trận đấu", "bàn thắng", "cup", 
        "giải đấu", "fifa", "sea games", "world cup", "premier league", "champions league", "euro", "penalty", 
        "sút phạt", "thủ môn", "hậu vệ", "tiền đạo", "tiền vệ", "đá bóng", "bóng", "sân cỏ", "trọng tài",
        "thẻ đỏ", "thẻ vàng", "việt vị", "phạt góc", "aff cup", "asian cup", "manchester", "barcelona", "real madrid",
        
        # Các môn thể thao khác
        "bóng rổ", "nba", "bóng chuyền", "quần vợt", "tennis", "cầu lông", "badminton", "bơi lội", "điền kinh",
        "võ thuật", "boxing", "muay thái", "taekwondo", "karate", "judo", "đấu vật", "marathon", "golf",
        "đua xe", "f1", "motogp", "billiards", "bi-a", "cờ vua", "esports", "thể hình", "gym", "yoga",
        
        # Thuật ngữ chung
        "vận động viên", "câu lạc bộ", "clb", "tuyển thủ", "sân vận động", "khán giả", "cổ động viên", 
        "thể dục", "huy chương", "thể thao", "kỷ lục", "vô địch", "á quân", "chiến thắng", "thua cuộc",
        "huấn luyện", "tập luyện", "thể lực", "thi đấu", "giải vô địch", "olympic", "asiad", "đội bóng",
        "liên đoàn", "phạt đền", "hiệp đấu", "tỷ số", "ghi bàn", "chấn thương", "sa thải"
    ],
    
    "Kinh doanh": [
        # Chứng khoán & tài chính
        "chứng khoán", "cổ phiếu", "vn-index", "vnindex", "hose", "hnx", "upcom", "trái phiếu", "cổ tức",
        "niêm yết", "giao dịch", "đầu tư", "nhà đầu tư", "quỹ đầu tư", "margin", "futures", "derivatives",
        
        # Ngân hàng
        "ngân hàng", "lãi suất", "tín dụng", "cho vay", "khoản vay", "thẻ tín dụng", "atm", "vietcombank",
        "agribank", "bidv", "vietinbank", "techcombank", "mbbank", "tpbank", "tiền gửi", "ngân hàng trung ương",
        "sbv", "nợ xấu", "tái cơ cấu", "lãi suất điều hành",
        
        # Kinh tế & doanh nghiệp
        "doanh nghiệp", "công ty", "tập đoàn", "tổng công ty", "cổ phần", "tnhh", "khởi nghiệp", "startup",
        "vingroup", "viettel", "fpt", "masan", "hòa phát", "vnsteel", "pv", "petrovietnam", "evn",
        "ceo", "tổng giám đốc", "chủ tịch hđqt", "doanh thu", "lợi nhuận", "thua lỗ", "phá sản", "m&a",
        "sáp nhập", "mua bán", "thương vụ", "hợp đồng", "thương mại", "xuất khẩu", "nhập khẩu", "kim ngạch",
        
        # Thị trường & hàng hóa
        "thị trường", "kinh tế", "gdp", "tăng trưởng", "lạm phát", "cpi", "tỷ giá", "ngoại hối", "vnd", "usd",
        "đồng đô la", "vàng", "giá vàng", "sjc", "bất động sản", "nhà đất", "căn hộ", "chung cư", "đất nền",
        "xăng dầu", "giá xăng", "petrolimex", "điện", "nước", "viễn thông", "hàng không", "logistics",
        "tài chính", "thuế", "ngân sách", "dự án", "đấu thầu", "đầu tư công", "fdi", "oda"
    ],
    
    "Công nghệ": [
        # Thiết bị & thương hiệu
        "smartphone", "điện thoại", "iphone", "samsung", "xiaomi", "oppo", "vivo", "huawei", "nokia",
        "apple", "google", "microsoft", "meta", "facebook", "amazon", "tesla", "nvidia",
        "máy tính", "laptop", "pc", "macbook", "ipad", "tablet", "smartwatch", "tai nghe", "airpods",
        "chip", "vi xử lý", "ram", "ssd", "gpu", "cpu", "processor", "snapdragon",
        
        # Công nghệ & phần mềm
        "công nghệ", "ai", "trí tuệ nhân tạo", "chatgpt", "openai", "machine learning", "deep learning",
        "phần mềm", "ứng dụng", "app", "android", "ios", "windows", "macos", "linux",
        "mạng xã hội", "social media", "tiktok", "youtube", "instagram", "twitter", "x", "threads",
        "internet", "mạng", "wifi", "5g", "4g", "viễn thông", "viettel", "mobifone", "vinaphone",
        "cloud", "đám mây", "server", "data center", "blockchain", "crypto", "bitcoin", "nft",
        "metaverse", "vr", "ar", "thực tế ảo", "game", "gaming", "esports",
        
        # An ninh mạng
        "virus", "malware", "hack", "hacker", "an ninh mạng", "bảo mật", "mã hóa", "lừa đảo trực tuyến",
        "ransomware", "phishing", "ddos", "data breach", "rò rỉ dữ liệu", "password", "firewall",
        
        # Công nghệ mới
        "drone", "robot", "tự động hóa", "iot", "internet vạn vật", "smart home", "nhà thông minh",
        "xe tự lái", "ev", "xe điện", "năng lượng mặt trời", "pin", "sạc nhanh", "công nghệ sinh học"
    ],
    
    "Pháp luật": [
        # Tội phạm & điều tra
        "công an", "cảnh sát", "bắt giữ", "bắt giam", "khám xét", "điều tra", "truy nã", "lệnh truy nã",
        "khởi tố", "tội phạm", "phạm tội", "tội danh", "án mạng", "giết người", "trộm cắp", "cướp giật",
        "cướp", "lừa đảo", "lừa đảo chiếm đoạt", "chiếm đoạt", "tham ô", "tham nhũng", "hối lộ", "đưa hối lộ",
        "ma túy", "ma tuý", "buôn bán ma túy", "tàng trữ", "vận chuyển", "mua bán", "bạo hành", "cưỡng đoạt",
        
        # Tòa án & xét xử
        "tòa án", "xét xử", "phiên tòa", "tòa", "thẩm phán", "luật sư", "biện hộ", "tranh tụng",
        "bị cáo", "bị hại", "nguyên đơn", "bị đơn", "chứng cứ", "kháng cáo", "kháng nghị", "giám đốc thẩm",
        "án", "bản án", "y án", "hủy án", "hoãn án", "hoãn thi hành án", "miễn trách nhiệm",
        
        # Hình phạt
        "tù", "tù chung thân", "tử hình", "án tử", "thi hành án", "phạt tù", "cải tạo", "quản chế",
        "phạt tiền", "tịch thu", "sung công", "bồi thường", "truy thu", "xử phạt", "vi phạm hành chính",
        
        # Luật & quy định
        "luật", "bộ luật", "nghị định", "thông tư", "quy định", "điều luật", "hiến pháp", "dân luật",
        "hình luật", "lao động", "hôn nhân gia đình", "đất đai", "vi phạm", "trái phép", "bất hợp pháp",
        "giấy phép", "chấp hành", "tuân thủ", "minh oan", "oan sai", "kháng án", "vụ án", "hồ sơ"
    ],
    
    "Giáo dục": [
        # Học sinh & sinh viên
        "học sinh", "sinh viên", "học viên", "nghiên cứu sinh", "ncs", "tiến sĩ", "thạc sĩ", "cử nhân",
        "trẻ em", "thiếu nhi", "thiếu niên", "thanh niên", "tuổi teen",
        
        # Trường học
        "trường học", "trường", "nhà trường", "mẫu giáo", "mầm non", "tiểu học", "thcs", "thpt",
        "đại học", "cao đẳng", "trung cấp", "dạy nghề", "phổ thông", "chuyên biệt",
        "quốc tế", "quốc gia", "bách khoa", "kinh tế", "sư phạm", "y dược", "nông nghiệp", "kỹ thuật",
        
        # Thi cử & tuyển sinh
        "thi", "kỳ thi", "thi tốt nghiệp", "tốt nghiệp thpt", "thi thpt", "tuyển sinh", "xét tuyển",
        "điểm thi", "điểm chuẩn", "nguyện vọng", "đăng ký", "hồ sơ", "đề thi", "bài thi", "giấy báo",
        "thí sinh", "cán bộ coi thi", "gian lận", "chép bài", "thi lại", "thi đại học", "thi vào 10",
        
        # Giảng dạy
        "giáo viên", "thầy", "cô", "thầy cô", "giảng viên", "giáo sư", "phó giáo sư", "bộ giáo dục",
        "sở giáo dục", "phòng giáo dục", "bộ gdđt", "đào tạo", "giảng dạy", "chương trình", "sách giáo khoa",
        "sgk", "giáo trình", "học liệu", "giáo án", "bài giảng", "dạy học", "lớp học", "lớp",
        
        # Học tập
        "học phí", "học bổng", "miễn giảm", "hỗ trợ", "chi phí", "bằng cấp", "văn bằng", "chứng chỉ",
        "học kỳ", "năm học", "khai giảng", "bế giảng", "nghỉ học", "học online", "elearning", "zoom",
        "điểm", "điểm số", "đánh giá", "thi học kỳ", "kiểm tra", "bài tập", "đồ án", "luận văn", "luận án",
        "nghiên cứu", "khoa học", "ngoại ngữ", "tiếng anh", "ielts", "toeic", "toán", "văn", "lý", "hóa"
    ],
    
    "Sức khỏe": [
        # Y tế & bệnh viện
        "bệnh viện", "phòng khám", "trạm y tế", "trung tâm y tế", "bệnh viện đa khoa", "chuyên khoa",
        "bác sĩ", "y sĩ", "y tá", "điều dưỡng", "dược sĩ", "hộ sinh", "kỹ thuật viên",
        "khám bệnh", "khám", "chữa bệnh", "điều trị", "chữa trị", "cấp cứu", "icu", "hồi sức",
        "bệnh nhân", "người bệnh", "ca bệnh", "trường hợp", "sức khỏe", "y tế", "chăm sóc sức khỏe",
        
        # Bệnh tật
        "bệnh", "dịch bệnh", "dịch", "covid", "covid-19", "sars-cov-2", "cúm", "sốt xuất huyết",
        "sốt", "ho", "khó thở", "đau", "đau đầu", "đau bụng", "tiêu chảy", "ói mửa",
        "ung thư", "ung thư phổi", "ung thư gan", "ung thư dạ dày", "bướu", "u", "ác tính", "lành tính",
        "tim mạch", "đột quỵ", "tai biến", "nhồi máu", "huyết áp", "đái tháo đường", "tiểu đường",
        "suy thận", "suy gan", "suy tim", "viêm gan", "xơ gan", "lao", "hiv", "aids", "lây nhiễm",
        "virus", "vi rút", "vi khuẩn", "nhiễm trùng", "nhiễm khuẩn", "ngộ độc", "dị ứng",
        
        # Điều trị & thuốc
        "thuốc", "dược", "kháng sinh", "giảm đau", "hạ sốt", "vitamin", "sinh tố", "vacxin", "vắc xin",
        "tiêm chủng", "tiêm", "tiêm phòng", "xét nghiệm", "test", "chẩn đoán", "siêu âm", "x-quang",
        "ct scan", "mri", "nội soi", "phẫu thuật", "mổ", "phẫu", "cấy ghép", "ghép tạng", "hiến",
        "truyền máu", "máu", "huyết", "liều", "đơn thuốc", "toa thuốc", "kê đơn",
        
        # Dinh dưỡng & sức khỏe
        "dinh dưỡng", "ăn uống", "chế độ ăn", "thực phẩm", "thực đơn", "calo", "protein", "chất béo",
        "tinh bột", "carb", "chất xơ", "khoáng chất", "canxi", "sắt", "kẽm", "omega",
        "giảm cân", "tăng cân", "béo phì", "thừa cân", "thiếu cân", "suy dinh dưỡng", "bổ dưỡng",
        "tập luyện", "vận động", "thể dục", "rèn luyện", "sức khỏe thể chất", "sức khỏe tinh thần",
        "trầm cảm", "lo âu", "stress", "căng thẳng", "tâm lý", "tư vấn tâm lý"
    ],
    
    "Giải trí": [
        # Nghệ sĩ & người nổi tiếng
        "ca sĩ", "danh ca", "nghệ sĩ", "nghệ sỹ", "diễn viên", "tài tử", "ngôi sao", "sao", "sao việt",
        "người mẫu", "model", "hoa hậu", "á hậu", "hoa khôi", "miss", "mister", "quán quân",
        "mc", "host", "dẫn chương trình", "biên đạo", "đạo diễn", "nhạc sĩ", "nhạc sỹ", "nhà sản xuất",
        
        # Showbiz
        "showbiz", "làng giải trí", "giới giải trí", "vbiz", "kbiz", "vpop", "kpop", "cpop",
        "drama", "scandal", "ồn ào", "thị phi", "tin đồn", "hẹn hò", "yêu đương", "chia tay", "ly hôn",
        "kết hôn", "đám cưới", "sinh con", "mang thai", "có bầu", "thảm đỏ", "sự kiện", "lễ trao giải",
        
        # Âm nhạc
        "nhạc", "âm nhạc", "bài hát", "ca khúc", "single", "album", "mv", "music video", "clip",
        "concert", "liveshow", "show diễn", "biểu diễn", "trình diễn", "tour diễn", "fanmeeting",
        "rapper", "dj", "producer", "hit", "bảng xếp hạng", "trending", "vpop chart",
        
        # Phim ảnh
        "phim", "điện ảnh", "phim chiếu rạp", "phim truyền hình", "series", "phim bộ", "phim truyện",
        "rạp phim", "cgv", "lotte", "galaxy", "đạo diễn", "kịch bản", "dàn cast", "quay phim",
        "trailer", "teaser", "ra rạp", "premiere", "liên hoan phim", "oscar", "cannes", "giải thưởng",
        
        # Truyền hình
        "truyền hình", "tv", "kênh", "vtv", "htv", "viettel tv", "fpt play", "netflix", "gameshow",
        "show", "chương trình", "talk show", "reality show", "thi thố", "cuộc thi", "giám khảo",
        "thí sinh", "ban giám khảo", "ban tổ chức", "sản xuất", "tập", "phát sóng", "lên sóng"
    ],
    
    "Đời sống": [
        # Gia đình
        "gia đình", "bố mẹ", "cha mẹ", "con cái", "vợ chồng", "anh chị em", "họ hàng", "bà con",
        "thế hệ", "hôn nhân", "kết hôn", "ly hôn", "li dị", "đám cưới", "cưới", "nuôi con", "sinh đẻ",
        
        # Tình yêu & quan hệ
        "tình yêu", "yêu", "yêu đương", "tình cảm", "hẹn hò", "bạn gái", "bạn trai", "người yêu",
        "chia tay", "tình dục", "tình dục an toàn", "quan hệ", "thủ dâm", "xuất tinh",
        
        # Du lịch
        "du lịch", "lữ hành", "tour", "khách sạn", "resort", "homestay", "villa", "booking",
        "vé máy bay", "hàng không", "sân bay", "điểm đến", "check in", "cảnh đẹp", "phượt",
        "đi chơi", "nghỉ dưỡng", "kỳ nghỉ", "du khách", "khách du lịch", "hướng dẫn viên",
        "hà nội", "sài gòn", "đà nẵng", "nha trang", "phú quốc", "đà lạt", "hạ long", "sapa",
        
        # Ẩm thực
        "ẩm thực", "món ăn", "đồ ăn", "thức ăn", "nấu ăn", "nấu nướng", "công thức", "recipe",
        "nhà hàng", "quán ăn", "quán", "buffet", "food", "foodie", "food tour", "review đồ ăn",
        "phở", "bún", "cơm", "bánh mì", "chả giò", "gỏi cuốn", "cà phê", "trà sữa", "milk tea",
        
        # Thời trang & làm đẹp
        "thời trang", "fashion", "quần áo", "váy", "áo", "giày dép", "túi xách", "phụ kiện",
        "làm đẹp", "beauty", "skincare", "makeup", "trang điểm", "mỹ phẩm", "serum", "kem dưỡng",
        "chăm sóc da", "spa", "salon", "tóc", "nail", "cắt tóc", "nhuộm tóc", "làm móng",
        "giảm cân", "detox", "làm trắng", "trẻ hóa", "căng da", "tiêm filler", "botox",
        
        # Nhà cửa & đời sống
        "nhà cửa", "trang trí", "nội thất", "thiết kế", "xây dựng", "sửa chữa", "nhà đẹp",
        "mẹo vặt", "tips", "hacks", "lifehacks", "diy", "tự làm", "handmade",
        "mua sắm", "shopping", "sale", "giảm giá", "khuyến mãi", "voucher", "flash sale",
        "thú cưng", "pet", "chó", "mèo", "cá cảnh", "chim", "nuôi thú"
    ],
    
    "Chính trị - Xã hội": [
        # Chính quyền trung ương
        "chính phủ", "thủ tướng", "thủ tướng chính phủ", "phó thủ tướng", "bộ trưởng", "bộ", "cơ quan",
        "quốc hội", "đại biểu quốc hội", "chủ tịch quốc hội", "phó chủ tịch", "ủy ban thường vụ",
        "tổng bí thư", "bộ chính trị", "ban chấp hành trung ương", "trung ương", "đảng", "đảng cộng sản",
        "chủ tịch nước", "chủ tịch", "thường trực", "ủy ban", "hội đồng", "thanh tra chính phủ",
        
        # Chính quyền địa phương
        "tỉnh", "thành phố", "quận", "huyện", "xã", "phường", "thị trấn", "địa phương",
        "chủ tịch tỉnh", "bí thư tỉnh", "hội đồng nhân dân", "ủy ban nhân dân", "ubnd", "hđnd",
        
        # Chính sách & luật lệ
        "nghị định", "quyết định", "nghị quyết", "chỉ thị", "thông tư", "công văn", "chính sách",
        "quy định", "quy chế", "chiến lược", "đề án", "kế hoạch", "chương trình", "dự án",
        "cải cách", "đổi mới", "phát triển", "xây dựng", "nông thôn mới", "đô thị hóa",
        
        # Xã hội
        "xã hội", "dân sinh", "đời sống", "nhân dân", "người dân", "công dân", "cư dân",
        "bảo hiểm xã hội", "bhxh", "bảo hiểm y tế", "bhyt", "trợ cấp", "phúc lợi", "an sinh",
        "hộ nghèo", "nghèo đói", "giảm nghèo", "thoát nghèo", "thu nhập", "lương", "tiền công",
        
        # Thời tiết & thiên tai
        "thời tiết", "dự báo thời tiết", "mưa", "nắng", "nóng", "rét", "lạnh", "gió",
        "bão", "áp thấp nhiệt đới", "áp thấp", "siêu bão", "tâm bão", "gió bão", "sóng", "triều cường",
        "lũ", "lũ lụt", "ngập", "ngập úng", "ngập lụt", "hạn hán", "khô hạn", "thiếu nước",
        "thiên tai", "thảm họa", "động đất", "sạt lở", "lở đất", "sụt lở", "cháy rừng",
        "cứu hộ", "cứu nạn", "ứng phó", "phòng chống", "bão lũ", "sơ tán", "di dời",
        
        # Giao thông & hạ tầng
        "giao thông", "đường sá", "đường bộ", "đường cao tốc", "cao tốc", "quốc lộ", "tỉnh lộ",
        "cầu", "hầm", "nút giao", "vòng xuyến", "đường sắt", "metro", "mrt", "tàu điện ngầm",
        "sân bay", "cảng", "bến xe", "ga", "tắc đường", "ùn tắc", "tai nạn", "tai nạn giao thông",
        "tngt", "va chạm", "đâm", "tông", "lật xe", "xe tải", "xe khách", "ô tô", "xe máy",
        "giao thông công cộng", "bus", "xe buýt", "taxi", "grab", "be", "uber",
        
        # Vấn đề xã hội
        "ô nhiễm", "môi trường", "rác thải", "nước thải", "khí thải", "ô nhiễm không khí",
        "biến đổi khí hậu", "nóng lên toàn cầu", "bảo vệ môi trường", "xanh", "sạch", "đẹp",
        "an ninh", "an toàn", "trật tự", "trị an", "tệ nạn xã hội", "cờ bạc", "mại dâm",
        "bạo lực", "bạo lực gia đình", "xâm hại", "xâm hại tình dục", "quấy rối", "hiếp dâm"
    ]
}
# ----------------------------------

def classify_news(title, content_snippet=""):
    """Hàm tự động đoán chủ đề bài báo dựa trên Tiêu đề và 1 phần Nội dung"""
    text = (title + " " + content_snippet).lower()
    
    # Duyệt qua từng Category theo thứ tự ưu tiên
    for category, keys in KEYWORDS.items():
        for key in keys:
            if key in text:
                return category # Trả về Category đầu tiên tìm thấy (Thể thao)
    
    # Nếu không khớp với bất kỳ từ khóa nào, mặc định là Chính trị - Xã hội
    return "Chính trị - Xã hội" 

def collect():
    print(f"\n--- BẮT ĐẦU QUÉT: {datetime.now()} ---")
    conn = get_conn()
    
    for src_name, func in [("VnExpress", vne), ("24h", haitu), ("Tuổi Trẻ", tt)]:
        print(f"\n>> Đang lấy tin từ: {src_name}...")
        try:
            articles = func()
            
            for art in articles:
                # 1. LƯU BÀI VIẾT
                article_id = save_article(
                    art["title"], art["link"], art["content"], 
                    art["source"], art["published_date"], art["image_url"]
                )
                
                # 2. PHÂN LOẠI TIN
                if article_id:
                    snippet = art["content"][:100] 
                    cat_name = classify_news(art["title"], snippet)
                    
                    # 3. GẮN NHÃN VÀO DATABASE
                    cat_id = get_category_id_by_name(conn, cat_name)
                    if cat_id:
                        add_article_category(conn, article_id, cat_id)
        except Exception as e:
            print(f"Lỗi NGHIÊM TRỌNG tại nguồn {src_name}: {e}")

    conn.close()
    print("\n--- HOÀN TẤT ---")

if __name__ == "__main__":
    collect()