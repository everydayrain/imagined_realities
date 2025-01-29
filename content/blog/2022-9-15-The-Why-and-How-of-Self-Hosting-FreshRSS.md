---
title: The Why and How of Self-hosting FreshRSS
date: 2022-09-15
---

Installing and setting up [FreshRSS](https://github.com/FreshRSS/FreshRSS) was another really simple self-hosted project. The author of FreshRSS devised an automated docker container install that is super easy to deploy. I recently rebuilt one of my Raspberry Pi 3B+s to upgrade the OS, and so reinstalled FreshRSS as well. Given that I did it so recently, and that the product has been so easy and stable, it deserves a nod! So here are some thoughts as to why and how I went about building FreshRSS at home.

Why self-host an RSS feed when you have so many attractive and easy hosted options to choose from? Well, aside from my desire to practice my technical skills, I'd rather not give others a detailed look at my reading habits. After all, the RSS feeds you follow, the posts you look at, save, and share, all can reveal a lot of insight into your habits, preferences, and interests.

## A Brief Appreciation of RSS

Anyone reading this probably already has a grasp on the value of RSS, but for the sake of promoting a very deserving protocol, and on the off chance a reader doesn't know, lets talk about RSS.

Really Simple Syndication (RSS) is "[a Web content syndication format](https://www.rssboard.org/rss-specification#whatIsRss)." Its maintainers specifically point out that it is a "dialect" of the Extensible Markup Language (XML), used for sharing web content. In other words its a way of obtaining web content, using a standardized format, without having to directly visit a website. Between the code that offers the RSS feeds and software that retrieves and displays them, one can retrieve serialized information from around the web efficiently.

Beyond these straightforward technical advantages, RSS also has informal advantages not detailed in its technical specifications. These advantages have to do with the structure of digital media today. Social media companies in particular seek to maximize the amount of time that you spend on their websites, within their ecosystems, looking at content derived on their platforms. For this reason, among others, RSS has no chance at corporate support as a means to keep up with specifically social media timelines (except for Reddit and a Twitter workaround, more on this below). RSS by contrast doesn't enforce consumption of only coporate content, but enables the liberty to follow a variety of different sources such as blogs or industry newsletters. In that regard, it has the advantage of being free of any one company's retail infrastructure and their collection of users' data. In this limited comparative sense, RSS is a liberating tech relative to the dominant models of user data capture operating today.

Some may be also aware that internet writers love to talk of the death of RSS, to much exaggeration. RSS is certainly alive and well. Not only does the standard offer an adaptable service, for everything from podcasts to The New York Times, but it also is indispensable for making sense out of the content generation machine that the web has become. Its flexibility has made consuming information a much easier task than simply that of browser tab management.

But that's not all! RSS can informally integrate following Twitter handles. When combined with Nitter (you'll have to pick an instance, but I jump around from nitter.unixfox.eu to nitter.1d4.us), you can subscribe to its RSS feeds and follow social media without quite the kind of anti-privacy features of Twitter's own products. Just head over to someone's handle, and then append **/rss** to the HTTP address. That should automatically download a file you can use with your aggregator. Many Reddit forums also offer RSS feeds, though I find following any of the more verbose options of these handles or subreddits way too prolific to manage.

## RSS Utilities

One term worth filing away: _RSS aggregators_, these are the category of software you use to collect, read, and manage articles distributed by the RSS protocol from the RSS formatted feeds you choose to follow. _RSS Readers_ are close relatives to aggregators, and sometimes overlap. There are a variety of aggregator and reader types to choose from. Some embrace aesthetic minimalism like the iOS client _Unread_ that limits options to foreground the reading experience. Others are brimming with additional utility, including functionalities to make annotations. Many have a variety of ways to optimize your flow with tags, stars, and folders. There are possibilities of integrating RSS readers into read-it-later services - it's a broad universe.

Distinguishing all this becomes a bit difficult for a lay person to straighten out when we talk about client readers versus aggregators. For example, some of you may be familiar with the web-app rss readers, such as _Feedly_, _Inonereader_, or the now (in)famous, and long dead, _GReader_. These do it all, offering a reading experience through a web user interface as well as aggregation, hosted by the service, allowing you to curate a collection of feeds (and to make things more complicated there are mobile clients for Feedly and Inonereader too). Then there are reader clients, typically for mobile devices, like iOS's _NewsBlur_, or _Feedbin_. These clients don't collect RSS feeds, but will present an aggregator's collection of feeds using their interface and functionalities as additional features.

Then there is FreshRSS, a self-hosted reader & aggregator that you run at home or through a web provider as a http server for reader clients. You can also read your feeds through its own web user interface. Since I already covered my rationale for self-hosting, lets dig right in.

## Installing a LAMP Stack on Raspbian OS (bullseye)

In setting up the fresh Raspbian OS, I had to go through all the steps of setting up a server again. To be clear, I had a simple use case that contributed to the ease of this install. I don't really spend much time away from home these days, so my use case for a RSS aggregator is that the server be available entirely through my LAN. This vastly simplifies the process, precluding the need for a hostname provided by a DNS service; configuring the Docker container to use the hostname; and the associated router configurations to isolate my raspberry pi on a vlan and securely allow traffic through my firewall.

