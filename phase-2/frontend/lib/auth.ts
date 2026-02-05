import { createAuthClient } from '@better-auth/client';

// Initialize Better Auth client
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000/api/auth',
  // JWT plugin configuration will be enabled
});

// Export auth functions
export const { signIn, signOut, getSession } = authClient;