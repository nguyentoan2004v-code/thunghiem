@extends('layouts.base', ['hasFixedNavbar' => true]) {{-- Đã thêm biến để cố định navbar --}}

@section('nav_content')
    @include('news.partials.navbar_index')
@endsection

{{-- 3. NỘI DUNG CHÍNH CỦA TRANG CHI TIẾT --}}
@section('content')
    <div class="container main-container">
        {{-- Đã xóa nút quay lại ở đây vì nó đã được chuyển lên Navbar --}}

        <div class="article-box">
            <div class="mb-3">
                <span class="badge bg-danger">{{ $article->source->name ?? 'Tổng hợp' }}</span>
                @foreach($article->categories as $cat)
                    <span class="badge bg-warning text-dark">{{ $cat->name }}</span>
                @endforeach
            </div>

            <h1 class="article-title">{{ $article->title }}</h1>

            <div class="article-meta" style="color: #777; font-size: 0.9rem; border-bottom: 1px solid #eee; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;">
                <span><i class="far fa-clock"></i> {{ \Carbon\Carbon::parse($article->published_date)->format('H:i, d/m/Y') }}</span>
                <a href="{{ $article->link }}" target="_blank" class="link-source-small">Xem bài gốc <i class="fas fa-external-link-alt"></i></a>
            </div>

           @if($article->image_url)
           @php $proxiedFeaturedImageUrl = 'https://images.weserv.nl/?url=' . urlencode($article->image_url); @endphp
             <img src="{{ $proxiedFeaturedImageUrl }}" class="img-fluid w-100 mb-4 rounded" onerror="this.style.display='none'" style="max-height: 450px; object-fit: cover;">
           @endif

            <div class="article-content">
                {!! $article->content !!}
            </div>

            <div class="action-bar" style="display: flex; justify-content: space-between; align-items: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <a href="{{ route('article.love', $article->id) }}" class="btn-love-styled" title="Yêu thích bài viết">
                    {{-- Class 'text-danger' đã được bỏ đi vì CSS mới xử lý màu sắc --}}
                    <i class="fas fa-heart"></i> Yêu thích ({{ $article->loves }})
                </a>
                <div class="d-flex align-items-center">
                    <span class="text-muted small me-2">Chia sẻ:</span>
                    <a href="https://www.facebook.com/" class="btn-share text-primary"><i class="fab fa-facebook fa-lg"></i></a>
                </div>
            </div>
        </div>

        <div class="comment-sec">
            <h5 class="fw-bold mb-4">Ý kiến bạn đọc ({{ $article->comments->count() }})</h5>
            
            @if(session('success'))
                <div class="alert alert-success py-2 small">{{ session('success') }}</div>
            @endif

            <form action="{{ route('news.comment', $article->id) }}" method="POST" class="mb-5">
                @csrf
                <div class="row g-2">
                    <div class="col-md-4"><input type="text" name="name" class="form-control" placeholder="Tên bạn..." required></div>
                    <div class="col-md-8"><input type="text" name="content" class="form-control" placeholder="Viết bình luận..." required></div>
                </div>
                <div class="text-end mt-2"><button class="btn btn-dark btn-sm px-4">Gửi</button></div>
            </form>

            @foreach($article->comments->whereNull('parent_id') as $comment)
                <div class="mb-4 pb-3 border-bottom">
                    <div class="d-flex">
                        <img src="https://ui-avatars.com/api/?name={{ urlencode($comment->name) }}&background=random" class="rounded-circle" width="40" height="40">
                        <div class="ms-3 w-100">
                            <div class="bg-light p-3 rounded">
                                <h6 class="fw-bold mb-1">{{ $comment->name }}</h6>
                                <p class="mb-0 small text-dark">{{ $comment->content }}</p>
                            </div>
                            <div class="mt-1 ms-2">
                                <a href="{{ route('comment.like', $comment->id) }}" class="btn-like" style="color: #666; font-size: 0.85rem; font-weight: 600; margin-right: 15px; text-decoration: none;"><i class="far fa-thumbs-up"></i> Thích ({{ $comment->likes }})</a>
                                <span class="text-muted small fw-bold" style="cursor: pointer;" onclick="toggleReply({{ $comment->id }})">Trả lời</span>
                                <span class="text-muted small ms-2">{{ $comment->created_at->diffForHumans() }}</span>
                            </div>
                        </div>
                    </div>

                    <div id="reply-form-{{ $comment->id }}" class="reply-form mt-2 ms-5" style="display: none;">
                        <form action="{{ route('news.comment', $article->id) }}" method="POST">
                            @csrf
                            <input type="hidden" name="parent_id" value="{{ $comment->id }}">
                            <div class="d-flex gap-2">
                                <input type="text" name="name" class="form-control form-control-sm w-25" placeholder="Tên..." required>
                                <input type="text" name="content" class="form-control form-control-sm" placeholder="Trả lời..." required>
                                <button class="btn btn-warning btn-sm text-white">Gửi</button>
                            </div>
                        </form>
                    </div>

                    @if($comment->replies->isNotEmpty())
                        @include('news.partials.comment_replies', ['replies' => $comment->replies, 'level' => 1, 'article' => $article])
                    @endif
                </div>
            @endforeach
        </div>
    </div>
@endsection