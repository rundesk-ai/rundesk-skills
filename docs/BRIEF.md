# Brief — rundesk-skills

*What this catalog is and why it exists. One screen, and it changes when the catalog does.*

## Story

`rundesk-skills` is the general-purpose guidance catalog Rundesk installs by default. Its packages
teach an agent repeatable judgment — how to name things, write a plan, hold a brief, work as an
assistant, evaluate performance, and create reusable design or document assets — the decisions any
capable agent has to make regardless of stack or domain.

It is guidance only. Nothing here runs a command, calls a service, or holds a credential.

## Why it exists

An agent arrives able to reason but not knowing how this owner wants work done. Without a shared
catalog, every project restates the same method in its own instruction file, each copy drifts, and no
two agents work the same way twice.

This catalog is the one place a general method is written down, so a change to it reaches every agent
that holds the skill rather than the one repository somebody remembered to update.

## Users

- Rundesk agents on any install, since this catalog is installed by default.
- The owner and contributors deciding which method an agent should follow, and changing it in one
  place.

*Sourced from the readme and the package contract. Who else depends on this catalog outside this
owner's installs is not recorded here.*

## Scope

- **Covers:** general method — planning, naming, performance, design assets, ecommerce storefronts,
  Stripe payment architecture, assistant work, task briefs, and PDF creation.
- **Refuses:**
  - Executables, service adapters, credentials, network calls, and `rundesk.json` declarations. Those
    belong in a guarded integration catalog.
  - Domain guidance a specialist catalog owns — marketing lives in the marketing team catalog,
    software delivery in the development team catalog, game work in the gamedev catalog, and service
    integrations in theirs.
  - Product-owned operating skills, which ship with Rundesk itself.
  - Restating another package's manual. A skill routes to the owner rather than copying it.

## External systems

- Rundesk — installs this catalog and grants its packages to named agents.
- GitHub — hosts the repository and serves the release a catalog install fetches.
