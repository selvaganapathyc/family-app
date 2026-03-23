-- Health medications table: tracks prescriptions and medicines per family member
CREATE TABLE IF NOT EXISTS public.health_medications (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    member_name TEXT NOT NULL,
    name        TEXT NOT NULL,
    dosage      TEXT NOT NULL,
    frequency   TEXT NOT NULL,
    start_date  DATE NOT NULL,
    end_date    DATE,
    is_active   BOOLEAN NOT NULL DEFAULT true,
    notes       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_health_medications_user_id ON public.health_medications(user_id);
CREATE INDEX IF NOT EXISTS idx_health_medications_member  ON public.health_medications(user_id, member_name);
CREATE INDEX IF NOT EXISTS idx_health_medications_active  ON public.health_medications(user_id, is_active);

ALTER TABLE public.health_medications ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own medications"   ON public.health_medications;
DROP POLICY IF EXISTS "Users can insert own medications" ON public.health_medications;
DROP POLICY IF EXISTS "Users can update own medications" ON public.health_medications;
DROP POLICY IF EXISTS "Users can delete own medications" ON public.health_medications;

CREATE POLICY "Users can view own medications"   ON public.health_medications FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own medications" ON public.health_medications FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own medications" ON public.health_medications FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own medications" ON public.health_medications FOR DELETE USING (auth.uid() = user_id);
