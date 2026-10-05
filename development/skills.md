# Agent Skills

This document describes the OpenCode agent skills used in the R.I.S.A.R.M.S. ecosystem.

## Global Skills

### discover-skills

**Location**: `~/.config/opencode/skills/discover-skills/SKILL.md`

**Purpose**: Discover, evaluate, recommend, and install relevant Agent Skills from the skills.sh ecosystem and other sources.

**Activation**: Triggers when user asks to find, evaluate, recommend, or install external skills (e.g., "Find skills for this project", "Search skills.sh for a testing skill", "What skills should I install?").

**Workflow**:
1. **Understand task** - Analyze intent, domain, scope, authorization
2. **Inspect project** - Detect languages, frameworks, package managers, testing, databases, APIs, DevOps, existing skills
3. **Check existing skills** - Scan all 6 OpenCode skill locations to avoid duplicates
4. **Search skills.sh** - Use CLI (`npx skills find`), optional API (with `SKILLS_SH_API_TOKEN`), or web search fallback
5. **Evaluate candidates** - Score on relevance, focus, documentation, maintenance, reputation, adoption, security, compatibility, overlap
6. **Security audit** - Multi-layer: GitHub repo check, skills.sh download endpoint, heuristic pattern scanning, local trust cache
7. **Classify** - INSTALL / CONSIDER / SKIP
8. **Install** - Via `npx skills add <owner/repo@skill> -g -y` with user authorization
9. **Verify** - Confirm directory, SKILL.md, frontmatter, OpenCode discovery, no duplicates

**Key Features**:
- Project-aware inspection (30+ file patterns across 14 categories)
- Security-first: treats third-party skills as untrusted until audited
- Bloat-resistant: install/consider/skip classification
- Verified installations with post-install checks
- User-controlled: no auto-install without explicit authorization
- Optional skills.sh API auth via `SKILLS_SH_API_TOKEN` environment variable
- Source code auditing when available (GitHub public repos, skills.sh download endpoint)
- Local trust cache (`~/.cache/opencode/skills-discovery/trust-cache.json`)

**Skills.sh API Token Setup**:
```bash
# 1. Go to https://skills.sh, sign in with Vercel
# 2. Settings → API Tokens → Generate new token
# 3. export SKILLS_SH_API_TOKEN="your-token"
# 4. Add to shell profile for persistence
```

**Reference Search Queries**:
| Technology | Example Queries |
|------------|-----------------|
| React | `react best practices`, `react testing`, `nextjs` |
| TypeScript | `typescript`, `type safety`, `tsconfig` |
| Python | `python`, `fastapi`, `django`, `pytest`, `pydantic` |
| Playwright | `playwright`, `e2e testing`, `browser automation` |
| Testing | `jest`, `vitest`, `testing`, `unit testing` |
| Security | `security audit`, `vulnerability`, `owasp` |
| GitHub | `github actions`, `pr review`, `code review` |
| FastAPI | `fastapi`, `async api`, `openapi` |
| Database | `database migration`, `orm`, `prisma`, `sqlalchemy` |
| Docker | `docker`, `docker-compose`, `container` |
| Kubernetes | `kubernetes`, `k8s`, `helm` |
| CI/CD | `github actions`, `gitlab ci`, `circleci` |
| Monorepo | `turbo`, `nx`, `pnpm workspace` |
| Linting | `eslint`, `prettier`, `biome`, `ruff` |

## Installed Skills (Global)

| Skill | Source | Purpose |
|-------|--------|---------|
| discover-skills | Local | Skill discovery and management |
| customize-opencode | Built-in | OpenCode configuration editing |
| code-review | mattpocock/skills | Two-axis code review (standards + spec) |

## Project-Local Skills

Project-local skills live in `.opencode/skills/` within each R.I.S.A.R.M.S. subsystem repository and are managed per-project.

## Adding New Skills

To add a skill globally:
```bash
npx skills add <owner>/<repo>@<skill-name> -g -y
```

To add a skill to a project:
```bash
npx skills add <owner>/<repo>@<skill-name>
```

## Skill Development

When creating new skills for the ecosystem:
1. Create skill directory: `~/.config/opencode/skills/<skill-id>/`
2. Write `SKILL.md` with valid YAML frontmatter (`name`, `description`)
3. Test with `opencode --pure run "What skills are available?"`
4. Verify activation triggers work correctly
5. Document in this file

## Security Guidelines

- Always audit third-party skills before installation
- Check for: credential access, secret harvesting, suspicious network requests, destructive commands, prompt injection
- Prefer skills from reputable maintainers (vercel-labs, anthropics, microsoft, etc.)
- Verify install count > 1K as a signal (not proof) of quality
- Reject skills with private repos that cannot be audited
- Use trust cache to avoid re-auditing known skills

## Limitations

- Skills.sh API requires Vercel OIDC authentication (optional, CLI fallback available)
- Cannot fully audit skills without exposed source code
- Project inspection limited to readable workspace files
- Cannot verify runtime behavior, only static analysis
- Trust cache is local per-machine