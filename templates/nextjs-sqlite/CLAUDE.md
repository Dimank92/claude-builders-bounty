# CLAUDE.md — Next.js 15 + SQLite (Turso / Drizzle) SaaS Standards

> Production guidelines, strict architectural conventions, and database workflows for Next.js 15 App Router with SQLite.

---

## ⚡ Essential Commands

```bash
# Development & Build
pnpm dev              # Start dev server with Turbopack (http://localhost:3000)
pnpm build            # Build production bundle (strict typechecking enforced)
pnpm lint             # Run ESLint + Prettier check

# Database & Migrations (Drizzle ORM + SQLite/Turso)
pnpm db:generate      # Generate SQL migration files from schema in src/db/schema.ts
pnpm db:migrate       # Apply pending migrations to the local/remote SQLite database
pnpm db:push          # Push schema changes directly during rapid local prototyping
pnpm db:studio        # Open Drizzle Studio web GUI on http://local.drizzle.studio

# Testing
pnpm test             # Run Vitest unit & integration tests
pnpm test:e2e         # Run Playwright end-to-end tests
```

---

## 🏛️ Project Architecture & Layout

```
├── src/
│   ├── app/                      # Next.js 15 App Router
│   │   ├── (auth)/               # Route group for login/signup/reset
│   │   ├── (dashboard)/          # Authenticated app layout & views
│   │   ├── api/                  # Webhook & external API routes only
│   │   ├── layout.tsx            # Global HTML & providers
│   │   └── page.tsx              # Landing page
│   ├── components/               # React components
│   │   ├── ui/                   # Primitive design tokens (shadcn/radix)
│   │   └── shared/               # Domain-specific reusable components
│   ├── db/                       # Database layer
│   │   ├── schema.ts             # Drizzle SQLite tables & relations
│   │   ├── migrations/           # Generated SQL migration files (NEVER edit manually)
│   │   └── index.ts              # SQLite client connection singleton
│   ├── lib/                      # Utilities & singletons (auth, stripe, email)
│   └── actions/                  # Next.js 15 Server Actions (form submissions, mutations)
```

---

## 🔒 Database & SQLite Rules

1. **Foreign Keys:** SQLite does not enforce foreign keys by default. Always ensure `PRAGMA foreign_keys = ON;` is executed on connection initialization.
2. **Dates & Timestamps:** Store all dates as integer UNIX epochs in milliseconds (`integer('created_at', { mode: 'timestamp_ms' })`) to avoid timezone parsing anomalies.
3. **Prepared Statements:** NEVER concatenate variables into raw SQL. Always use Drizzle query builders or parameterized statements (`sql` tag).
4. **Migration Discipline:**
   - Production migrations must always be applied via `pnpm db:migrate`.
   - Never run `db:push` in production environments.

---

## 🧩 Architectural Patterns to Follow

- **Server-First by Default:** Keep components as React Server Components (RSC) unless interactivity (`useState`, `useEffect`, `onClick`) is explicitly required.
- **Server Actions for Mutations:** Put all write operations in `src/actions/` with `'use server'` and Zod input validation.
- **Optimistic UI:** Pair `useOptimistic` or React Query with Server Actions for instantaneous user feedback.
- **Strict Error Boundaries:** Every route segment should contain `error.tsx` and `loading.tsx`.

---

## 🚫 Anti-Patterns to Avoid

- ❌ **No `useEffect` Data Fetching:** Fetch data directly inside Server Components or Route Handlers.
- ❌ **No Sensitive Secrets in Client Code:** Variables without `NEXT_PUBLIC_` prefix must never leak into client components.
- ❌ **No Unbounded Queries:** Never query SQLite without an explicit `.limit(N)` clause to prevent memory exhaustion.
- ❌ **No Synchronous Disk I/O in Hot Paths:** Avoid blocking `better-sqlite3` calls inside long-running async server handlers.

---

## 📋 Naming Conventions

- **Files:** Kebab-case (`user-profile.tsx`, `auth-guard.ts`).
- **Components:** PascalCase (`UserProfileCard`).
- **Server Actions:** CamelCase with action verbs (`createUserAction`, `updateSubscriptionAction`).
- **Database Tables:** Snake_case plural (`users`, `subscriptions`, `audit_logs`).
