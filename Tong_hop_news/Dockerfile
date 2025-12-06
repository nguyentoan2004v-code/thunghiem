# Tong_hop_news/Dockerfile

# =========================================================================
# Giai đoạn 1: Builder - Cài đặt dependencies và chạy lệnh build
# =========================================================================
FROM php:8.2-fpm-alpine AS builder

# 1. CÀI ĐẶT CÁC GÓI HỆ THỐNG VÀ EXTENSION CHO PHP
RUN apk update && apk add --no-cache \
    nginx \
    nodejs \
    npm \
    libzip-dev \
    # Cài đặt các extension PHP cần thiết cho Laravel và MySQL
    && docker-php-ext-install pdo pdo_mysql opcache ctype mbstring openssl bcmath zip

# 2. CÀI ĐẶT COMPOSER
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 3. COPY MÃ NGUỒN
WORKDIR /app
COPY . /app

# 4. THỰC THI CÁC LỆNH BUILD (trong thư mục NewsWeb)
RUN composer install --working-dir=NewsWeb --prefer-dist --no-dev --optimize-autoloader
RUN npm install --prefix NewsWeb && npm run build --prefix NewsWeb

# 5. CHẠY LARAVEL SETUP
RUN cp NewsWeb/.env.example NewsWeb/.env
RUN php NewsWeb/artisan key:generate --force
RUN php NewsWeb/artisan migrate --force

# =========================================================================
# Giai đoạn 2: Final - Khởi chạy Nginx và PHP-FPM
# =========================================================================
FROM alpine:3.18 AS final

# Copy các thành phần cần thiết
COPY --from=builder /usr/sbin/nginx /usr/sbin/nginx
COPY --from=builder /usr/local/sbin/php-fpm /usr/local/sbin/php-fpm
COPY --from=builder /usr/local/bin/php /usr/local/bin/php
COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /lib /lib
COPY --from=builder /usr/local/etc/php-fpm.d/www.conf /usr/local/etc/php-fpm.d/www.conf
COPY --from=builder /app /app

# CẤU HÌNH NGINX
RUN mkdir -p /etc/nginx/conf.d
RUN echo "server { \
    listen 8080; \
    root /app/NewsWeb/public; \
    index index.php; \
    location / { \
        try_files \$uri \$uri/ /index.php?\$query_string; \
    } \
    location ~ \.php$ { \
        fastcgi_pass 127.0.0.1:9000; \
        fastcgi_index index.php; \
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name; \
        include fastcgi_params; \
    } \
}" > /etc/nginx/conf.d/default.conf

# Thiết lập cổng và lệnh khởi chạy
EXPOSE 8080
CMD php-fpm && nginx -g "daemon off;"