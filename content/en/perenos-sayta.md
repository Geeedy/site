# CONTENT · perenos-sayta · /uslugi/razrabotka-saitov/perenos-sayta/

> Gate 4 (15.08.2026). SERVICES page. Structure: [../../drafts/structures/perenos-sayta.md](../../drafts/structures/perenos-sayta.md). Em-dash: 0.

## Мета

- **Title:** Website Migration to New Hosting, CMS or Domain | skill-dev
- **Meta description:** We migrate a working website to new hosting, Bitrix, WordPress or Tilda with no loss of data, layout or search rankings. 301 redirects, mirror merging. Free audit.
- **OG title:** Website Migration Without Losing Data or Rankings
- **OG description:** We migrate a working website to new hosting, Bitrix, WordPress or Tilda with no loss of data, layout or search rankings. 301 redirects, mirror merging. Free audit.

---

# Website Migration to New Hosting, CMS or Domain Without Losing Data or Rankings

You already have a working website, and it needs to move to different hosting, a different CMS or a new domain. The task sounds simple, but the migration itself is where data gets lost, layouts break and search rankings drop. We migrate the site as is: the content, database and appearance stay the same, only the infrastructure changes. Before the switch we set up a staging environment, make a full backup with rollback, and place per-page 301 redirects so search traffic survives the move. This is part of our [website development](/uslugi/razrabotka-saitov/) practice: we work under contract, take accesses from a list, and monitor indexation after launch.

- Full backup of files and database before we start, with rollback for any problem.
- A staging environment on the new hosting, closed from indexation, before the switch.
- Per-page 301 redirects and meta tag transfer to preserve rankings.

[CTA-hero: Free migration audit | Ask a question]
[IMG: ../assets/images/perenos-sayta-hero.jpg | Website migration to new hosting, CMS or domain without losing data]

## What website migration is

Website migration is moving a working site to different hosting, a different CMS or a different domain while preserving content, database, layout and search rankings. Unlike a redesign or building from scratch, the site moves as is: the infrastructure changes, not the product itself. You get the same site in a new place, and visitors and search engines barely notice the move.

## When you need website migration

A move is rarely started without a reason. Most often clients come to us with one of these scenarios.

- **Hosting is slow or getting expensive.** The site loads slowly, buckles under load, and support answers in days. Changing hosting fixes this without rebuilding the site.
- **The site outgrew the website builder.** Tilda or Wix has become too tight: you need a catalog, integrations, serious SEO and flexibility that a builder does not provide.
- **Rebranding and a domain change.** The company changed its name or is merging projects, and the site moves to a new domain while keeping the weight it has built up.
- **Several versions of the site in the index.** www and non-www, http and https, old and new domain live in parallel and create duplicates. You need to merge mirrors into one main one.
- **Changing contractor.** The site is locked inside someone else's infrastructure and needs to be brought under your control, taking back accesses, files and the database.

## What exactly we migrate: files, database, domain, email, DNS

A website is not one file but five connected entities. We migrate and check each one separately, otherwise some functions break right after the switch.

| Entity | What it includes | Risk if lost |
|---|---|---|
| Files | code, templates, modules, images, CSS/JS, configs | layout and functions break |
| Database | pages, products, orders, users, URL settings | content and requests are lost |
| Domain | link to the server via DNS (the domain itself does not move) | the site goes offline |
| Email | MX records, mailboxes | emails and requests disappear |
| DNS | A/AAAA, CNAME, MX, TXT (SPF/DKIM/DMARC), TTL | site and email downtime |

A separate note on the domain. It stays with its registrar and does not go anywhere. What moves is not the domain itself, but its link to the new server through DNS records. Confusion here is expensive: misconfigured DNS takes down both the site and the email.

[INFOGRAPHIC: ../assets/infographics/perenos-sayta-1.svg | Migration flow diagram: files, database, domain, email, DNS]

## Website migration to new hosting

The most common and safest scenario is when the CMS and URL structure stay the same and the site simply moves to a fast server. The order is as follows:

