import { createAuth } from "@better-auth/react";

// Initialize Better Auth client
export const { useSession, signIn, signOut } = createAuth({
  basePath: "/api/auth",
});