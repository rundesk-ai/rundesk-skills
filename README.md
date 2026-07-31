# Rundesk Development Skills

Curated, guidance-only development skills for Rundesk agents. The catalog contains complete
Agent Skills packages and no service integration commands or credentials.

Install the repository into Rundesk's machine-wide skill library:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-skills-dev
```

Installation makes every declared skill available but grants none automatically. Grant only
the skills an agent needs:

```sh
rundesk skills grant <agent> python-patterns
```
