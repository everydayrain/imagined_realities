---
author: Chris
title: A Basic LAMP Stack Install Guide
date: 2022-11-08
---

This post is dedicated to an example build of that staple of self-hosted, web-based, home projects: the _LAMP_ stack. For those that don't know, the LAMP stack is the foundation of creating a web server. [These folks](https://www.ibm.com/cloud/learn/lamp-stack-explained) define the LAMP acronym as **L**inux, **A**pache, **M**ySQL, and **P**HP, though there are substitutions such as Perl or Python to that last for dynamic scripting in web pages. Basically, if you want to host your own web pages, whether on your internal network or on the public internet, the LAMP stack is your first stop on a journey of all things web-server based.

I want to dive right in, but first a couple of notes: For this guide, I have outlined a MariaDB install instead of MySQL. For my purposes, I want to install LAMP stacks on Raspberry Pis. Raspbian OS as a Debian distro doesn't come pre-populated with repositories for MySQL 5.5.3+. You can find such repositories among those currently maintained by Oracle, if you are inclined to stick with MySQL. Alternatively, you can easily find MariaDB in the Raspbian repositories and MariaDB is styled by its creators as a "drop-in." By that term, they seem to mean that it accepts MySQL syntax, and is probably compatible with a lot of use cases. I can confirm for initial database config, it certainly works for a lot of services I run.

Oh, and just an acknowledgement: I owe a dept of student learning to other blogs in my journeys with LAMP stacks. Check out [LinuxBabe](https://www.linuxbabe.com/linux-server/install-apache-mariadb-and-php7-lamp-stack-on-ubuntu-16-04-lts) in particular. If you have any problems with this sequence, that link is good for troubleshooting/retracing your steps.

Note: I will be using a Debian-based Linux distribution (distro), and so I will be using apt for installation. Additionally it will help to run some of the following using the superuser 'sudo' prefix before the commands.

### L - Linux: Update & Upgrade

I said I'd do an example build here. Well, I won't cover everything! You'll have to decide on a Linux distro and install it yourself since that is outside this article's aims. Suffice it to say, you'll need a working distro with a terminal shell.

First, before you start a new project, you want to make sure your repositories have the most recent versions of what you are after (that is "recent" within the scope of your repositories' release model). In Debian (or Raspbian OS) for example you'd update using apt:

```
sudo apt update && sudo apt upgrade -y
```

### A - Install Apache2

Next, we start building the server using Apache:

```
sudo apt install -y apache2 apache2-utils
```

You can verify your installation of Apache2 using the following:

```
systemctl status apache2
```

You should receive a report that says its "loaded" and "active(running)."

You'll next want to make sure that Apache starts at boot:

```
sudo systemctl enable apache2
```

If you are installing Apache on your local machine you can also go to the localhost IP (127.0.0.1) to verify that it is working. You should see a "It works!" page.

You should also set the Apache user as the owner of the web root, instead of the default of the root user:

```
sudo chown www-data:www-data /var/www/html/ -R
```

Next you have to configure Apache for hosting a page by creating a .config file for the page's IP. Using the nano editor be sure to replace the text in brackets with your hostname:

```
sudo nano /etc/apache2/sites-available/[yourwebpage].conf
```

Now copy the following text into that blank document. Insert your IP address or a domain name pointing to your IP after VirtualHost:

```
	<VirtualHost 127.0.0.1:80>

      <Directory /apache/htdocs>

        Require all granted

        Options None

      </Directory>
        </VirtualHost>
```

Save, exit, and enable this virtual host:

```
sudo a2ensite [yourwebpage].conf
```

Enable the rewrite Apache module:

```
sudo a2enmod rewrite
```

Restart Apache to apply changes:

```
sudo systemctl restart apache2.service
```

### M - Install MariaDB Server

As I mentioned, I will install MariaDB instead of MySQL:

```
sudo apt install mariadb-server mariadb-client
```

You'll also need to secure MariaDB. Run the following script; it will take you to an interactive terminal interface where you can populate the fields with regular text.

That is:

```
sudo mysql_secure_installation
```

A few pointers:

> - When it asks you to enter MariaDB root password, press `Enter` key as the root password isn’t set yet.
> - Don’t switch to unix_socket authentication because MariaDB is already using unix_socket authentication.
> - Don’t change the root password, because you don’t need to set root password when using unix_socket authentication.
> - You do want to remove anonymous users
> - You do want to disallow root login remotely
> - You do want to remove test database and access to it
> - You do want to reload privilege tables

You'll also need to configure a new database specifically for the service or app you wish to run. Very generally speaking, this is the kind of sequence you might go through to configure a database (replacing the stuff in brackets with your own designations):

```
sudo mariadb -u root -p
```

```
MariaDB [(none)]> CREATE DATABASE [somedatabasename];
```

```
MariaDB [(none)]> CREATE USER '[someusername]'@'localhost' IDENTIFIED BY '[somepassword]';
```

```
MariaDB [(none)]> GRANT ALL PRIVILEGES ON [somedatabasename].* TO '[someusername]'@'localhost';
```

```
MariaDB [(none)]> exit;
```

And enable MariaDB to start at boot:

```
sudo systemctl enable mariadb
```

### P - Install PHP

What version of PHP you are able to install will depend upon your distro. For example, if you are using Debian, you might have to check which version of PHP is available in your repositories. You can check for those Debian-PHP versions [at this page](https://wiki.debian.org/PHP#PHP_and_Debian). If you have a rolling release distro or one with non-Debian repositories, you might check to see what version is supported. At the time of this writing, PHP7.4 was all I could find on Debian Bullseye. When you know what you are after, substitute the version number into these installation candidates:

```
sudo apt install php7.4 libapache2-mod-php7.4 php7.4-mysql php-common php7.4-cli php7.4-common php7.4-opcache php7.4-readline php7.4-mbstring php7.4-gd php7.4-curl
```

Then enable the service to run at boot:

```
sudo a2enmod php7.4
```

Then restart the Apache module to recognize PHP:

```
sudo systemctl restart apache2
```

Next, you can check to see if it is working by creating the following file:

```
sudo nano /var/www/html/info.php
```

Paste the following into that file:

```
<?php phpinfo(); ?>
```

Then head over to your hostname or localhost IP appended with /info.php. You should find an output stating your PHP version. If you are simply self-hosting on your local network only, without a public domain name, then use: http://127.0.0.1/info.php. That is a sign that you've successfully installed PHP.

For security purposes, make sure to remove that file once you are done:

```
sudo rm /var/www/html/info.php
```

And that's it! You've got the basics of a LAMP stack. There are a variety of other technologies to explore in hosting web pages, this is only the start. And of course you'll have the specific configuration steps next for the service you wish to run. Happy journeys!
