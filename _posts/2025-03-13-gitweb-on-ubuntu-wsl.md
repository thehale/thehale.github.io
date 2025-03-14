---
layout: post
title: "Today I Learned -- Git's built-in website"
description: Git ships with a built-in web interface for a code repository. Here's how to set it up!
tags:
 - Git
 - Today I Learned
image:
  path: /assets/img/posts/gitweb-on-ubuntu-wsl/gitweb-landing-page.png
  alt: A screenshot of the Git Web landing page for Joseph Hale's "Git Authorship" project.
---

Today I learned that Git ships with a built-in web interface for a code repository. Here's how to set it up!

1. Open a terminal
2. Navigate to a Git repository on your computer
3. Start the instaweb server with `git instaweb --local --httpd=webrick`
4. Open a web browser to `localhost:1234` to explore your git repository.

> On my system (Ubuntu 24.04 in WSL) I also had to `sudo apt install libcgi-session-perl` since the Git Web server uses CGI scripts on its backend.
{: .prompt-info }

And that's it!

I thought it was really neat to see how smooth the setup was. I've previously seen these types of Git repositories hosted online (e.g. the [RSS reader TTRSS](https://git.tt-rss.org/fox/tt-rss.git/)), so it was fun to learn how those work behind the scenes.