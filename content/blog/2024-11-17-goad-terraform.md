---
author: Chris
title: "Installing Game of Active Directory on Proxmox: Part 4 - Terraform"
date: 2024-11-17
---

This is part 4 of of my series on [Orange Cyberdefense's](https://github.com/Orange-Cyberdefense/GOAD/tree/main) Game of Active Directory (GOAD) on Proxmox VE. In the [third installment](https://christopherbauer.xyz/blog/2024-11-14-templates) I covered preparing templates and creating them in packer in preparation of creating the GOAD machines. In this post we'll deploy the domain and its machines using Terraform.

As I mentioned before, I'm deeply indebted to Mayfly277's [canonical guide](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com), and this post follows Mayfly277's work closely to provide readers with a resource to be used as a standalone or as a supplement.

Should you need more orientation to the context of this series, or on my rationale for creating it, see [first post](https://christopherbauer.xyz/blog/2024-11-08-GOAD-networking) in this series.

## Preparation

### Proxmox

First, as Mayfly277 says, "we will go dirty" by giving admin privileges to the user we created in [part 3](https://christopherbauer.xyz/blog/2024-11-14-templates). On the command line of the Proxmox machine, change the infra_as_code user's privileges to admin.

```
pveum acl modify / -user 'infra_as_code@pve' -role Administrator
```

### Specifying Terraform Variables

#### Variables.tf

Next we're going to set up a Terraform file with some initial variables for the build on the provisional machine.

Log on to the provisioner.

```
ssh goadprovisioner
```

Make an active copy of the Terraform variables file.

```
cd /root/GOAD/ad/GOAD/providers/proxmox/terraform
```

```
cp variables.tf.template variables.tf
```

Next we'll modify the file to our specifications. Mayfly277 [lays out the full specifications](https://mayfly277.github.io/posts/GOAD-on-proxmox-part3-terraform/#configure-terraform) in the code, so rather than reproduce the entire file, I'll simply review what I changed. I had to modify the following in the variables.tf file.

- the vlan tag (according to my [unique arrangement](https://christopherbauer.xyz/blog/2024-11-08-GOAD-networking), yours may differ)
- node name
- gateway address
- password
- storage
- id numbers for the vms created

#### Goad.tf

Now we'll modify the goad.tf file in the same directory.

I had to modify that file under the section starting with _`variable "vm_config"`_. I changed the static IPs of the five machines to reflect the VLAN subnet they were on (according to my [unique arrangement](https://christopherbauer.xyz/blog/2024-11-08-GOAD-networking), if you followed Mayfly277's instructions this step will be unnecessary).
{% imagesmall '/img/2024-10-28_15-37.png', '' %}

## Deploy the AD VMs

Now we're ready to create the VM's using Terraform. We'll first initialize, then run a plan to create an output for the Terraform run.

```
terraform init
```

```
terraform plan -out goad.plan
```

Now we'll run the Terraform plan. Mayfly277 reports this took 25 minutes. That seems about what mine took. Also, I did have to run it more than once, but ultimately it did work.

```
terraform apply "goad.plan"
```

Now you should see five new VMs withe the names you specified in goad.tf in the Proxmox web user interface.

{% imagesmall '/img/2024-11-14_15-16.png', '' %}

Troubleshooting note: if you find that it takes an unacceptably long time to complete the Terraform build, ask yourself what storage you selected in [part 3](https://christopherbauer.xyz/blog/2024-11-14-templates) when you modified the config.auto.pkrvars.hcl file. If it wasn't local-lvm, that might have something to do with it.

## Deployment Complete

That wraps up the deployment section. Next we'll configure the AD machines using Ansible.

## Resources

- [Mayfly277's blog](https://mayfly277.github.io/posts/GOAD-on-proxmox-part1-install/?ref=benheater.com)
- Orange-Cyberdefense's [GitHub Repo](https://github.com/Orange-Cyberdefense/GOAD)
- " " [proxmox instructions](https://github.com/Orange-Cyberdefense/GOAD/blob/main/docs/install_with_proxmox.md)
