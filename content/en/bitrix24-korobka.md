# CONTENT v1.0 · bitrix24-korobka · /uslugi/vnedrenie-crm/bitrix24/korobochnaya-versiya/

> Gate 4 (16.08.2026). SERVICES page (L3). Structure: [../../drafts/structures/bitrix24-korobka.md](../../drafts/structures/bitrix24-korobka.md).
> Style: no em-dash. Em-dash: 0.

## Мета

- **Title:** Bitrix24 On-Premise Version: Server Implementation | skill-dev.ai
- **Meta description:** We deploy the on-premise Bitrix24 version on your server: edition and license selection, installation, source-code customization, renewal, data under 152-FZ. Free estimate.
- **OG title:** Bitrix24 On-Premise Version: Deployment on Your Own Server | skill-dev.ai
- **OG description:** We implement on-premise Bitrix24: your own infrastructure, code access, updates and license renewal, data storage under 152-FZ. We help you choose between on-premise and cloud.

---

# Bitrix24 On-Premise Version: Implementation on Your Server

The on-premise Bitrix24 version lives on your server, not in the vendor's cloud. You get the product files, the database, and access to the source code, so you fully control the infrastructure, customization, and data storage. We select the edition for the task, deploy the portal on your hardware or in a data center, customize it to your processes, and honestly tell you when cloud is the better choice.

[CTA-hero: Estimate on-premise implementation | Ask a question]
[IMG: ../assets/images/bitrix24-korobka-hero.jpg | On-premise Bitrix24 implementation on the company server]

## What the On-Premise Bitrix24 Version Is

The on-premise (self-hosted) version is an edition of the portal that is installed on the company's own server or in a rented data center, rather than rented as a cloud service. The owner gets a distribution with the product files, their own database, and full access to the source code ([helpdesk.bitrix24.ru](https://helpdesk.bitrix24.ru/)).

The difference from cloud is simple. Cloud Bitrix24 runs on the SaaS model, where the vendor handles infrastructure and updates while you pay a subscription and use a ready-made portal. On-premise hands you the server, the code, and the responsibility for maintenance. We cover the platform overview and turnkey cloud implementation on the [Bitrix24 implementation](/uslugi/vnedrenie-crm/bitrix24/) page, and here we focus only on the on-premise ownership model.

## On-Premise or Cloud Bitrix24: Comparison

The main question before purchase sounds like this: where the data must reside and how deeply you will customize the system. The answer determines the choice between on-premise and cloud. Below is a comparison across seven criteria that most often decide the outcome.

[INFOGRAPHIC: ../assets/infographics/bitrix24-korobka-1.svg | On-premise or cloud Bitrix24: comparison across seven criteria]

| Criterion | On-premise | Cloud (SaaS) |
|---|---|---|
| Where data is stored | On your server or in your data center | In the vendor's data centers |
| Access to source code | Yes, you edit files and modules | No, only through the API |
| Depth of customization | Any, down to the core | Within the REST API and settings |
| Payment model | One-time license plus renewal | Monthly or annual subscription |
| Updates | Installed by your administrator | Delivered automatically |
| Infrastructure load | Your server, your maintenance | Vendor's infrastructure |
| Getting started | Requires a server and installation | Sign up and start right away |

