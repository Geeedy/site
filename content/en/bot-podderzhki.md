# CONTENT · bot-podderzhki · /uslugi/chat-boty/bot-podderzhki/

> Gate 4 (16.08.2026). SERVICES page. Structure: [../../drafts/structures/bot-podderzhki.md](../../drafts/structures/bot-podderzhki.md). Em-dash: 0.

## Мета

- **Title:** Support Bot Development for Business | skill-dev.ai
- **Meta description:** We build a first-line support chatbot that answers typical questions from your knowledge base, opens tickets, and escalates hard cases to an agent. Free demo.
- **OG title:** Support Bot: First Line on Autopilot
- **OG description:** A first-line support chatbot on GPT and your knowledge base. It answers typical requests, opens tickets, and passes hard cases to an agent. We will show a demo on your requests.

---

# Support Bot: Closes Typical Requests and Takes Load off Your Agents

Support teams drown in the same questions: where is my order, how do I return an item, what are the working hours, what to do about an error. A first-line support bot takes that flow off their hands. It receives the request, answers from the company knowledge base, opens a ticket when needed, and hands complex cases to a live agent. It works around the clock on both the website and messengers, with no night shifts and no queues. We assemble a bot like this around your real request flow and show a demo before launch. This is part of our approach to [AI chatbots](/uslugi/chat-boty/): a solution built for the task, not a boxed subscription.

[CTA-hero: Show a demo on your requests | Ask a question]
[IMG: ../assets/images/bot-podderzhki-hero.jpg | Support bot answers a client and opens a ticket in chat]

## What a support bot is

A support bot is a first-line chatbot that receives customer requests, answers typical questions from the company knowledge base, opens a ticket in the helpdesk when needed, and passes complex or sensitive cases to a live agent. It works around the clock on both the website and messengers, and the client types a question in plain text, with no rigid button menu. Where exactly the bot lives (the channel) and which engine it runs on (GPT) are separate questions, covered below. An autonomous task executor that performs actions in systems on its own is already an [AI agent](/uslugi/vnedrenie-ii/), a different service.

## What a support bot can do: answers, tickets, escalation

[INFOGRAPHIC: ../assets/infographics/bot-podderzhki-1.svg | Three groups of support bot functions: FAQ answers, ticket handling, escalation to an agent]

First-line work breaks down into three groups of functions.

