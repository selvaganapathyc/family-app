-- =============================================================================
-- Seed: family_members.sql
-- How to create the 4 family members and insert their profiles.
-- =============================================================================
--
-- STEP 1: Create users in Supabase Auth
-- ------------------------------------
-- Go to your Supabase project dashboard:
--   Authentication > Users > "Add user" (Invite user or create manually)
--
-- Create the following 4 users:
--
--   Name   | Email                    | Role
--   --------+--------------------------+--------
--   Selva   | selva@yourdomain.com     | parent
--   Udhaya  | udhaya@yourdomain.com    | parent
--   Kayal   | kayal@yourdomain.com     | child
--   Kathir  | kathir@yourdomain.com    | child
--
-- After creating, go to Authentication > Users to get each user's UUID.
--
-- STEP 2: Insert family member profiles
-- --------------------------------------
-- Replace each <...-uuid> placeholder with the actual UUID from Supabase Auth.
-- Run this SQL in the Supabase SQL Editor.

INSERT INTO public.family_members (user_id, name, role, email)
VALUES
    -- Selva (parent) - replace UUID
    (
        '<selva-auth-uuid>',
        'Selva',
        'parent',
        'selva@yourdomain.com'
    ),
    -- Udhaya (parent/wife) - replace UUID
    (
        '<udhaya-auth-uuid>',
        'Udhaya',
        'parent',
        'udhaya@yourdomain.com'
    ),
    -- Kayal (child/daughter) - replace UUID
    (
        '<kayal-auth-uuid>',
        'Kayal',
        'child',
        'kayal@yourdomain.com'
    ),
    -- Kathir (child/son) - replace UUID
    (
        '<kathir-auth-uuid>',
        'Kathir',
        'child',
        'kathir@yourdomain.com'
    )
ON CONFLICT (id) DO NOTHING;

-- =============================================================================
-- STEP 3: Set passwords
-- ---------------------
-- In Supabase dashboard: Authentication > Users > click each user > "Send password reset"
-- Or set temporary passwords directly via the Supabase dashboard user management UI.
--
-- STEP 4: Verify
-- --------------
-- SELECT * FROM public.family_members;
--
-- You should see 4 rows, one for each family member.
-- =============================================================================
