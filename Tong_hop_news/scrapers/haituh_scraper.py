import requests
import datetime
from bs4 import BeautifulSoup

def get_articles():
    source_name = "24h"
    url = "https://www.24h.com.vn/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        # Tìm link bài viết
        candidates = [h.find('a') for h in soup.find_all(['h2', 'h3', 'h4']) if h.find('a')]
        seen = set()
        count = 0
        for link_tag in candidates:
            if count >= 6: break
            href = link_tag.get('href')
            title = link_tag.get('title') or link_tag.text.strip()
            
            if href and len(title) > 10:
                if href not in seen and 'du-bao-thoi-tiet' not in href:
                    seen.add(href)
                    if not href.startswith('http'): href = 'https://www.24h.com.vn' + href
                    
                    content, published_date, image_url = get_article_content(href, headers)
                    if content and len(content) > 100:
                        articles.append({
                            'title': title, 'link': href, 'content': content,
                            'source': '24h', 'published_date': published_date, 'image_url': image_url
                        })
                        count += 1
        return articles
    except: return []

def get_article_content(article_url, headers):
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. DỌN RÁC KỸ THUẬT
        for tag in soup.find_all(['script', 'style', 'iframe', 'video', 'object', 'center', 'button', 'input']): tag.decompose()
        rac_classes = [
            'viewVideoPlay', 'video-content', 'banner-ads', 'zone-ad', 
            'baiviet-lienquan', 'bv-lienquan', 'btn-link-ads', 'not-in-view', 'box-tin-lien-quan',
            'k-save-news', 'box-luu-tin' # Class chứa nút lưu tin
        ]
        for div in soup.find_all(class_=rac_classes): div.decompose()

        # 2. LẤY ẢNH BÌA & NGÀY
        image_url = None
        meta_img = soup.find('meta', property='og:image')
        if meta_img: image_url = meta_img.get('content')

        published_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_tag = soup.find('div', class_='cate-24h-foot-arti-deta-cre-post')
        if date_tag:
            try:
                txt = date_tag.text.strip()
                clean_date = txt.split(',')[-1].replace('ngày', '').split('(GMT')[0].strip()
                dt = datetime.datetime.strptime(clean_date, '%d/%m/%Y %I:%M %p')
                published_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except: pass
        
        # 3. XỬ LÝ NỘI DUNG (CÓ LỌC TỪ KHÓA RÁC)
        sapo = soup.find('h2', class_='baiviet-sapo')
        body = soup.find('article', id='article_body') or soup.find('div', id='article_body')
        
        full_html = ""
        if sapo: full_html += f'<p class="fw-bold"><strong>{sapo.get_text().strip()}</strong></p>'

        if body:
            # Danh sách từ khóa rác cần loại bỏ
            bad_phrases = [
                "Nguồn:", "Theo:", "Lưu bài viết", "xem lại bài viết", 
                "Tin bài đã lưu", "Mời độc giả xem thêm"
            ]

            for el in body.descendants:
                if el.name == 'p':
                    text = el.get_text().strip()
                    
                    # --- KIỂM TRA TỪ KHÓA RÁC ---
                    is_garbage = False
                    for phrase in bad_phrases:
                        if phrase in text:
                            is_garbage = True
                            break
                    if is_garbage: continue 
                    # ----------------------------

                    img = el.find('img')
                    if img:
                        src = img.get('data-original') or img.get('src')
                        if src and 'icon' not in src and 'banner' not in src:
                            caption = img.get('alt') or ""
                            full_html += f'<figure class="text-center"><img src="{src}" class="img-fluid rounded" alt="{caption}"><figcaption class="text-muted small fst-italic">{caption}</figcaption></figure>'
                    elif text:
                        full_html += f'<p>{text}</p>'
                
                elif el.name in ['h2', 'h3', 'h4']:
                    full_html += f'<{el.name} class="fw-bold mt-3 mb-2">{el.get_text().strip()}</{el.name}>'
                
                elif el.name == 'table':
                    full_html += str(el)

        return full_html, published_date, image_url
    except: return None, None, None