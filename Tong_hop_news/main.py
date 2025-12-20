from datetime import datetime
from scrapers.vnexpress_scraper import get_articles as vne
from scrapers.haituh_scraper import get_articles as haitu
from scrapers.tuoitre_scraper import get_articles as tt
from db import save_article, get_conn, get_category_id_by_name, add_article_category

# --- BỘ TỪ KHÓA ĐÃ TỐI ƯU (Thể thao ưu tiên cao nhất) ---
KEYWORDS = {
     "Thể thao": [

        "bóng đá", "v-league", "hlv", "cầu thủ", "đội tuyển", "trận đấu", "bàn thắng", "cup", 
        "vận động viên", "giải đấu", "fifa", "sea games", "bóng rổ", "bóng chuyền", "quần vợt", 
        "câu lạc bộ", "clb", "tuyển thủ", "sân vận động", "số 10", "tiền vệ", "đội bóng", "trận hòa", "đối thủ",
        "pickleball", "padel", "teqball", "var", "việt vị", "chuyển nhượng", "hat-trick", 
        "ghi bàn", "kiến tạo", "thẻ đỏ", "thẻ vàng", "huy chương", "thế vận hội", "olympic"
    ],
    "Kinh doanh": [
        "chứng khoán", "ngân hàng", "tỷ giá", "doanh nghiệp", "kinh tế", "lãi suất", "bất động sản", 
        "xăng dầu", "tài chính", "thị trường", "khoản vay", "tập đoàn", "lạm phát", "gdp", "cổ phiếu", 
        "trái phiếu", "vàng sjc", "đấu giá", "xuất khẩu", "nhập khẩu", "thương mại", "ceo", "phá sản"
    ],
    "Công nghệ": [
        "smartphone", "ai", "trí tuệ nhân tạo", "apple", "samsung", "công nghệ", "ứng dụng", "phần mềm", 
        "virus", "chatgpt", "iphone", "google", "metaverse", "chip", "máy tính", "laptop", "blockchain", 
        "kỹ thuật số", "an ninh mạng", "hacker", "mạng xã hội", "nền tảng", "algorithm", "thuật toán"
    ],
    "Pháp luật": [
        "công an", "bắt giữ", "khởi tố", "tội phạm", "án mạng", "tòa án", "vi phạm", "trộm cắp", 
        "điều tra", "cảnh sát", "xét xử", "tù", "ma túy", "tham nhũng", "bị cáo", "bị can", 
        "luật sư", "hình sự", "dân sự", "tranh chấp", "lừa đảo"
    ],
    "Giáo dục": [
        "học sinh", "sinh viên", "đại học", "trường học", "thi tốt nghiệp", "bộ giáo dục", "thầy cô", 
        "học phí", "tuyển sinh", "tiến sĩ", "bằng cấp", "giáo viên", "đào tạo", "du học", "học bổng", "sách giáo khoa"
    ],
    "Sức khỏe": [
        "bệnh viện", "bác sĩ", "ung thư", "covid", "sức khỏe", "y tế", "thuốc", "phẫu thuật", 
        "virus", "dinh dưỡng", "ngộ độc", "vacxin", "khám bệnh", "bệnh nhân", "cấp cứu", 
        "dịch bệnh", "đột quỵ", "tiểu đường", "thực phẩm chức năng"
    ],
    "Giải trí": [
        "hoa hậu", "ca sĩ", "diễn viên", "showbiz", "nghệ sĩ", "phim", "nhạc", "concert", 
        "người mẫu", "sao việt", "thảm đỏ", "truyền hình", "mv", "liveshow", "rạp phim", "drama"
    ],
  
    "Đời sống": [
        "du lịch", "ẩm thực", "gia đình", "tình yêu", "mẹo vặt", "thời trang", "làm đẹp", "hôn nhân", 
        "nhà cửa", "món ngon", "địa điểm", "check-in"
    ],
    "Chính trị - Xã hội": [
        "chính phủ", "thủ tướng", "bộ trưởng", "nghị định", "quốc hội", "tổng bí thư", "bão", "lũ", 
        "giao thông", "nhà nước", "thời tiết", "chủ tịch", "tỉnh", "thành phố", "ủy ban", "đề xuất", 
        "quy hoạch", "dự án", "cao tốc"
    ],
    "Thế giới": [
        
        "quốc tế", "thế giới", "toàn cầu", "global", "international", "ngoại giao", "diplomatic",
        "hội nghị", "thượng đỉnh", "summit", "đối thoại", "hội đàm", "thỏa thuận", "hiệp định",
        "ký kết", "hợp tác", "cooperation", "quan hệ", "đối tác", "chiến lược", "liên minh",
        "đồng minh", "ngoại trưởng", "bộ trưởng ngoại giao", "đại sứ", "lãnh sự", "đại sứ quán"]
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