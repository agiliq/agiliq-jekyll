---
layout: post
comments: true
title:  "Python and Django development on Windows with WSL"
description: "Django on Windows with WSL"
keywords: "python, django, wsl, windows"
date:   2018-07-25
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

Now that we have a linux environment, we can install any command line tool. 
I was able to install Redis, Postgres, Python, Virtualenv and more with zero issues. 

We will not go in details about installing, but they could be as simple as

    apt-get install postgresql-server

Follow any appropriate tutorial to install the CLI tools. 
Becuase we have full Linux environment (Except for the GUI), any Linux specific tutorial will work.

![WSL Ubuntu with Django](/assets/images/wsl-ubuntu-with-django.png)

Now you can run `python manage.py startproject` 
and then `python manage.py runserver` to get the default Django page.

    (django-test2) ~$ django-admin startproject hello
    (django-test2) ~$ cd hello
    (django-test2) ~/hello$ python manage.py runserver
    Performing system checks...

Port forwarding
-------------------

When you run `manage.py runserver`, which starts on port 8000, inside of WSL, 
the same servers are also available in windows on same port.

This mapping is automatic, no port forwarding is explicitly required.

So if you access `localhost:8000` in windows, this is what you see.

![WSL Ubuntu with Django](/assets/images/wsl-django-quickstart.png)

Beautiful.

Sharing code between Windows and Linux
-----------------------------------------

Our code runs in WSL, but we want to edit it from Windows. So we need to share code between WSL and Windows.

The window filesystem is available inside WSL at `/mnt/`. The `C:\` drive is mapped to `/mnt/c/`.

To simplify our work, I will create a symbolic link. 

    ln -s /mnt/c/Users/shabda/repos ~/repos

and move the Django folder to `~/repos`. I can now edit it in Windows at `C:\users\shabda\repos`.


Installing and using VSCode in Windows
---------------------------------------

Download and install VSCode the regular way. There is nothing special about VSCode, 
but it offers an easy way to switch the builtin terminal to WSL bash, so we will use it.

Go to your VSCode settings using Ctrl+Shift+P) and choosing Preferences: Open User Settings. 
Then change the JSON to include:

   "terminal.integrated.shell.windows": "C:\\WINDOWS\\System32\\wsl.exe"

Now when you start a new integrated terminal, the WSL bash will start.


Conclusion
----------------

With this setup, we can run ANY non-GUI linux applications and edit 
and work with them using GUI editors/IDEs from windows. 

I had started evaluating WSL without very high hopes, 
but was pleasantly surprised by how seamless everything was.
