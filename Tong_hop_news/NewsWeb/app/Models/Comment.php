<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    use HasFactory;
    
    protected $fillable = ['article_id', 'name', 'content', 'parent_id', 'likes'];

    // Quan hệ để lấy các câu trả lời con
    public function replies()
    {
        return $this->hasMany(Comment::class, 'parent_id');
    }
}