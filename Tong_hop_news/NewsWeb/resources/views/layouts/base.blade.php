<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="no-referrer">
    <title>@yield('title', 'Báo Đốm - Tin tức nhanh & chính xác')</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Merriweather:wght@700;900&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        /* --- CSS TỔNG HỢP --- */
        :root { 
            --primary: #c0392b;
            --secondary: #2c3e50;
            --bg-gray: #fcfcfc;
            --text-dark: #1a1a1a;
            --border-light: #ececec;
            --navbar-height: 70px;
          
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Inter', sans-serif; 
            background-color: var(--bg-gray); 
            color: var(--secondary); 
            display: flex;
            flex-direction: column;
            min-height: 100vh; 
            line-height: 1.6;
            font-size: 16px;
        }

        
        body.has-fixed-navbar { padding-top: 130px; } 

        .main-navbar { 
            background: #fff; 
            padding: 0; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            z-index: 1000;
            height: auto;
        }
        
        .main-navbar.fixed-top { position: fixed; top: 0; left: 0; right: 0; width: 100%; }
        
        .header-container { 
            display: flex; 
            align-items: center; 
            justify-content: space-between; 
            min-height: 70px; 
            padding: 0 20px;
        }
        
        .brand-logo { 
            font-family: 'Merriweather', serif; 
            font-weight: 900; 
            font-size: 1.6rem; 
            color: var(--primary); 
            text-decoration: none; 
            display: flex; 
            align-items: center;
            flex-shrink: 0;
        }
        
        /* Hàng menu nằm dưới header-container */
        .nav-row {
            background: #fff;
            border-bottom: 3px solid var(--primary); 
            box-shadow: 0 1px 5px rgba(0,0,0,0.05);
        }
        
        /* --- STYLES CHO MENU DANH MỤC --- */
        .nav-menu { 
            width: 100%;
            overflow-x: auto; 
            white-space: nowrap; 
            scrollbar-width: none;
            display: flex; 
            align-items: center;
            padding: 0 20px;
        }
        
        .nav-menu::-webkit-scrollbar { display: none; }
        
        .nav-menu a { 
            text-decoration: none; 
            color: #666; 
            font-weight: 600; 
            font-size: 0.9rem; 
            padding: 12px 15px; 
            display: flex; 
            align-items: center; 
            border-bottom: 3px solid transparent; 
            transition: 0.2s; 
            text-transform: uppercase;
            flex-shrink: 0;
            gap: 6px;
        }
        
        .nav-menu a i {
            color: #999;
            transition: all 0.2s;
        }

        .nav-menu a:hover,
        .nav-menu a.active { 
            color: var(--primary); 
            background-color: transparent; 
        }

        .nav-menu a.active { 
            border-bottom-color: var(--primary); 
            padding: 12px 15px 9px 15px;
        }

        .nav-menu a:hover i,
        .nav-menu a.active i {
            color: var(--primary);
        }
        
        /* --- STYLES CHO TÌM KIẾM --- */
        .search-form { position: relative; width: 280px; flex-shrink: 0; }
        
        .search-input { 
            border: 1px solid #ddd; 
            border-radius: 25px; 
            padding: 8px 20px 8px 45px; 
            font-size: 0.9rem; 
            width: 100%; 
            background: #f8f8f8; 
            box-shadow: none; 
            transition: 0.3s; 
        }
        
        .search-input:focus { outline: none; border-color: #bbb; background: #fff; }
        
        .search-input::placeholder { color: #aaa; }
        
        .search-icon-btn { 
            position: absolute; 
            left: 18px; 
            top: 50%; 
            transform: translateY(-50%); 
            color: #999; 
            border: none; 
            background: none; 
            pointer-events: none;
            font-size: 1rem;
        }
        
        /* --- STYLES CHO NỘI DUNG VÀ CARD --- */
        .main-content-wrap { flex: 1; width: 100%; }
        
        .section-title { 
            font-family: 'Merriweather', serif; 
            font-weight: 900; 
            color: var(--text-dark); 
            border-left: 6px solid var(--primary); 
            padding-left: 15px; 
            margin: 15px 0 30px; 
            text-transform: uppercase; 
            font-size: 1.2rem; 
            letter-spacing: 0.5px;
        }

        .news-card { 
            background: #fff; 
            border: 1px solid var(--border-light); 
            border-radius: 8px; 
            overflow: hidden; 
            transition: transform 0.3s, box-shadow 0.3s; 
            height: 100%; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.02); 
        }
        
        .news-card:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 10px 20px rgba(0,0,0,0.08); 
        }
        
        .news-title { 
            font-size: 1rem; 
            font-weight: 700; 
            line-height: 1.4; 
            margin-bottom: 10px; 
            display: -webkit-box; 
            -webkit-line-clamp: 3; 
            -webkit-box-orient: vertical; 
            overflow: hidden; 
        }

        .news-title a { color: inherit; text-decoration: none; }
        .news-title a:hover { color: var(--primary); }
        
        /* --- STYLES CHO CHI TIẾT (SHOW) --- */
        .main-container { max-width: 850px; margin: 30px auto; flex: 1; padding: 0 15px; } 
        
        .article-box { 
            background: white; 
            padding: 40px 50px; 
            border-radius: 8px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
            border: 1px solid var(--border-light); 
        }
        
        .article-title { 
            font-family: 'Merriweather', serif; 
            font-size: 2.5rem; 
            font-weight: 900; 
            color: var(--text-dark); 
            line-height: 1.25; 
            margin-bottom: 20px; 
        } 
        
        .article-content { 
            font-family: 'Merriweather', serif; 
            font-size: 1.1rem; 
            line-height: 1.8; 
            color: #333; 
            text-align: justify; 
        } 
        
        .comment-sec { 
            margin-top: 50px; 
            background: #fff; 
            padding: 35px; 
            border-radius: 8px; 
            border-top: 5px solid var(--primary); 
            box-shadow: 0 2px 10px rgba(0,0,0,0.03); 
        }

        .btn-love-styled {
            display: inline-flex;
            align-items: center;
            padding: 8px 18px;
            border-radius: 25px; 
            background: #ffebeb; 
            color: var(--primary); 
            border: none;
            font-weight: 700;
            font-size: 0.95rem;
            text-decoration: none; 
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08); 
            text-transform: uppercase;
        }
        
        .btn-love-styled:hover {
            background: var(--primary);
            color: #fff;
            box-shadow: 0 6px 10px rgba(192, 57, 43, 0.4);
            transform: translateY(-2px);
        }

        .btn-love-styled i {
            color: var(--primary);
            margin-right: 8px;
            transition: color 0.3s;
        }

        .btn-love-styled:hover i {
            color: #fff;
        }
        
        /* --- FOOTER CHUNG --- */
        .main-footer { 
            background-color: #1a1a1a; 
            color: #ccc; 
            padding-top: 70px; 
            margin-top: 100px; 
            font-size: 0.9rem; 
            border-top: 3px solid var(--primary); 
        }
        
        .footer-brand { 
            color: #fff; 
            font-family: 'Merriweather', serif; 
            font-weight: 900; 
            font-size: 1.8rem; 
            text-decoration: none; 
            display: inline-block; 
            margin-bottom: 15px; 
        }
        
        .footer-title { 
            color: #fff; 
            font-weight: 900; 
            margin-bottom: 25px; 
            text-transform: uppercase; 
            font-size: 1rem; 
            letter-spacing: 1.5px; 
            position: relative; 
        }
        
        .footer-title::after { 
            content: ''; 
            position: absolute; 
            left: 0; 
            bottom: -8px; 
            width: 50px; 
            height: 3px; 
            background: var(--primary); 
        }
        
        .footer-links { list-style: none; padding: 0; }
        .footer-links li { margin-bottom: 10px; }
        
        .footer-links a { 
            color: #ccc; 
            text-decoration: none; 
            transition: all 0.3s; 
            display: inline-block; 
        }
        
        .footer-links a:hover { color: var(--primary); padding-left: 8px; }

        .footer-desc { line-height: 1.8; margin: 15px 0; }

        .social-links { display: flex; gap: 10px; }

        .social-links a {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            color: #fff;
            text-decoration: none;
            transition: all 0.3s;
        }

        .social-links a:hover { background: var(--primary); transform: translateY(-3px); }

        .copyright {
            background: #111;
            padding: 20px 0;
            margin-top: 50px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }

        .copyright a:hover { color: var(--primary) !important; }
        
        /* --- RESPONSIVE FIXES --- */
        @media (max-width: 992px) {
            .header-container { flex-wrap: nowrap; min-height: 60px; }
            .search-form { width: 250px; }
            .nav-menu a { font-size: 0.8rem; padding: 0 10px; }
        }

        @media (max-width: 768px) {
            body.has-fixed-navbar { padding-top: 100px; }
            .main-navbar { min-height: 60px; padding-bottom: 0; }
            .header-container { flex-wrap: wrap; padding: 10px; min-height: 50px; }
            .brand-logo { font-size: 1.4rem; margin-right: 10px; flex: 0 0 auto; }
            .search-form { order: 2; width: 100%; flex: 1 1 100%; max-width: none; margin-left: 0; margin-top: 5px; }
            .nav-row { position: static; border-top: 1px solid var(--border-light); }
            .nav-menu { padding: 0 10px; height: 45px; }
            .nav-menu a { font-size: 0.75rem; padding: 0 8px; height: 40px; }
            .search-input { font-size: 0.85rem; padding: 6px 15px 6px 35px; }
            .article-box { padding: 20px; border-radius: 8px; }
            .article-title { font-size: 1.8rem; line-height: 1.3; }
            .article-content { font-size: 1rem; line-height: 1.7; }
            .main-container { margin: 20px auto; }
            .comment-sec { padding: 20px; }
        }

        @media (max-width: 576px) {
            body.has-fixed-navbar { padding-top: 110px; }
            .header-container { padding: 8px; }
            .brand-logo { font-size: 1.2rem; margin-right: 8px; }
            .brand-logo .fas { font-size: 1rem; }
            .search-input { padding: 5px 12px 5px 30px; font-size: 0.8rem; }
            .search-icon-btn { left: 10px; font-size: 0.85rem; }
            .nav-menu { height: 40px; }
            .nav-menu a { font-size: 0.7rem; padding: 0 6px; height: 35px; }
            .nav-menu a i { font-size: 0.7rem; }
        }
    </style>

    <script>
        function toggleReply(id) {
            const form = document.getElementById('reply-form-' + id);
            document.querySelectorAll('.reply-form').forEach(f => {
                 if (f.id !== 'reply-form-' + id) f.style.display = 'none';
            });
            form.style.display = (form.style.display === 'block') ? 'none' : 'block';
        }

        // Smooth scroll for navbar on mobile
        document.addEventListener('DOMContentLoaded', function() {
            const navMenu = document.querySelector('.nav-menu');
            if (navMenu) {
                const activeLink = navMenu.querySelector('.active');
                if (activeLink && window.innerWidth < 768) {
                    activeLink.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                }
            }
        });
    </script>
