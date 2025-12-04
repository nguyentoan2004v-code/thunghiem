<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Source extends Model
{
    use HasFactory;

    protected $table = 'sources';

   
    // Khai báo: Một Nguồn báo (Source) có nhiều Bài viết (Articles)
    public function articles()
    {
        return $this->hasMany(Article::class, 'source_id', 'id');
    }
}