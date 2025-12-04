<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Category extends Model
{
    use HasFactory;
    
    protected $table = 'categories';
    
    // Hàm này BẮT BUỘC phải có 'return'
    public function articles()
    {
        return $this->belongsToMany(Article::class, 'article_category', 'category_id', 'article_id');
    }
}