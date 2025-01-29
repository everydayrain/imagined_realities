---
title: Installing Pi-hole on a RPI3B+
date: 2022-06-13
---

I hesitate to write up my experience installing Pi-hole because, even back in 2019, the installation was a snap. As it turns out, I had to go through this process again in 2022 when I updated the OS on my Raspberry Pi. Still, because installing Pi-hole was my first experience with Linux it deserves the write-up treatment. It was also my first experience completing a project using CLI tools. I have to pay tribute to that victory, to that event that helped me see the virtue of Unix machines. So buckle up for my take on installing Pi-hole!

For those that don't know, Pi-hole bills itself as a "DNS sinkhole." And with that, Pi-hole has already provided us with riches in the form of including "sinkhole" in our daily vocabulary. Basically they mean its a network-based adblocker. I won't go into the details of how a DNS sinkhole works in this post, as there is ample documentation on [Pi-hole.net](https://docs.pi-hole.net/).

Pi-hole is a powerful tool for all its simplicity. Unlike the powerful, though demanding, uBlockOrigin, Pi-hole has a flexibility of commitment that makes it a nice SOHO option. Of course, uBlockOrigin performs a different service and obtains different ends, but for the sake of comparing daily overhead, Pi-hole is a lot less needy. It can take a lot of config, or it can be relatively hands off (after you upload some blocklists and tweak your router). The choice is yours!

# Installing RaspbianOS lite

I installed Pi-hole on a Raspberry Pi 3b+ (RPI). It was my first experience with RPIs, Raspbian OS, and with the command line (CLI). Up to this point I had worked entirely within Microsoft's ecosystem, with the exception of some open-source office apps. I had made a lot of tweaks on Windows to reduce telemetry, but that is for a different post.

While the desktop OS for Raspbian was certainly nice, I immediately saw the utility of the command line and instead switched out of all the noise of a desktop to a headless setup. That is, I wanted to access the RPI remotely, without a need for an additional monitor, keyboard, or mouse on the RPI. In truth, I did this in part to save money and not have to connect my RPI to my TV for a monitor every time I wanted to run a shell.

I installed Raspbian on a headless setup and used Putty on my Windows machine to configure the RPI. To install a headless version of Raspbian, I needed to flash the Raspbian lite system image to an SD card. Nowadays you can find a [handy installer](https://www.raspberrypi.com/software/) (that includes all the system images) from the Raspberry Pi foundation itself. Back then I had to find an SD card; format it using the SD foundation's formatter; download Etcher; get the system iso (using torrent magnet link - of course); and then flash the iso to the sd card.

To access a bash shell on the newly minted Raspbian OS, I wanted to use SSH. This meant I had to set up wireless networking and SSH by placing a wpa_supplicant.conf file and a SSH file (no extension) in the boot folder of the new Rasbian OS SD card. You can find instructions on the Raspberry Pi site [here](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi). In sum, the .conf file just required a few tweaks about the SSID and passkey for my network. Upon the first boot wpa_supplicant.conf aided in establishing connection to my wireless network and from there I could can go headless and sign in over SSH.

This method is still relevant, and you can find some documentation [here](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi).

# The easy part - installing Pi-hole

Installation was pretty simple from there. Back then, the Pi-hole organization recommended using a "one-step automated install" using a curl command that piped to bash (this is [still an option](https://docs.pi-hole.net/main/basic-install/?h=curl) incidentally). It was among the only options to install Pi-hole on the RPI, and given that I was a noob, it seemed like the best way to facilitate install. While I recommend you use the link above to ensure you understand all of the details, I 'll include that curl command here for the sake of posterity.

```
curl -sSL https://install.pi-hole.net | bash
```

This command takes care of all of the server installation for you, no need to go out and install any database, or DNS server components individually. Really easy.

Even at that time, the developers of Pi-hole pointed out that this was a controversial move, to their credit. I took the risk because I knew Pi-hole was reputable and figured I could wipe the SD card if something was awry. The stakes were low. Upon running the command, Pi-hole was flawless on the install, and pretty hands off.

I'll skip over some of the webUI based config of Pi-hole as mertiting a post in its own right. Identifying blocklists to import, and establishing groups of your SOHO hosts are worth the time. Group management options are pretty useful for a household like mine, where there are personal and work hosts that can tolerate intermediary devices like a Pi-hole differently. Also, my wife has different preferences for certain social media that can get caught by Pi-hole's lists, so the granularity of selecting lists for hosts is really nice. The group settings help our household balance a bunch of different preferences.

One point on privacy - Pi-hole by default is going to log all your dns requests. It is capable of some cool dashboard analytics in this regard, though unless you've gone to the trouble of gathering a baseline of your network, they lack context (posters on r/pihole are forever asking if Pi-hole's X% blocked figure is "good/bad/broken" ect, without realizing its all relative to their network's typical performance). In principle sinkhole logs are handy, to ensure that you know what devices are calling to known malicious/known anti-privacy domains. Whether long-term storage is necessary to achieve that however may be up for debate.

Moreover, these logs are basically one more store of record on all your internet habits. I can't comment on other people's setups, but I installed Pi-hole on a Raspberry Pi, that has very modest security features, and they aren't enabled by default. I don't know for sure, but I don't think Raspbian supports OS-level encryption, for example. I'm not too comfortable with anyone, blackhat or otherwise, having access to that kind of info. We do indeed live in a world of logs, so it is kind of like putting your finger in a dam to suggest avoiding this particular log, but I turned long-term logging off.

# Configuring router settings

At this point you still probably won't have your traffic traversing through your Pi-hole host. Next step is to redirect dns query traffic to the Pi-hole host in order to identify, allow/block, and log the traffic. This is relatively straightforward but the exact config will depend upon your router.

For an Edgerouter X, this was as simple as entering the Pi-hole host IP into the DNS server field of the DHCP server scope options. First you access your router Web UI using its IP in your browser. The flow for EdgeOS to the DNS option is: Services tab > DHCP tab > Actions dropdown > view details > DNS 1 field.

Pi-hole also recommends setting upstream DNS providers. Of course you can select whatever you like, but for me I installed unbound to work with Pi-hole as a DNS solution. But that is for another post.

That was it! Find some blocklists like the ones that Pi-hole recommends, or web search for lists suited to your specific devices and you're off.
