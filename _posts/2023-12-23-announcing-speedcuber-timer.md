---
layout: post
title: "Announcing Speedcuber Timer: A mobile app for smart Rubik's Cubes"
category:
 - Projects
 - Speedcuber Timer
tags:
 - Open Source
 - Rubik's Cube
 - Speedcuber Timer
 - React Native
 - Android
 - iOS
 - Mobile App
image:
  path: /assets/img/posts/announcing_speedcuber_timer/speedcuber_timer_banner.png
  lqip: /assets/img/posts/announcing_speedcuber_timer/speedcuber_timer_banner_lqip.jpg
  alt: Speedcuber Timer helps you solve the Rubik's Cube faster
---

Finally, a native Android/iOS Rubik's Cube solving timer/trainer with broad smartcube support!

The app is free to download and use. Try it out today!
 - Apple App Store: [https://apps.apple.com/us/app/the-speedcuber-timer/id6468855171](https://apps.apple.com/us/app/the-speedcuber-timer/id6468855171)
 - Google Play: [https://play.google.com/store/apps/details?id=org.speedcuber.timer](https://play.google.com/store/apps/details?id=org.speedcuber.timer)

Speedcuber Timer has all the standard features of a typical cubing app:
 - Time your solves for any WCA Event, and tons of unofficial events too
 - Scramble generation for all NxNxN cubes
 - Averages of 3, 5, 12, 50, 100, 1000
 - Charts of your averages over time.

When you connect a smartcube to the app you automatically get tons of additional features:
 - Automatic CFOP reconstructions (ZZ and Roux are supported, but not yet shown in the UI).
 - TPS over time graphs
 - Statistics per solution phase
 
Speedcuber Timer also has several features that I don't think exist anywhere else:
 - Solve multiple puzzles in a single solution attempt (e.g. Multi-BLD or Relays)
 - Connect multiple smartcubes at once (e.g. for Multi-BLD or Relays)
 - Completely offline. After a few assets are downloaded on the first boot, the app never needs internet access.
    - Every other smartcube app requires an active internet connection in order to access the full feature set.

Speedcuber Timer already supports multiple brands of smartcubes:
 - Giiker 2x2x2
 - Giiker 3x3x3
 - GoCube Edge
 - GoCube 2x2x2
 - Rubik's Connected
 - HeyKube
 - [(More puzzles planned)](https://github.com/SpeedcuberOSS/speedcuber-timer/issues)

The [source code](https://github.com/SpeedcuberOSS/speedcuber-timer) is already publicly available on GitHub. There are lots of options for the community to contribute, even if someone has never written code before:
 - Adding translations to new languages.
 - Suggest new unofficial events to support.
 - Design new event/infraction icons.
 - Recommend new features/report bugs.