So really, the only challenging part of these limited aims was setting up the LAMP stack. Actually, FreshRSS comes with its own SQLite database capability built in, so you might not even need to install MySQL. For more on installing a LAMP stack, see [this post](https://christopherbauer.org/2022/11/08/lamp-install.html).

One additional note: at the time of this writing FreshRSS had a requirement to use an earlier version of PHP than currently offered (its most current was 8.1). So you'll have to ensure that you install an earlier version by specifying the version number in apt.

## Install Docker

According to the [official Docker instructions](https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script), the folks at Docker do not offer a compatible repository version of docker for Raspbian OS. Instead, they recommend[ a curl script](https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script). The sharp eyed will note curl scripts are a risky business to get involved with. For one, you are installing software outside of the saftey of the package management system with its security keys ensuring that you are downloading from the right vendor. For another, this curl script is not even the script itself, but downloads the script to run with a second command.

Whether the risk is worth it is up to you dear reader. However, its worth pointing out that Docker includes information on how to implement a dry-run of the script to see what it downloads and runs prior to actually executing. That extra step is certainly a half point in their favor, even if you might not have the technical skills to interpret what you see on the dry run.

In any event, I ran that curl script and proceeded from there.

## Pull the Right Docker Container Variety

In my case the author of FreshRSS recommended the [linux server ](https://hub.docker.com/r/linuxserver/freshrss) variant from [Linuxserver.io](https://hub.docker.com/r/linuxserver/freshrss) for my ARMv8 64-bit System on a Chip, as the server version covered a variety of systems as opposed to the base FreshRSS variant. So, before we go any further, lets make sure to verify your system's configuration.

There are a couple of terminal commands you can use to sort this out. One to give you info on your OS/distro is:

```
lsb_release -a
```

Two others to give you more info on kernel type and support for 64-bit binaries are:

```
uname -m
```

and

```
cat /proc/version
```

Using the info gathered from those, you can head over to FreshRSS's [docker section](https://hub.docker.com/r/freshrss/freshrss/tags), and select the tag appropriate for your system.

## Automated Quick Run Install

Remember that automated quick install? Well the easy-to-follow instructions are [found at GitHub](https://github.com/FreshRSS/FreshRSS/tree/edge/Docker#quick-run). To reproduce them here, that sequence is:

```
docker run -d --restart unless-stopped --log-opt max-size=10m \
  -p 8080:80 \
  -e TZ=Europe/Paris \
  -e 'CRON_MIN=1,31' \
  -v freshrss_data:/var/www/FreshRSS/data \
  -v freshrss_extensions:/var/www/FreshRSS/extensions \
  --name freshrss \
  freshrss/freshrss
```

Regarding these parameters, I made some changes. I selected America/Los_Angeles since I live on the West Coast. I wanted updates more often than the default, so I adjusted the cron entry to 'CRON_MIN=4,34'. For those unfamiliar with cron expressions, there are cron translators that take plain English and translate into cron, [like this site](https://crontab.guru/). I adjusted the last line as well to reflect the docker container pull tag I had downloaded.

Once you run that command and its associated parameters, the container with FreshRSS should be up and running. Easy.

Just head over to your hostname (an alternative would be to try http://127.0.0.1:8080) and you should see a web user interface beginning with an automated installation screen. It is straightforward, I promise.

From the web interface, you'll see an automated installation service begin. For step one, you choose your language. During step two FreshRSS runs checks on your config.

Assuming the check is all green, you head to step three where you choose your database configuration. One tricky part for entry-level folks: even though I have a MariaDB instance through my LAMP stack, I decided to allow FreshRSS to use SQLite for the database. This may indeed have caused some conflicts that haven't cropped up yet, but my (potentially short-sighted) analysis was that FreshRSS would operate better using its preferred, built-in equivalent; that SQLite was pretty low-resource intensive; and that there was enough similarity between SQLite and MariaDB that I'd avoid some conflicts.

For step four, create an identity and password. Then step five, you're done!

## Configuring the API for Clients

If you want to consume your FreshRSS feeds on clients, you'll have to enable the API interface within FreshRSS. This is a matter of turning the API on, and setting up a password for the API.

Head over to your web interface and sign in. Under the cog in the upper right corner go to authentication and check the box next to "Allow API access (required for mobile apps)" and hit submit.

Then head to the profile option under the cog in the upper right corner and head to the new section "API Management." There will be a space there for you to add a password, so enter a complex, strong password and hit submit.

These should enable you to use a reader client on a mobile device. That configuration will vary from device to device, but one general point is to keep a lookout in the initial client setup for a FreshRSS option to integrate the client with FreshRSS's API, or alternatively, to use Fever integration. FreshRSS tends to favor Fever when there is no native FreshRSS option. [Look at this page](https://github.com/FreshRSS/FreshRSS#apis--native-apps) for client reader options and enabled services.

## Updating

First, you want to back up your feeds. Head to subscription management in the FreshRSS interface and then the import/export option in the menu on the left-hand side. There will be options to export at the bottom.

For the backup process you'll want to use the instructions on the [GitHub web page](https://github.com/FreshRSS/FreshRSS/tree/edge/Docker#how-to-update)e for upgrading. To summarize, you'll pull the new docker image corresponding to your instance, stop and rename the out-of-date image, and run the new image.

These were the update commands at the time of this writing. Replace freshrss/freshrss with your tags. For the fourth command down you'll use the same parameters as you did for the automated quick run install above.

```
docker pull freshrss/freshrss
```

```
docker stop freshrss
```

```
docker rename freshrss freshrss_old
```

```
docker run ... --name freshrss freshrss/freshrss
```

```
docker rm freshrss_old
```

## Conclusion

There you go! You should be up and running with FreshRSS. Enjoy the simplified RSS management and privacy of a self-hosted service.
