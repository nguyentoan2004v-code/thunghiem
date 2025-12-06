FROM php:8.2-apache

WORKDIR /var/www/html

RUN a2enmod rewrite

RUN apt-get update && apt-get install -y \
    zip unzip curl git libpng-dev libonig-dev libxml2-dev

RUN docker-php-ext-install pdo pdo_mysql mbstring gd

# Copy toàn bộ repo
COPY . /var/www/html

# Trỏ Apache vào đúng thư mục public của Laravel
RUN sed -i 's!/var/www/html!/var/www/html/Tong_hop_news/NewsWeb/public!g' /etc/apache2/sites-enabled/000-default.conf

# Cài composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Chạy composer trong đúng thư mục Laravel
WORKDIR /var/www/html/Tong_hop_news/NewsWeb
RUN composer install --no-dev --optimize-autoloader

# Phân quyền
RUN chmod -R 777 storage bootstrap/cache

EXPOSE 80
CMD ["apache2-foreground"]
