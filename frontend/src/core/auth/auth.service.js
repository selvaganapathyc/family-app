import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.error(
    'Missing Supabase environment variables. Check VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.',
  )
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

/**
 * Sign in with email and password.
 * Returns { data, error }
 */
export async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })
  return { data, error }
}

/**
 * Sign out the current user.
 * Returns { error }
 */
export async function signOut() {
  const { error } = await supabase.auth.signOut()
  return { error }
}

/**
 * Get the current session.
 * Returns { data: { session }, error }
 */
export async function getSession() {
  const { data, error } = await supabase.auth.getSession()
  return { data, error }
}

/**
 * Subscribe to auth state changes.
 * callback receives (event, session)
 * Returns the subscription object (call .unsubscribe() to clean up)
 */
export function onAuthStateChange(callback) {
  const { data: subscription } = supabase.auth.onAuthStateChange(
    (event, session) => {
      callback(event, session)
    },
  )
  return subscription
}
