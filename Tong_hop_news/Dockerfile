FROM php:8.2-apache

# Thư mục làm việc
WORKDIR /var/www/html

# Bật mod rewrite cho Laravel
RUN a2enmod rewrite

# Cài thư viện cần thiết
RUN apt-get update && apt-get install -y \
    zip unzip curl git libpng-dev libonig-dev libxml2-dev

# Cài extension cho PHP
RUN docker-php-ext-install pdo pdo_mysql mbstring gd

# Trỏ Apache về thư mục public của Laravel
RUN sed -i 's!/var/www/html!/var/www/html/public!g' /etc/apache2/sites-enabled/000-default.conf

# Copy đúng source Laravel (đang nằm trong thư mục con)
COPY Tong_hop_news/NewsWeb/ /var/www/html/

# Cài Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Cài package Laravel
RUN composer install --no-dev --optimize-autoloader

# Phân quyền cho Laravel ghi cache/log
RUN chmod -R 777 storage bootstrap/cache

EXPOSE 80

CMD ["apache2-foreground"]
