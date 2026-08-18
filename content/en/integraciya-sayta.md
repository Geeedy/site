# CONTENT · integraciya-sayta · /uslugi/razrabotka-saitov/integraciya-sayta/

> Gate 4 (15.08.2026). SERVICES page. Structure: [../../drafts/structures/integraciya-sayta.md](../../drafts/structures/integraciya-sayta.md). Em-dash: 0.

## Мета

- **Title:** Website Integration with 1C, CRM and Delivery | skill-dev.ai
- **Meta description:** Website integration with 1C, CRM, card payments, delivery and marketplaces. Catalog, stock and orders sync automatically, requests are never lost. Free audit.
- **OG title:** Website Integration with Your Business Back-End Systems
- **OG description:** Website integration with 1C, CRM, card payments, delivery and marketplaces. Catalog, stock and orders sync automatically, requests are never lost. Free audit.

---

# Website Integration with 1C, CRM, Payments and Delivery

A website often lives a separate life from the business. Products are entered by hand, stock drifts away from 1C, requests are copied from email into the CRM, and payments are reconciled against a bank statement. Website integration removes these manual bridges. We connect your existing site with accounting, sales, payments and logistics so that data moves on its own. This is one of the areas of [website development](/uslugi/razrabotka-saitov/): we do not rewrite the site from scratch, we add data exchange with the systems you already use.

[CTA-hero: Check what can be integrated on your site | Ask a question]
[IMG: ../assets/images/integraciya-sayta-hero.jpg | Website integration with 1C, CRM, payments and delivery]

## What website integration is

Website integration is the setup of automatic data exchange between the site and the company's external systems. The catalog and stock arrive on the site from 1C, orders and requests leave the site for 1C and the CRM, payments are accepted through a payment gateway, delivery cost is calculated by the logistics service, and product cards are distributed across marketplaces. The site stops being an island and becomes part of a shared loop, where every customer action is reflected in accounting without manual transfer.

It is important not to confuse this service with two neighboring ones. Website integration is not the development of a new site, it is a layer of data exchange added on top of a working one. And it is not [Bitrix24 integration with external services](/uslugi/vnedrenie-crm/bitrix24/integraciya/): there the center is the CRM, which is connected to telephony, email and messengers. Here the center is the site as a source of orders and a consumer of the catalog, and the back-end systems are connected to it.

## What we integrate the site with

The set of systems depends on the business, but most often a site is connected with six areas. Below you can see what each connection gives and by which method it is done.

| System | What it gives | Exchange method |
|---|---|---|
| 1C | Catalog, prices, stock and orders sync automatically | CommerceML, standard exchange, REST exchange |
| CRM | Form requests land in the pipeline without manual transfer | Form webhook, CRM API |
| Payment gateway | Card and SBP payments accepted right on the site | Payment system REST API, payment widget |
| Delivery | Cost and lead-time calculation, tracking numbers in the order | Delivery service APIs |
| Marketplaces | Single catalog and stock on Ozon, Wildberries, Yandex Market | Marketplace APIs |
| Analytics | End-to-end data on requests, orders and sales | Event tracking, UTM tags |

You do not have to start everything at once. Usually we first connect what slows the work down the most, and add the rest in later stages.

## Website integration with 1C for catalog, stock and orders

Linking the site with 1C is the core of most projects. 1C remains the owner of data about products, prices and stock, while the site receives it on a schedule and returns placed orders.

[INFOGRAPHIC: ../assets/infographics/integraciya-sayta-1.svg | Data exchange between 1C and the site: catalog down, orders up]

The exchange runs in two directions. Downward, from 1C to the site, go the item list, categories, properties, images, prices and stock. Upward, from the site to 1C, go placed orders together with customer details, payment method and delivery. For product sites on Bitrix this is most often the CommerceML standard and the standard exchange, for other platforms we build the exchange through an API. The schedule is tuned to the load: stock and prices are usually updated every 5–30 minutes so that customers do not buy what is already out of stock.

We close two typical pain points at the start. Duplicate products appear when the site and 1C match items by name, so we link them by a stable code or SKU. Stock desync is cured by logging: every exchange writes a log, and a discrepancy is visible right away rather than a week later through customer complaints. If on top of 1C you want smart scenarios such as demand forecasting or auto-ordering, that is already a task for [AI paired with 1C](/uslugi/vnedrenie-ii/ii-v-1c/), and it is convenient to plan for it once the exchange with the site is already in place.

