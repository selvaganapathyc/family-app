-- =============================================================================
-- Migration: finance/002_budgets.sql
-- Creates the budgets table for the Finance module.
-- Run this in the Supabase SQL Editor after 001_transactions.sql.
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.budgets (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    month       INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year        INTEGER NOT NULL CHECK (year BETWEEN 2000 AND 2100),
    category    TEXT NOT NULL,
    amount      NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Each user can have only one budget per category per month/year
    CONSTRAINT budgets_unique_per_period
        UNIQUE (user_id, month, year, category)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_budgets_user_id         ON public.budgets(user_id);
CREATE INDEX IF NOT EXISTS idx_budgets_user_month_year ON public.budgets(user_id, year, month);

-- Enable Row Level Security
ALTER TABLE public.budgets ENABLE ROW LEVEL SECURITY;

-- Policy: users can only read their own budgets
CREATE POLICY "Users can view own budgets"
    ON public.budgets
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: users can insert their own budgets
CREATE POLICY "Users can insert own budgets"
    ON public.budgets
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: users can update their own budgets
CREATE POLICY "Users can update own budgets"
    ON public.budgets
    FOR UPDATE
    USING (auth.uid() = user_id);

-- Policy: users can delete their own budgets
CREATE POLICY "Users can delete own budgets"
    ON public.budgets
    FOR DELETE
    USING (auth.uid() = user_id);