1. We take a full backup of files and a database dump.
2. We deploy a copy on the new hosting on a technical subdomain, closed from indexation.
3. We check key pages, forms and the cart on the staging environment.
4. One or two days before the switch we lower the A record TTL so DNS updates quickly.
5. We switch DNS during a quiet period, set up SSL and check the site on the new server.
6. We monitor logs for 5xx and 404 errors for the first 24 hours after the move.

With proper preparation the real site downtime is from a few minutes to a couple of hours, not days. The URLs do not change, so search rankings are barely affected.

[CTA-mid: We will assess your move and its risks. Send the site address and where you are moving to → form]

## Changing CMS: migration to Bitrix, WordPress or Tilda

Changing CMS is harder than changing hosting, because the URL structure often changes together with the engine. Here copying files is not enough: content and layout are transferred by hand, and for every old address a mapping is prepared, old URL → new URL. The mapping can be one to one or many to one, but without it search traffic is lost.

Where we usually migrate to:

- **To Bitrix** when you need a catalog, 1C integration and work with a large product range. More about the platform on the [Bitrix website](/uslugi/razrabotka-saitov/sait-na-bitrikse/) page.
- **To WordPress** when flexibility, a blog and content projects with many pages matter. See [WordPress website](/uslugi/razrabotka-saitov/sait-na-wordpress/).
- **To Tilda** when you need a quick landing page and simple self-editing. See [Tilda website](/uslugi/razrabotka-saitov/sait-na-tilde/).

We will tell you honestly: if your current CMS suits you and the only problem is a slow server, there is no need to change the engine, changing hosting is enough. Moving to a new CMS is justified by tasks, not by fashion.

## How we preserve SEO rankings during migration

This is the core of the service. Traffic drops after a move for predictable reasons: URLs changed without a one-to-one mapping, redirects were done wrong (chains, 302 instead of 301, only the homepage redirected), meta tags and canonical were lost, robots.txt blocked crawling, and a new sitemap was not submitted. Google directly recommends moving content together with correct [301 redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) to preserve the ranking signals of old addresses.

What we do so rankings survive the move:

- keep the URL structure as close to the original as possible;
- place a per-page 301 redirect from every old URL to the matching new one;
- remove redirect chains, sending one step straight to the final address;
- transfer title, description, H1 and canonical unchanged;
- rewrite internal links straight to the new URLs, without passing through a redirect;
- generate and submit a new sitemap.xml;
- set one main mirror and merge duplicates;
- in Search Console we run the "Change of Address" tool after 301 is set, and in Yandex.Webmaster the "Site Move" tool;
- send the changed pages for reindexing.

Google describes this process in detail in its guide on [a site move with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes), and the order from Moz and Ahrefs practice matches it: first the redirect map, then the switch, then indexation control. After the move it is useful to run an [SEO audit](/uslugi/seo-prodvizhenie/seo-audit/) to catch broken redirects and dropped pages before they hit traffic.

## Stages and timelines of migration

The move follows one route regardless of the scenario, only the details of each step change.

1. **Audit of the current site.** We collect the list of URLs, response codes, meta tags and existing redirects.
2. **Backup of files and database.** A full copy you can roll back to.
3. **Staging environment.** We deploy the site on the new hosting, closed from indexation.
4. **URL mapping.** We prepare the address mapping when the CMS or domain changes.
5. **Setting up 301, robots, sitemap, canonical.** We assemble the whole SEO layer in advance.
6. **DNS switch.** We move the site to the new place during a quiet period.
7. **Monitoring.** We watch indexation and rankings for 2 to 4 weeks after launch.

[IMG: ../assets/images/perenos-sayta-2.jpg | Website migration stages: backup, staging environment, DNS switch]

Approximate timelines for the technical part:

- changing hosting without changing CMS, 1–2 days;
- moving from a builder to a CMS, 3–10 days;
- changing domain, 1–3 days of work plus reindexing time;
- merging mirrors, 1–2 days.

A separate note: moving the domain itself between registrars through an EPP code usually takes 5–7 days depending on the zone, and this is worth planning for in advance.

## How much website migration costs

