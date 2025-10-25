# Future Planning - v2.5 & v3.0

**Last Updated:** October 25, 2025
**Status:** Strategic planning for post-v2.0 development

---

## Strategic Direction

**v2.0 Focus (Current):** Portfolio-first, generic multi-user document management SaaS
**v2.5+ Focus (Future):** Potential pivot to architecture vertical OR open source + managed hosting

**Key Insight:** v2.0 provides technical foundation that supports BOTH paths. Decision on which direction will be made after:
1. v2.0 ships and demonstrates technical capability (portfolio value)
2. Market validation with architecture firms (10+ conversations)
3. Analysis of open source vs vertical tradeoffs

---

## Path A: Architecture Vertical (v2.5 → v3.0)

### Market Opportunity

**Target Market:** Small to medium architecture firms (5-50 people) in Australia

**Market Size:**
- ~5,000 architecture firms in Australia
- ~2,000 firms with 5-20 employees (sweet spot)
- Target: 1% market penetration = 20-50 paying customers
- Revenue potential: $50K-200K ARR

**Core Problem Identified (10 Years Domain Experience):**
- Documents siloed in email (RFIs, specs, consultant responses)
- Folder-based storage (no relationships, can't query across projects)
- Tribal knowledge (only senior staff know where things are)
- Manual data entry rejected (Notion/database attempts failed due to friction)
- Compliance requirements (councils need audit trails, documentation evidence)

**Why They Don't Use Existing Tools:**
- ❌ Notion/Airtable: Too much manual data entry, doesn't fit workflow
- ❌ ArchiOffice/Workflowmax: Practice management but poor document intelligence
- ❌ Folders + Email: "Good enough" but massive time waste

**The Unique Value Proposition:**
> "Drop your project documents (emails, RFIs, specs, reports) into Vectory. We automatically extract Projects, Consultants, RFIs, and Clients into a searchable database - no manual data entry. Query across all projects instantly."

### v2.5: Architecture-Specific Features (Months 4-6 Post-v2.0)

**Priority 1: RFI Intelligence**
- Auto-detect RFI documents from uploaded PDFs/emails
- Extract: RFI number, consultant, discipline, item description, due date, status
- Track RFI threads (original request → consultant response → resolution)
- Generate RFI status reports (open items by consultant, overdue items)

**Priority 2: Project Organization**
- Auto-detect project name/address from documents
- Group all documents by project automatically
- Project dashboard: documents, consultants involved, RFI status, timeline
- Fast project handover (new PM can search entire project history)

**Priority 3: Consultant Tracking**
- Extract consultant names and disciplines from documents
- Build consultant directory (who said what, when, on which projects)
- Track consultant performance (response times, open items)
- Generate consultant coordination reports

**Priority 4: Basic Reporting**
- "Show all open RFIs across all projects"
- "What did the hydraulic consultant say about fire rating?"
- "List all structural items from Smith Engineering"
- "Generate compliance evidence for council submission"

**Technical Implementation:**
- Build on v2.0 Docling extraction (already handles PDFs, DOCX)
- Add RFI-specific prompt templates for GPT-4o-mini metadata generation
- Create architecture-specific Supabase tables: `projects`, `consultants`, `rfi_items`
- Custom UI components: RFI dashboard, consultant directory, project overview

**Success Metrics:**
- 3-5 beta architecture firms using the product
- Measurable time savings (track: hours/week finding documents, compiling reports)
- User testimonials ("saves 10 hours/week on RFI tracking")
- Willingness to pay validation ($99-299/month confirmed)

### v3.0: StackDocs Schema Intelligence (Months 7-12)

**Core Innovation: Automatic Schema Discovery**

**How It Works:**
1. **Initial uploads (Weeks 1-4):**
   - Firm uploads 100+ documents (emails, RFIs, specs, reports, drawings)
   - System extracts entities using AI (projects, consultants, items, dates)
   - Stores everything in flexible JSONB initially

2. **Pattern recognition (Weeks 4-8):**
   - PageRank-style importance scoring across all extracted entities
   - "Smith Engineering" appears in 15 documents → High importance
   - "RFI" structure appears 50+ times → Common pattern
   - "Fire rating" mentioned across 12 projects → Important concept

3. **Automatic schema evolution (Week 8+):**
   - System proposes structured tables:
     - `projects` (name, address, client, start_date, status)
     - `consultants` (name, discipline, contact, projects_count)
     - `rfi_items` (project, consultant, item, due_date, status, category)
     - `compliance_items` (project, requirement, status, evidence_document)
   - Migrates historical data from JSONB to structured tables
   - Enables relational queries across all projects

4. **Continuous learning:**
   - New document types → New entity patterns
   - System adapts to firm's specific workflow
   - Field name consolidation ("property_address" ≈ "project_address")

**Key Features:**

**Entity Relationship Mapping:**
- Automatically connect consultants across projects
- Track which consultants work together frequently
- Identify project patterns (type, size, consultant combinations)

**Advanced Querying:**
- Natural language: "Show all fire rating issues from last 3 months"
- Relational: "Which consultants have open items on projects with heritage overlays?"
- Cross-project: "Find all documents mentioning BCA Part J requirements"

**Compliance Intelligence:**
- Auto-detect compliance requirements from specifications
- Track evidence documents against requirements
- Generate audit trails for council submissions
- Alert on missing documentation

**Predictive Insights:**
- "Consultant X typically responds to RFIs in 5 days" (based on history)
- "Projects of this type usually require these consultants" (pattern recognition)
- "This RFI category often leads to variations" (risk flagging)

**Technical Implementation:**
- PageRank algorithm for entity importance scoring (using NetworkX or custom implementation)
- Entity resolution (detect "Smith Engineering" = "Smith Eng." = "Smith & Associates")
- Automatic database migration system (JSONB → structured tables)
- Field frequency analysis from StackDocs spike learnings
- Schema normalization agent (consolidate duplicate field names)

**Differentiation from Generic RAG:**
- Not just "chat with documents" (ChatGPT already does this)
- **Automatic database creation** from unstructured documents
- Eliminates manual data entry (the reason Notion failed)
- Builds institutional knowledge automatically

### Pricing Model (Architecture Vertical)

```
Solo Practice ($99/month or $999/year):
- 1 user
- 5 active projects
- 500 documents
- Auto-extraction + search + basic reporting
- Email support

Small Firm ($299/month or $2,999/year):
- Up to 10 users
- Unlimited projects
- 5,000 documents
- Everything in Solo, plus:
  - RFI tracking + status reports
  - Consultant directory
  - Chat with documents (RAG)
  - Priority support

Studio ($599/month or $5,999/year):
- Up to 25 users
- Unlimited documents
- Everything in Small Firm, plus:
  - StackDocs schema intelligence
  - Compliance tracking
  - Custom fields
  - API access
  - Onboarding + training
  - Dedicated support

Enterprise (Custom pricing: $10K-30K/year):
- 25+ users
- On-prem deployment option
- Custom integrations (Outlook, Dropbox, ArchiOffice)
- White-label
- Annual contract
- Dedicated account manager
```

**ROI Justification:**
- Small firm saves 10-15 hours/week finding documents, tracking RFIs
- At $200/hour billing rate: **$2,000-3,000/week saved**
- Monthly cost: $299
- **ROI: 6.7x-10x** (no-brainer for firms billing $150-300/hour)

### Go-to-Market Strategy

**Phase 1: Network Validation (Months 1-3 during v2.0 build)**
- Leverage 10 years of architecture contacts
- Coffee meetings with 10-20 firm principals/PMs
- Show mockups/early prototype of v2.0
- Key questions:
  - "How do you currently manage RFIs?"
  - "Would auto-extraction from emails save you time?"
  - "What would you pay for this?"
  - "What features are missing?"

**Phase 2: Beta Testing (Months 4-6, v2.5 build)**
- Recruit 3-5 beta firms from validation phase
- Offer free 3-month trial
- White-glove onboarding (screen share, manual setup)
- Weekly check-ins to gather feedback
- Measure time savings (before/after surveys)
- Capture testimonials and case studies

**Phase 3: Paid Launch (Months 7-9)**
- Convert beta firms to paid (offer 50% discount for first year)
- Referral program (existing customers refer new firms, get 1 month free)
- LinkedIn content marketing (architecture groups are active)
- Case studies: "How [Firm X] saved 15 hours/week on RFI tracking"

**Phase 4: Growth (Months 10-24)**
- Content + SEO: "How to manage RFIs", "Architecture document management"
- YouTube: Quick tips for practice management
- Partnerships: Architecture associations, CAD resellers
- Conferences: Architecture/BIM conferences, speaking opportunities
- Goal: 20-40 paying customers, $50K-100K ARR

### Revenue Projections (Architecture Path)

| Timeframe | Customers | MRR | ARR | Notes |
|-----------|-----------|-----|-----|-------|
| Month 6 | 3 beta | $0 | $0 | Free beta testing |
| Month 9 | 8 paid | $1,789 | $21K | 5×$99, 3×$299 |
| Month 12 | 15 paid | $3,582 | $43K | 8×$99, 6×$299, 1×$599 |
| Month 18 | 25 paid | $6,970 | $84K | 10×$99, 12×$299, 3×$599 |
| Month 24 | 40 paid | $11,952 | $143K | 15×$99, 20×$299, 5×$599 |

**Path to $200K ARR:**
- 20 solo practices × $99 = $1,980/month
- 30 small firms × $299 = $8,970/month
- 8 studios × $599 = $4,792/month
- 2 enterprise × $2,083 (annual/12) = $4,166/month
- **Total: $19,908/month = $239K ARR**

### Risks & Challenges

**Market Risks:**
- Conservative industry (slow to adopt new software)
- "Good enough" problem (folders + email barely works but people tolerate it)
- Small market size (~2,000 target firms in AU)
- Recession risk (architecture firms cut software budgets first)

**Execution Risks:**
- Long sales cycles (3-6 months from demo to paid)
- High-touch sales required (not self-serve like consumer SaaS)
- Custom needs per firm (residential vs commercial, small vs large)
- Integration complexity (Outlook, Dropbox, ArchiOffice, AutoCAD, Revit)

**Competition Risks:**
- Practice management software adds document AI features
- Microsoft 365 Copilot improves Outlook/SharePoint search
- Large firms have resources to build custom solutions

**Mitigation Strategies:**
- Start with small firms (5-15 people) - faster decisions, less complexity
- Focus on RFI pain point initially (universal, clearly measurable ROI)
- Charge annually upfront to reduce churn and improve cash flow
- Build integration with most common tools first (Outlook, Gmail, Dropbox)
- Differentiate on schema intelligence (automatic database creation, not just search)

---

## Path B: Open Source + Managed Hosting (Alternative to Architecture Vertical)

### Strategic Rationale

**If architecture vertical validation fails** (low interest, won't pay, long sales cycles), pivot to open source model.

**Why This Works:**
- Proven model (Supabase, PostHog, Cal.com, Plausible)
- Builds community and trust via GitHub stars
- Multiple revenue streams (hobbyists, professionals, enterprises)
- Lower customer acquisition cost (organic GitHub traffic)
- Not vertical-dependent (useful for any knowledge worker)

### Open Source Strategy

**What's Open Source (MIT License):**
- Complete v2.0 codebase (frontend + backend)
- Docker Compose setup for self-hosting
- Documentation for deployment
- Community features (basic auth, stacks, upload, search)

**What's Premium (Closed Source / Paid-Only):**
- Team collaboration features (shared stacks, permissions)
- SSO/SAML integration (enterprise auth)
- Advanced analytics (usage tracking, insights)
- API access with higher rate limits
- White-label / custom branding
- Priority support + SLA

### Pricing Model (Open Source Path)

```
Open Source (Free):
- Self-host on your infrastructure
- Core features (auth, upload, search, basic chat)
- Community support (GitHub Discussions)
- MIT license (modify and distribute freely)

Cloud Starter ($9/month):
- Managed hosting (no DevOps needed)
- Everything in open source
- 5GB storage
- Email support
- Automatic updates

Cloud Pro ($29/month):
- 50GB storage
- Team features (shared stacks, permissions)
- API access
- Advanced search features
- Priority support

Cloud Team ($99/month):
- Unlimited storage
- SSO/SAML
- Custom domain
- Advanced analytics
- Dedicated support

Enterprise (Custom: $10K-50K/year):
- Self-hosted license with support
- White-label branding
- Custom integrations
- SLA + dedicated account manager
- Professional services (setup, training)
```

### Go-to-Market (Open Source Path)

**Launch Strategy:**
1. **GitHub Release** (Month 4 post-v2.0)
   - Clean README with architecture diagram
   - Docker Compose one-command setup
   - Comprehensive documentation
   - Demo video (3 minutes)

2. **Community Building** (Months 4-6)
   - Post to Hacker News (Show HN)
   - Submit to Product Hunt
   - Share in Reddit (r/selfhosted, r/datahoarder, r/opensource)
   - Tweet on Tech Twitter
   - Goal: 500-1,000 GitHub stars

3. **Managed Hosting Launch** (Month 6)
   - Set up Railway/Fly.io infrastructure
   - Stripe integration for payments
   - Launch landing page
   - Convert free users to paid (convenience revenue)

4. **Growth** (Months 7-12)
   - Content marketing (blog posts, tutorials)
   - SEO for "self-hosted document management", "open source RAG"
   - YouTube demos and tutorials
   - Community contributions (features, bug fixes)
   - Goal: 2,000+ stars, 50-100 paying hosted customers

### Revenue Projections (Open Source Path)

| Timeframe | GitHub Stars | Paid Hosted | MRR | ARR | Notes |
|-----------|--------------|-------------|-----|-----|-------|
| Month 6 | 500 | 10 | $190 | $2.3K | 7×$9, 3×$29 |
| Month 9 | 1,000 | 30 | $633 | $7.6K | 15×$9, 10×$29, 5×$99 |
| Month 12 | 2,000 | 75 | $1,728 | $20.7K | 30×$9, 30×$29, 15×$99 |
| Month 18 | 4,000 | 150 | $4,185 | $50.2K | 50×$9, 70×$29, 30×$99 |
| Month 24 | 7,000 | 300 | $9,357 | $112K | 100×$9, 150×$29, 50×$99 |

**Plus enterprise deals** (2-5 per year at $10K-50K each adds $20K-250K ARR)

**Path to $200K ARR:**
- 150 Cloud Starter × $9 = $1,350/month
- 200 Cloud Pro × $29 = $5,800/month
- 80 Cloud Team × $99 = $7,920/month
- 5 Enterprise × $2,083 (annual/12) = $10,415/month
- **Total: $25,485/month = $306K ARR**

### Hybrid Approach: Open Source THEN Architecture Features

**Possible best of both worlds:**
1. **Launch v2.5 as open source** (build community, trust)
2. **Add architecture features as premium plugins** (RFI tracking, compliance)
3. **Charge architecture firms for specialized features** ($299/month)
4. **Keep core open source** (upload, search, basic chat)

This allows:
- Community growth from open source
- Revenue from architecture vertical
- Flexibility to pivot if one path underperforms

---

## Decision Framework

**After v2.0 ships (Month 3), evaluate:**

### Go Architecture Vertical If:
- ✅ 5+ architecture firms express strong interest during validation
- ✅ Firms confirm willingness to pay $99-299/month
- ✅ Clear time savings measurable (10+ hours/week)
- ✅ You're excited to focus on one industry for 12-24 months

### Go Open Source If:
- ✅ Architecture validation is lukewarm (<5 interested firms)
- ✅ Don't want sales-heavy business (prefer self-serve)
- ✅ Prefer community building over vertical focus
- ✅ Want faster path to revenue (many small customers vs few large)

### Hybrid Approach If:
- ✅ Architecture validation is moderate (3-5 interested firms)
- ✅ Want to hedge bets (keep options open)
- ✅ Willing to maintain two GTM strategies simultaneously

---

## Technical Roadmap

### v2.0 Foundation (Months 1-3) - CURRENT FOCUS
✅ Multi-user authentication (Supabase Auth)
✅ Stack-based organization
✅ Multi-format upload (PDF, DOCX, TXT via Docling)
✅ AI metadata generation (GPT-4o-mini)
✅ Semantic search (ChromaDB)
✅ Liquid Glass UI (iOS 26 design)
✅ Freemium tier enforcement
✅ Deployment (Railway/Fly.io)

**Goal: Portfolio-quality SaaS application**

### v2.5 - Architecture Features OR Open Source Prep (Months 4-6)

**If Architecture Path:**
- RFI extraction and tracking
- Project organization
- Consultant directory
- Basic reporting
- Beta testing with 3-5 firms

**If Open Source Path:**
- Clean up codebase for public release
- Comprehensive documentation
- Docker Compose optimization
- GitHub README + demo video
- Launch on HN/PH/Reddit

### v3.0 - Advanced Intelligence OR Growth (Months 7-12)

**If Architecture Path:**
- StackDocs schema intelligence (PageRank, auto-tables)
- Compliance tracking
- Advanced querying (natural language + relational)
- Entity relationship mapping
- Integrations (Outlook, Dropbox)

**If Open Source Path:**
- Team collaboration features (premium)
- SSO/SAML integration (enterprise)
- API with higher limits (pro tier)
- Custom branding (white-label)
- Professional services offering

---

## Success Metrics

### Portfolio Success (v2.0 Goal)
- ✅ Shipped production SaaS application
- ✅ Modern tech stack demonstrated (Supabase, ChromaDB, Docling, Next.js, FastAPI)
- ✅ Complex features implemented (multi-tenancy, RAG, Liquid Glass UI)
- ✅ Professional documentation (ADRs, tasks, development notes)
- ✅ Clean git history (granular commits)
- ✅ Deployed and publicly accessible
- ✅ Demo video for job interviews

### Business Success (v2.5+ Goals)

**Architecture Path:**
- 6 months: 5 paying customers, $1.5K MRR
- 12 months: 15 paying customers, $3.5K MRR ($42K ARR)
- 24 months: 40 paying customers, $12K MRR ($144K ARR)

**Open Source Path:**
- 6 months: 1,000 GitHub stars, 10 paid hosted users, $200 MRR
- 12 months: 2,000 stars, 75 paid users, $1.7K MRR ($20K ARR)
- 24 months: 7,000 stars, 300 paid users, $9K MRR ($108K ARR)

---

## Key Takeaways

1. **v2.0 is foundation for BOTH paths** - build it well, decide direction later
2. **Architecture vertical has higher revenue potential** ($200K ARR from 40 customers)
3. **Open source has lower risk, proven model** (Supabase validates this works)
4. **Validate before building v2.5** - talk to 10+ architecture firms during v2.0 development
5. **Don't need to choose now** - focus on shipping excellent v2.0 first
6. **Hybrid is possible** - open source core + premium architecture features
7. **Domain expertise is valuable** - 10 years in architecture creates unfair advantage

---

## Next Actions

**During v2.0 Development (Months 1-3):**
1. Build v2.0 as planned (generic, portfolio-first)
2. Conduct 10-20 validation conversations with architecture firms
3. Create mockups of RFI tracking features for validation
4. Document feedback and willingness-to-pay signals
5. Prototype simple RFI extraction to test technical feasibility

**Post-v2.0 (Month 4):**
1. Review validation findings
2. Decide: Architecture vertical OR open source OR hybrid
3. Update this document with chosen path
4. Begin v2.5 development

**Always Remember:**
- v2.0 portfolio value is real regardless of monetization path
- Technical skills gained building v2.0 are valuable for career
- Optionality is preserved - can pivot based on market feedback
- Shipping beats planning - focus on execution first

---

**This document will be updated as validation proceeds and decisions are made.**
