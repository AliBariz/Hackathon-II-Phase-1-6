# frontend/CLAUDE.md - Next.js Frontend for Todo Application

## Overview
This is the frontend for the full-stack todo application built with Next.js 16+ using the App Router. It handles user authentication via Better Auth and provides a UI for task management with features like search, filter, and sort.

## Tech Stack
- Framework: Next.js 16+ (App Router)
- Language: TypeScript/JavaScript
- Styling: Tailwind CSS
- Authentication: Better Auth with JWT tokens
- API Client: Axios (for centralized API calls with JWT handling)

## File Structure
- `pages/` - Main application pages (login, dashboard, etc.)
- `components/` - Reusable UI components (TaskList, TaskForm, etc.)
- `lib/` - Utility functions and API client
- `public/` - Static assets
- `styles/` - Global styles

## Development Guidelines
- All API calls must include JWT tokens in the Authorization header
- Use centralized API client from lib/api.ts for all backend communications
- Components should be reusable and follow Next.js best practices
- Implement responsive design for different device sizes
- Handle JWT token expiration gracefully (redirect to login)

## Authentication Flow
1. User registers/logs in via Better Auth
2. JWT token is stored securely
3. Token is attached to all API requests automatically
4. Expired tokens trigger redirect to login page

## API Integration
- All API calls should go through the centralized API client
- Include proper error handling for different HTTP status codes
- Implement loading states for better UX
- Ensure proper data validation before sending to backend