# Use an official PHP image as the base image
FROM php:7.4-apache

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy the contents of the local web-ui folder to the container's working directory
COPY . /var/www/html/

# Expose port 80 for the Apache web server
EXPOSE 80

# Define a volume for /web-db to allow data to persist outside the container
VOLUME ["/web-db"]

# Disable PHP access log
RUN sed -i 's/CustomLog .*/CustomLog \/dev\/null combined/' /etc/apache2/apache2.conf

# Start the Apache web server
CMD ["apache2-foreground"]
