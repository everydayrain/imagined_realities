---
author: Chris
title: "Installing Game of Active Directory on Proxmox: Part 3 - Templating"
date: 2024-11-14
---
This is Part 3 of my series on [Orange Cyberdefense's](https://github.com/Orange-Cyberdefense/GOAD/tree/main) Game of Active Directory (GOAD) on Proxmox VE.  In the [second installment](https://christopherbauer.org/2024/11/11/provisioner.html) I covered creating a provisioner machine in Proxmox and installing Packer, Terraform and Ansible in preparation of creating the GOAD machines.  In this post we'll create templates  for future deployment of the individual AD DCs and servers.

As I mentioned before, I'm deeply indebted to [Mayfly277's canonical guide](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com), and this post follows Mayfly277's work closely to provide readers with a resource to be used as a standalone or as a supplement to Mayfly277's guide.

Should you need more orientation to the context of this series, or on my rationale for creating it, see the [first post in this series](https://christopherbauer.org/2024/11/08/GOAD-networking.html).

## Preparation

### Obtain the Windows ISOs
First we'll need to obtain the Windows ISOs to serve as the basis of the templates.  Mayfly277 helpfully identified [registration-free](https://mayfly277.github.io/posts/GOAD-on-proxmox-part2-packer/#download-the-isos) links to those ISOs, so I recommend going directly to his guide for those links.  You can either download them to your local machine and subsquently upload them to Proxmox, or you can download them directly to Proxmox in the web user interface (WUI).

### Obtain the Cloudbase-init
Returning to the provisioner machine, download the cloudbase-init service files to initialize and configure the Windows machines.
```
cd /root/GOAD/packer/proxmox/scripts/sysprep 
```

```
wget https://cloudbase.it/downloads/CloudbaseInitSetup_Stable_x64.msi
```

{% imagesmall '/img/2024-10-28_11-01.png', '' %}

### Create a User in Proxmox
We need to create a dedicated user for the steps that follow.  Mayfly277 suggests two options, either a user with limited privileges or a user with admin privileges.  I was ultimately forced to add admin privileges as I got the 403 error that Mayfly277 mentioned in their guide.  Ordinarily I'd advise against giving admin privileges out unless absolutely necessary, but in this case Mayfly277 himself uses admin privileges in later steps, so it may make sense to implement them here.  In any event, I'll add both privileged and non-privileged options. Admin privileges are outlined in the last command below.

To create the user and packer privileges, on the Proxmox command line enter the following commands in sequence.
```
pveum useradd infra_as_code@pve
```

```
pveum passwd infra_as_code@pve
```

```
pveum roleadd Packer -privs "VM.Config.Disk VM.Config.CPU VM.Config.Memory Datastore.AllocateTemplate Datastore.Audit Datastore.AllocateSpace Sys.Modify VM.Config.Options VM.Allocate VM.Audit VM.Console VM.Config.CDROM VM.Config.Cloudinit VM.Config.Network VM.PowerMgmt VM.Config.HWType VM.Monitor SDN.Use"
```

Then choose the sort of role you want the user to have.

To create a user with only the packer privileges of the command above, enter:
```
pveum acl modify / -user 'infra_as_code@pve' -role Packer
```

If instead you want to create a user with full admin privileges, enter:
```
pveum acl modify / -user 'infra_as_code@pve' -role Administrator
```


### Modifying config.auto.pkrvars.hcl
On the provisioner machine change to `/root/GOAD/packer/proxmox/` and copy the config.auto.pkrvars.hcl template file to a version for our use.
```
cp config.auto.pkrvars.hcl.template config.auto.pkrvars.hcl
```

I next used a little trial and error to follow Mayfly277's instructions on modifying config.auto.pkrvars.hcl.  Mayfly277 says "*The config.auto.pkrvars.hcl file will contain all the informations [sic] needed by packer to contact the proxmox api.*"  To interpret that a bit, I changed the following in the file: 

- "proxmox_url" -> I set this to the gateway of GOAD LAN `192.168.2.1:8006` so that it'd be translated by NAT to Proxmox as we completed in [part 1](https://christopherbauer.org/2024/11/08/GOAD-networking.html)
- "proxmox_username" -> change this to the user you created above
- "proxmox_password" -> change this to the user you created above
- "proxmox_node" -> changed to the name of the home Proxmox node
- "proxmox_vm_storage" -> storage for the machines you'll create

### Creating Custom ISOs for the Template
For this step we'll create an ISO file for use with the template through a custom script that is located in the GOAD repository on the provisioner machine.
```
cd /root/GOAD/packer/proxmox/
```

```
./build_proxmox_iso.sh
```
Mayfly277 [describes what's going on](https://mayfly277.github.io/posts/GOAD-on-proxmox-part2-packer/#prepare-iso-files) with the script and understands it far better than I do.  If you'd like to understand the inner workings before running it, head over [there](https://mayfly277.github.io/posts/GOAD-on-proxmox-part2-packer/#prepare-iso-files).

Once the script runs and the ISO file has been created, we'll transfer it to Proxmox with scp.  For this step, Mayfly277 remarks "*the cloudinit iso file is pretty large we will copy it from the proxmox ssh access*."  However, if you set up key-only access to the provisioner in the [previous post in this series](https://christopherbauer.org/2024/11/11/provisioner.html), you won't be able to use scp.  You can do the unthinkable and transfer the private key you use to access the provisioner container to your Proxmox host in order to do this.  But that'd be a bad habit to get into, even if only on your LAN. It may be better practice to simply set up a password for SSH on the provisioner container. 

To transfer using scp and a password, enter the Proxmox command line.
```
ssh goadproxmox
```

```
scp <SOME_PROXMOX_USER>@<SOME_PROXMOX_IP>:/root/GOAD/packer/proxmox/iso/scripts_withcloudinit.iso /var/lib/vz/template/iso/scripts_withcloudinit.iso
```

Now SSH into your Proxmox machine and download the [virtio-win.iso](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso) file that has drivers for Windows VMs hosted on Linux hypervisors.
```
cd /var/lib/vz/template/iso 
```

```
wget https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso
```

With that you should have ISOs named "scripts_withcloudinit.iso" and "virtio-win.iso" visible in your Proxmox WUI storage.
{% imagesmall '/img/2024-11-11_10-14.png', '' %}

### Modifying packer.pkr.hcl 
Mayfly277 says "*A generic packer.pkr.hcl file is present in GOAD folder* ."  That path is `/root/GOAD/packer/proxmox/packer.json.pkr.hcl`.  

I modified the packer.pkr.hcl file so that the "vlan_tag" entry read "30" according to how I set up the networking in my [first post](https://christopherbauer.org/2024/11/08/GOAD-networking.html).

### Modifying the Individual Computer Config Files
Next we'll modify the packer files for the individual templates.  Before we begin, it'd be helpful to have the sha256 hashes for a couple of dependent files referenced in the packer files.  To collect those, head to the provisioner machine.

On the provisioner, change directories, and note the hashes produced by the following commands:
```
cd /root/GOAD/packer/proxmox/iso
```

```
sha256sum Autounattend_winserver2016_cloudinit.iso
```

```
sha256sum Autounattend_winserver2019_cloudinit.iso
```

Now we'll modify the packer files, starting with the 2016 .hcl file:
```
cd /root/GOAD/packer/proxmox
```

Use your favorite text editor to open `windows_server2016_proxmox_cloudinit.pkvars.hcl` (I use vi/vim).

I left most settings in that file alone.  Do enter the hash you derived for the Autounattend_winserver2016_cloudinit.iso into the field "autounattend_checksum".  I also had an issue when running Packer in the next step where the error message mentioned no file type.  Eventually I appended the following line to make it work:
```
vm_disk_format = "qcow2"
```

Then do the same process but using the second hash for the file windows_server2019_proxmox_cloudinit.pkvars.hcl.

Here are the specs for the two files that I ended up with.  The 2016 .hcl file appears below as the first screenshot, and the 2019 .hcl file appears below as the second.
{% imagesmall '/img/2024-11-11_10-23.png', '' %}

{% imagesmall '/img/2024-11-11_10-23_1.png', '' %}

## Create the Templates
Now we're ready to launch the packer template builds for the 2016 and 2019 templates that will later be used to create the VMs.

Initialize packer, 
```
packer init .
```

Validate the file, and then build for each respectively.
```
packer validate -var-file=windows_server2019_proxmox_cloudinit.pkvars.hcl .
```

```
packer build -var-file=windows_server2019_proxmox_cloudinit.pkvars.hcl .
```

```
packer validate -var-file=windows_server2016_proxmox_cloudinit.pkvars.hcl .
```

```
packer build -var-file=windows_server2016_proxmox_cloudinit.pkvars.hcl .
```

If that all goes well, you should be able to see two template VMs in your Proxmox WUI that correspond to the 2016 and 2019 files we modified.
{% imagesmall '/img/2024-10-28_15-41.png', '' %}

## Template Creation Complete
With that we've created the templates and are ready to create machines with Terraform in the next entry of this series.

## Resources
- [Mayfly277's blog](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com)
- Orange-Cyberdefense's [GitHub Repo](https://github.com/Orange-Cyberdefense/GOAD)
- Orange-Cyberdefense's [proxmox instructions](https://github.com/Orange-Cyberdefense/GOAD/blob/main/docs/install_with_proxmox.md)
