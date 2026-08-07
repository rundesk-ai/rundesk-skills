# Sources

Verified August 7, 2026. These sources establish the practices in this package; the package
synthesizes them into a provider-neutral assistant workflow.

## Personalized, concise briefs

- The CIA's history of the first President's Daily Summary describes the need to synthesize
  uncoordinated and sometimes contradictory reporting, and its history of the President's Daily
  Brief describes a product tailored to each recipient's preferences: [first daily summary](https://www.cia.gov/legacy/museum/artifact/editors-copy-of-the-first-presidential-daily-summary/)
  and [PDB public-release remarks](https://www.cia.gov/stories/story/brennan-delivers-keynote-at-presidents-daily-brief-public-release-event/).
  These support reconciliation and personalization rather than a generic information dump.
- The UK Office for National Statistics says to put the most important information first, organize
  around top user needs, use scannable headings, and remove repeated or unchanged content between
  editions: [Structuring content](https://service-manual.ons.gov.uk/content/writing-for-users/structuring-content).
  This maps to `Needs you` first, empty-section removal, and delta-only recurring reports.
- ONS's mobile-specific guidance says time-poor online users scan, smaller screens increase
  scrolling, and complex content takes longer to understand on mobile; it recommends brief, plain,
  frontloaded content: [How people read online](https://service-manual.ons.gov.uk/content/writing-for-users/how-people-read-online).
  This maps to the phone-first brief, short bullets, stable headings, and decision summary before
  detail.
- The CDC Clear Communication Index is a research-based assessment tool. Its user guide calls for
  one main message near the beginning, a clear call to action, and audience testing:
  [CC Index user guide](https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf).
  This supports action-first items and adapting the brief from recipient feedback.
- ServiceNow's conversation-design guidance recommends brief, clear, friendly, consistent,
  scannable, and personalized responses: [Guidelines for any conversation](https://horizon.servicenow.com/guidelines/conversation-design/guidelines-for-any-conversation).
  This supports a short greeting and consistent delivery, not a catalog-prescribed persona or
  repeated pleasantries.
- Google's conversation-design guidance says to focus on the user, avoid monologues, keep greetings
  brief, and shorten them for returning users: [Language](https://developers.google.com/assistant/conversation-design/language)
  and [Greetings](https://developers.google.com/assistant/conversation-design/greetings). This
  supports the configurable one-line greeting; no source establishes a universal gap duration.

## Attention and status

- Shamsi Iqbal and Eric Horvitz observed 27 computer users for two weeks and interviewed 14 of them.
  Alert-triggered task switches consumed nearly ten minutes on average, followed by another 10–15
  minutes before focused work resumed: [Disruption and Recovery of Computing Tasks](https://www.erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf),
  CHI 2007. The small naturalistic study does not establish a universal cadence; it supports a high
  threshold for interruption and batching routine checks.
- Google's Site Reliability Engineering chapter separates page-worthy interruptions, important
  subcritical work routed to a queue, and informational records, while emphasizing alert-noise
  reduction: [Practical alerting](https://sre.google/sre-book/practical-alerting/). The catalog
  applies that operational attention model by inference to `interrupt → brief → track → omit`; the
  source is not an executive-assistant specification.
- GitLab's practitioner guidance for asynchronous updates asks for current progress, next steps,
  blockers, confidence, specificity, concision, and supporting links:
  [Async updates](https://handbook.gitlab.com/handbook/engineering/ai/ai-coding/how-we-work/async-updates/).
  This maps to the status-delta questions and outcome-over-activity examples.
- David Allen Company's published Weekly Review checklist separates calendar review, next actions,
  waiting-fors, projects, and someday/maybe work, and asks that each active project have a current
  next action: [GTD Weekly Review](https://gettingthingsdone.com/wp-content/uploads/2014/10/2016-GTD-Weekly-Review-.pdf).
  This named-practitioner source supports distinct waiting, next, and parked states; the package
  does not mandate GTD or Inbox Zero.

## Inbox behavior and urgency traps

- Shirin Sarrafzadeh and coauthors studied email triage through 15 contextual interviews and a
  91-person survey of daily Outlook users at one US technology company. They found that unhandled
  email acts as task management, deferral is common, and users follow different inbox strategies:
  [Email triage: going beyond labels](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/02/Email_Triage_CHIIR19.pdf),
  CHIIR 2019. The single-company sample and 9.1% survey response limit generalization; it still
  supports adapting to the recipient's system rather than enforcing Inbox Zero.
- Anna Cox and coauthors ran a three-week field experiment with 45 participants receiving 360
  controlled messages each. Urgency cues prompted faster responses regardless of importance or
  effort: [Prioritizing unread e-mails](https://research.birmingham.ac.uk/en/publications/prioritizing-unread-e-mails-people-send-urgent-responses-before-i/),
  *Human–Computer Interaction*, 2021. This supports checking consequence and request instead of
  trusting an `urgent` cue.

## Agent ecosystems

- Hermes Agent's official daily-briefing guide makes recurring jobs self-contained, recommends a
  concise linked report tailored to the person's interests, and explicitly defines categories to
  skip: [Build a daily briefing bot](https://github.com/NousResearch/hermes-agent/blob/a8c50eb1d841563eff22bd707d80472e7f1e9c9f/website/docs/guides/daily-briefing-bot.md).
  This supports a standing brief contract and explicit exclusions. Hermes commands, scheduling,
  model choices, emojis, and news categories are implementation details and are not copied here.
- OpenClaw's official heartbeat guidance says not to infer or repeat old tasks, respects active
  hours and timezone, keeps the recurring checklist small, surfaces only what is due, and permits a
  quiet acknowledgement when nothing needs attention: [Heartbeat](https://docs.openclaw.ai/gateway/heartbeat).
  This supports current-state reconciliation, quiet hours, small stable contracts, and no-news
  behavior. OpenClaw configuration syntax is excluded.
- OpenClaw's memory guidance distinguishes curated durable preferences from raw daily notes,
  supersedes corrected values, and requires action-sensitive memory to retain authority, expiry,
  timing, and source context: [Memory](https://docs.openclaw.ai/concepts/memory). This maps to the
  active preference record and safe handoff contract.
- OpenClaw's current-main commitment guidance records the retirement of conversation-derived
  commitments:
  [commitment retirement at commit 8c68f74](https://github.com/openclaw/openclaw/blob/8c68f74ef914763e846f4b3c2fef8b80ace56f5e/docs/concepts/commitments.md).
  This supports explicit, sourced open items instead of inferring obligations from casual
  conversation; it does not prescribe a storage mechanism.
- Community assistant packages reinforce the same operational traps: Hermes Chief of Staff reads a
  canonical state before reporting and creates explicit follow-ups for external dependencies
  ([task manager](https://github.com/TheCraigHewitt/hermes-chief-of-staff/blob/ac280028d09d44d9255ce969e86c95a23253820e/skills/daily-task-manager/SKILL.md)),
  while OpenClaw's Daily Briefing Hub collapses related items and omits empty sections
  ([community listing](https://clawhub.ai/ariktulcha/skills/daily-briefing-hub)). These are community
  practice, not independent empirical validation; the Hermes package identifies an OpenClaw lineage.
- OpenClaw's maintained `gog` inbox workflow says to inspect likely-actionable full threads, classify
  by requested action and consequence, and never infer urgency from sender alone:
  [inbox triage at commit 8fe3e79](https://github.com/openclaw/gogcli/blob/8fe3e7995d0b6a7df769f24b48fa69c88a8b7330/.agents/skills/gog-inbox-triage/SKILL.md).
  This directly supports treating sender seniority as context rather than a sufficient priority
  signal.
- A current ClawHub daily-briefing example places shipment and payment confirmations under email
  needing attention: [Daily Briefing v1.0.5](https://clawhub.ai/antgly/skills/daily-briefing).
  The inbox good/bad pair minimizes that reproduced community failure and replaces it with the
  action-oriented `gog` workflow. The listing is community evidence, not an endorsement.
- Hermes' official Google Workspace guidance requires confirmation for consequential mutations and
  its email guidance records a case where SMTP succeeded before a later failure, making a blind
  retry send a duplicate: [mutation policy](https://github.com/NousResearch/hermes-agent/blob/a8c50eb1d841563eff22bd707d80472e7f1e9c9f/skills/productivity/google-workspace/SKILL.md)
  and [duplicate-send trap](https://github.com/NousResearch/hermes-agent/blob/a8c50eb1d841563eff22bd707d80472e7f1e9c9f/skills/email/himalaya/SKILL.md).
  These support explicit authority and verify-before-retry, not Hermes-specific commands.

## Safety and authority

- OWASP documents indirect prompt injection through webpages, documents, email, and attachments;
  it recommends separating instructions from external data, least privilege, output monitoring,
  and human approval for high-impact actions:
  [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
  This supports the data-lane rule and action approval boundary.
- OpenClaw's security guidance says prompt injection is not solved by prompting alone and identifies
  email, attachments, web content, and shared documents as untrusted inputs:
  [Gateway security](https://docs.openclaw.ai/gateway/security). Its threat model likewise treats
  external integrations as a trust boundary:
  [Threat model](https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS). These support minimizing
  privileges and refusing content-borne instructions.
- RFC 5545 defines tentative, confirmed, and cancelled event states, timezone components,
  recurrence instances, and revision sequences: [iCalendar](https://www.rfc-editor.org/rfc/rfc5545.html).
  This maps to calendar-state and timezone verification; it does not establish meeting etiquette.
- NIST's Privacy Framework covers authorization, revocation, processing preferences, data
  minimization, selective disclosure, provenance, and audit records:
  [Privacy Framework 1.0](https://www.nist.gov/system/files/documents/2020/01/16/NIST%20Privacy%20Framework_V1.0.pdf).
  This supports opt-in personal dates, channel-aware detail, and granular authority. It does not
  mandate a particular assistant interface.

## Example mapping

- The action-first core and daily-brief structures directly minimize the CDC and ONS main-message,
  call-to-action, and inverted-pyramid practices; placeholders prevent invented facts while showing
  decisions, consequences, due times, and source links instead of unread-count narration.
- The coverage-gap, meeting, and weekly shapes apply ONS mobile/frontloading guidance, GitLab's
  outcome/next-step/blocker/source pattern, RFC 5545 event-state checks, and the CIA's recipient-
  tailored selection. They are information structures, not prescribed wording or tone.
- The waiting-on examples apply the GTD separation of next actions and waiting-fors plus GitLab's
  owner, next-step, blocker, and linked-evidence guidance.
- The urgent-email examples apply Cox et al.'s reproduced urgency-bias finding and Sarrafzadeh et
  al.'s evidence that triage is task management rather than unread-count reduction.
