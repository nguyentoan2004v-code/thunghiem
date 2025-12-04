<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\NewsController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
*/

// 1. Trang chủ & Tìm kiếm
Route::get('/', [NewsController::class, 'index'])->name('news.index');

// 2. Lọc tin theo Danh mục (Thể thao, Giáo dục...)
Route::get('/danh-muc/{id}', [NewsController::class, 'category'])->name('news.category');

// 3. Lọc tin theo Nguồn báo (VnExpress, Tuổi Trẻ...) <--- DÒNG BẠN ĐANG THIẾU
Route::get('/nguon/{id}', [NewsController::class, 'source'])->name('news.source');

// 4. Xem chi tiết bài viết
Route::get('/bai-viet/{id}', [NewsController::class, 'show'])->name('news.show');

// 5. Gửi bình luận
Route::post('/bai-viet/{id}/comment', [NewsController::class, 'comment'])->name('news.comment');

// 6. Thả tim Bài Viết
Route::get('/article/{id}/love', [NewsController::class, 'loveArticle'])->name('article.love');

// 7. Thích Bình Luận
Route::get('/comment/{id}/like', [NewsController::class, 'likeComment'])->name('comment.like');