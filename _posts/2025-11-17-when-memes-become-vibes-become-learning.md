---
layout: post
title: When Memes become Vibes become Learning
tags:
 - Vibe Coding
 - Artificial Intelligence
 - Code Review
 - Security
 - Teaching
 - Mentorship
image:
  path: /assets/img/posts/when-memes-become-vibes-become-learning/vibe-cover.png
  alt: A non-programmer's sketch of an iOS widget, and the result she eventually coded.
redirect_from:
 - /posts/when-memes-become-vibes-become-learning/
---

The last few months have been full of boom and bust stories about "vibe coding" -- the phenomenon where an individual can produce a working app by asking an AI tool to generate and edit code. Hypesters claim that professional programmers will soon be fully replaced by AI agents writing code, while experienced engineers quickly point out the risks and vulnerabilities that are rampant in the current crop of vibe-coded apps.

Here, I would like to cut through all the hype and anti-hype by sharing a real-life story about a vibe coding project that went well. This story showcases the benefits of vibe coding, especially for non-developers, while crediting the sophisticated professional engineering that enabled the project's success.

## A non-developer's first iOS widget

[![
    friend: can you build me an app that ...
    me: yes
    friend: ... has a calendar feature to ...
    me: no
](/assets/img/posts/when-memes-become-vibes-become-learning/can-you-build-me-an-app-calendar.webp)](https://www.reddit.com/r/ProgrammerHumor/comments/zglb1l/yeah_sure_i_can_do_that_while_having_totally_no/)

One of my good friends -- let's call her Amanda -- recently asked me the following question:

> What language(s) do you use to develop mobile apps?
> 
> I am looking for a super duper simple ongoing schedule app [for iOS] and I'm not finding anything that fits what I need. I'm curious if I could vibe code it and just get what I want that way...hmph. Not sure if I can make a widget based on a web app.

She even included a handwritten document with notes/mockups of exactly how she wanted the app/widget to look and behave.

![](/assets/img/posts/when-memes-become-vibes-become-learning/design.jpg)

Unfortunately, Amanda doesn't know how to code. She's smart, technically savvy, and hardworking, but she has zero software development experience. As a result, five years ago her app idea wouldn't have made it beyond the paper where she wrote it down.

But, times have changed -- building a functional app is easier than ever thanks to new platforms/frameworks and AI tools that can generate/explain code. In Amanda's case, she discovered an iOS app called [Scriptable](https://scriptable.app) and its corresponding [subreddit](https://www.reddit.com/r/Scriptable/) where people share the scripts they've written to automate their iPhone with JavaScript.

Between finding subreddit posts similar to her ideas and asking Perplexity AI to write the code, Amanda started making rapid progress on her widget. Multiple times a day I would receive a new text with an updated screenshot showing a new feature/design improvement she had completed. With each new version, her excitement and enthusiasm for the project increased. Eventually, the widget satisfied her core needs -- even if it didn't look as pretty as her initial drawings. 

![](/assets/img/posts/when-memes-become-vibes-become-learning/widgets.png)


A few days later, we sat down to review the code together. 

As expected, the AI-generated code had many organizational flaws, which actually provided the perfect examples to demonstrate the value of multiple software engineering principles. We moved code around to put similar operations closer together to improve cohesiveness. We extracted functions to add modularity. We added parameters to function signatures to provide more flexibility when composing UI layouts. After each small step, we tested the change on the phone then committed the updates to practice incremental improvement, version control, and reading diffs. That short, ~1.5 hour session was easily the most productive teaching time I've spent with someone learning how to code.

Notably, there were some sections of AI-generated code that we didn't touch. One example was the rendering of the "progress wheel" showing what percent of the current time block had elapsed. Instead of trying to render a custom wheel that would precisely fill in the exact percentage, Amanda had the clever idea to make a dozen images of progressively filled wheels then asked Perplexity to write a function to choose the image closest to the elapsed duration of the current time block. The code was clear, obvious, and well scoped in response to her prompt.

## Takeaways

**AI-assisted coding is here, and it is making software development more accessible than ever to first-time developers.**

I think this is amazing! There are tons of people like Amanda who have ideas for improving their interactions with the technology that surrounds us. There is tremendous value in empowering them to turn those ideas into reality.

Also, not everyone who wants to write code wants to become a developer. For Amanda, learning just enough coding to build and maintain her iOS widget helps her spend more time on other pursuits she considers more interesting and worthwhile. It's perfectly okay for a first-time developer to end up being a one-time developer after satisfying his/her personal need.

**Frameworks and sandboxes are more valuable than ever, and they still need skilled developers to build/maintain them.**

AI-code generators may be able to produce code more readily then ever, but without the appropriate runtime environment, that code is just a text file with a weird extension.

A big part of what makes Scriptable such an effective runtime is its ease of use. With the single, familiar action of downloading an app, one has access to a sandbox with a solid API where it's safe to experiment, make mistakes, and see real results. Without Scriptable, Amanda's iOS widget wouldn't have happened. The alternative -- downloading Xcode + all the iOS SDKs, working through Apple's barriers to install your custom app on your own phone, etc. -- exposes far too much complexity for a novice who only has the appetite to experiment with coding for a few hours.

Building a secure framework and runtime that are accessible to non-developers requires significant expertise. For Scriptable, that requires understanding the iOS toolchains and SDKs, binding a JavaScript execution environment to Swift/Objective-C APIs, writing documentation, and an ongoing effort to maintain backwards compatibility while the mobile platform continually moves out from under the maintainer's feet. That expertise requires much more than can be provided by the current state of AI powered code generators.

**It's an exciting time to be involved in software development!**
