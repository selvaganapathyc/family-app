-- Health vitals table: tracks key health metrics per family member
CREATE TABLE IF NOT EXISTS public.health_vitals (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    member_name TEXT NOT NULL,
    date        DATE NOT NULL,
    vital_type  TEXT NOT NULL,
    value       NUMERIC(10, 2) NOT NULL,
    unit        TEXT NOT NULL,
    notes       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Supported vital types: Weight, Blood Pressure Systolic, Blood Pressure Diastolic,
-- Heart Rate, Temperature, Blood Glucose, SpO2

CREATE INDEX IF NOT EXISTS idx_health_vitals_user_id          ON public.health_vitals(user_id);
CREATE INDEX IF NOT EXISTS idx_health_vitals_member_date       ON public.health_vitals(user_id, member_name, date DESC);
CREATE INDEX IF NOT EXISTS idx_health_vitals_type_member_date  ON public.health_vitals(user_id, vital_type, member_name, date DESC);

ALTER TABLE public.health_vitals ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own vitals"   ON public.health_vitals;
DROP POLICY IF EXISTS "Users can insert own vitals" ON public.health_vitals;
DROP POLICY IF EXISTS "Users can update own vitals" ON public.health_vitals;
DROP POLICY IF EXISTS "Users can delete own vitals" ON public.health_vitals;

CREATE POLICY "Users can view own vitals"   ON public.health_vitals FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own vitals" ON public.health_vitals FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own vitals" ON public.health_vitals FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own vitals" ON public.health_vitals FOR DELETE USING (auth.uid() = user_id);
