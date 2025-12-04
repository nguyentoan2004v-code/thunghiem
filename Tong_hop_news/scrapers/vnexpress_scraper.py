import requests
import datetime
from bs4 import BeautifulSoup
import re

# Hàm kiểm tra URL ảnh có phải là rác (logo, icon) hay không
def is_valid_image_url(url):
    if not url: return False
    url = url.lower()
    # Danh sách các từ khóa rác phổ biến
    garbage_keywords = ['logo', 'icon', 'default', 'no_photo', '30x', '180x', 'thumb_w', 'q_50', 'banner', 'ads', 'square', 'small']
    if any(k in url for k in garbage_keywords):
        return False
    # Kiểm tra URL quá ngắn
    if len(url.split('/')) < 5:
        return False
    return True

def get_articles():
    url = "https://vnexpress.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        title_tags = soup.find_all(['h1', 'h2', 'h3', 'h4'], class_='title-news')
        count = 0
        for tag in title_tags:
            if count >= 6: break
            link_tag = tag.find('a') if tag.name != 'a' else tag
            if link_tag:
                link = link_tag.get('href')
                title = link_tag.get('title') or link_tag.text.strip()
                
                if link and 'video' not in link and 'podcast' not in link and 'eclick' not in link:
                    if not link.startswith('http'): link = 'https://vnexpress.net' + link
                    
                    content, published_date, image_url = get_article_content(link, headers)
                    
                    if content and len(content) > 100:
                        articles.append({
                            'title': title, 'link': link, 'content': content,
                            'source': 'VnExpress', 'published_date': published_date, 'image_url': image_url
                        })
                        count += 1
        return articles
    except: return []

def get_article_content(article_url, headers):
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. DỌN DẸP RÁC
        for tag in soup.find_all(['script', 'style', 'iframe', 'video', 'object', 'meta', 'link', 'svg', 'button']): 
            tag.decompose()
        rac_classes = ['header-content', 'footer-content', 'box_embed_video', 'box-related', 'related-news', 'banner-ads', 'box_brief', 'meta-news', 'box-date', 'breadcrumb', 'width_common', 'box_author', 'container-tab']
        for div in soup.find_all(class_=rac_classes): div.decompose()

        # 2. LẤY NGÀY
        published_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_tag = soup.find('span', class_='date')
        if date_tag:
            try:
                parts = date_tag.text.strip().split(', ')
                if len(parts) >= 2:
                    dt = datetime.datetime.strptime(f"{parts[1]}, {parts[2].split(' (')[0]}", '%d/%m/%Y, %H:%M')
                    published_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except: pass

        # 3. LẤY NỘI DUNG VÀ ẢNH BÌA (TỐI ƯU ƯU TIÊN ẢNH NỘI DUNG)
        image_url = None
        full_html = ""
        
        sapo = soup.find('p', class_='description')
        body = soup.find('article', class_='fck_detail') or soup.find('div', class_='fck_detail')

        if body:
            # A. SĂN ẢNH THUMBNAIL (Ưu tiên ẢNH NỘI DUNG)
            first_content_fig = body.find('figure')
            if first_content_fig:
                img_tag = first_content_fig.find('img')
                if img_tag:
                    temp_url = img_tag.get('data-src') or img_tag.get('src')
                    # Kiểm tra và chỉ lấy nếu URL hợp lệ
                    if is_valid_image_url(temp_url):
                        image_url = temp_url
            
            # B. Fix ảnh trong bài và link rác
            for el in body.find_all(['p', 'figure', 'h2', 'h3', 'ul', 'ol', 'table']):
                if el.name == 'figure':
                    img = el.find('img')
                    if img:
                        src = img.get('data-src') or img.get('src')
                        if is_valid_image_url(src):
                            img['src'] = src
                            img['class'] = 'img-fluid rounded shadow-sm'
                            for attr in ['width', 'height', 'style', 'onclick', 'data-src']: 
                                if attr in img.attrs: del img[attr]
                        else:
                            el.decompose()
                elif el.name in ['p', 'h2', 'h3', 'ul', 'ol', 'table']:
                    text = el.get_text().strip()
                    if text or el.find('img'):
                        for a in el.find_all('a'): a.unwrap()
                        full_html += str(el)

        # C. FALLBACK CUỐI CÙNG: Dùng OG:Image nếu ảnh nội dung không có và URL OG hợp lệ
        if not image_url:
            meta_og = soup.find('meta', property='og:image')
            if meta_og: 
                 temp_url = meta_og.get('content')
                 if is_valid_image_url(temp_url):
                    image_url = temp_url

        # D. Xử lý Sapo và Clean HTML cuối cùng
        if sapo:
            for a in sapo.find_all('a'): a.unwrap()
            full_html = f'<p style="font-weight:bold; font-size:1.1em;">{sapo.get_text().strip()}</p>' + full_html
        
        # Clean up khoảng trống thừa
        full_html = re.sub(r'<(p|div|figure|h[1-6]|ul|ol|table)\s*[^>]*>\s*<\/\1>', '', full_html, flags=re.IGNORECASE)

        return full_html, published_date, image_url
    except Exception as e:
        print(f"Lỗi chi tiết VnExpress: {e}")
        return None, None, None