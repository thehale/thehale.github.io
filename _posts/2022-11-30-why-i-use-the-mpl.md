---
layout: post
title: "Why my open-source code uses the Mozilla Public License"
tags:
 - Open Source Licensing
 - Mozilla Public License
 - MPL-2.0
---

I believe an open-source software license should ensure that code can always be
used everywhere. The [Mozilla Public
License](https://www.mozilla.org/en-US/MPL/) does a great job of meeting that
goal.

## What is an open-source software license?
By default, you are the only person allowed to use any code you write. That's
because you [automatically own a
copyright](https://www.copyright.gov/registration/other-digital-content/) for
your source code as soon as you type it.

For anyone else to use your code, you have to give them permission in the form
of a legal document called a **license**.

Writing your own software license is complex, so multiple organizations have
written generic **open-source software licenses** which you can use to safely
grant other people permission to use your code.


## What types of open-source software licenses are there?
Most open-source software licenses allow anyone to use the code freely. The
differences arise from the additional rules each license requires people to
obey.


### Permissive Licenses
Licenses with few extra rules are called **permissive licenses**. The [MIT
license](https://choosealicense.com/licenses/mit/), [Apache
license](https://choosealicense.com/licenses/apache-2.0/), and [BSD
licenses](https://opensource.org/licenses/BSD-3-Clause) are commonly used
permissive licenses.

#### Benefits of Permissive Licenses
Permissive licenses are great because they allow code to easily be used by
anyone, for any project (open-source or not), with few limitations. For example,
my [Expressive Resume](https://github.com/thehale/expressive-resume) project is
licensed permissively so that anyone can use it to create a resume while keeping
the corresponding formatting code private.

#### Problems with Permissive Licenses
The problem with permissive licenses is that their lenient permissions make it
difficult/impossible to ensure that improvements to the code remain available to
everyone. For example, some organization could legally copy the code for
[Expressive Resume](https://github.com/thehale/expressive-resume), make a few
private improvements, then start sharing the result with a more restrictive
license (e.g. selling the improved code). As long as that organization gives me
credit for the original version, there's no legal mechanism to force them to
share their improvements.


### Copyleft Licenses
Licenses with strict conditions are called **copyleft licenses**. The GPL family
of licenses [[1]](https://choosealicense.com/licenses/lgpl-3.0/)
[[2]](https://choosealicense.com/licenses/gpl-3.0/)
[[3]](https://choosealicense.com/licenses/agpl-3.0/) are the most famous
examples of copyleft licenses.

#### Benefits of Copyleft Licenses
Copyleft licenses are great because they ensure that all usages of the code
remain available for everyone. For example, the [Linux operating
system](https://github.com/torvalds/linux) uses a copyleft license which
requires anyone who shares an improved version of Linux to also share their
source-code. Additionally, if someone copied an algorithm from the Linux code to
build a video game, all the code for the video game would have to be
open-sourced even though a video game has nothing to do with operating systems.

#### Problems with Copyleft Licenses
The problem with copyleft licenses is that their strict code-sharing
requirements often discourage people and companies from using copyleft-licensed
code. Most companies, small or large, want to keep portions of their code secret
to maintain a competitive advantage, which is usually impossible if they use any
GPL licensed code.

Sometimes other circumstances make it impossible to use copyleft-licensed code.
For example, apps published on the Apple App Store cannot legally contain any
code licensed under the copyleft GPL license because [some of Apple's Terms of
Service conflict with the
GPL](https://www.fsf.org/news/2010-05-app-store-compliance).


## What type of license is the Mozilla Public License?
The Mozilla Public License (abbreviated as the MPL) is a **middle ground**
between permissive and copyleft licenses.

Like permissive licenses, code shared under the MPL can be used in any project,
public or private.

Like copyleft licenses, the MPL ensures that improvements to the original code
are available for everyone.

Unlike permissive licenses, modifications to the licensed code must be
open-sourced.

Unlike copyleft licenses, new software which only uses the licensed code can
stay private.

For example, if you use my
[multicounter](https://github.com/thehale/multicounter) library in a Python
project you don't need to open-source anything. If you fix a bug or add a new
feature to `multicounter`, then only that bug fix/feature needs to be
open-sourced. If you copy an algorithm from `multicounter` into your code, then
only the file containing the copied algorithm needs to be open-sourced while
everything else can stay private.

As a result, the Mozilla Public License preserves most of the benefits of
permissive and copyleft licenses, while simultaneously mitigating their
problems.

## Why do you prefer the Mozilla Public License for your open-source projects?
I put a lot of time into building useful, high-quality software. I want people
to use my work to build amazing new things I never would have imagined. By using
the Mozilla Public License for my code, you and everyone else in the world can
freely use my code for any of your projects, open-source or not.

However, when I provide a strong foundation to everyone for free, I think it's
only fair to expect people to share any enhancements they make to that
foundation in the same way. By using the Mozilla Public License, I ensure that
improvements to my code are neither locked away behind a proprietary paywall nor
burdened with the extra restrictions of a strict copyleft license like the GPL.

## How do I use the Mozilla Public License for my open-source projects?
It's easy!

Create a file called `LICENSE` in the root folder of your project and copy the
[license text](https://www.mozilla.org/media/MPL/2.0/index.48a3fe23ed13.txt)
from [Mozilla's website](https://www.mozilla.org/en-US/MPL/). You don't need to
change the license text at all.

You should also add a [short
comment](https://www.mozilla.org/en-US/MPL/headers/) to the top of each source
code file indicating its MPL license. Mozilla also makes it easy to copy/paste
these comments from [their website](https://www.mozilla.org/en-US/MPL/headers/).

To make everything even easier, I like to use the following VS Code Plugins:
 - [Choose a
   License](https://marketplace.visualstudio.com/items?itemName=ultram4rine.vscode-choosealicense):
   Create the `LICENSE` file without ever leaving VS Code.
 - [licenser](https://marketplace.visualstudio.com/items?itemName=ymotongpoo.licenser):
   Automatically adds license headers to each source code file.

## Where are good places to learn more?
The best place to learn more about the Mozilla Public License is the [official
FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/).

If you want to learn more about open-source software licensing in general, I
recommend the following sites:
 - [Choose a License](https://choosealicense.com/): Helps developers understand
   which software license(s) best match their values/goals for a project.
 - [Fossa Blog](https://fossa.com/blog/): A blog with detailed explanations of
   all common open-source software licenses using everyday language.
    - Produced by a company which specializes in building automated tools to
      help companies follow the rules of software licenses.

Of course, you should always seek any legal advice from a lawyer who specializes
in copyright law.

> While I am knowledgeable about open-source software licensing, I am not
an attorney. Thus, my comments cannot be considered legal advice under any
circumstances.
{: .prompt-danger }
