# Subspace.money Product Teardown & Prototype

**Product Intern Assignment, May 2026**

---

## Project Overview

This is a **product analysis and interactive prototype** of Subspace.money, India's subscription sharing and management platform. The prototype showcases a dark-themed, modern UI with the five key product improvements outlined below.

**Live Prototype:** Open `subspace.html` in your browser for a fully interactive experience.

---

## Five Sharps Feedbacks

### 1. **Trust Problem: No Protection Against Admin Fraud**
**Status:** CRITICAL

**Problem:** Users are getting kicked out of groups, denied access, or banned after giving honest feedback. With no escrow system, admins pocket money with zero accountability.

**Solution:** Subspace Shield
- Payment held in escrow for 48 hours after member confirms access
- Members can dispute "Access Denied" instantly; payment frozen
- Admin quality scores made public (3+ complaints = auto-suspend)
- Dispute resolution within 24 hours or full refund

---

### 2. **Login Wall: Nobody Knows What They're Buying**
**Status:** HIGH IMPACT ON CONVERSION

**Problem:** Homepage hides the group marketplace behind a login wall. New visitors can't see prices, savings, or available groups before entering their phone number.

**Solution:** Public browse, paywall at checkout
- Make full marketplace visible without login
- Show real prices, available slots, admin ratings upfront
- Add savings calculator on homepage (e.g., "You'll save ₹700/month")
- Only require login when clicking "Join Group"

---

### 3. **Hidden Superpower: Bill Negotiation API Is Invisible**
**Status:** REVENUE OPPORTUNITY BEING WASTED

**Problem:** Subspace automatically negotiates recurring bills but nobody knows it exists. Feature is buried; users think it's just an OTT sharing app.

**Solution:** Make negotiation the hero feature
- Lead homepage with bill negotiation prominently
- Add live ticker: "₹3.4 crore saved for Subspace users this month"
- Revenue model: Share percentage of savings (aligned incentives)
- Create comparison content vs. competitors like Rocket Money

---

### 4. **Strongest Moat, Zero Visibility: Local Marketplace**
**Status:** LONG-TERM STRATEGIC ADVANTAGE

**Problem:** Local subscriptions (gyms, tiffin, yoga, tutoring) are completely immune to Netflix crackdown but buried in navigation. No users know it exists.

**Solution:** Build supply + demand simultaneously
- Provider side: Self-serve listing page (free for 3 months)
- Consumer side: City-specific SEO landing pages ("Gym memberships in Bangalore")
- Target: Urban Indians 25-35 on YouTube finance channels & Reddit personal finance communities
- Competitive moat: Only Subspace has relationships with hyperlocal providers

---

### 5. **AI Promised, Frustration Delivered**
**Status:** RETENTION & BRAND RISK

**Problem:** Subspace runs 90% on AI but users only interact with it via broken support bots. Turns tech advantage into negative signal.

**Solution:** Spend Brain — Monthly WhatsApp insights
- AI sends personalized message once per month
- Example: "You're spending ₹2,840 on subscriptions. Switch 3 to groups = save ₹600 this month"
- Makes AI visible and helpful instead of hidden
- Creates monthly touchpoint for re-engagement
- Partner with fintech (Fi Money, Razorpay) for better transaction data

---

## Priority Order

1. **Shield (Trust)** — Users leaving + bad word-of-mouth. Ship first.
2. **Public Browse** — Fixes conversion funnel immediately. Ship with Shield.
3. **Negotiate Visible** — Revenue upside. Do this next.
4. **Local Marketplace** — Supply/demand takes time. Start GTM work now.
5. **Spend Brain** — Retention feature. Do once core product is solid.

---

## Market Context

- India's subscription management market: $286M (2025), growing 10%+ annually
- Competitors: myPaisaa, MoneyClub, Finlok (all smaller, less complete)
- Subspace current: ₹36.5 crore ARR, bootstrapped, 90% AI-operated
- Window to establish market leadership is real but time-limited

---

## Prototype Features

This interactive HTML prototype demonstrates:
- ✅ Dark Subspace-inspired theme with professional branding
- ✅ Public marketplace with 6 service groups (Netflix, Spotify, Prime, Canva, YouTube, JioHotstar)
- ✅ Live savings calculator showing "pick what you use — see what you save"
- ✅ Shield protection system with escrow indicators and dispute flow
- ✅ Bill negotiation interface (live ticker, savings estimates)
- ✅ Local marketplace with city-specific services
- ✅ Fully responsive design (desktop + mobile navigation)
- ✅ Professional logos and icons throughout

---

## How to Use

1. Open `subspace.html` in any modern browser
2. Browse the prototyped pages using top navigation or bottom mobile nav
3. Use the calculator to select services and see savings breakdown
4. Filter by Shield protection status
5. View the Shield protection flow and rules

---

## Tech Stack

- **Frontend:** Plain HTML, CSS, JavaScript (no frameworks)
- **Styling:** CSS variables system with dark theme
- **Fonts:** Google Fonts (Plus Jakarta Sans, Fraunces)
- **Responsiveness:** Mobile-first with desktop breakpoints

---

## Research Sources

- Direct product usage (web + mobile app)
- 3,000+ Play Store reviews analysis (3.44★ rating, 130K downloads)
- Crunchbase, Tracxn, ProductHunt company data
- IMARC Group market sizing report
- Competitor analysis (myPaisaa, MoneyClub, Rocket Money)

---

## Author Notes

This teardown and prototype were created as part of a product management case study. The goal was to identify the highest-leverage improvements Subspace could ship to accelerate ARR growth and competitive positioning in India's subscription economy.

The prototype is a working interactive model demonstrating how these improvements could appear in the actual product.

---

**Last Updated:** May 31, 2026
