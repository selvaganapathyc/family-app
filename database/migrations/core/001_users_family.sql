-- =============================================================================
-- Migration: 001_users_family.sql
-- Creates the family_members table for tracking the family profiles.
-- Run this in the Supabase SQL Editor.
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.family_members (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('parent', 'child')),
    email       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for fast lookups by user_id
CREATE INDEX IF NOT EXISTS idx_family_members_user_id ON public.family_members(user_id);

-- Enable Row Level Security
ALTER TABLE public.family_members ENABLE ROW LEVEL SECURITY;

-- Policy: each authenticated user can only see their own family member record
CREATE POLICY "Users can view own family member record"
    ON public.family_members
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own family member record"
    ON public.family_members
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own family member record"
    ON public.family_members
    FOR UPDATE
    USING (auth.uid() = user_id);

-- =============================================================================
-- SEED INSTRUCTIONS
-- After creating the 4 family users via Supabase Auth dashboard, run:
--
-- INSERT INTO public.family_members (user_id, name, role, email) VALUES
--   ('<selva-auth-uuid>',  'Selva',  'parent', 'selva@example.com'),
--   ('<udhaya-auth-uuid>', 'Udhaya', 'parent', 'udhaya@example.com'),
--   ('<kayal-auth-uuid>',  'Kayal',  'child',  'kayal@example.com'),
--   ('<kathir-auth-uuid>', 'Kathir', 'child',  'kathir@example.com');
--
-- Replace <...-auth-uuid> with the actual UUIDs from the Supabase Auth users table.
-- =============================================================================
