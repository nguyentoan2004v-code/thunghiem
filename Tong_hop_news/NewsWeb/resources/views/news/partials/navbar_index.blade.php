@php
    // Lấy categories nếu chưa có
    if (!isset($categories)) {
        $categories = App\Models\Category::all();
    }
@endphp

<div class="nav-menu">
    <a href="{{ url('/') }}" class="{{ !isset($currentCategory) && !isset($currentSource) && Request::is('/') ? 'active' : '' }}">
        <i class="fas fa-home me-1"></i> Tất cả
    </a>
    @if($categories && $categories->count() > 0)
        @foreach($categories as $cat)
            <a href="{{ route('news.category', $cat->id) }}" 
               class="{{ (isset($currentCategory) && $currentCategory->id == $cat->id) ? 'active' : '' }}">
               <i class="fas {{ $cat->icon_class ?? 'fa-folder' }} me-1 opacity-75"></i>
               {{ $cat->name }}
            </a>
        @endforeach
    @endif
</div>

