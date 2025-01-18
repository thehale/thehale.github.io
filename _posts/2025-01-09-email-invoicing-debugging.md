---
layout: post
title: "Solving a Tricky Email Invoicing Bug"
description: How I traversed library code, programming language implementations, and operating system updates to solve a critical email invoicing issue.
tags:
 - Python
 - Debugging
 - Software Engineering
 - Testing
---

Solved a really involved bug today...

Some of our B2B customers were unable to email invoices to their clients, delaying incoming payments.

My coworker traced the problem to the built-in Python function `email.utils.getaddresses`, which was being used to extract email addresses from some text. In a test environment the function was returning the expected email addresses, but in production no emails were found.

Adding to the confusion, Python's `sys.version` and `sys.implementation` reported identical Python versions and builds in each environment. Additionally, scans of our code and our dependencies' code found no monkey-patches of the email parsing function. How could a built-in language function behave differently between apparently identical environments?

The first breakthrough occurred after I rebuilt the affected service's Docker image from scratch, which replicated the issue locally. I decided to identify which layer of the image introduced the issue, which I accomplished via a "binary search"-style approach -- comment out half the lines of the Dockerfile at a time until I found the surprising line which introduced the bug: `apt install python3-dev`

This discovery led to the next breakthrough when I searched the history of `python3-dev` on Debian's package repository. Apparently, a security issue within Python had been published last September, and Debian had recently backported the fix to our version of Python. While, the original security issue didn't affect our systems, its fix changed Python's default email parsing behavior, breaking our emailing tools.

From there, we were able to adjust our approach to email parsing to restore the original functionality, pass our newly written regression tests, and enable our customers to start sending invoices again.

While this was one of the hardest bugs I've solved -- traversing through library code into programming language implementations down into OS updates -- it is exciting to feel the confidence boost of knowing that I can do it again.