- **Answers to typical questions.** The bot understands a question phrased freely and answers from the knowledge base: statuses, terms, instructions, working hours. Per [McKinsey](https://www.mckinsey.com/capabilities/operations/our-insights/where-is-customer-care-in-2024), mature AI support automates about 65% of tasks and 50–70% of contacts.
- **Ticket handling.** If a question is not resolved in the dialogue, the bot collects the data and opens a request in the helpdesk, then sends the client a status and confirmation.
- **Escalation to an agent.** A complex, non-standard, or legally sensitive question the bot passes to a human along with the dialogue history, instead of "guessing" an answer.

[CTA-mid: We will assemble a demo bot on your real requests in a few days → form]

## How the bot reduces the support team's load

The effect of the first line is measured by the deflection rate, the share of requests closed without an agent. But this single number cannot be taken in isolation: it is read together with the resolution rate (the share actually resolved) and the re-contact rate (the share of repeat requests), otherwise the effect is overstated. Below are market benchmarks.

| Metric | Value | Source |
|---|---|---|
| Deflection of basic chat rollouts | 20–40% | [Zendesk / eesel.ai](https://www.eesel.ai/blog/zendesk-deflection-rate) |
| Deflection of mature AI rollouts | 60–80% | [Zendesk / eesel.ai](https://www.eesel.ai/blog/zendesk-deflection-rate) |
| Median first-line deflection | 41.2%, top quartile 58.7% | [Zendesk CX Trends 2026 / digitalapplied.com](https://www.digitalapplied.com/blog/ai-customer-service-deflection-benchmarks) |
| First-contact resolution with automation | 58–65% | [Gartner Customer Service Survey 2025 / stealthagents.com](https://stealthagents.com/customer-service-automation-statistics/) |
| Support productivity gain from gen AI | 30–45% | [McKinsey / venbit.ai](https://venbit.ai/blog/generative-ai-customer-support) |

Resolvability depends heavily on the request type. Bots close returns and cancellations in about 48% of cases, but disputed charges in only 17% ([Gartner / try.experience.com](https://try.experience.com/customer-service-automation-benchmarks)). So the bot's goal is to take off the typical flow, not to replace the agent on every task.

## What it runs on: GPT and RAG over your knowledge base

[IMG: ../assets/images/bot-podderzhki-1.jpg | Diagram: how the support bot answers from the knowledge base and escalates to an agent]

The reliability of answers rests on three pillars.

- **GPT/LLM** understands free text and holds the dialogue context, so the client writes the question as is, without a button tree.
- **RAG** forces the system to search fragments in the company knowledge base before answering and to build the answer only on them, by the rule "no data, escalate." This keeps the bot from making things up.
- **Human-in-the-loop** sends the question to an agent when the model's confidence is low.

We cover the GPT engine itself and protection against hallucinations in more detail on the [GPT bot](/uslugi/chat-boty/bot-na-gpt/) page. One thing matters here: the bot answers with your policies, not the model's general knowledge.

## Integration with CRM, helpdesk, and channels

A support bot does not work in a vacuum, it embeds into the service loop.

- **Helpdesk and service desk:** opening and updating tickets, statuses, routing (Zendesk, Bitrix24, and analogs).
- **CRM:** the client card, request history, handing the deal to a manager. More on how this is set up is on the [CRM implementation](/uslugi/vnedrenie-crm/) page.
- **Channels:** the website and messengers (Telegram, WhatsApp, VK) with a single dialogue history across them.

The economics here are transparent. Per [McKinsey / brilo.ai](https://brilo.ai/blog/ai-customer-service-cost-per-contact), one request closed by AI costs around $0.62 versus $7.40 with a live agent, and for chat it is about $0.41. Round-the-clock work absorbs peaks and night requests without night shifts.

## Which channels the support bot works in

A channel is where exactly the bot lives. The support task is one, but there are several venues, and each has its own page: [website bot](/uslugi/chat-boty/bot-na-sait/) for a widget on the page and [Telegram bot](/uslugi/chat-boty/telegram-bot/) for the messenger. Here the topic is the support task itself, so we keep channels brief: the bot works on the website and in messengers with a shared dialogue history. And if you need not a responding assistant but an autonomous executor that performs actions in systems on its own, that is an [AI agent](/uslugi/vnedrenie-ii/), a neighbor among the services, not a first-line bot.

## How development goes

[IMG: ../assets/images/bot-podderzhki-2.jpg | Five stages of support bot development]

We go from requests to a working bot step by step.

1. **Request audit.** We build the knowledge base from FAQs, policies, and agent scripts.
2. **Scenario mapping.** We define what the bot closes itself, what it opens as a ticket, what it escalates.
3. **Assembly.** We set up RAG and the prompt loop, connect the helpdesk and CRM.
4. **Testing.** We check on real requests and measure deflection and answer accuracy.
5. **Launch.** We roll the bot out to channels, train agents, and keep updating the knowledge base.

## How much a support bot costs

[INFOGRAPHIC: ../assets/infographics/bot-podderzhki-2.svg | What makes up the cost of a support bot and how it pays off]

The cost is made up of three parts, and the total depends on your flow.

- **Development** depends on the size of the knowledge base and the number of scenarios; we lock the estimate after a short request audit.
- **Monthly costs** are the model API plus knowledge base upkeep, with a market benchmark for GPT bots of 3,000–15,000 RUB/month depending on dialogue volume.
- **What the price depends on** is the size of the knowledge base, the number of channels, the depth of CRM and helpdesk integration, and the target deflection.

Payback is calculated through the drop in cost per request: $0.41–0.62 for a bot versus $7.40 for an agent ([McKinsey / brilo.ai](https://brilo.ai/blog/ai-customer-service-cost-per-contact)). The result is measured not by a single number but by the deflection rate together with the resolution and re-contact rates ([digitalapplied.com](https://www.digitalapplied.com/blog/ai-customer-service-deflection-benchmarks)).

## FAQ

**How does a support bot differ from an ordinary chatbot?**
It is a first-line bot built for the support task: it answers from the knowledge base, opens tickets, and escalates complex cases to an agent, rather than just holding a free-form conversation. An ordinary chatbot is a broader notion, while a support bot is tuned for customer service.

**How does a client message the support bot?**
The bot is available on the website and in messengers. The client opens the chat and types a question in plain text, without picking menu items. The bot understands free phrasing and answers from the knowledge base, and if it cannot resolve the issue itself, it opens a ticket or hands it to an agent.

**What share of requests will the bot close?**
Market benchmark: 20–40% at the start and 60–80% in a mature rollout ([Zendesk / eesel.ai](https://www.eesel.ai/blog/zendesk-deflection-rate)). The exact share depends on the request type and the quality of the knowledge base, so we measure it on your real requests in a pilot.

**Will the bot replace agents?**
No. It takes off the typical flow and escalates complex and sensitive cases to a human. Bots rarely resolve disputed requests: returns and cancellations about 48%, disputed charges only 17% ([Gartner](https://try.experience.com/customer-service-automation-benchmarks)). Agents stay, but handle only what truly needs a human.

**Where does the bot get its answers?**
From your knowledge base through RAG. Before answering, the system searches the needed fragments in the company's policies and FAQs and builds the answer only on them, by the rule "no data, hand to an agent." This protects against made-up answers and keeps responses within your rules.

**Which engine does the bot run on?**
On GPT/LLM; for Russian projects YandexGPT and GigaChat with data processing in Russia are a fit. More on the engine itself and protection against hallucinations is on the [GPT bot](/uslugi/chat-boty/bot-na-gpt/) page.

**Which channels does the support bot work in?**
On the website and in messengers (Telegram, WhatsApp, VK) with a single dialogue history. Specific channels have their own pages: [website bot](/uslugi/chat-boty/bot-na-sait/) and [Telegram bot](/uslugi/chat-boty/telegram-bot/).

**How does the bot integrate with the helpdesk and CRM?**
The bot opens and updates tickets in the helpdesk, writes to the client card in CRM, and hands the request to a manager with the dialogue history. We close the CRM-loop setup on the [CRM implementation](/uslugi/vnedrenie-crm/) service side.

**How does a support bot differ from an AI agent?**
A support bot runs the first line: it answers and escalates. An AI agent autonomously performs actions in systems: it places, changes, and launches processes. These are different services; the agent belongs to the [AI implementation](/uslugi/vnedrenie-ii/) area.

**How do you build a support bot for a company?**
Assemble the knowledge base from FAQs and policies, map scenarios (what the bot closes itself, what it escalates), connect the model and the helpdesk, and test on real requests. We walk this path for you and show a demo before launch.

**Is the solution compliant with 152-FZ?**
Yes. With Russian models, data is processed in Russia, and we set up the handling of personal data per the law's requirements. The data loop stays under your control.

**How do you tell the bot is working effectively?**
By the deflection rate together with the resolution rate and the re-contact rate, not by a single number. We measure these indicators in the pilot and after launch to see the real effect, not the share of formally "closed" dialogues.

[CTA-final: Send examples of your requests. We will assemble a demo bot and show what share it can close → form]

## Why us

We are an independent integrator and assemble the bot around your request flow, rather than selling a single platform with a subscription. We show a demo on the client's real requests before launch, and honestly map what the bot closes itself and what goes to an agent. Data stays within your loop, and we build 152-FZ requirements into the architecture. You can meet the team on the [about](/o-kompanii/) page and discuss your task through [contacts](/kontakty/).

---
*Word count: ~1550. FAQ: 12. Infographics: 2. Images: 3. Internal links: 9. Em-dash: 0.*
