---
layout: compress
permalink: '/sw.js'
# PWA service worker
---

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (event) => event.waitUntil(remove()));

async function remove() {
  const keys = await caches.keys();
  await Promise.all(keys.map((key) => caches.delete(key)));
  await self.registration.unregister();
  const tabs = await self.clients.matchAll({ type: "window" });
  tabs.forEach((tab) => tab.navigate(tab.url));
}
