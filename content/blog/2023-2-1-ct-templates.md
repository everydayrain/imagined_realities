---
author: Chris
title: Unofficial CT Templates In Proxmox
date: 2023-02-01
---

{% imagesmall '/img/canonical.png', '' %}

I've been toying around with system containers (CT for short) in Proxmox, trying to learn more about how they differ from application containers. One challenge has been figuring out how to obtain "templates" for these Linux-based system containers.

In this tutorial I'll run through how to download a CT template from [Canonical's image server](https://us.lxd.images.canonical.com/images/) using Proxmox's graphical user interface (GUI).

### The Problem

In a default installation, Proxmox provides what they call "officially supported distribution" templates through the GUI. If you need one of those containers, its a breeze to set one up. If you want a system outside of those offerings for your container, then you've got to do some searching. And while [the Proxmox documentation](https://pve.proxmox.com/pve-docs/index.html) is adequate for a number of other issues, on the topic of unofficial CT templates, it has little to say.

## Background

### What is LXC?

The short hand for system containers is LXC. LXC is [described by](https://linuxcontainers.org/lxc/introduction/) its project leaders as "userspace interface for the Linux kernel containment features." If I were to try to interpret that as someone from outside computer science, I'd say LXC is a way of interacting with Linux's own ability to create containers.

### Officially Supported Distributions

To set up one of Proxmox's official CT templates, you simply select one of your storage options in the left-hand tree, select "CT Templates" in the middle pane, and finally select the "Templates" button.

{% imagesmall '/img/ct_repository_button.png', '' %}

That will open up a pop up and you can search for your distribution of choice.

{% imagesmall '/img/temp_menu.png', '' %}

### Uploading Unofficial Templates

First, do some research at [Canonical's image server](https://us.lxd.images.canonical.com/images/) to determine which distribution you're looking for that Proxmox doesn't offer. Once you've narrowed that down, locate the link for "rootfs.tar.xz".

For example, if I wanted to download a CT template for OpenWrt, I'd locate the distribution in that Canonical menu, select the architecture for my Proxmox host, maybe select the latest distribution and then arrive at a screen with options like the following photo. Again, that after file your after is called "rootfs.tar.xz"

{% imagesmall '/img/openwrt.png', '' %}

Copy the URL for that file.

To download OpenWrt's CT Template, you'll use the URL you just copied but using the method above. Instead of selecting the "Templates" button, select the "Download from URL" button.

{% imagesmall '/img/ct_download_button.png', '' %}

That will lead to a popup menu. The first field in the popup is for the URL you just copied. Paste it in, then give it a name. The name will have to end with the extension ".tar.xz".

{% imagesmall '/img/download_pop.png', '' %}

Make sure you have the "Advanced" box next to the "Download" button selected. That will give you additional options for checksums. Select SHA-256 from the drop down. Then head back to Canonical's webpage for OpenWrt and find the SHA256SUM file:

{% imagesmall '/img/sha.png', '' %}

Open that file, and it'll display the hashes for the rootfs.tar.xz files on the previous page. Find the hash for rootfs.tar.xz, copy it, and head back to the Proxmox GUI. Paste that copied hash into the checksum box.

Hit download and you are off! That'll give you an unofficial template to use with Proxmox's "Create CT" tool.
