# Bắt đầu từ image PHP + Apache
FROM php:8.2-apache

# Đặt working directory
WORKDIR /var/www/html

# Bật mod_rewrite để Laravel sử dụng đường đẹp / lịch sử url
RUN a2enmod rewrite

# Cài các thư viện cần thiết + công cụ hỗ trợ
RUN apt-get update && apt-get install -y \
    zip unzip curl git \
    libpng-dev libonig-dev libxml2-dev \
    && docker-php-ext-install pdo pdo_mysql mbstring gd

# Copy toàn bộ mã nguồn vào container
COPY . /var/www/html

# Cài Composer (nếu bạn dùng composer để quản lý thư viện)
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Chạy composer install để cài dependencies PHP
RUN composer install --no-dev --optimize-autoloader

# Đảm bảo quyền ghi cho các thư mục Laravel cần write
RUN chmod -R 777 storage bootstrap/cache

# Expose cổng 80 (webserver Apache)
EXPOSE 80

# Lệnh khi container khởi động
CMD ["apache2-foreground"]
