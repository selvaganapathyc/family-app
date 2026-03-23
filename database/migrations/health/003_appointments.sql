-- Health appointments table: tracks doctor visits and scheduled appointments
CREATE TABLE IF NOT EXISTS public.health_appointments (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    member_name  TEXT NOT NULL,
    doctor_name  TEXT NOT NULL,
    specialty    TEXT NOT NULL,
    date         DATE NOT NULL,
    time         TIME,
    status       TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    notes        TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_health_appointments_user_id ON public.health_appointments(user_id);
CREATE INDEX IF NOT EXISTS idx_health_appointments_date    ON public.health_appointments(user_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_health_appointments_member  ON public.health_appointments(user_id, member_name, date DESC);
CREATE INDEX IF NOT EXISTS idx_health_appointments_status  ON public.health_appointments(user_id, status, date DESC);

ALTER TABLE public.health_appointments ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view own appointments"   ON public.health_appointments;
DROP POLICY IF EXISTS "Users can insert own appointments" ON public.health_appointments;
DROP POLICY IF EXISTS "Users can update own appointments" ON public.health_appointments;
DROP POLICY IF EXISTS "Users can delete own appointments" ON public.health_appointments;

CREATE POLICY "Users can view own appointments"   ON public.health_appointments FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own appointments" ON public.health_appointments FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own appointments" ON public.health_appointments FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own appointments" ON public.health_appointments FOR DELETE USING (auth.uid() = user_id);
