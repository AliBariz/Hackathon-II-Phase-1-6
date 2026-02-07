# Research: User Authentication with JWT Implementation

## Decision: Better Auth Integration with JWT
**Rationale**: Better Auth is the mandated authentication provider according to the constitution. It can be configured to issue JWT tokens that can be shared between Next.js frontend and FastAPI backend, enabling proper user isolation.

**Alternatives considered**:
- Traditional session-based authentication (rejected - doesn't meet constitution requirement for JWT tokens between frontend and backend)
- Custom JWT implementation (rejected - Better Auth provides secure, tested solution)
- Third-party providers like Auth0 (rejected - constitution mandates Better Auth)

## Decision: FastAPI JWT Middleware
**Rationale**: FastAPI has excellent support for JWT verification middleware that can decode and validate tokens, extract user identity, and enforce user ownership rules.

**Alternatives considered**:
- Manual token validation in each endpoint (rejected - creates security vulnerabilities and code duplication)
- Python-Jose library (selected - provides secure JWT handling)
- Authlib (rejected - more complex than needed for basic JWT validation)

## Decision: SQLModel for Database Models
**Rationale**: Constitution mandates SQLModel as the ORM. It provides Pydantic-compatible models with SQLAlchemy under the hood, perfect for FastAPI integration.

**Alternatives considered**:
- SQLAlchemy Core (rejected - lacks Pydantic integration needed for FastAPI)
- Tortoise ORM (rejected - constitution mandates SQLModel)
- Peewee (rejected - not compatible with async FastAPI setup)

## Decision: Neon PostgreSQL Database Integration
**Rationale**: Constitution mandates Neon Serverless PostgreSQL. It provides serverless scaling and is fully compatible with SQLModel.

**Alternatives considered**:
- SQLite (rejected - constitution mandates Neon PostgreSQL)
- MongoDB (rejected - constitution mandates PostgreSQL)
- MySQL (rejected - constitution mandates PostgreSQL)

## Decision: Next.js App Router with Better Auth
**Rationale**: Constitution mandates Next.js 16+ with App Router. Better Auth integrates seamlessly with Next.js App Router for authentication flows.

**Alternatives considered**:
- Page Router (rejected - constitution mandates App Router)
- Custom authentication solution (rejected - constitution mandates Better Auth)
- Other frameworks like React + Vite (rejected - constitution mandates Next.js)

## Decision: Centralized API Client for JWT Handling
**Rationale**: A centralized API client on the frontend will automatically attach JWT tokens to requests, ensuring consistent authentication across all API calls.

**Alternatives considered**:
- Manual token attachment in each request (rejected - error-prone and inconsistent)
- Axios interceptors (selected - provides clean token management)
- Fetch wrapper (rejected - less feature-rich than Axios)

## Decision: Task Filtering, Search, and Sorting Implementation
**Rationale**: Backend implementation of filtering, search, and sorting ensures user isolation (users can only search/filter their own tasks) and reduces frontend complexity.

**Alternatives considered**:
- Frontend-only filtering (rejected - violates user isolation requirement)
- Client-side search (rejected - security concern, performance issues)
- Hybrid approach (rejected - adds unnecessary complexity)