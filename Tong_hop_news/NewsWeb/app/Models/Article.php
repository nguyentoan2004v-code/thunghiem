<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
// use App\Models\Comment; // Dòng này không bắt buộc nếu cùng thư mục, nhưng viết vào cho chắc

class Article extends Model
{
    use HasFactory;
    
    protected $table = 'articles';

    public function source() {
        return $this->belongsTo(Source::class, 'source_id', 'id');
    }

    public function categories() {
        return $this->belongsToMany(Category::class, 'article_category', 'article_id', 'category_id');
    }
    
    // QUAN HỆ VỚI COMMENT
    public function comments() {
        
        return $this->hasMany(\App\Models\Comment::class)->orderBy('id', 'desc');
    }
}