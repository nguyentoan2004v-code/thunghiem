@extends('layouts.base') 

{{-- 1. HEADER DÀNH RIÊNG CHO TRANG CHỦ --}}
@section('nav_content')
    @include('news.partials.navbar_index')
@endsection

{{-- 2. NỘI DUNG CHÍNH CỦA TRANG CHỦ --}}
@section('content')
    {{-- FIX TẠM THỜI: Xóa lớp mt-4 và dùng lớp tùy chỉnh để đảm bảo khoảng cách trên --}}
    <div class="container pt-4"> 
        <div class="row">
            
            <div class="col-lg-9">
                <h4 class="section-title">
                    @if(isset($currentSource)) <i class="fas fa-newspaper me-2"></i>Tin từ: <span class="text-danger">{{ $currentSource->name }}</span>
                    @elseif(isset($currentCategory)) <i class="fas fa-folder-open me-2"></i>{{ $currentCategory->name }}
                    @elseif(request('search')) <i class="fas fa-search me-2"></i>Kết quả: "{{ request('search') }}"
                    @else <i class="fas fa-bolt me-2"></i>Tin Mới Cập Nhật @endif
                </h4>

                @if(isset($articles) && $articles->count() > 0)
                    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                        @foreach ($articles as $article)
                        <div class="col">
                            <div class="news-card h-100">
                                <div class="card-img-wrap" style="position: relative; padding-top: 60%; overflow: hidden; background: #eee;">
                                    <a href="{{ route('news.show', $article->id) }}">
                                        @php 
                                            $articleId = $article->id;
                                            $categoryName = $article->categories->first()->name ?? 'Tin tức';
                                            $iconClass = 'fa-image';
                                            $proxiedImageUrl = !empty($article->image_url) 
                                                                ? 'https://images.weserv.nl/?url=' . urlencode($article->image_url) 
                                                                : null;
                                        @endphp

                                        {{-- Khung Placeholder chung (luôn có) --}}
                                        <div id="fallback-home-{{ $articleId }}" 
                                             class="fallback-img" 
                                             style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                                                    display: flex; flex-direction: column; align-items: center; justify-content: center; 
                                                    color: rgba(255,255,255,0.9); background: linear-gradient(135deg, #34495e, #c0392b); 
                                                    text-align: center; z-index: 1;">
                                            <i class="fas {{ $iconClass }} fa-3x mb-2 opacity-50"></i>
                                            <span class="small fw-bold text-uppercase opacity-75">{{ $categoryName }}</span>
                                        </div>

                                        @if($proxiedImageUrl)
                                            {{-- Ảnh chính (Cố gắng tải, nếu thành công sẽ đè lên Placeholder) --}}
                                            <img id="img-{{ $articleId }}" 
                                                 src="{{ $proxiedImageUrl }}" 
                                                 class="card-img-top" 
                                                 style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; transition: 0.5s; z-index: 2;"
                                                 onerror="document.getElementById('img-{{ $articleId }}').style.display='none';">
                                        @endif
                                        
                                    </a>
                                    <span class="source-tag" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: #fff; padding: 2px 8px; font-size: 0.7rem; border-radius: 4px; font-weight: bold; z-index: 5;">{{ $article->source->name ?? 'News' }}</span>
                                </div>

                                <div class="card-body">
                                    <h5 class="news-title">
                                        <a href="{{ route('news.show', $article->id) }}">
                                            @if(request('search')) {!! preg_replace('/(' . preg_quote(request('search'), '/') . ')/i', '<span style="background-color: yellow;">$1</span>', $article->title) !!}
                                            @else {{ $article->title }} @endif
                                        </a>
                                    </h5>
                                    <div class="news-meta" style="margin-top: auto; font-size: 0.8rem; color: #888; border-top: 1px dashed #eee; padding-top: 10px; display: flex; justify-content: space-between;">
                                        <span><i class="far fa-clock"></i> {{ \Carbon\Carbon::parse($article->published_date)->format('d/m H:i') }}</span>
                                        <span class="text-primary cursor-pointer" onclick="window.location='{{ route('news.show', $article->id) }}'">Xem <i class="fas fa-arrow-right"></i></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        @endforeach
                    </div>
                    <div class="d-flex justify-content-center mt-5 mb-5">{{ $articles->links() }}</div>
                @else
                    <div class="alert alert-light text-center py-5 border"><p class="text-muted">Không tìm thấy tin nào.</p></div>
                @endif
            </div>

            {{-- Vùng Sidebar (3 cột) --}}
            <div class="col-lg-3 ps-lg-4">
                <div class="sticky-top" style="top: 100px;">
                    <div class="sidebar-box" style="background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
                        <div class="sidebar-head" style="font-weight: 700; text-transform: uppercase; font-size: 0.9rem; border-left: 4px solid var(--primary); padding-left: 10px; margin-bottom: 15px; color: #222;">Nguồn Báo</div>
                        
                        @if(isset($sources) && $sources->count() > 0)
                            <ul class="list-vertical m-0 p-0" style="list-style: none;">
                                <li>
                                    <a href="{{ url('/') }}" class="{{ !isset($currentSource) ? 'text-danger' : '' }}" style="text-decoration: none; color: #555; font-weight: 600; display: flex; justify-content: space-between; align-items: center; transition: 0.2s;">
                                        <span><i class="fas fa-globe me-2"></i>Tất cả nguồn</span>
                                    </a>
                                </li>
                                @foreach($sources as $src)
                                <li>
                                    <a href="{{ route('news.source', $src->id) }}" class="{{ (isset($currentSource) && $currentSource->id == $src->id) ? 'text-danger' : '' }}" style="text-decoration: none; color: #555; font-weight: 600; display: flex; justify-content: space-between; align-items: center; transition: 0.2s; padding: 5px 0;">
                                        <span>{{ $src->name }}</span>
                                        <span class="count-badge" style="background: var(--bg-gray); color: #888; padding: 2px 8px; border-radius: 10px; font-weight: normal; font-size: 0.75rem;">{{ $src->articles_count ?? $src->articles()->count() }}</span>
                                    </a>
                                </li>
                                @endforeach
                            </ul>
                        @else
                            <p class="text-muted small">Đang cập nhật nguồn...</p>
                        @endif
                    </div>

                    <div class="sidebar-box text-center text-white" style="background: linear-gradient(45deg, #c0392b, #e64c3c); border:none; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <i class="fas fa-mobile-alt fa-2x mb-2"></i>
                        <h6 class="fw-bold">App Báo Đốm</h6>
                        <button class="btn btn-sm btn-light w-100 fw-bold text-danger mt-2">Tải Ngay</button>
                    </div>

                </div>     
            </div>

        </div>
    </div>
@endsection