We give an exact quote after a short audit, because the price depends on the scope of work. The cost is affected by:

- site type: landing page, corporate site, store or catalog;
- platform and whether the CMS changes;
- volume of content and number of pages;
- integrations: CRM, 1C, payment, delivery;
- whether the URL structure and structured data need to be preserved;
- depth of SEO support after the move;
- availability of accesses to hosting, domain and database.

| Scenario | What it includes | What we look at |
|---|---|---|
| Changing hosting | backup, staging, transfer, DNS, SSL | volume of files and database |
| Changing CMS | all of the above plus URL mapping and content transfer | number of pages and integrations |
| Changing domain | transfer plus 301, merging, change of address in search engines | connectivity of old links |
| Merging mirrors | setting up the main mirror and redirects | number of duplicates in the index |

[INFOGRAPHIC: ../assets/infographics/perenos-sayta-2.svg | Effects of a correct migration: downtime, preserved traffic, indexation recovery time]

The rule for deciding is simple: the migration should cost less than what bad hosting, lost traffic or site downtime costs you over the same time.

## Why us

We are an independent contractor and are not tied to our own hosting, so we migrate to where it is best for you, not for us. Before the switch we always set up a staging environment and do not touch the live site until the copy is verified. We keep a full backup and the option to roll back in case of any surprise. We place per-page 301 redirects and control indexation after launch instead of dropping the site right after the move. We work under contract and take accesses from a list: hosting, domain, CMS, analytics. You can meet the team on the [about company](/o-kompanii/) page, and discuss the move through [contacts](/kontakty/).

## FAQ

**Will rankings drop after website migration?**
With correct per-page 301 redirects and preserved URL structure and meta tags, rankings hold. A short-term dip is possible during reindexing, after which traffic returns. It is exactly for this that we prepare the redirect map before the switch, not after.

**How long will the site be unavailable during the move?**
From a few minutes to a few hours. The migration is prepared in advance on a staging environment, and we switch DNS during a quiet period, so visitors barely notice any real downtime.

**Will the data and layout be preserved?**
Yes. We transfer the files and database in full, and the layout stays one to one. The site looks and works the same as before the move, unless you separately order changes.

**Will email and requests be preserved?**
Yes. We transfer MX records and mailboxes, and check the feedback forms and CRM link so that emails and requests are not lost after the DNS change.

**How is migration different from a redesign?**
Migration keeps the site's appearance as is and changes only the infrastructure. A redesign, on the contrary, changes the design and structure. If you need to update the look rather than move, that is a different service.

**Can you migrate a site from a builder to your own hosting?**
Yes. A site from Tilda or Wix is moved to a full CMS, but the content and layout are transferred by hand, not with one button. In return you get flexibility and full SEO capabilities.

**What do you need from us as the client?**
Accesses to hosting, domain, CMS, analytics and, if any, CRM. The fuller the accesses at the start, the faster and safer the move goes.

**How is a domain moved between registrars?**
Through an EPP code (authorization code) that you request from your current registrar. The process usually takes 5–7 days depending on the domain zone, and during that time the site keeps working.

**What is mirror merging and why is it needed?**
Merging combines different versions of a site (www and non-www, http and https, old and new domain) into one main mirror. Without it search engines see duplicates and spread weight across copies instead of one address.

**Do you have to change the CMS during migration?**
No. If your current CMS suits you, it is enough to change hosting and keep the engine. Changing the CMS is worth it only when the old one gets in the way of business tasks.

**Will the site stay in the Yandex and Google index?**
Yes. For a controlled move we use the "Site Move" tool in Yandex.Webmaster and "Change of Address" in Google Search Console, and we send the pages for reindexing.

**Do you make a backup and rollback?**
Yes. We take a full backup of files and database before the migration starts. If something goes wrong in the new place, we roll back to the working copy without losing data.

[CTA-final: Migrate your site without losses. Send the site address and where you are moving to, and we will return a migration plan and a risk assessment → form]

---
*Word count: ~1650. FAQ: 12. Infographics: 2. Images: 2. Internal links: 7. Em-dash: 0.*
