---
title: I'm an Irked Docker Maintainer and Homeprodder
date: 2025-03-26
tags:
  - graylog
  - docker
  - logs
---
Pointing folks to tools for more insight into Docker containers.  
## Overview in Brief
- {% linkprimary "Context", "https://christopherbauer.org/blog/docker-trouble/#context-homelab-and-homeprod" %}
- {% linkprimary "GELF", "https://christopherbauer.org/blog/docker-trouble/#gelf-for-graylog-servers" %}
- {% linkprimary "Oxker", "https://christopherbauer.org/blog/docker-trouble/#oxker-for-on-demand-log-viewing" %}
- {% linkprimary "Lazyjournal", "https://christopherbauer.org/blog/docker-trouble/#oxker-for-on-demand-log-viewing" %}

## Context: Homelab and Homeprod
I've reached a milestone in the maturity of my homelab where a certain number of services are so integral to my family's routines as to be indispensable.  Perhaps this reflects maturation from "lab" to "production" that many enthusiasts before me have gone through, but the amount of administrative attention required has had me reconsidering the design of those services in the *prod* category.  

Concomitantly, my patience for inscrutable containers or processes that are difficult to manage by hand (looking at you API-only distros like Talos), is very low these days.  Point in case: I recently spun up a K8s cluster and I couldn't help but admire how cool it is to abstract away the process of making a container multi-node by way of API-orchestration-land.  My awe quickly melted away in the face of complexity and was accompanied by a sense that this technical marvel is not immune {% linkprimary "to the same sorts vulnerabilities", "https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities" %} as any other. Given K8s' complexity, it was probably inevitable that I'd come back around to Docker compose files as the primary source of my bedrock services.

That said, Docker containers aren't great.  They're nice in terms of installing and configuring  services (depending on the documentation), but they are a pain to troubleshoot.  So going deep on Docker has been rocky, and I wanted to share a few insights for looking at logs and general Docker tinkering.


## Quick and Dirty Troubleshooting of Docker Containers
Of course you can always `docker exec -it <SOME_CONTAINER_NAME> sh` or `docker logs <SOME_CONTAINER_NAME>` if you need to troubleshoot a service.  

I don't find these methods terribly adroit in headless ecosystems.  Moreover, looking at raw log entries in single space on the CLI is, for me, a fast road to missing critical information.  I do that enough when hacking, I don't want more of it at home.  I'd like to have some colorized, formatted output please.


## GELF for Graylog Servers
In "today-I-learned" news, Docker has native support for the {% linkprimary "Graylog Extended Formate (GELF)", "https://docs.docker.com/engine/logging/drivers/gelf/" %} logging format.  If you run Graylog, you can easily ingest Docker logs with the simple addition of a few lines to docker-compose files.  Since compose files are in that ever readable *yaml* format, this amounts to little more than adding the following block, say after the "restart: always" line.  Yaml is sensitive to spacing, so make sure the "logging" text lines up with the previous entry's indentation.
```yaml
logging:
  driver: "gelf"
  options:
    gelf-address: "udp://<YOUR_LOGGING_SERVER_IP:PORT>"
    tag: "<SOME_TAG>"
```


## Oxker for On-Demand Log Viewing
As an alternative, I ran across {% linkprimary "Oxker", "https://github.com/mrjackwills/oxker" %}, a "simple TUI to view and control docker containers."  Oxker is run itself as a docker container.  If you are at all familiar with {% linkprimary "LazyGit", "https://github.com/jesseduffield/lazygit" %} then Oxker's TUI interface will be intuitive.  Oxker shares a lot in common with the more widely known tool, {% linkprimary "LazyDocker", "https://github.com/jesseduffield/lazydocker" %} but in my tests LazyDocker was both ineffective in exposing logs on my machine and offered superfluous information (to me) regarding volumes and images.  Perhaps the former issue was an omitted parameter on my part, but since a log-first tool was what I was after as a matter of priority, I wasn't prepared to tinker and moved on quickly to Oxker.  It's a straightforward tool offering logs and some controls over containers.  The logs themselves are still single space and not colorized, but it is nice to see the layout orchestrated with cpu and memory stats this way.

{% imagesmall '/img/2025-03-26_12-30.png', '' %}

I favor running Oxker on the docker command line rather than as a compose file as I tend to use it ad-hoc rather than as a perpetual service and I don't store any data or configurations long-term.  The last parameter is if you'd like to have the log entries appear with the local timestamp instead of GMT.
```cli
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock:ro --pull=always mrjackwills/oxker --timezone <YOUR_TIMEZONE>
```


## Lazyjournal for On-Demand Log Viewing
{% imagesmall '/img/2025-03-26_13-54.png', '' %}
I saved the one with the most potential to fill my toolkit for last. {% linkprimary "Lazyjournal", "https://github.com/Lifailon/lazyjournal" %} is well-known but new to me. Like Oxker it offers a Lazygit-style readout. This is a viewing TUI-based tool, it doesn't manipulate containers or give you system stats like Oxker above. While it is primarily pointed at journalctl entries, it also works with containers. The maintainers favor a download method of using a go binary with links to your path for linux instances. I find Lazyjournal's interface a bit busy, especially when I'm only after containers and have to shift through journalctl entries and syslog stuff.  However, I really like the formatted and colorized logs it offers and the filter is fast and a nice alternative to grepping through journalctl entries.


## Conclusion
As I mentioned, I've been leaning towards Lazyjournal these past few days.  Hope this quick survey of tools to reveal Docker logs has been useful.  Should you want to connect, feel free reach out on {% linkprimary "Mastodon", "https://infosec.exchange/@anthro_packets" %}. 