## Website integration with CRM so requests are not lost

A request that came in from a form but did not reach the CRM is a lead paid for with advertising and lost along the way. Website integration with a CRM closes this gap: every submitted form creates a deal or a lead automatically.

[IMG: ../assets/images/integraciya-sayta-1.jpg | A form request from the site lands in the CRM without manual transfer]

We connect site forms with Bitrix24, amoCRM or RetailCRM through a webhook and API methods such as crm.lead.add. Together with the request, UTM tags, the page of contact and the source go into the card, so the manager sees where the client came from and the marketer measures channel payback. Repeat and duplicate requests from the same person are cut off by anti-duplicate rules, so the pipeline does not clog with junk.

We should separately stress the split of services. Here we link exactly the site with the CRM in the direction of requests. If instead you need to connect Bitrix24 itself to telephony, email, messengers and other services, that is [Bitrix24 integration](/uslugi/vnedrenie-crm/bitrix24/integraciya/) as a separate service, and the vector there is the opposite.

[CTA-mid: We will show on your site where requests and data are being lost right now. Free integration audit → form]

## Website integration with payments and a payment gateway

Accepting payment on the site removes the "we will issue an invoice and wait" step and raises the share of orders taken all the way to money. We connect the site with the YooKassa, Tinkoff, Sber and Robokassa payment gateways and SBP payments, working with their REST APIs and ready-made payment widgets.

Connecting payments is not just a button. Under Federal Law 54-FZ the customer needs a fiscal receipt, so we link the payment gateway with an online cash register so that the receipt is generated at the moment of payment, and the order status on the site and in 1C changes automatically after the payment is confirmed. Refunds and partial payments are also built into the logic, so accounting does not reconcile them by hand.

## Website integration with delivery and marketplaces

Two logistics tasks are solved through an API. The first is calculating delivery right on the site. We connect CDEK, Russian Post, Yandex Delivery and Boxberry, and the customer sees the cost and lead-time before checkout, based on their address and the order dimensions. After checkout the tracking number is pulled into the order, and the client receives it for tracking.

[INFOGRAPHIC: ../assets/infographics/integraciya-sayta-2.svg | Effects of website integration with delivery and marketplaces]

The second task is marketplaces. When products sell both on the site and on Ozon, Wildberries and Yandex Market, stock easily drifts apart and overselling appears. We link the site and the marketplaces through their APIs so that the catalog and stock come from a single source, and orders from the platforms are collected into a shared loop. For an online store this is especially critical, and we cover this scenario in more detail on the [online store development](/uslugi/razrabotka-saitov/internet-magazin/) page.

## How website integration goes

We run the integration step by step and do not touch the live site until we are sure the exchange works on a copy.

[IMG: ../assets/images/integraciya-sayta-2.jpg | Stages of website integration from audit to launch]

1. **Systems audit.** We look at what the site is built on, which version of 1C and the CRM you have, what exports already exist, and where the data chain breaks right now.
2. **Field mapping.** We map which site field corresponds to which 1C and CRM field, and how products and order statuses are matched.
3. **Exchange development.** We write and configure the exchange, building in logging and error handling.
4. **Testing on a copy.** We run the catalog, orders, payments and delivery on a test copy, catching duplicates and discrepancies before launch.
5. **Launch and monitoring.** We move the exchange to the live site and, for the first while, watch the logs to react to rare failures right away.

Timelines depend on scope. A basic link of the site with 1C for catalog, stock and orders usually takes 2–4 weeks, connecting payments or a single delivery service is done faster, a complex project with several systems takes longer.

## How much website integration costs

We give an exact estimate after a short audit, because the price depends on the number of systems, the state of the data, and whether your platform has ready-made exchange mechanisms. To get a sense of what makes up the cost, look at the types of work and the price factors.

