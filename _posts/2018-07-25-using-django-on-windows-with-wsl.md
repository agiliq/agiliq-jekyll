---
layout: post
comments: true
title:  "Python and Django development on Windows with WSL"
description: "Django on Windows with WSL"
keywords: "python, django, wsl, windows"
date:   2018-07-22
categories: [python, django, wsl]
author: Shabda
---

Most professional Django developers use Mac or Linux. I also belong to the same group. For the last 8 years, I have been using Mac for local development and Ubuntu for servers. However with Apple's recent reluctance to make developer focussed laptops, I evaluated using Windows with WSL. I was pleasantly surprised by how good the experience was. This post is a short tutorial to about setting up the complete Django development environment using windows.

Motivations for this setup
-----------------------------

Why WSL instead of dual booting or VMs?

I have dual booted machines in the past, but have found the lid-shutdown behaviour flakey and 
the battery life limited. While it might be fixed in recent Linux releases, I did not want to spend a lot of time figuring this out.
I could have used a VM, but I felt running the IDEs and editors in their native OS provides a better experience.


Installing WSL and Ubuntu on WSL
------------------------------------

Microsoft and Canonical have written a comprehensive tutorial on installing WSL and Ubuntu. We will not repeat those here. Instead, you can follow the links.

- [Install the Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
- [Install Ubuntu](https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0)

After the install is finished, you would have a real and complete linux environment.

![WSL Ubuntu](/assets/images/wsl-ubuntu.png)

As you can see, I have got `16.04 LTS`

Installing Python, Postgres, Django and other CLI tools inside WSL
------------------------------------------------------------------

Installing VSCode in Windows
---------------------------------------

Sharing code between Windows and Linux
-----------------------------------------

Port forwarding
-------------------

Conclusion
----------------