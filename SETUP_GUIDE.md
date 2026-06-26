# Kaku Waitlist — Setup Guide
## No OTP, No Edge Functions needed for collecting emails

---

## STEP 1 — Create Supabase Project (Free)

1. Go to https://supabase.com → "Start your project" → sign up with GitHub
2. Create new project → name it "kaku-waitlist" → set a DB password → region: Southeast Asia
3. Wait ~2 min for setup

### Create the database table
Go to **SQL Editor** → paste and run:

```sql
-- Waitlist table
CREATE TABLE waitlist (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  verified BOOLEAN DEFAULT TRUE,
  joined_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

-- Allow anyone to insert (so visitors can join waitlist)
CREATE POLICY "Anyone can join waitlist" ON waitlist
  FOR INSERT WITH CHECK (true);

-- Allow anyone to read count only
CREATE POLICY "Public can count waitlist" ON waitlist
  FOR SELECT USING (true);
```

4. Go to **Settings → API** → copy:
   - `Project URL` → this is your `SUPABASE_URL`
   - `anon public` key → this is your `SUPABASE_ANON_KEY`

---

## STEP 2 — Update index.html

Open `index.html` and fill in the CONFIG at the top (around line 202):

```js
const CONFIG = {
  SUPABASE_URL:  'https://xxxx.supabase.co',
  SUPABASE_ANON: 'eyJxxxx....',
};
```

That's it! Emails will now be collected directly into Supabase with no backend needed.

---

## STEP 3 — Update admin.html

Open `admin.html` and fill in the same keys (around line 112):

```js
const CONFIG = {
  SUPABASE_URL:  'https://xxxx.supabase.co',
  SUPABASE_ANON: 'eyJxxxx....',
  BACKEND_URL:   'https://xxxx.supabase.co/functions/v1',  // only needed for broadcast emails
  ADMIN_PASSWORD: 'your_secure_password_here'  // change this!
};
```

---

## STEP 4 — Host for free on Netlify

1. Go to https://netlify.com → "Add new site" → "Deploy manually"
2. Drag your entire project folder into the browser
3. Done! You get a URL like `https://kaku-waitlist.netlify.app`
4. Optional: add a custom domain in Netlify settings

---

## STEP 5 — Admin Panel

Open `admin.html` in your browser (or at yourdomain.com/admin.html).
- Default password: `kaku_admin_2024` (change it inside admin.html CONFIG!)
- View all subscribers, search, export CSV
- Send broadcast email to everyone with one click

---

## Broadcast Email Setup (optional — for sending emails from admin)

The broadcast button in admin.html calls a Supabase Edge Function.
To enable it, deploy the `broadcast` function:

```bash
npm install -g supabase
supabase login
supabase init
supabase functions deploy broadcast --project-ref YOUR_PROJECT_REF
```

Set secrets:
```bash
supabase secrets set RESEND_API_KEY=re_xxxxxxxxxx
supabase secrets set SUPABASE_SERVICE_KEY=eyJxxxxxxxxxx
supabase secrets set FROM_EMAIL=hello@yourdomain.com
```

Then update BACKEND_URL in admin.html:
```
BACKEND_URL: 'https://xxxx.supabase.co/functions/v1'
```

Sign up at https://resend.com for free (3,000 emails/month).

---

## How it works now

```
User enters email → click "Get early access"
        ↓
Email inserted directly into Supabase waitlist table
        ↓
Success message shown instantly ✓
        ↓
Admin panel: one click to email everyone
```

## Monthly cost: ₹0
- Supabase: Free (500MB DB, 50k requests/month)
- Resend: Free (3,000 emails/month) — only if using broadcast
- Netlify: Free (100GB bandwidth/month)
