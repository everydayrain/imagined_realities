---
title: Compiling Wallabag & Self-Hosting in 2019
date: 2022-02-06
---

Following on the success of setting up my first Raspberry Pi with PiHole, I picked up a second to continue tinkering. For the second I purchased a Raspberry Pi 3b+ and installed [Wallabag](https://wallabag.org/en). Wallabag is a "read-it-later" style service that allows you to save web pages as text. The app works on a LAMP stack creating a database of annotations and tags for the web pages you save as part of a personal database.

It certainly wasn't easy for a Bash novice like myself to compile Wallabag on my own, but it was a great learning experience. If I had to do it again today, I'd first do some research about container options for the install. That would probably make it easier to set up networks, HTTPS, and ensure fewer dependency problems down the road.

This is a record of my steps and a few hiccups from back in 2019 when I tackled this project.

### A brief word on self-hosting

There are other options to take advantage of Wallabag if you need an easier alternative. Wallabag offers a pay by the month hosted service. There are some pre-made software packages for other hosted services; Yubohost is among the possibilities. I believe the Softalicious suite provided by many website hosts even has a Wallabag module that might make instillation pretty straightforward on a website.

I wanted to "self-host" however. For one thing, I wanted the CLI training. For another, I believe that information about people's reading habits is a privacy risk. I ought to be the only one with a comprehensive view of what I read. That is becoming a tougher ask each day it seems.

### References

I relied on the work of others, particularly [raspbiblog](https://raspiblog.noblogs.org/post/2018/01/31/self-hosting-your-wallabag-to-your-raspberry-pi/), [Linux Babe](https://www.linuxbabe.com/ubuntu/install-wallabag-ubuntu-16-04), and [this website](https://nxnjz.net/2019/02/install-wallabag-on-ubuntu-18-04-lts/) to set up. I'll cover many of the steps here, but these were touchstones.

### Raspbian Headless Install & Securing

As I said, I wanted the experience, and to be comprehensive in using the RPI. So I first flashed Raspbian Lite [as a headless setup](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi) to my SD card. I connected to it using putty, and then proceeded to secure the board. I then instituted SSH key-based login over my LAN. I won't go into details with this part, there are plenty of guides. [The securing a raspberry pi page](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi) is worth a look for those who are unfamiliar.

Regarding depenencies and associated programs, I needed compose to help deal with PHP. I don't recall if it comes standard on Raspbian Lite, but you'll need it. Compose is in the Raspbian repositories. You'll also need git, and find that in the same.

Also, I secured my site hosted on No-Ip with HTTPS by using [Certbot](https://certbot.eff.org/) in connection with [Lets Encrypt!](https://letsencrypt.org/). However, I'll save that setup for a separate post since it can be reasonably done after the Wallabag install. I just want to note here that it invovled installing systemd. Back in 2019, Raspbian lite came with sysvinit instead, so it took some detective work to figure out why Certbot wasn't working.

### The LAMP Stack

The first part of this project lies in creating a LAMP stack. According to [these folks](https://www.ibm.com/cloud/learn/lamp-stack-explained), that is a combination of Linux, Apache, MySQL, and PHP (or Python/Perl), though in this case I use MariaDB instead of MySQL.

It helps to run these installs using sudo or as the root user, but don't do that for the next section. I followed the instructions over at [LinuxBabe](https://www.linuxbabe.com/linux-server/install-apache-mariadb-and-php7-lamp-stack-on-ubuntu-16-04-lts) on the LAMP stack install.

You'll also want to install a number of php modules. Ensure that you have the following:

```
sudo apt install php7.4-bcmath php7.4-xml php7.4-zip php7.4-curl php7.4-mbstring php7.4-gd php-tidy php-intl
```

#### Composer Hell

Also ensure that you have composer. I've had a ton of problems with composer from the standard RaspbianOS repos over time, so I've come to learn that it makes more sense to install a local version in the wallabag file than to rely on a global version from the repo. In part this is born of the experince that the repo version is often so old that it won't work with wallabag's version. These instructions are cribbed from [the composer site](https://getcomposer.org/download), and will change after the time of this writing, it'd be best to go to the website and follow their instructions. For the sake of completeness, here is what I did:

```
cd [your/wallabag/directory]
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === '55ce33d7678c5a611085589f1f3ddf8b3c52d662cd01d4ba75c0ee0459970c2200a51f492d557530c71c15d8dba01eae') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```

When I installed, I recieved composer 2.3.10, whereas the wallabag composer.lock file threw an error on requireing less than 2.3. If you get the same error down the line, run:

```
php composer.phar self-update --2.2
```

Because a lot of the LAMP stack services were available to install through the Raspbian apt repositories, it is pretty straightforward to install the primary services and dependencies.

Aside from securing the MariaDB, which the link above covers, you'll also need to configure a new database specifically for Wallabag. In particular, I used these instructions:

```
sudo mysql -u root -p
```

```
MariaDB [(none)]> CREATE DATABASE wallabag;
```

```
MariaDB [(none)]> CREATE USER 'wallabaguser'@'localhost' IDENTIFIED BY 'wallabagpassword';
```

```
MariaDB [(none)]> GRANT ALL PRIVILEGES ON wallabag.* TO 'wallabaguser'@'localhost';
```

```
MariaDB [(none)]> exit;
```

Next you have to configure Apache by creating a .config file for Wallabag's IP. I used the nano editor:

```
nano /etc/apache2/sites-available/wallabag.conf
```

Use the following text for that blank file. Insert your IP address or a domain name pointing to your IP for ServerName. I chose to use port 443 for HTTPS. If you choose to go that route you'll have to reconfigure the VirtualHost line as well.

    <VirtualHost *:80>
    ServerName IP_or_DOMAIN_NAME
    DocumentRoot /var/www/wallabag/web
    <Directory /var/www/wallabag/web>
        AllowOverride None
        Order Allow,Deny
        Allow from All
        <IfModule mod_rewrite.c>
            Options -MultiViews
            RewriteEngine On
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteRule ^(.*)$ app.php [QSA,L]
        </IfModule>
    </Directory>
    <Directory /var/www/wallabag/web/bundles>
        <IfModule mod_rewrite.c>
            RewriteEngine Off
        </IfModule>
    </Directory>
    ErrorLog /var/log/apache2/wallabag_error.log
    CustomLog /var/log/apache2/wallabag_access.log combined
    </VirtualHost>

Save, exit, and enable this virtual host:

```
sudo a2ensite wallabag.conf
```

Enable the rewrite Apache module:

```
sudo a2enmod rewrite
```

Restart Apache to apply changes:

```
sudo systemctl restart apache2.service
```

### Compiling Wallabag

Nowadays you can clone Wallabag from a git repository. You should choose a location (many suggest /var/wallabag) and then run:

```
git clone https://github.com/wallabag/wallabag.git
```

Now you'll want to move the wallabag folder over to your apache directory:

```
sudo mv wallabag /var/www/
```

```
cd wallabag
```

If I assume that you, dear reader, are maintaining this solo, eventually you'll want to make sure there are 750 permissions on the files and folder, but if you have problems installing use abundant permissions and change them back to this after you are successful:

```
sudo chmod 750 -R [/YOUR/LOCATION/wallabag]
```

Before you compile it wouldn't hurt to verify with composer that you have the recommended dependencies:

```
php composer.phar update
```

Next you compile, but you want to make sure you run from the apache user and _not_ as root, so do the following. Make sure you are in the /var/www/wallabag folder when you run these:

```
sudo -u www-data /bin/bash
php composer.phar install
```

There will be a big output from the command. Once the compile gets going without errors, you have a lot of output as composer deals with the dependencies. Eventually you'll reach a section where you'll have to input information. You can hit enter to use the defaults, but, at a minimum, you'll want to enter in the user, password and name of the MariaDB, the domain information, and a password for the secret parameter:

```
Generating optimized autoload files
> Incenteev\ParameterHandler\ScriptHandler::buildParameters
Creating the "app/config/parameters.yml" file
Some parameters are missing. Please provide them.
database_driver (pdo_mysql):
database_driver_class (null):
database_host (127.0.0.1):
database_port (null):3306
database_name (wallabag):
database_user (root): wallabag
database_password (null): MYgoodPasWord
database_path (null):/var/lib/mysql/wallabag
database_table_prefix (wallabag_):
database_socket (null):
database_charset (utf8mb4):
domain_name ('https://your-wallabag-url-instance.com'): https://mydomain.dynamicdns.com:88XX
mailer_transport (smtp):
mailer_host (127.0.0.1):
mailer_user (null):
mailer_password (null):
locale (en):
secret (ovmpmAWXRCabNlMgzlzFXDYmCFfzGv): thisshouldbegeneratedsecret
twofactor_auth (true):
twofactor_sender (no-reply@wallabag.org): myemailsender@host.com
fosuser_registration (true): false
fosuser_confirmation (true): false
from_email (no-reply@wallabag.org): myemailsender@host.com
rss_limit (50):
rabbitmq_host (localhost):
rabbitmq_port (5672):
rabbitmq_user (guest):
rabbitmq_password (guest):
rabbitmq_prefetch_count (10):
redis_scheme (tcp):
redis_host (localhost):
redis_port (6379):
redis_path (null):
redis_password (null):
> Sensio\Bundle\DistributionBundle\Composer\ScriptHandler::buildBootstrap
> Sensio\Bundle\DistributionBundle\Composer\ScriptHandler::clearCache
```

If you have problems compiling, you should consider changing the owner of the Wallabag file to the Apache user (I think this is usually www-data).

```
chown -R www-data [/YOUR/LOCATION/]
```

As the compiler finishes installing, it will enter a final phase where it checks system requirements and then begins another series questions. I did reset the database and did set up an admin user with password.

Finally you'll have to change both the apache2.conf & 000-default.conf files to point to the file location of Wallabag (this time it was /var/wallabag/web) and restart Apache.

First, add the following to the virtual hosts section of apache2.conf file in the apache2 folder:

    <Directory /var/www/wallabag/web/>
    		Options Indexes FollowSymLinks
    		AllowOverride None
    		Require all granted
    </Directory>

Next, modify 000-default.conf in /etc/apache2/sites-avaiable/. Using nano edit the .conf file and look for the DocumentRoot section. In that section write in the Wallabag folder location.

Ensure you have the right permissions set by implimenting the following:

```
sudo chown -R www-data:www-data /var/www/wallabag/bin
sudo chown -R www-data:www-data /var/www/wallabag/app/config
sudo chown -R www-data:www-data /var/www/wallabag/vendor
sudo chown -R www-data:www-data /var/www/wallabag/data/
sudo chown -R www-data:www-data /var/www/wallabag/web/
```

FInally, enable the Wallabag site and restart Apache:

```
sudo a2ensite wallabag
```

```
sudo systemctl restart apache2.service
```

### Port Forwarding

Ensure you have port forwarding to the port you selected in the parameters.yml file set up on your router. Since router types very so widely, I can't assist with this part.

### Verify

That should be it. Use a browser to navigate to your domain and you should see a page asking for your credentials.

There are apps on the app stores for using Wallabag on your mobile devices. I hope to cover setting up HTTPS in a seperate post.
