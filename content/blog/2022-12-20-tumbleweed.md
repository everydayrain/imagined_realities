---
author: Chris
title: An Anthropologist's Encounter with Tumbleweed
date: 2022-12-20
---
OpenSUSE Tumbleweed is technically a great system.  I'd even go so far as to say it gives gateway-drug distros, like Linux Mint or Ubuntu, a run for their money in terms of ease and desktop-friendly polish.  The Snapper integration to support the rolling release model is just damned elegant.  I'm using it on a secondary machine at this moment.

As an anthropologist turned InfoSec practitioner, I'd argue that the technical merits aren't all that matters.  There have been hundreds of technical reviews for Tumbleweed in any event.  Socio-cultural factors, as much as technical design, are an important consideration.  While I can't speak to the technical reasoning for why the OpenSUSE Project devs made some of the design decisions they have with Tumbleweed, I can say that from a subjective standpoint I notice minor, but ideologically-leaning, design choices.  What do these design choices add up to as a subjective experience of Tumbleweed?  My working hypothesis is that Tumbleweed is a curious example of a community project producing a centralized product.

## Select High-Level Merits
Tumbleweed caught my eye as a rolling release distro.  In particular I wanted some privacy updates to Firefox that hadn't made it to Debian stable's release cycle.  As a noob to InfoSec I can't judge how well OpenSUSE did with the releases, but I noticed that security updates came out for Firefox a day or so after Mozilla's press releases (for me anyway).

Another reason I was drawn to Tumlbeweed was the snapshot integration.  I wanted to learn more about how snapshots work and Tumbleweed definitely gave me a look at this as the technology is deeply integrated into its package management design through the use of Snapper.  From the moment you install the system, this Snapper integration is at work, creating a baseline snapshot.  Through each update, Snapper also automatically creates pre- and post- snapshots to facilitate rollback in case of bugs.  If an update breaks your system, you simply choose an alternate snapshot at startup (such as the one taken immediately prior to the update), boot it, and then direct Snapper to make the read-only snapshot you booted into permanent for the system.

To my surprise, I did encounter a one bug with significant consequences that required a rollback.  I had heard tell that Tumbleweed didn't usually break.  One of the recent updates to sudo created this bug.  When I ran Zypper, and subsequently went to use sudo, the command prompt reported that my user was no longer in the sudoers group.  To remediate it was pretty simple to simply reboot the system and choose the pre-update snapshot.  In the subreddit   [r/opensuse](https://www.reddit.com/r/openSUSE/comments/ym52a4/user_not_in_sudoers_after_update/) some comments suggested that such bugs were rare.  Possibly that is true for Tumbleweed, though I didn't use it long enough to say for sure.    

Don't let the brevity of this section fool you, the snapshot features were very impressive indeed.

## Select Drawbacks
In terms of drawbacks, there was a new package management system to learn, though this would be true for anyone switching package management schemes.  Zypper has slightly different commands from apt, and Zypper has subtle differences between Leap and Tumbleweed that require attention on the command line.  That said, as long as the app you are after is pretty common, Zypper was a breeze and the apps were indeed pretty up to date. 

Some design choices stood out to me.  Tumbleweed differs from Debian a bit in shuffling around a few typical GNU/Linux directories and logs.  A single example kind of speaks to this: there is no syslog file.  This kind of threw me as a practice outside my workflow. I would typically enter in something on the command line like this when trying to troubleshoot: 
```
tail -n25 /var/log/syslog
```
That kind of command isn't a possibility in OpenSUSE out of the box.  That is a minor thing but it also obviates the ability to data wrangle on the syslog file with grep and so on.  Similarly there is no faillog command.  But you do still have journalctl, so it is possible to data wrangle on journalctl.  Sure these little design choice nuisances are to be expected.  They are the kind of UX quirks that come with migrating to a new OS.  They are little more than an annoyance.  But it also gives you a taste of Tumbleweed's personality.  

Now consider these decisions alongside the whole supporting ecosystem of YaST apps. These tools are very polished and a breeze to use.  I had to partition a drive through one of the YaST apps.  Since I was still a bit gun shy on using some of the command line tools after an unrelated mistake, I was hoping for a solid desktop option. The YaST partitioner implementation couldn't have made things easier compared to my experience with some KDE desktop tools.  The YaST NFS Client was equally user friendly in setting up shared storage.

But what gains are made in terms of ease and polish of the YaST ecosystem come at the sacrifices of creating distro that is highly standardized around YaST tools. I wouldn't call this bloat really.  Bloat implies unwanted apps that take up material or psychological resources.  The ecosystem of YaST apps don't fit that description; they are unseen when unused, and too polished to complain about when you do use them.  But they are a bit too structured, if not centralized.  You are indeed pushed toward the YaST ecosystem.

Lastly, I found KDE Plasma a bit of a pain to use on OpenSUSE.  Whereas in other distros the task manager config was relatively straightforward, the task bar and icons were all wonky in OpenSUSE.  Not sure what accounts for these problems, and this may not be anything to do with OpenSUSE.

## Conclusion
If I were to make a recommendation on Tumbleweed based strictly on technical merits, I would endorse it to anyone who asked.  I have reservations however when I consider Tumbleweed in the context of the historical development of GNU/Linux and hacking more broadly.  To explain, indulge me on a digression.

