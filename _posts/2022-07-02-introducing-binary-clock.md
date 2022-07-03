---
layout: post
title: "Introducing Binary Clock: Your Nerdy Mobile Timepiece"
category:
 - Projects
 - BinaryClock
tags:
 - react-native
 - android
 - iOS
 - mobile-app
---

Meet [**Binary Clock**](https://github.com/thehale/BinaryClock), the new nerdy
app for telling time on Android/iOS!

![Screenshot of the Binary Clock app running on both an Android and iOS
device](/assets/img/binaryclock/binary_clock_demo.gif)

## Table of Contents
 - [How does it work?](#how-does-it-work)
 - [Why did you make it?](#why-did-you-make-it)
 - [Where can I get it?](#where-can-i-get-it)
 - [Can I contribute? If so, how?](#can-i-contribute-if-so-how)
 - [Enjoy!](#enjoy)

## How does it work?
A binary clock works just like a standard digital clock, showing the current
time in hours, minutes, and seconds.

However, instead of showing decimal numbers the binary clock shows the
corresponding binary numbers as a series of bright and dim colored dots.

Let's go through an example.

Consider the time `08:47:13`. To show that time on a binary clock, we have to
convert the numbers `08`, `47`, and `13` to binary. 

| Decimal Number | Binary Number |
|----------------|---------------|
|       08       |    001000     |
|       47       |    101111     |
|       13       |    001101     |


_If you don't know how to convert decimal numbers into binary check out Khan
Academy's [3 minute video](https://youtu.be/H4BstqvgBow) explaining the
process._

With those binary numbers in hand, the only step remaining to display the binary
clock is to show each `1` as a bright dot, and each `0` as a dim dot (shown
vertically for aesthetics).

```
 0   1   0           ⚪ 🟢 ⚪
 0   0   0           ⚪ ⚪ ⚪
 1   1   1           🟢 🟢 🟢
 0   1   1    -->    ⚪ 🟢 🟢
 0   1   0           ⚪ 🟢 ⚪
 0   1   1           ⚪ 🟢 🟢

08 :47 :13
```

As you can see, the result is the vertical version of the binary clock shown in
the picture at the beginning of this article.

Alternatively, converting each decimal digit into a separate binary number will
yield the horizontal version of the clock.

| Decimal Number | Binary Number |
|----------------|---------------|
|       0        |     0000      |
|       8        |     1000      |
|       4        |     0100      |
|       7        |     0111      |
|       1        |     0001      |
|       3        |     0011      |

```
0  1   0  0   0  0           ⚪ 🟢  ⚪ ⚪  ⚪ ⚪
0  0   1  1   0  0           ⚪ ⚪  🟢 🟢  ⚪ ⚪
0  0   0  1   0  1    -->    ⚪ ⚪  ⚪ 🟢  ⚪ 🟢
0  0   0  1   1  1           ⚪ ⚪  ⚪ 🟢  🟢 🟢
                  
0  8 : 4  7 : 1  3
```

## Why did you make it?
Two reasons: nostalgia and practice.

#### Nostalgia
One of my elementary school teachers kept a binary clock on her desk, and I felt
so brilliant once I finally figured out how to read it. Recreating a binary
clock as a mobile app has given me the opportunity to relive the elementary
school excitement that accompanied my first experiences with the mathematics
that power modern computers. 

#### Practice
Binary Clock is my first venture into the world of mobile app development, and I
wanted to start with a relatively simple project before tackling my more
ambitious ideas for fun/useful mobile apps.

## Where can I get it?

Currently, Binary Clock is only available on the [Google Play
Store](https://play.google.com/store/apps/details?id=dev.jhale.binaryclock).

Binary Clock is compatible with iOS and iPad OS, but listing it on the Apple App
Store requires me, the developer, to pay a $99/year subscription.

If you really want to see Binary Clock on the App Store, consider [sponsoring my
open-source development](https://github.com/sponsors/thehale) or [sending a
monetary gift via PayPal](https://paypal.me/jhale1805).

## Can I contribute? If so, how?
The [code behind Binary Clock](https://github.com/thehale/BinaryClock) is
open-source on GitHub. That means there are lots of ways you can contribute. For
example, you can request new features, report issues, offer new code, or
donate money to support continued development.

You can find the full contribution guidelines
[here](https://github.com/thehale/BinaryClock/blob/master/CONTRIBUTING.md).


## Enjoy!
Thanks for reading to the end of this article! I hope you enjoyed learning about
binary clocks, and I look forward to hearing what you think of the app!

> Tick, tock, tick, tock, the Binary Clock is here.
>
> Just on, off, on, off, the numbers have disappeared.
>
> The moment has come to have some fun,
>
> with this one-of-a-kind timepiece!
> 
> -- Joseph Hale
