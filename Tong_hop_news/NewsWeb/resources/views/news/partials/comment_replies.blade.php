{{-- File: resources/views/news/partials/comment_replies.blade.php --}}

@foreach($replies as $reply)
    {{-- Thụt đầu dòng dựa trên cấp độ --}}
    <div class="d-flex mt-3 ps-3 border-start border-3" style="margin-left: {{ $level * 10 }}px; border-color: #eee;"> 
        
        <img src="https://ui-avatars.com/api/?name={{ urlencode($reply->name) }}&background=random" class="rounded-circle" width="35" height="35">
        
        <div class="ms-3 w-100">
            <div class="bg-light p-2 rounded-3">
                <span class="fw-bold small">{{ $reply->name }}</span>
                <span class="text-secondary small ms-2">{{ $reply->content }}</span>
            </div>
            
            <div class="mt-1 ms-1 d-flex align-items-center">
                <a href="{{ route('comment.like', $reply->id) }}" class="btn-like small text-decoration-none me-3">
                    <i class="far fa-thumbs-up"></i> {{ $reply->likes }}
                </a>
                <span class="text-muted small fw-bold" style="cursor: pointer;" onclick="toggleReply({{ $reply->id }})">Trả lời</span>
            </div>

            <div id="reply-form-{{ $reply->id }}" class="reply-form mt-2" style="display: none;">
                <form action="{{ route('news.comment', $article->id) }}" method="POST">
                    @csrf
                    <input type="hidden" name="parent_id" value="{{ $reply->id }}">
                    <div class="d-flex gap-2">
                        <input type="text" name="name" class="form-control form-control-sm w-25" placeholder="Tên..." required>
                        <input type="text" name="content" class="form-control form-control-sm" placeholder="Trả lời..." required>
                        <button class="btn btn-warning btn-sm text-white">Gửi</button>
                    </div>
                </form>
            </div>
            
            {{-- ĐỆ QUY: Gọi lại chính file này nếu có comment con --}}
            @if($reply->replies->count())
                @include('news.partials.comment_replies', ['replies' => $reply->replies, 'level' => $level + 1, 'article' => $article])
            @endif
        </div>
    </div>
@endforeach