In 2017 the anthropologist Gabriella Coleman explored the social and political salience of hackers, sketching out three elements of the hacker subjectivity. First she noted their craftiness.  Second, she noted their distinct anti-authoritarian instincts. Third, she described their purposeful creation of community through the “sustenance of fellowship around labor in free spaces” (Coleman 2017, S95).

When I think about Tumbleweed, I think about its YaST ecosystem and its tightened-up file structure in the context of Coleman's quotation.  There is no doubt that OpenSUSE Tumbleweed emerges from a community of devs sponsored by a number of private companies.  One need only head over to the [OpenSUSE forums](https://lists.opensuse.org/archives/) to see Gabriella's labor and fellowship in action.  But, subjectively speaking, the distro can feel a bit retail, in that YaST can be both helpful and suffocating. Tumbleweed can lull one into a state of complacency to not expand beyond YaST because its ecosystem so excellently takes care of most needs. Tumbleweed sometimes feels distant from the more idiosyncratic needs of a hacker that might lie outside of a unified solution of desktop apps in the YaST system and in a traditional view of the directory structure.  I can't help but feel that I feel that migrating from, for example, the CUPS printer management app to the YaST printer manager would be a step backwards in developing fellowship around labor in free spaces even while it offers an elegant user experience.  That kind of unified solution in the YaST ecosystem seems to channel labor to a distinct segment of the Linux ecosystem.  This is a subtle difference from other distros.  Is that an argument for making Tumbleweed shaggier?  Certainly not.

I also learned an entirely separate lesson by dipping  my toe into OpenSUSE Tumbleweed.  That lesson is this: if you find yourself comfortable and complacent in your distribution, yearning for a rolling release and all of its upgrades, recognize that feeling for what it is, the impulsive drive of inexperience. Ignore the enchanting call of current software. But this is not news to many. Heck Debian even has dedicated an [official wikipage ](https://wiki.debian.org/DontBreakDebian) to that very message.

I'm joking a bit.  My experience as a noob with OpenSUSE was very good, and my reasons for trying it and switching away have nothing to do with its technical implementation.  In fact, it is an excellent design, from the desktop apps to its Snapper integration. In may ways it is a breeze to use.  I moved away from because for social/ideological reasons.  That's okay, the world is big enough for distros of different stripes. 

# Installation Miscellany
## Downloading the .iso
I use sha256sum to check hashes.  The file names will depend on the snapshot you download, so I'll give them with asterisks here for ease.  Download the .iso file of the snapshot and the corresponding sha256 (easily found on the dropdown menu next to downloads).  Its nice that folks still offer .sha files.
```
sha256sum openSUSE-*.iso
sha256sum -c openSUSE-*.iso.sha256
```

The first command records the hash for the .iso file, and the second with the check flag runs the .sha256 has against the one it stored and will verify "okay" if they match.

## Creating the Bootable USB
For those keeping track, I'm using the instructions on setting up a bootable USB stick from the [openSUSE.org](https://en.opensuse.org/SDB:Live_USB_stick#Using_commandline_tools), but with expanded commentary because they've done some elegant little moves here that go above and beyond the usual instructions on how to create bootable USBs.

The command line instructions for creating a bootable usb are pretty interesting.  To find out what the exact path of your usb stick might be, instructions for Linux typically suggest running the lsblk command.  The folks over at OpenSUSE take this a step further in convenience, by  piping the output of a special lsblk command to a temporary file when the USB stick is unplugged/unmounted, and repeat for a second file when it is plugged in to the host.  They then run a diff command with a flag that compares the two to isolate what path your USB stick is on.  Without the USB:
```
lsblk --fs > /tmp/withoutusb.txt

```
After plugging in the USB:
```
lsblk --fs > /tmp/withusb.txt
diff --ignore-space-change /tmp/withoutusb.txt /tmp/withusb.txt
```
That last diff command should reveal the label assigned to the usb, identifying how to populate the output file field of the dd command that follows in the documentation.  I appreciate this attention to detail.

Users following with me can simply go to the link above to find out the rest.  I just thought that was another point in the favor of OpenSUSE's elegance worth noting.

## Brief Notes on Installation Using the GUI 
Plug in the usb and hit the key to enter your UEFI.  You'll have to use the pre-assigned key on your keyboard that opens up the UEFI options or otherwise allows you to select what order items boot from in order to choose the USB.  On my Dell that was F11.  The first steps of the installer where pretty straightforward.

### Disk Encryption
In the default installation there is no disk encryption added through the installer GUI.  So on the menu heading labeled "Disk" or the page called "Suggested Partitioning" its necessary to click the "Guided Setup" button.  That will take you to options to run through an encryption setup by selecting boxes to "Enable Disk Encryption" and add a  password.  You also have the option to enable Logical Volume Management.  That seems like a good idea if you distro hop.  Also, [according to this site](https://joros.blog/posts/opensuse-full-disk-encryption/) the benefit of LVM is that "all partitions (or rather logical volumes) can be put into one encrypted container."  

On the next page of File System Options I kept the default selections, especially because Snapper relies upon BTRFS for creating snapshots.  I did however create a home volume as BTRFS as well because I wanted to experiment with snapshots there.

### Media Codecs Config
Don't forget to install the codecs allowing you to run media.  They are not installed on Tumbleweed by default. These are necessary for basic media playback for viewing streaming media such as Netflix.  You can find the instructions on how to setup a repository and prioritize it for those codecs on [this page](https://en.opensuse.org/SDB:Installing_codecs_from_Packman_repositories)
