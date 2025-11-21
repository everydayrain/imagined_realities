---
author: Chris
title: "Installing Game of Active Directory on Proxmox: Part 2 - Provisioner"
date: 2024-11-11
---
This entry consists of Part 2 of my series on [Orange Cyberdefense's](https://github.com/Orange-Cyberdefense/GOAD/tree/main) Game of Active Directory (GOAD) on Proxmox VE.  In my [previous post](https://christopherbauer.xyz/blog/2024-11-08-GOAD-networking), I covered networking for the entire Active Directory setup.  In this post we'll create a Linux provisioner machine on the LAN that will later be responsible for creating, deploying and configuring the Active Directory DCs and servers.

As I mentioned before, I'm deeply indebted to [Mayfly277's canonical guide](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com), and this post follows Mayfly277's work closely to provide readers with a resource to be used as a standalone or as a supplement to Mayfly277's work.

Should you need more orientation to the context of this series, or on my rationale for creating it, see my [previous post](https://christopherbauer.xyz/blog/2024-11-08-GOAD-networking).

## Create the Provisioner Container

### Proxmox Setup
As [Mayfly277](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/#create-provisioning-ct) lays out, we're first going to create the container that will serve as the provisioner.  You'll first need an up to date Ubuntu template on your Proxmox host, that I won't cover here.  

Before we get started, we'll need to create a public SSH key for use with the provisioner.  To create a key pair, enter the following on your local machine:
```
ssh-keygen -t ed25519 -a 32 -f ~/.ssh/<SOME_KEY_NAME>
```

Once the key is created, you can set up your provisioner container in the Proxmox Web User Interface (WUI).  In the upper left corner of the WUI, you should see a "Create CT" button.  Once you've clicked that you enter the first tab in a sequence called "General."  Fill out the information as you wish, and click the "Load SSH Key File" to select the key that you just made.  You'll want to enter the one with the extension of ***.pub***.  

Then proceed through the other tabs.  I gave my provisioner 4 GB of memory, 2 cores, and 40 GB of storage.  Most of the other options were the same as Mayfly277's, except that when I reached the networking tab, I selected the LAN or "vmbr2."

### Provisioner Networking
As in the [previous post](https://christopherbauer.xyz/blog/2024-11-08-GOAD-networking), I don't have a screen shot of creating the WAN firewall rule for the provisioner to allow an SSH tunnel, however you can gleam the settings from the following screenshot of the final state of my WAN firewall.

{% imagesmall '/img/2024-10-28_08-38.png', '' %}

Apply changes after you've added the firewall rule.

Now add the provisioning container to your ssh config file.  If you haven't set up a security key for your Proxmox machine now is the time.  Creating the key is the same process as above, and once done you'll transfer the public key to Proxmox with `ssh-copy-id` followed by `<SOME_USER@SOME_IP>`  That key will be necessary to use Proxmox as a jump box in the next steps (alternatively, you can use Proxmox's WUI to access the command line and enter the next steps manually).  Mayfly277 suggests the following for a config file placed in `~/.ssh`:
```
Host goadproxmox
   User root
   Hostname x.x.x.x
   Port 22
   IdentityFile ~/.ssh/id_rsa_kimsufi_goad
   # pfsense
   LocalForward 8082 192.168.2.2:80

Host goadprovisioning
   User root
   Hostname 192.168.2.3
   Port 22
   IdentityFile ~/.ssh/id_rsa_kimsufi_goad
   Proxyjump goadproxmox
```

Then you should be able to SSH into the provisioner using `ssh goadprovisioning`.

## Configuring the Provisioner 
Now we can start the Provisioner to begin configuring Packer, Terriform and Ansible.  Should you need more detail, [Mayfly277](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/#install-packer) offers links to the original install instructions for each vendor.

### Packer Install
As usual, it's good practice to update and upgrade once you've got it up and running for the first time.
```
apt update && apt upgrade
```

Mayfly277 also recommends installing a handful of useful apps, though you might not need vim if you prefer a different text editor, nor tmux if you don't use tmux shells all that much.  Do make sure you have the others entries though.
```
apt install git vim tmux curl gnupg software-properties-common mkisofs
```

Now we'll install the GPG signing key and add the repository for packer.
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
```

```
apt-add-repositorysitory "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
```

That should create an output that looks like the following:
{% imagesmall '/img/2024-10-28_08-59.png', '' %}

Now you can install:
```
apt update && apt install packer
```

Now you can enter `packer -v` and get a valid response.
{% imagesmall '/img/2024-10-28_08-58.png', '' %}

### Terraform Install
Following Mayfly277's instructions, I had no problems with this section.  Enter the following commands to install the GPG keys, verify them, add the Terraform repository, and then install Terraform.
```
wget -O- https://apt.releases.hashicorp.com/gpg | \ 
```

```
gpg --dearmor | \ 
```

```
tee /usr/share/keyrings/hashicorp-archive-keyring.gpg  
```

```
gpg --no-default-keyring \ 
```

```
--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \ 
```

```
--fingerprint  
```

```
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \ 
```

```
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \ 
```

```
tee /etc/apt/sources.list.d/hashicorp.list  
```

```
apt update && apt install terraform
```

Now you can enter `terraform -v` and get a valid response.
{% imagesmall '/img/2024-10-28_09-01.png', '' %}

### Ansible Install
As per [this documentation](https://orange-cyberdefense.github.io/GOAD/installation/linux/#__tabbed_1_5) we have to install an older version of Python, Python 3.10, before we can proceed with this section.  Additionally, Debian derivatives have disabled the ability to use pip in exchange for apt based python package management.  This may or may not affect readers depending on the distro you are using.  In any event, I was unable to use Mayfly277's guide for this section.

#### Python 3.10 Install and Venv
 Instead of using apt for the Python packages, I use virtual environments.  A drawback to this approach is that if you need to go come back to the provisioner at a later point to redo something Python-related, you'll have to first enter the virtual environment with `source .venv/GOAD/bin/activate`.  An alternative to this cumbersome process would be to use something like pipx, though that is outside the scope of this blog.  In what follows I use the virtual environments approach.

First we'll add a repositorysitory with older versions of python.
{% imagesmall '/img/2024-10-28_10-40.png', '' %}

Next, we'll Install Python 3.10.
{% imagesmall '/img/2024-10-28_10-41_1.png', '' %}

Then we'll make sure we can create virtual environments by installing the version appropriate venv package from apt as well.
{% imagesmall '/img/2024-10-28_10-41_2.png', '' %}

##### Virtual Environment-Based Package Install
Now we can begin installing by creating a virtual environment for GOAD for the packages.  Do that first by making sure you are in the root directory of the provisioner and entering:
```
python3.10 -m venv .venv/GOAD
```
{% imagesmall '/img/2024-10-28_10-42.png', '' %}

Then source the virtual environment.  This will cause your environment to be prefaced by `(goad)` to signal you're in it.
```
source .venv/GOAD/bin/activate
```
{% imagesmall '/img/2024-10-28_10-42_2.png', '' %}

Now install the packages.
```
.venv/GOAD/bin/pip install ansible-core==2.12.6
```

{% imagesmall '/img/2024-10-28_10-43.png', '' %}
```
.venv/GOAD/bin/pip install pywinrm
```

Now you can check to see if you receive valid responses telling you that Ansible installed correctly.
```
ansible-galaxy --version
```

```
ansible --version
```


##### Troubleshooting
It was at this point that I started to encounter problems related to missing ansible-galaxy components.  To troubleshoot, I decided to use Orange Cyberdefense's [checker script](https://github.com/Orange-Cyberdefense/GOAD/blob/main/docs/install_with_proxmox.md).  The checker script is also the primary script used in the next phase for provisioning, and therefore this troubleshooting step coinicded with  Mayfly277's guide to clone the GOAD GitHub repository.
```
cd /root 
```

```
git clone https://github.com/Orange-Cyberdefense/GOAD.git
```

Change directories into the GOAD repository and use the *goad.sh* script by entering the following.  You might have to change permissions on the script with `chmod 744`.
```
./goad.sh -t check -l GOAD -p proxmox
```

In my case, the check script suggested running ansible-galaxy on the requirements file contained within the repository's ansible directory in order to install dependencies.
```
ansible-galaxy install -r ansible/requirements.yml
```

{% imagesmall '/img/2024-10-28_10-58.png', '' %}

After that, I re-checked with the goad.sh script and received a green light.
{% imagesmall '/img/2024-10-28_10-58_1.png', '' %}

## Creating a Proxmox Pool
Lastly, Mayfly277 doesn't mention the need for a Proxmox pool in the guide, but subsequent steps seem to rely upon a pool.   Now is a good time to head over to the WUI and select the Datacenter entry on the left-hand menu.  Under Permissions drop-down in the center menu you should see an entry "pools."  Click the create button and give it the name "GOAD."

{% imagesmall '/img/2024-10-28_14-04_1.png', '' %}

## Provisioner Machine Creation Complete
That wraps up the creation of the provisioner machine.  Next we'll work on creating the template with packer.


## Resources
- [Mayfly277's blog](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com)
- [Ben Heater's blog](https://benheater.com/proxmox-lab-goad-environment-setup/)
- Orange-Cyberdefense's [GitHub Repo](https://github.com/Orange-Cyberdefense/GOAD)
- " " [proxmox instructions](https://github.com/Orange-Cyberdefense/GOAD/blob/main/docs/install_with_proxmox.md)
