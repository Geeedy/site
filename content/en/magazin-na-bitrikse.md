# CONTENT · magazin-na-bitrikse · /uslugi/razrabotka-saitov/internet-magazin/na-bitrikse/

> Gate 4 (16.08.2026). SERVICES page. Structure: [../../drafts/structures/magazin-na-bitrikse.md](../../drafts/structures/magazin-na-bitrikse.md). Em-dash: 0.

## Мета

- **Title:** Turnkey Online Store on 1C-Bitrix | skill-dev.ai
- **Meta description:** We build online stores on 1C-Bitrix: catalog, cart, YooKassa and SBP acquiring, 1C exchange via CommerceML. Edition from 47,000 RUB, store from 235,000 RUB.
- **OG title:** Online Store on 1C-Bitrix: Catalog, Cart, 1C Exchange
- **OG description:** Turnkey store on 1C-Bitrix with two-way 1C exchange via CommerceML (products, prices, stock, orders), acquiring, and SEO. Small Business and Business editions.

---

# Turnkey Online Store Development on 1C-Bitrix

We build e-commerce on the 1C-Bitrix engine: a catalog with trade offers, a cart, online payment, and two-way exchange with your 1C. This is not just a [website on 1C-Bitrix](/uslugi/razrabotka-saitov/sait-na-bitrikse/) with a contact form, but a full store where products, prices, and stock live in 1C while the buyer places and pays for the order on the site. If you are still choosing a platform and comparing engines, start with the overview page about the [online store](/uslugi/razrabotka-saitov/internet-magazin/); if the decision in favor of Bitrix is already made, you are on the right page.

[CTA-hero: Order an online store on 1C-Bitrix | Ask a question]
[IMG: ../assets/images/magazin-na-bitrikse-hero.jpg | Turnkey online store development on 1C-Bitrix]

## Why online stores choose 1C-Bitrix

An online store on 1C-Bitrix is an e-commerce site on the commercial CMS "1C-Bitrix: Site Management" with a catalog, cart, online payment, and out-of-the-box 1C exchange. The platform is chosen for a store for three reasons.

- **Native 1C exchange.** Catalog, price, and stock uploads and order intake work without a third-party connector, because both the accounting system and the CMS are made by one vendor.
- **Ready e-commerce core.** Catalog, cart, discounts, coupons, payment and delivery modules come in the store editions rather than being built from scratch.
- **Maturity for load and SEO.** Composite cache, human-readable URLs, and meta management by sections and products are built into the engine, so the store handles growth in assortment and traffic.

