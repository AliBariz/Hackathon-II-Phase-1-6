import { createAuthClient } from "better-auth/client";

// Initialize Better Auth client
export const { useSession, signIn, signOut } = createAuth({
  basePath: "/api/auth",
});
