<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB; // Nhớ thêm dòng này để dùng DB::table

return new class extends Migration
{
    public function up(): void
    {
        // 1. Bảng Nguồn báo
        Schema::create('sources', function (Blueprint $table) {
            $table->id();
            $table->string('name');
        });

        // 2. Bảng Danh mục
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name');
        });

        // 3. Bảng Bài viết
        Schema::create('articles', function (Blueprint $table) {
            $table->id();
            $table->string('title', 500);
            
            
            $table->string('link', 191)->unique()->nullable(); 
            // ------------------------------------
            
            $table->longText('content')->nullable();
            $table->string('image_url', 500)->nullable();
            $table->dateTime('published_date')->nullable();
            $table->unsignedBigInteger('source_id')->nullable();
            $table->integer('loves')->default(0); 
            $table->timestamps();

            $table->foreign('source_id')->references('id')->on('sources')->onDelete('cascade');
        });

        // 4. Bảng Trung gian
        Schema::create('article_category', function (Blueprint $table) {
            $table->unsignedBigInteger('article_id');
            $table->unsignedBigInteger('category_id');
            $table->primary(['article_id', 'category_id']);
            
            $table->foreign('article_id')->references('id')->on('articles')->onDelete('cascade');
            $table->foreign('category_id')->references('id')->on('categories')->onDelete('cascade');
        });

        // 5. Bảng Bình luận
        Schema::create('comments', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('article_id');
            $table->unsignedBigInteger('parent_id')->nullable();
            $table->string('name');
            $table->text('content');
            $table->integer('likes')->default(0);
            $table->integer('loves')->default(0);
            $table->timestamps();

            $table->foreign('article_id')->references('id')->on('articles')->onDelete('cascade');
        });
        
        // 6. Nạp dữ liệu mẫu
        DB::table('categories')->insert([
            ['name' => 'Chính trị - Xã hội'], ['name' => 'Thế giới'],
            ['name' => 'Kinh doanh'], ['name' => 'Giáo dục'],
            ['name' => 'Thể thao'], ['name' => 'Pháp luật'],
            ['name' => 'Giải trí'], ['name' => 'Công nghệ'],
            ['name' => 'Sức khỏe'], ['name' => 'Đời sống'],
        ]);
        
        DB::table('sources')->insert([
            ['name' => 'VNExpress'], ['name' => 'Tuổi Trẻ'], ['name' => '24h']
        ]);
    }

    public function down(): void
    {
        Schema::dropIfExists('comments');
        Schema::dropIfExists('article_category');
        Schema::dropIfExists('articles');
        Schema::dropIfExists('categories');
        Schema::dropIfExists('sources');
    }
};