</head>
<body @if(isset($hasFixedNavbar) && $hasFixedNavbar) class="has-fixed-navbar" @endif>

    <nav class="main-navbar @if(isset($hasFixedNavbar) && $hasFixedNavbar) fixed-top @endif">
       
        <div class="header-container">
            <a href="{{ url('/') }}" class="brand-logo">
                <i class="fas fa-paw me-2"></i>BÁO ĐỐM
            </a>
            
            <form action="{{ route('news.index') }}" method="GET" class="search-form">
                <button type="submit" class="search-icon-btn"><i class="fas fa-search"></i></button>
                <input type="text" name="search" class="search-input" placeholder="Tìm kiếm..." value="{{ request('search') }}">
            </form>

        </div>

        
        @if(View::hasSection('nav_content'))
            <div class="nav-row">
                @yield('nav_content')
            </div>
        @endif
        
    </nav>
    
    <div class="main-content-wrap">
        @yield('content')
    </div>

    <footer class="main-footer">
        <div class="container">
            <div class="row">
                <div class="col-md-5 mb-4">
                    <a href="{{ url('/') }}" class="footer-brand">
                        <i class="fas fa-paw"></i> BÁO ĐỐM
                    </a>
                    <p class="footer-desc">
                        Hệ thống tổng hợp tin tức tự động thông minh, mang đến cho bạn những thông tin nóng hổi, chính xác và đa chiều nhất từ các nguồn báo chí uy tín hàng đầu Việt Nam.
                    </p>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-facebook-f"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-youtube"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>

                <div class="col-md-4 mb-4">
                    <h5 class="footer-title">Liên Hệ Nhóm 8</h5>
                    <ul class="footer-links">
                        <li><i class="fas fa-map-marker-alt me-2 text-danger"></i> Đại học Công Nghệ TP.HCM</li>
                        <li><i class="fas fa-envelope me-2 text-danger"></i> contact@baodom.com</li>
                        <li><i class="fas fa-phone-alt me-2 text-danger"></i> (039) 6046 671</li>
                    </ul>
                </div>

                <div class="col-md-3 mb-4">
                    <h5 class="footer-title">Nhận Tin Mới</h5>
                    <div class="mt-3">
                        <span class="d-block text-white mb-2 fw-bold">Đăng ký nhận tin:</span>
                        <div class="input-group">
                            <input type="email" class="form-control form-control-sm" placeholder="Email...">
                            <button class="btn btn-danger btn-sm">Gửi</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="copyright">
            <div class="container">
                <div class="row">
                    <div class="col-md-6 text-md-start text-center mb-2 mb-md-0">
                        © 2025 <strong>Báo Đốm</strong>. All Rights Reserved.
                    </div>
                    <div class="col-md-6 text-md-end text-center">
                        <a href="#" class="text-white text-decoration-none mx-2 small">Điều khoản</a>
                        <a href="#" class="text-white text-decoration-none mx-2 small">Bảo mật</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>