Bitrix suits small and medium businesses above all, those who need a catalog, cart, online payment, delivery, SEO, and 1C integration without developing a platform from scratch ([gendalf.ru](https://www.gendalf.ru/), [alekseybulchuk.ru](https://alekseybulchuk.ru/), 2026).

## 1C exchange via CommerceML is the core of the store

Exchange with 1C is what sets a Bitrix store apart from an ordinary site. It runs on the CommerceML 2.0 / 2.09 standard in XML format and works both ways: catalog, prices, stock, and attributes are uploaded from 1C to the site, while placed orders and their statuses go from the site back to 1C. The built-in exchange handler is `/bitrix/admin/1c_exchange.php`, and the exchange is always initiated by 1C:Enterprise ([1c.1c-bitrix.ru](https://1c.1c-bitrix.ru/ecommerce/technology.php), [v8.1c.ru](https://v8.1c.ru/), 2026).

[INFOGRAPHIC: ../assets/infographics/magazin-na-bitrikse-1.svg | Diagram of two-way exchange between an online store on 1C-Bitrix and 1C via CommerceML: products, prices, stock, orders]

| Data | Direction | Why |
|---|---|---|
| Catalog, properties, structure | from 1C to site | the storefront always matches accounting |
| Prices and stock | from 1C to site | the buyer sees the current price and availability |
| Attributes and trade offers | from 1C to site | sizes, colors, packaging in the product card |
| Orders and statuses | from site to 1C | the manager processes the order in familiar 1C |

A typical upload is split into files: `import` with the catalog structure, products, and properties, and `offers` with prices, stock, and trade offers; orders run as a separate flow back to 1C ([truetech.by](https://truetech.by/), [ciftix.ru](https://ciftix.ru/), 2026). The exchange is built into "1C-Bitrix: Site Management," a separate connector module is not needed, and a dedicated administrator user with a login and password is created for synchronization ([kalinkindev.ru](https://kalinkindev.ru/), [dev.1c-bitrix.ru](https://dev.1c-bitrix.ru/), 2026). If, beyond the exchange, you want to automate the accounting system itself, take a look at our [AI in 1C](/uslugi/vnedrenie-ii/ii-v-1c/) service.

[CTA-mid: Need exchange with your 1C? We will walk through catalog and order uploads in a free consultation → form]

## Payment and delivery in the store

A store without payment and delivery is a storefront, so we connect payment and logistics modules in the base build. A typical project connects acquiring and several payment systems, most often YooKassa and SBP, while delivery is set up from a single method in the base package to several carriers with automatic rate calculation ([mwi.me](https://mwi.me/), [gendalf.ru](https://www.gendalf.ru/), 2026).

- **Payment:** YooKassa acquiring, SBP (Faster Payments System) via QR code, cash on delivery, and pay on receipt.
- **Delivery:** pickup, courier services, and carriers with cost calculation by address and weight.
- **Fiscalization:** sending receipts to the online cash register under Federal Law 54-FZ through the payment service.

Payment and delivery methods are set up for your sales scheme rather than imposed by the box, so we agree on the set of modules at the start.

## Editions and licenses for an online store

For a store, 1C-Bitrix has separate editions with a cart and catalog. The difference between them is in the complexity of sales logic and headroom for growth, not in whether e-commerce is present at all.

| Edition | Price 2026 | For which store |
|---|---|---|
| Small Business | from [47,000 RUB](https://www.1c-bitrix.ru/buy/products/cms.php) | typical store: catalog, prices, stock, orders, CommerceML exchange |
| Business | from [96,500 RUB](https://www.1c-bitrix.ru/buy/products/cms.php) | complex sales logic, discount rules, assortment growth |
| Enterprise | from [1,950,000 RUB](https://www.gendalf.ru/) | large high-load projects and distributed infrastructure |

For most small and medium business projects, the Small Business edition is enough: it already has a cart, catalog, order intake, and 1C exchange. Business is chosen when complex discounts, loyalty programs, and scaling headroom are needed. At the start, we select the edition for your goals so you do not overpay for features you will not use.

## Catalog, properties, and product import

The catalog is the store's storefront, and on Bitrix it is built around sections, products, and trade offers. A product with variations (for example, a T-shirt in three colors and four sizes) is described as a product with trade offers, not as twelve separate cards. The CommerceML 2.09 format, current for 1C:Trade Management 11 and newer, supports uploading product attributes, packaging, and bundles, so properties reach the site straight from the accounting system ([1c-expert](https://1c-expert.ru/), 2026).

[IMG: ../assets/images/magazin-na-bitrikse-1.jpg | Catalog and trade offers of an online store on 1C-Bitrix]

Smart catalog filters are assembled from the attributes that arrived via exchange: by price, brand, color, size, and any product property. This is convenient for the buyer and useful for SEO, because filter combinations become landing pages for queries like "buy a red size 44 dress."

## SEO of an online store on Bitrix

A store exists so it can be found in search, so we lay down SEO at the development stage, not after launch. 1C-Bitrix provides out-of-the-box tools for this: human-readable URLs for catalog sections and product cards, title and description management at the section and element level, filters as landing pages, automatic sitemap.xml generation, and a composite cache for speed ([dev.1c-bitrix.ru](https://dev.1c-bitrix.ru/), 2026).

- **Human-readable URLs and structure.** Readable section and product addresses instead of parameters in the URL.
- **Templated meta.** Automatic yet manageable title and description for thousands of cards.
- **Filter landing pages.** Pages for long-tail queries from combinations of catalog properties.
- **Speed.** Composite cache and optimization for Core Web Vitals, which matters for mobile search.

We tune these mechanisms to your semantic core so the catalog starts collecting traffic from the first weeks after launch rather than waiting for manual rework.

## How much an online store on 1C-Bitrix costs

The store budget is made up of the license, design, development, integrations, and content, so a single turnkey figure does not exist. Market benchmarks for 2025–2026 look like this.

[INFOGRAPHIC: ../assets/infographics/magazin-na-bitrikse-2.svg | What makes up the cost of an online store on 1C-Bitrix]

| Project level | Cost | What is included |
|---|---|---|
| Ready solution, budget | [150,000–300,000 RUB](https://abcwww.ru/) | template, basic catalog, payment, and 1C exchange |
| Standard with integrations | [400,000–700,000 RUB](https://www.gendalf.ru/) | design adaptation, several integrations, filters |
| Custom development | [from 500,000–580,000 RUB](https://digital-sail.ru/) | unique design, complex logic, high load |

The 1C-Bitrix license from [47,000 RUB](https://www.1c-bitrix.ru/buy/products/cms.php) and support are budgeted separately, with support in the first year estimated at [20–30% of the development budget](https://codingteam.ru/). Large projects with unique logic reach 1.4–2.7 million RUB, but that is more the exception for medium business. We lock the exact estimate after a short brief, once the assortment, integrations, and design are clear.

## How store development goes

We run development in stages so you see the result at every step rather than getting a "black box" at the end.

[IMG: ../assets/images/magazin-na-bitrikse-2.jpg | Stages of online store development on 1C-Bitrix]

1. **Brief and prototype.** We examine the assortment, sales scheme, payment, and delivery, and draw the catalog structure and prototypes of key pages.
2. **Design.** We render the storefront, product card, cart, and checkout for your brand.
3. **Development and 1C exchange.** We build the catalog, cart, and checkout, and set up two-way exchange via CommerceML.
4. **Integrations.** We connect acquiring, delivery, analytics, and, if needed, CRM.
5. **Content and SEO.** We load products from 1C and set up human-readable URLs, meta, and filter landing pages.
6. **Launch and support.** We test, move to the production domain, and hand over the store with support.

## Why us

An online store on Bitrix is one of the areas within our [website development](/uslugi/razrabotka-saitov/), and here we focus on what brings money: working 1C exchange, a clear catalog, and payment without failures. We do not sell a box and disappear after launch; we study your accounting system, set up catalog and order uploads, and take responsibility for keeping the storefront in sync with 1C. We lay down SEO at the development stage, not as a separate service later. You can meet the team on the [about](/o-kompanii/) page and discuss your store through [contacts](/kontakty/).

## FAQ

**How is an online store on 1C-Bitrix different from an ordinary Bitrix site?**
An ordinary [website on 1C-Bitrix](/uslugi/razrabotka-saitov/sait-na-bitrikse/) is an engine for a corporate site, catalog, or portal without selling online. An online store is an e-commerce build on top of the same engine: cart, checkout, online payment, and two-way exchange with 1C. If sales and payment happen on the site, you need a store, not just a site.

**How does 1C exchange work and what exactly is synchronized?**
The exchange runs on the CommerceML standard in XML format. Catalog, prices, stock, and attributes are uploaded from 1C to the site, while orders and their statuses come back from the site to 1C. The exchange is always initiated by 1C, and Bitrix's built-in handler works on the site side.

**Does my 1C need to be already configured for exchange?**
1C must have the standard "Site Exchange" processing enabled, which is present in current configurations like Trade Management. If the exchange node is not set up yet, we will configure it: create a user for synchronization, set the schedule, and check catalog uploads and order intake.

**Which edition to choose, Small Business or Business?**
For a typical store with a catalog, prices, stock, orders, and CommerceML exchange, the Small Business edition is enough. Business is chosen when complex discount rules, loyalty programs, and assortment growth headroom are needed. We will select the edition at the start for your sales scheme.

**How much does a 1C-Bitrix license for a store cost?**
The Small Business license costs from [47,000 RUB](https://www.1c-bitrix.ru/buy/products/cms.php), Business from [96,500 RUB](https://www.1c-bitrix.ru/buy/products/cms.php), and Enterprise for large projects from [1,950,000 RUB](https://www.gendalf.ru/). The license is a one-time purchase and is paid separately from development.

**How much does a turnkey online store on 1C-Bitrix cost?**
A ready template-based solution costs [150,000–300,000 RUB](https://abcwww.ru/), a standard project with integrations and design adaptation [400,000–700,000 RUB](https://www.gendalf.ru/), and custom development [from 500,000–580,000 RUB](https://digital-sail.ru/). The budget is made up of the license, design, development, integrations, and content, so we lock the estimate after the brief.

**Which payment and delivery methods can be connected?**
For payment, the most common are YooKassa and SBP acquiring, as well as cash on delivery and pay on receipt. For delivery, pickup, courier services, and carriers with rate calculation by address are set up. We agree on the set of modules for your sales scheme.

**Can an existing store be moved to 1C-Bitrix without losing products and SEO?**
Yes. Products are transferred via 1C exchange or catalog import, and old addresses are closed with 301 redirects to the new human-readable URLs to preserve search positions. Before the move, we capture the URL and meta-tag map so as not to lose traffic after launch.

**Bitrix or another platform for a store, which to choose?**
Bitrix is strong in native 1C exchange and a mature e-commerce core, so it is chosen when accounting is kept in 1C. If you are still comparing engines and are not tied to 1C, look at the overview page about the [online store](/uslugi/razrabotka-saitov/internet-magazin/), where we break down platform choice by task.

**How long does store development take?**
A store on a ready solution is assembled in a few weeks, a standard project with integrations and design adaptation takes from one and a half to three months, and custom development is longer. Timing depends on the assortment, number of integrations, and content readiness; we give an exact schedule after the brief.

**How is SEO and promotion set up in a Bitrix store?**
Bitrix provides human-readable URLs for the catalog and products, title and description management by sections and elements, filters as landing pages, automatic sitemap.xml generation, and a composite cache for speed. We tune these mechanisms to your semantic core so the catalog collects traffic from the first weeks.

**Is support needed after launch and how much does it cost?**
Support is needed so that 1C exchange, payment, and updates run stably. First-year support is usually estimated at [20–30% of the development budget](https://codingteam.ru/). We take support on ourselves or train your team to run the store in-house.

[CTA-final: Leave a request. We will select the 1C-Bitrix edition and calculate the cost of your store → form]

---
*Word count: ~1650. FAQ: 12. Infographics: 2. Images: 3. Em-dash: 0.*