| Integration type | What is included | What the price depends on |
|---|---|---|
| Site form and CRM | Form webhook, UTM tracking, anti-duplicates | Number of forms and processing rules |
| Payments and gateway | Payment system connection, 54-FZ receipt | Number of payment methods, refunds |
| Site exchange with 1C | Catalog, stock, prices, orders on a schedule | 1C version and configuration, item volume |
| Delivery | Cost calculation, tracking numbers | Number of delivery services |
| Marketplaces | Single catalog and stock on the platforms | Number of platforms, update frequency |

The decision benchmark is simple. Integration should cost less than what manual data transfer, lost requests and sales of out-of-stock items cost you now. We start with the area where the losses are most visible, so you see the return before expanding the project.

## Why us

We work as an independent integrator on top of your existing site and do not force you to change platforms for the sake of the exchange. A site on Bitrix, WordPress, Tilda or a custom engine we link with 1C and the CRM by whatever method is available on that platform. Every exchange we test on a copy and equip with logging and documentation, so that when staff or the 1C configuration changes it is clear how everything works, and so that a data discrepancy is visible right away. You can meet the team on the [about company](/o-kompanii/) page, and discuss your systems setup through [contacts](/kontakty/).

## FAQ

**How is website integration different from developing a new site?**
Website development is the creation of the site itself from scratch, while integration is a layer of data exchange added on top of an already working site. We do not redo the design and structure, we link your current site with 1C, the CRM, payments and delivery so that data moves automatically.

**My site is on Tilda, WordPress or Bitrix, can it be integrated with 1C?**
Yes. For Bitrix there is the standard CommerceML exchange, for WordPress and other platforms we build the exchange through an API. With Tilda the exchange is usually built through exports and an intermediate service. We choose the method for your platform at the audit stage.

**How often do stock and prices sync with 1C?**
The schedule is tuned to the load. Usually stock and prices are updated every 5–30 minutes so that customers do not buy an item that is already out of stock. If needed, the exchange runs more often.

**What is done so products do not duplicate during the exchange?**
Duplicates appear when the site and 1C match items by name. We link products by a stable code or SKU rather than by text, so one item stays a single one both in 1C and on the site.

**How is website integration with a CRM different from integrating Bitrix24 itself?**
These are different services with a different vector. Website integration with a CRM sends form requests into the pipeline. [Bitrix24 integration](/uslugi/vnedrenie-crm/bitrix24/integraciya/) connects the CRM itself with telephony, email, messengers and other services. In the first case the center is the site, in the second it is the CRM.

**Which payment systems can be connected?**
We connect YooKassa, Tinkoff, Sber, Robokassa and SBP payments. We work with their REST APIs and payment widgets, set up the order status change after payment is confirmed, and handle refunds.

**Do I need an online cash register and how do I comply with 54-FZ?**
To accept payment from individuals a fiscal receipt is required. We link the payment gateway with an online cash register so that the receipt is generated at the moment of payment. The register can be cloud-based or your own, and we will suggest an option for your order volume.

**Can CDEK delivery cost be calculated right on the site?**
Yes. Through the CDEK API the cost and lead-time are calculated on the site by the address and order dimensions before checkout. Russian Post, Yandex Delivery and Boxberry are connected the same way, and the tracking number is pulled into the order.

**How do I upload products to Ozon and Wildberries from a single catalog?**
We link the site and the marketplaces through their APIs so that the catalog and stock come from a single source. Then the items and availability match on the site and on the platforms, and overselling from drifting stock does not occur.

**How long does integration take?**
A basic link of the site with 1C for catalog, stock and orders usually takes 2–4 weeks. Connecting payments or a single delivery service is done faster, a complex project with several systems takes longer. We give an exact timeline after the audit.

**What if we have a non-standard 1C configuration?**
With a customized configuration the exchange is built through an API and field-mapping rules tailored to your structure. At the audit stage we review how products, orders and statuses are set up, and build the exchange around your real 1C rather than a standard one.

**Will form requests really not be lost?**
Yes, this is one of the main goals of the integration. Every submitted form creates a lead or a deal in the CRM automatically, together with UTM tags and the source. The exchange writes a log, so it is visible that the request arrived, and anti-duplicates cut off repeats.

[CTA-final: Send a link to your site and a list of systems it needs to be connected with. We will return an integration plan and estimate → form]

---
*Word count: ~1750. FAQ: 12. Infographics: 2. Images: 3. Internal links: 6. Em-dash: 0.*