Neither option wins on every row at once. On-premise wins on control and customization, cloud wins on start speed and freedom from server care ([vc.ru](https://vc.ru/)).

## Who Needs the On-Premise Version

On-premise is for those who need control over the server and the data. This is the public sector, finance, healthcare, industry, and any company with 152-FZ and industry-specific requirements. It also covers tasks of deep customization, code-level integration, and isolating the portal from the external network.

Cloud is the more honest recommendation in a different situation. If you have no in-house IT team, need a fast start, and the team is small, on-premise adds server and administration costs without a clear benefit. In that case we offer cloud [CRM implementation](/uslugi/vnedrenie-crm/) and do not sell anything extra.

From our practice, the choice between on-premise and cloud almost always comes down to two factors: data-localization requirements and customization plans. When both factors are weak, on-premise becomes more expensive to own without any upside, and we say so directly.

## Editions, Licenses, and Renewal of the On-Premise Version

### On-premise editions

On-premise Bitrix24 ships in several editions for different scales: "Online Store + CRM", "Corporate Portal", and "Enterprise". Licensing is tied to the number of employees who work in the system, not to the server ([1c-bitrix.ru](https://www.1c-bitrix.ru/)). We verify the exact edition contents and user limits against the vendor's current price list before the estimate, because the lineup changes periodically.

[IMG: ../assets/images/bitrix24-korobka-1.jpg | License contents of the on-premise Bitrix24 version]

### License renewal

The first year of updates and technical support is included in the on-premise license cost. After that, to keep receiving new versions and patches, the license is renewed for a fraction of its cost per year ([helpdesk.bitrix24.ru](https://helpdesk.bitrix24.ru/)). If you do not arrange the renewal, the portal will keep running on the current version but will stop receiving official updates, which over time creates security and compatibility risks. We calculate the specific amounts and renewal percentage from the vendor's price list for your edition.

## Deployment on Your Own Server: Requirements

Before installation, the server is prepared for the product's requirements. The basic environment set looks like this ([helpdesk.bitrix24.ru](https://helpdesk.bitrix24.ru/)):

- **OS.** Linux is recommended as the primary option, Windows is also supported.
- **Web server.** Apache or Nginx with the required configuration.
- **PHP** in a version supported by the product.
- **Database.** MySQL or MariaDB.
- **Resources.** Disk and RAM sized for the number of users and the data volume.
- **Backup.** A backup policy on the company's side.

The portal can be deployed in three ways: on your own physical server, on a VDS or VPS, or through the ready-made "1C-Bitrix: Virtual Machine" (BitrixVM) image, which the vendor recommends as the fastest way to bring up a correct environment ([1c-bitrix.ru](https://www.1c-bitrix.ru/)). We verify specific software versions against the documentation before installation, because the requirements are updated along with the product.

[CTA-mid: Send your server specifications. We will tell you whether it can handle on-premise and what to add → form](/kontakty/)

## Customization and Access to Source Code

The main technical advantage of on-premise lies at the code level. You edit components and templates, write your own modules, embed custom business logic, and build integrations through the D7 core, not only through the REST API ([1c-bitrix.ru](https://www.1c-bitrix.ru/)). Cloud has no such depth, where only the API and interface settings are available.

This freedom comes with engineering discipline. Changes are best moved into separate modules without touching the core files directly, otherwise an update will wipe out the customizations. We design customization so it survives renewal and updates. We split fine-tuning of functions inside the portal (pipelines, permissions, robots) into a separate [Bitrix24 configuration](/uslugi/vnedrenie-crm/bitrix24/nastroika/) service, so that server deployment and business-logic configuration are not mixed together.

## Data on Your Own Server and 152-FZ

On-premise addresses personal-data storage requirements through physical placement. The data resides on the company's infrastructure in Russia, which simplifies meeting the personal-data localization requirements under the Russian data-localization law (152-FZ). The company configures access control, logging, network-segment isolation, encryption, and backups according to its own internal policies.

An important caveat. On-premise provides the technical basis for compliance, but it is not a certificate in itself. The company builds organizational measures, the threat model, and, if needed, certification of the information system on its own or with a specialized information-security contractor. Our job is to make sure the technical side of the portal does not hinder these requirements but supports them. We cover on-premise integrations with internal systems, including 1C and telephony, in the [1C and telephony integration](/uslugi/vnedrenie-crm/bitrix24/integraciya/) service.

## Updates for the On-Premise Version

On-premise updates are installed by the administrator through the built-in update module, not automatically by the vendor. The company decides for itself when to move to a new version and keeps the update under control ([helpdesk.bitrix24.ru](https://helpdesk.bitrix24.ru/)). This distinguishes on-premise from cloud, where updates arrive without your involvement.

The on-premise update process requires care. Customizations are checked for compatibility, the update is first run on a test copy, and only then rolled out to the production portal. We take this work into maintenance: we track version releases, test compatibility with your modules, and update the portal without downtime for the department.

## Implementation Stages and Cost

### Stages

We run on-premise implementation in five steps:

1. **Requirements audit and edition selection.** We work through the tasks, the number of users, and the data requirements.
2. **Server preparation.** Environment, BitrixVM or your configuration, backups.
3. **Installation and initial setup.** Distribution, license, basic portal structure.
4. **Data migration and customization.** Database transfer, custom modules, integrations.
5. **Launch, training, and maintenance.** Go-live, team training, update support.

[INFOGRAPHIC: ../assets/infographics/bitrix24-korobka-2.svg | Stages and timeline of on-premise Bitrix24 implementation]
[IMG: ../assets/images/bitrix24-korobka-2.jpg | Installation stages of the on-premise Bitrix24 version on your own server]

### Cost

The final on-premise budget is made up of several line items.

| Line item | Reference point | Comment |
|---|---|---|
| On-premise license | Per the vendor's price list by edition | Depends on the edition and number of employees |
| Installation work | By project scope | Server preparation, installation, setup |
| Customization | By task scope | Modules, integrations, custom logic |
| License renewal | A fraction of the license cost per year | The first year is included in the on-premise price |

Exact figures depend on the edition, the server, and the depth of customization, so we lock the estimate only after an audit. We are an independent integrator, not a license reseller, so we select the edition for the task rather than selling the largest one. Read more about the approach on the [independent integrator](/o-kompanii/) page.

## FAQ
**How does the on-premise Bitrix24 version differ from the cloud one?**
On-premise is installed on your server, gives access to the source code, and is paid for with a one-time license plus renewal. Cloud runs on a subscription on the vendor's servers without code access. See the overview of the cloud option on the [Bitrix24 implementation](/uslugi/vnedrenie-crm/bitrix24/) page.

**Can you move from cloud Bitrix24 to on-premise and back?**
Yes, migration between cloud and on-premise is possible, but it is not a flip of a switch. The database, users, and settings are transferred, and customizations are adapted to the new environment. We plan such a move as a separate project with data and history preserved.

**How much does the on-premise Bitrix24 version cost?**
The cost is made up of the license per the vendor's price list, installation and customization work, and the annual renewal. The price depends on the edition, the number of employees, and the depth of customization. We provide an exact estimate after a requirements and server audit.

**What is included in the on-premise license and how is it licensed?**
The license includes the product distribution, source-code access, and the first year of updates with technical support. Licensing is tied to the number of employees in the system, and the edition is chosen for the scale of the tasks. We verify the edition contents against the vendor's current price list.

**What does license renewal provide and what happens if you do not renew it?**
Renewal preserves access to updates and technical support for a fraction of the license cost per year. The first year is included in the on-premise price. Without renewal the portal keeps running on the current version but stops receiving patches, which over time increases security risks.

**How is the on-premise version updated and who installs the updates?**
Updates are installed by the administrator through the built-in update module, and the company decides the timing of the move. The update is first checked on a test copy, then rolled out to the production portal. We take this work into maintenance and check the compatibility of customizations.

**What are the server requirements for installing the on-premise version?**
You need a Linux or Windows OS, an Apache or Nginx web server, a supported PHP version, and a MySQL or MariaDB database. Resources are sized for the number of users and the data volume. The fastest way to bring up a correct environment is through the BitrixVM image.

**Is there access to the source code and can the system be customized?**
Yes, on-premise gives full access to the code. You edit components and templates, write your own modules, and build integrations through the D7 core, not only through the API. We move customizations into separate modules so they survive updates.

**How does the on-premise version help meet 152-FZ requirements?**
On-premise places personal data on your infrastructure in Russia, which simplifies meeting the personal-data localization requirements. Access control and logging remain on your side. On-premise provides the technical basis, while the company handles certification and organizational measures itself.

**Can the on-premise Bitrix24 be connected to 1C?**
Yes, on-premise integrates with 1C, telephony, and external systems, including at the code level. This is a separate task with its own exchange scenarios. We cover integrations in detail in the [Bitrix24 integration](/uslugi/vnedrenie-crm/bitrix24/integraciya/) service.

**How long do installation and implementation of the on-premise version take?**
The timeline depends on the server's readiness and the volume of customization. Installation and initial setup take little time, most of the time goes into data migration and customization. We provide an exact schedule after a requirements audit.

**Do you need your own system administrator for the on-premise version?**
On-premise needs someone responsible for the server, backups, and updates. This can be your in-house administrator or our maintenance under contract. Without such a role, on-premise loses its point, and then cloud is the more honest choice.

[CTA-final: Free project estimate. We will work through the tasks and tell you whether on-premise or cloud is the better fit → form](/kontakty/)

---
*Word count: ~1500. FAQ: 12. Infographics: 2. Images: 3. Em-dash: 0.*
