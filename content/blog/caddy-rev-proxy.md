---
title: Caddy Reverse Proxy with TLS and Cloudflare DNS Challenge - A Caddyfile Example
date: 2025-03-27
tags:
  - caddy
  - DNS
  - homeprod
---

Installing and configuring a {% linkprimary "Caddy", "https://caddyserver.com/" %} webserver from a binary with a Caddyfile for a reverse-proxy was a little more involved than I expected. This post clarifies a single stage of this process by illustrating how to configure a Caddyfile with an example for a reverse-proxy and TLS. This post won't cover building a Proxmox LXC container, obtaining an User API key from Cloudflare, or installing the Caddy custom binary.

## Overview in Brief

- {% linkprimary "Downloading Caddy", "https://christopherbauer.xyz/blog/caddy-rev-proxy/#downloading-and-configuring-caddy" %}
- {% linkprimary "Creating the Caddyfile", "https://christopherbauer.xyz/blog/caddy-rev-proxy/#creating-the-caddyfile" %}

## Hostname Provisioning is Homeprod

I've recently discovered how critical a reverse proxy is when using domain names and TLS. I've been homelabbing for a few years now, but I've only recently moved to making production-level services available to extended family. As any good {% linkprimary "homeprodder", "https://awfulwoman.com/notes/2024/11/homeprod-not-homelab/" %} knows, that means hostnames instead of IPs and TLS. So far so good, just set up {% linkprimary "Nginx-Reverse-Proxy", "https://nginxproxymanager.com/" %} with Cloudflare DNS challenge and you're good to go, right? Well, my version of Nginx-Reverse-Proxy lived on a server I didn't keep powered on at production-level five nines. As the number of services I'm hosting has multiplied, and the number of users has also grown, I found myself in a situation where the sudden disappearance of a hostname immediately causes a lot of problems.

If the hostname disappears, its as though the service has disappeared, and that is true not only for people unable to reach those services but also for automation. Any sort of monitoring solution will go a bit nuts if not made aware hostnames suddenly dropping off the radar, even if the underlying service is still responsive. Cron starts clogging up logs. Not to mention that I can no longer remember off-hand what the IP of a service is when there are dozens operating. That means manual troubleshooting when hostnames go missing is harder than it once was as well. Needless to say, it quickly became evident that offering hostnames by way of a reverse proxy needed to become a full time operation.

Looking into the alternatives, I learned some things. First, I didn't realize that Nginx-Reverse-Proxy isn't maintained by the official Nginx team but rather by an individual (the GUI is so polished I just assumed it was an official product). That doesn't concern me greatly, but it may explain the next thing I learned. Second, Nginx-Reverse-Proxy is only offered as a Docker container. That posed a problem. Shifting a reverse proxy to the always-on Intel n100 minipc would mean spinning up a new VM just to host Docker for Nginx-Reverse-Proxy. That seemed like unacceptable overhead to me. Sure, I've heard of folks running Docker in Proxmox LXCs, but the Proxmox team {% linkprimary "don't recommend it", "https://pve.proxmox.com/wiki/Linux_Container" %} and my Proxmox host is janky enough as is. With that in mind, I created a LXC with a reverse proxy using a Caddy binary.

## Assumptions

This guide will assume the reader is familiar with the linux command line, has a domain registered, and has generated a User API Token in Cloudflare to access Cloudflare's DNS management capabilities.

## Downloading Caddy

To use Caddy with the Cloudflare DNS you have to {% linkprimary "download a custom Caddy binary", "https://caddyserver.com/download" %} that builds in the dns.providers.cloudflare plugin to the finished product. Once you've downloaded the binary, you can use {% linkprimary "this docs page", "https://caddyserver.com/docs/running#manual-installation" %} for instructions on how to proceed.

To quickly recap my steps, I placed the downloaded binary in my path and added a group and user with parameters tailored to Caddy. I made sure the binary in `/usr/bin/` was executable by world. Next I {% linkprimary "created a systemd unit file", "https://github.com/caddyserver/dist/blob/master/init/caddy.service" %}. According to {% linkprimary "the docs", "https://caddyserver.com/docs/running#manual-installation" %}, I selected the systemd caddy.service (non-api) unit file type, went to its github page, and manually entered that code into a file:`/etc/systemd/system/caddy.service`.

## Creating the Caddyfile

I then created a Caddyfile at `/etc/caddy/Caddyfile`, with the following initial wildcard certificate DNS request to Cloudflare based on [this format](https://caddyserver.com/docs/caddyfile/patterns#wildcard-certificates).  Below I offer an example of what this Caddyfile can look like.  The example sets up the DNS challenge for TLS and then creates proxies for hypothetical Plex and Nextcloud instances. Readers can add or modify according to their needs.


```shell
*.example.com {
        tls {
                dns cloudflare <SOME_CLOUDFLARE_API_KEY>
        }

        @plex host plex.example.com
        handle @plex {
                reverse_proxy <PLEX_IP:PORT>
        }

        @nextcloud host nc.example.com
        handle @nextcloud {
                reverse_proxy <NEXTCLOUD_IP:PORT>
        }

        log {
                output file /var/log/caddy/<SOME_FILENAME>.log
        }
}
```

Whenever you update that file, be sure to reload Caddy using `systemctl reload caddy` rather than Caddy's command line commands.

## Conclusion

I spent a few more minutes than I would have liked trying to sort out the Caddyfile's particulars. They weren't hard to get right, but the documentation wasn't immediately clear either. Hope this saves you a few minutes somewhere down the line. 

Should you want to connect, feel free reach out on {% linkprimary "Mastodon", "https://infosec.exchange/@anthro_packets" %}.
