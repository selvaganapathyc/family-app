-- =============================================================================
-- Migration: finance/001_transactions.sql
-- Creates the transactions table for the Finance module.
-- Run this in the Supabase SQL Editor after the core migrations.
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.transactions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    date        DATE NOT NULL,
    description TEXT NOT NULL,
    amount      NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    type        TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    category    TEXT NOT NULL,
    member_name TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_transactions_user_id   ON public.transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date      ON public.transactions(date DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_type      ON public.transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON public.transactions(user_id, date DESC);

-- Enable Row Level Security
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;

-- Policy: users can only read their own transactions
CREATE POLICY "Users can view own transactions"
    ON public.transactions
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: users can insert their own transactions
CREATE POLICY "Users can insert own transactions"
    ON public.transactions
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: users can update their own transactions
CREATE POLICY "Users can update own transactions"
    ON public.transactions
    FOR UPDATE
    USING (auth.uid() = user_id);

-- Policy: users can delete their own transactions
CREATE POLICY "Users can delete own transactions"
    ON public.transactions
    FOR DELETE
    USING (auth.uid() = user_id);

-- NOTE: The backend uses the service role key (bypasses RLS), so RLS is
-- enforced as a safety net for direct DB access or Supabase client calls.
