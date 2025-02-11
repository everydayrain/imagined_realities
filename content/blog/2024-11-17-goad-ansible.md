---
author: Chris
title: "Installing Game of Active Directory on Proxmox: Part 5 - Ansible"
date: 2024-11-18
---

This is part 5 of my series on [Orange Cyberdefense's](https://github.com/Orange-Cyberdefense/GOAD/tree/main) Game of Active Directory (GOAD) on Proxmox VE. In the [fourth installment](https://christopherbauer.org/2024-11-17-goad-terraform) I covered how to use Terraform to create the Windows VMs. In this post we'll configure the individual Windows VMs using Ansible to create the final GOAD topology.

As I mentioned before, I'm deeply indebted to Mayfly277's [canonical guide](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com), and this post follows Mayfly277's work closely to provide readers with a resource to be used as a standalone or as a supplement.

Should you need more orientation to the context of this series, or on my rationale for creating it, see [first post](https://christopherbauer.org/2024-11-08-GOAD-networking) in this series.

## Configuring The AD VMs

### Preparation

#### Modify the Inventory

On the provisioner, there should be an _inventory_ file as part of the cloned GOAD repo. Change to that directory so that you can modify it.

```
cd ~/GOAD/ad/GOAD/providers/proxmox
```

In the inventory I changed the static IPs of the five machines to reflect the VLAN subnet they were on (this according to my [unique arrangement](https://christopherbauer.org/2024-11-08-GOAD-networking), if you followed Mayfly277's instructions this step will be unnecessary).

At this point Mayfly277 suggests [installing the requirements for ansible-galaxy](https://mayfly277.github.io/posts/GOAD-on-proxmox-part4-ansible/#install-the-requirements). In my guide, we completed that step as part of [the provisioner setup](https://christopherbauer.org/2024-11-11-provisioner), so we're now ready to run Ansible's playbook.

## Run Ansible

To configure the machines, switch to the Ansible directory on the provisioner and run the playbook.

```
cd /root/GOAD/ansible
```

```
export ANSIBLE_COMMAND="ansible-playbook -i ../ad/GOAD/data/inventory -i ../ad/GOAD/providers/proxmox/inventory"
```

If all goes according to plan, it will cover a lot of ground and say "command successfully executed."

{% imagesmall '/img/2024-10-29_19-13.png', '' %}

This wasn't the case during my installation, I ran into multiple problems. Before I dig into those, remember that if you need to come back to the project after a restart of the provisioner, you might have to source the python packages again according to the [virtual environment](https://christopherbauer.org/2024-11-11-provisioner) we set up in part 2.

### Troubleshooting the Ansible Run

I ran into errors in attempting to complete the entire Ansible run. Ultimately, I was able to complete the run successfully. I just troubleshooted the error messages and re-ran until the run completed. Adding `-vvv` might help add verbosity for revealing error messages if you need to troubleshoot, and the [issues section](https://github.com/Orange-Cyberdefense/GOAD/issues) of Orange-Cyberdefense's Github Repo was very helpful.

There is quite a lot to the Ansible playbook, so if you troubleshoot and successfully resolve, you'll have to run again and sit tight for a while as it proceeds.

#### "Failed to get SMBIOS buffer information... "

The first time I ran Ansible, I received an error similar to [this thread](https://github.com/Orange-Cyberdefense/GOAD/issues/177). I eventually got it working after a Proxmox reboot and temporarily taking out all the VLAN30 rules while adding a single allow any any rule. I was unable to determine what specifically caused the error.

#### "Add a domain user/group from another Domain..."

Next I had to troubleshoot again on the "Add a domain..." error for DC03. I eventually ran across [this fix](https://github.com/Orange-Cyberdefense/GOAD/issues/58#issuecomment-1558976147).

## Create Snapshots

Once the Ansible run is successful, we're done creating the GOAD topology and settings, so it's a good time to take snapshots so that we may easily revert the machines to a clean state after our penetration testing.

Mayfly277 offers [a bevy of bash variables and a for loop](https://mayfly277.github.io/posts/GOAD-on-proxmox-part4-ansible/#create-snapshots) to create snapshots of the newly configured machines on the Proxmox command line. This is the faster way, though you can take snapshots manually by going to each of the five machines in the web user interface (WUI) and selecting the Snapshots option in the middle menu column and the "Take Snapshot" button.

## Configuration Complete

That wraps up the deployment section. Next we'll configure a vpn tunnel allowing us to connect an attacking machine to the internal network.
to the internal network.
