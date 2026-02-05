// This is a Next.js API route for Better Auth
import { authHandler } from '@better-auth/next-js';

// Configure Better Auth handler
export default authHandler({
  basePath: '/api/auth',
  // Configuration options will be set up in the backend
});