---
layout: post
title: "How to remove all stopped Docker containers"
description: "A one-line shell command to clean up old, discarded containers"
tags:
 - Docker
---

_TL;DR_
```bash
docker rm $(docker ps -a | grep Exited | cut -d " " -f 1)
```

## How it works

Recently, I forgot to include `--rm` when running a bunch of throwaway containers, so my system was cluttered with loads of stopped containers with auto-generated names.

> Quickly create lots of throwaway containers:
> 
> ```bash
> for i in {1..10}; do docker run hello-world; done
> ```
> Replace `10` with the number of containers to create.
{: .prompt-info }

To remove stopped containers we need to invoke `docker rm CONTAINER`, where `CONTAINER` is repeatable and can be either a container's name or id.

The command `docker ps -a` lists all existing containers and their ids. We can select the rows for stopped containers with  `grep Exited`. Then we can extract the container id with `cut -d " " -f 1` which splits the row on spaces (the "`d`elimiter") then chooses the first column (1-indexed).

```bash
# Lists the IDs of all stopped containers
docker ps -a | grep Exited | cut -d " " -f 1
```

We can pass the output of that command to `docker rm` as a shell expansion

```bash
# Removes all stopped containers
docker rm $(docker ps -a | grep Exited | cut -d " " -f 1)
```

And just like that all your stopped Docker containers will be removed!
