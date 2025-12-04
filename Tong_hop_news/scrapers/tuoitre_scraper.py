import requests
import datetime
from bs4 import BeautifulSoup
import re 

def is_valid_image_url(url):
    if not url: return False
    url = url.lower()
    # Chỉ lọc những từ khóa rác thực sự, nới lỏng điều kiện
    garbage = ['icon', 'banner', 'ads', 'advert', 'sponsored']
    if any(k in url for k in garbage): return False
    return True

def get_articles():
    url = "https://tuoitre.vn/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        links = [a for item in soup.find_all(['div', 'li'], class_=['box-category-item', 'box-li']) if (a := item.find('a'))]
        
        count = 0
        for link_tag in links:
            if count >= 6: break
            href = link_tag.get('href')
            title = link_tag.get('title') or link_tag.text.strip()
            
            if href:
                link = 'https://tuoitre.vn' + href if not href.startswith('http') else href
                if 'video' not in link and 'podcast' not in link:
                    content, published_date, image_url = get_article_content(link, headers)
                    # Chỉ lấy bài có nội dung
                    if content and len(content) > 100:
                        articles.append({
                            'title': title, 'link': link, 'content': content,
                            'source': 'Tuổi Trẻ', 'published_date': published_date, 'image_url': image_url
                        })
                        count += 1
        return articles
    except: return []

def get_article_content(article_url, headers):
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. DỌN RÁC (Chỉ xóa các thành phần kỹ thuật và quảng cáo)
        for tag in soup.find_all(['script', 'style', 'iframe', 'video', 'audio', 'object', 'button', 'input']): tag.decompose()
        
        # Xóa các khối quảng cáo đặc thù
        rac_classes = ['VCCorpPlayer', 'relate-container', 'box-relate', 'ads', 'banner-ads', 'sponsor', 'detail-content-bottom', 'audioplayer', 'box-tin-tai-tro', 'news-relate-bot', 'tin-tuong-tu', 'VCSocialShare', 'right-tool-detail', 'VCPaywall', 'box-tin-can-biet']
        for div in soup.find_all(class_=rac_classes): div.decompose()

        # 2. LẤY ẢNH BÌA (TỪ META)
        image_url = None
        meta_img = soup.find('meta', property='og:image')
        if meta_img and is_valid_image_url(meta_img.get('content')): 
            image_url = meta_img.get('content')

        # Lấy ngày
        published_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_tag = soup.find('div', attrs={'data-role': 'publishdate'})
        if date_tag:
            try:
               dt = datetime.datetime.strptime(date_tag.text.strip().split('GMT')[0].strip(), '%d/%m/%Y %H:%M')
               published_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except: pass
        
        # 3. XỬ LÝ NỘI DUNG (GIỮ LẠI TOÀN BỘ ẢNH)
        sapo = soup.find('h2', class_='sapo')
        body = soup.find('div', id='main-detail-body') or soup.find('div', class_='detail-content')
        
        full_html = ""
        if sapo: full_html += f'<p style="font-weight:bold; font-size:1.1em;">{sapo.get_text().strip()}</p>'

        if body:
            clean_soup = BeautifulSoup('', 'html.parser')

            # Quét tất cả các thẻ con cấp 1
            for el in body.find_all(['p', 'div', 'figure', 'h2', 'h3', 'ul', 'ol', 'table'], recursive=False):
                
                # A. Xử lý Ảnh Tuổi Trẻ (VCSortableInPreviewMode)
                if el.name == 'div' and 'VCSortableInPreviewMode' in el.get('class', []):
                    img = el.find('img')
                    if img:
                        src = img.get('data-original') or img.get('src')
                        
                        # Lấy Caption (Chú thích) - Tuổi Trẻ thường để trong div PhotoCMS_Caption
                        caption = ""
                        caption_div = el.find('div', class_='PhotoCMS_Caption')
                        if caption_div:
                            caption = caption_div.get_text().strip()
                        else:
                            # Thử tìm trong các thẻ p con nếu không có class chuẩn
                            p_cap = el.find('p')
                            if p_cap: caption = p_cap.get_text().strip()

                        if is_valid_image_url(src):
                            # Tạo thẻ Figure chuẩn HTML5
                            new_figure = clean_soup.new_tag("figure")
                            new_img = clean_soup.new_tag("img", src=src, **{'class': 'img-fluid rounded'})
                            new_figure.append(new_img)
                            
                            # Nếu có caption thì thêm vào
                            if caption:
                                new_cap = clean_soup.new_tag("figcaption")
                                new_cap.string = caption
                                new_figure.append(new_cap)
                            
                            clean_soup.append(new_figure)
                            
                            # Nếu chưa có ảnh bìa thì lấy ảnh đầu tiên này làm ảnh bìa
                            if not image_url: image_url = src

                # B. Xử lý Văn bản
                elif el.name in ['p', 'h2', 'h3']:
                    text = el.get_text().strip()
                    # Lọc từ khóa quảng cáo
                    if text and not any(k in text.lower() for k in ['quảng cáo', 'tin tài trợ', 'bấm để xem', 'đăng ký']):
                         if len(text) > 2: # Bỏ dòng quá ngắn
                            for a in el.find_all('a'): a.unwrap() # Xóa link
                            clean_soup.append(el)
                         
                # C. Xử lý Danh sách & Bảng
                elif el.name in ['ul', 'ol', 'table']:
                     clean_soup.append(el)

            full_html += clean_soup.decode_contents()
            
            # Xóa khoảng trống thừa
            full_html = re.sub(r'<(p|div|figure|h[1-6]|ul|ol|table)\s*[^>]*>\s*<\/\1>', '', full_html, flags=re.IGNORECASE)

        return full_html, published_date, image_url
    except: return None, None, None