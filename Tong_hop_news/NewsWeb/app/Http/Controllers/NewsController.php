<?php

namespace App\Http\Controllers;

use App\Models\Article;
use App\Models\Category;
use App\Models\Comment;
use App\Models\Source; // Đã thêm: Import Model Source

use Illuminate\Http\Request;

class NewsController extends Controller
{
    
    public function index(Request $request)
    {
        // Khởi tạo query và eagerly load các mối quan hệ cần thiết
        $query = Article::with(['source', 'categories']);

        // Kiểm tra tìm kiếm thông minh: Chỉ thực hiện nếu tham số 'search' có giá trị
        if ($request->filled('search')) {
            // Lấy từ khóa và chuyển về chữ thường để đảm bảo tìm kiếm Case-Insensitive
            $keyword = strtolower($request->search);

            // Áp dụng điều kiện tìm kiếm (sử dụng whereRaw và LOWER() cho Case-Insensitive)
            $query->where(function ($q) use ($keyword) {
                // Điều kiện 1: Tiêu đề (title) chứa từ khóa
                $q->whereRaw('LOWER(title) LIKE ?', ["%{$keyword}%"]);
                  // Điều kiện 2: HOẶC Nội dung (content) chứa từ khóa
                //   ->orWhereRaw('LOWER(content) LIKE ?', ["%{$keyword}%"]);
            });

            // Sắp xếp: Ưu tiên những bài viết có từ khóa trong tiêu đề
            $query->orderByRaw(
                "CASE WHEN LOWER(title) LIKE ? THEN 1 ELSE 2 END",
                ["%{$keyword}%"]
            );
        }
        
        // Sắp xếp mặc định: Bài viết mới nhất (theo ID hoặc created_at)
        $query->orderBy('id', 'desc');

        // Phân trang kết quả và giữ lại các tham số truy vấn (bao gồm cả 'search')
        $articles = $query->paginate(15)->appends($request->query());

        // Lấy dữ liệu cho Menu và Sidebar
        $categories = Category::all(); 
        $sources = Source::all(); 

        return view('news.index', compact('articles', 'categories', 'sources'));
    }

    // 2. LỌC TIN THEO DANH MỤC
    public function category($id)
    {
        $currentCategory = Category::findOrFail($id);
        $articles = $currentCategory->articles()
                                     ->with(['source', 'categories'])
                                     ->orderBy('id', 'desc')
                                     ->paginate(15);
                                     
        $categories = Category::all();
        $sources = Source::all(); // Cần biến này để hiển thị sidebar
        
        return view('news.index', compact('articles', 'categories', 'sources', 'currentCategory'));
    }

    // 3. LỌC TIN THEO NGUỒN BÁO
    public function source($id)
    {
        $currentSource = Source::findOrFail($id);
        $articles = $currentSource->articles()
                                     ->with(['source', 'categories'])
                                     ->orderBy('id', 'desc')
                                     ->paginate(15);
                                     
        $categories = Category::all();
        $sources = Source::all();
        
        return view('news.index', compact('articles', 'categories', 'sources', 'currentSource'));
    }

    // 4. XEM CHI TIẾT
    public function show($id)
    {
        $article = Article::with(['source', 'categories', 'comments' => function($q) {
            $q->whereNull('parent_id')->orderBy('id', 'desc');
        }])->findOrFail($id);
        
        return view('news.show', compact('article'));
    }

    // 5. CÁC HÀM XỬ LÝ KHÁC (Comment, Like, Tim)
    public function comment(Request $request, $id)
    {
        $request->validate(['name'=>'required', 'content'=>'required']);
        Comment::create([
            'article_id' => $id, 'name' => $request->name, 
            'content' => $request->content, 'parent_id' => $request->input('parent_id')
        ]);
        return redirect()->back()->with('success', 'Đã gửi bình luận!');
    }

    public function react($id, $type)
    {
        $comment = Comment::findOrFail($id);
        ($type == 'like') ? $comment->increment('likes') : $comment->increment('loves');
        return redirect()->back();
    }

    public function loveArticle($id)
    {
        Article::findOrFail($id)->increment('loves');
        return redirect()->back();
    }

    public function likeComment($id)
    {
        Comment::findOrFail($id)->increment('likes');
        return redirect()->back();
    }
}