/**
 * Auth abstraction layer.
 * Reads VITE_AUTH_PROVIDER from env and loads the matching provider.
 * All other code imports from here — never from a provider directly.
 *
 * To switch providers: change VITE_AUTH_PROVIDER in your .env file.
 * Supported values: "supabase" (default)
 */

const provider = import.meta.env.VITE_AUTH_PROVIDER || 'supabase'

const providers = {
  supabase: () => import('./providers/supabase.provider.js'),
  backend:  () => import('./providers/backend.provider.js'),
  // clerk:  () => import('./providers/clerk.provider.js'),
}

if (!providers[provider]) {
  throw new Error(`Unknown auth provider: "${provider}". Check VITE_AUTH_PROVIDER in your .env file.`)
}

const authProvider = await providers[provider]().then((m) => m.default)

export const { signIn, signOut, getSession, onAuthStateChange, getAccessToken } = authProvider
export default authProvider
