#!/usr/bin/env python3
"""
GRN Site Builder — Guardian Restoration Network
Generates all national service pages and city pages from master template.
Run: python3 build_grn.py
Output: ./output/ directory
"""

import os, shutil

OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── BRAND CONSTANTS ────────────────────────────────────────────────────────
PHONE_DISPLAY = "(888) 625-0666"
PHONE_TEL     = "8886250666"
PHONE_FULL    = "+1 888-625-0666"
GHL_WIDGET    = '69d5585984d8772ba9958d7e'
GA_ID         = "G-GNCZJ4J4BN"
BRAND         = "Guardian Restoration Network"
DOMAIN        = "https://guardianrestorationnetwork.com"
LEGAL         = "Lulabella Management DBA Guardian Restoration Network"
GUARDIAN_ENTITY = f"""{BRAND} is a national insurance claim management and restoration network. We confirm active homeowners insurance coverage, become the property owner's single point of contact with their insurance carrier, and dispatch vetted local contractors to complete restoration work. We work directly with your insurance carrier on billing — you are responsible for your deductible per your policy. Guardian serves both residential homeowners and commercial property owners nationwide, available 24 hours a day, 7 days a week at {PHONE_DISPLAY}."""

# ─── LOGOS (INLINE SVG) ──────────────────────────────────────────────────────
NAV_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 132" height="56" width="auto">
  <path d="M54 0 L108 20 L108 66 C108 97 82 116 54 128 C26 116 0 97 0 66 L0 20 Z" fill="#ff5500"/>
  <path d="M54 9 L99 27 L99 66 C99 93 75 111 54 120 C33 111 9 93 9 66 L9 27 Z" fill="none" stroke="#000000" stroke-width="2.8" opacity="0.75"/>
  <text x="54" y="93" font-family="Arial Black, sans-serif" font-size="70" font-weight="900" fill="white" text-anchor="middle">G</text>
  <text x="122" y="52" font-family="Arial, sans-serif" font-size="44" font-weight="700" fill="white" letter-spacing="-0.5">GUARDIAN</text>
  <text x="124" y="78" font-family="Arial, sans-serif" font-size="15" font-weight="400" fill="#ff5500" letter-spacing="3.5">RESTORATION NETWORK</text>
  <rect x="124" y="86" width="338" height="1.5" rx="1" fill="#ff5500" opacity="0.5"/>
  <text x="124" y="102" font-family="Arial, sans-serif" font-size="10.5" fill="#ff7a00" letter-spacing="1.2">DAMAGE COVERED. EXPERT DISPATCHED.</text>
</svg>"""

FOOTER_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 115" height="44" width="auto">
  <g transform="translate(10, 4)">
    <path d="M46 0 L88 16 L88 54 C88 80 68 97 46 107 C24 97 4 80 4 54 L4 16 Z" fill="#0b1d3a"/>
    <path d="M46 7 L82 21 L82 54 C82 77 64 93 46 101 C28 93 10 77 10 54 L10 21 Z" fill="none" stroke="#ff5500" stroke-width="2.2"/>
    <text x="46" y="76" font-family="Arial Black, sans-serif" font-size="54" font-weight="900" fill="white" text-anchor="middle">G</text>
  </g>
  <text x="115" y="44" font-family="Arial, sans-serif" font-size="32" font-weight="700" fill="white" letter-spacing="-0.5">GUARDIAN</text>
  <text x="115" y="66" font-family="Arial, sans-serif" font-size="11" font-weight="400" fill="#ff5500" letter-spacing="4">RESTORATION NETWORK</text>
  <rect x="115" y="73" width="278" height="1.5" rx="1" fill="#ff5500" opacity="0.6"/>
  <text x="115" y="89" font-family="Arial, sans-serif" font-size="9" fill="rgba(255,255,255,0.45)" letter-spacing="1.2">DAMAGE COVERED. EXPERT DISPATCHED.</text>
</svg>"""

# ─── SHARED CSS ──────────────────────────────────────────────────────────────
SHARED_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Barlow', -apple-system, BlinkMacSystemFont, sans-serif; color: #1e293b; }
:root {
  --navy: #0b1d3a; --navy-light: #0f2650;
  --orange: #ff5500; --orange-light: #ff7a00;
  --white: #ffffff; --gray-light: #f8fafc; --gray-text: #64748b;
}
/* NAV */
.nav { position: sticky; top: 0; z-index: 200; background: var(--navy); padding: 0 5%; display: flex; align-items: center; justify-content: space-between; height: 72px; box-shadow: 0 2px 12px rgba(0,0,0,0.3); border-bottom: 1px solid rgba(255,85,0,0.15); }
.nav-logo { text-decoration: none; display: flex; align-items: center; }
.nav-right { display: flex; align-items: center; gap: 12px; }
.nav-phone { color: #ff5500; font-size: 14px; font-weight: 700; text-decoration: none; white-space: nowrap; }
.nav-phone:hover { color: #ff7a00; }
.btn-nav { background: var(--orange); color: var(--white); padding: 10px 22px; border-radius: 6px; font-size: 14px; font-weight: 700; text-decoration: none; text-transform: uppercase; letter-spacing: 0.5px; transition: background 0.2s; white-space: nowrap; }
.btn-nav:hover { background: var(--orange-light); }
/* BREADCRUMB */
.breadcrumb { background: var(--navy-light); padding: 10px 5%; font-size: 13px; color: rgba(255,255,255,0.5); }
/* HERO */
.hero { background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 60%, #1a3a6e 100%); padding: 72px 5% 80px; text-align: center; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 70% 50%, rgba(255,85,0,0.08) 0%, transparent 70%); }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,85,0,0.15); border: 1px solid rgba(255,85,0,0.4); color: #ff8844; padding: 8px 18px; border-radius: 50px; font-size: 13px; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 24px; text-transform: uppercase; }
.hero-badge::before { content: '●'; color: #ff5500; font-size: 10px; }
.hero h1 { font-size: clamp(28px, 4.5vw, 52px); font-weight: 900; color: var(--white); line-height: 1.1; max-width: 800px; margin: 0 auto 20px; letter-spacing: -1px; }
.hero h1 span { color: var(--orange); }
.hero-sub { font-size: clamp(15px, 1.8vw, 18px); color: rgba(255,255,255,0.78); max-width: 580px; margin: 0 auto 36px; line-height: 1.6; }
.hero-ctas { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.btn-primary { background: var(--orange); color: var(--white); padding: 16px 36px; border-radius: 8px; font-size: 16px; font-weight: 800; text-decoration: none; transition: all 0.2s; box-shadow: 0 4px 20px rgba(255,85,0,0.4); }
.btn-primary:hover { background: #e64d00; transform: translateY(-1px); }
.btn-secondary { background: transparent; color: var(--white); padding: 16px 36px; border-radius: 8px; font-size: 16px; font-weight: 700; text-decoration: none; border: 2px solid rgba(255,255,255,0.4); transition: all 0.2s; }
.btn-secondary:hover { border-color: rgba(255,255,255,0.8); background: rgba(255,255,255,0.08); }
/* TRUST BAR */
.trust-bar { background: var(--orange); padding: 16px 5%; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 10px 32px; }
.trust-item { display: flex; align-items: center; gap: 8px; color: var(--white); font-size: 13px; font-weight: 700; letter-spacing: 0.3px; }
.trust-item::before { content: '✓'; font-size: 15px; font-weight: 900; }
/* URGENCY STRIP */
.urgency { background: var(--orange); padding: 14px 5%; text-align: center; }
.urgency p { color: #fff; font-size: 15px; font-weight: 700; letter-spacing: 0.3px; }
.urgency a { color: #fff; text-decoration: underline; }
/* SECTION SHARED */
.section-label { font-size: 11px; font-weight: 700; letter-spacing: 2px; color: var(--orange); text-transform: uppercase; margin-bottom: 10px; }
.section-title { font-size: clamp(26px, 3.5vw, 38px); font-weight: 800; color: var(--navy); margin-bottom: 14px; letter-spacing: -0.5px; }
.section-sub { font-size: 16px; color: var(--gray-text); max-width: 540px; margin: 0 auto 48px; }
/* SPLIT BLOCK */
.split { background: var(--white); padding: 72px 5%; }
.split-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; max-width: 1100px; margin: 0 auto; align-items: start; }
.split-block h3 { font-size: 22px; font-weight: 800; color: var(--navy); margin-bottom: 12px; }
.split-block p { font-size: 15px; color: var(--gray-text); line-height: 1.7; margin-bottom: 10px; }
.split-block ul { list-style: none; margin-top: 12px; }
.split-block ul li { padding: 6px 0 6px 22px; position: relative; font-size: 14px; color: var(--gray-text); line-height: 1.5; border-bottom: 1px solid #f1f5f9; }
.split-block ul li::before { content: '→'; position: absolute; left: 0; color: var(--orange); font-weight: 700; }
/* PROBLEM BLOCK */
.problem { background: var(--gray-light); padding: 72px 5%; text-align: center; }
.damage-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; max-width: 1000px; margin: 0 auto; }
.damage-card { background: var(--white); border-radius: 10px; padding: 24px 16px; text-align: center; border: 1px solid #e2e8f0; }
.damage-card .icon { font-size: 28px; margin-bottom: 10px; }
.damage-card h4 { font-size: 14px; font-weight: 700; color: var(--navy); }
/* SCOPE GRID */
.scope { background: var(--white); padding: 72px 5%; text-align: center; }
.scope-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; max-width: 1100px; margin: 0 auto; }
.scope-card { background: var(--gray-light); border-radius: 10px; padding: 28px 24px; text-align: left; border-left: 3px solid var(--orange); }
.scope-card h4 { font-size: 15px; font-weight: 800; color: var(--navy); margin-bottom: 8px; }
.scope-card p { font-size: 13px; color: var(--gray-text); line-height: 1.6; }
/* MID CTA */
.mid-cta { background: var(--orange); padding: 48px 5%; text-align: center; }
.mid-cta h3 { font-size: clamp(22px, 3vw, 32px); font-weight: 900; color: #fff; margin-bottom: 20px; }
/* HOW GUARDIAN HELPS */
.how-helps { background: var(--navy); padding: 72px 5%; text-align: center; }
.how-helps .section-title { color: var(--white); }
.how-helps .section-sub { color: rgba(255,255,255,0.65); }
.numbered-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1100px; margin: 0 auto; }
.numbered-card { background: var(--navy-light); border-radius: 10px; padding: 28px 24px; text-align: left; border: 1px solid rgba(255,255,255,0.07); }
.numbered-card .num { font-size: 36px; font-weight: 900; color: var(--orange); opacity: 0.6; line-height: 1; margin-bottom: 10px; }
.numbered-card h4 { font-size: 16px; font-weight: 800; color: #fff; margin-bottom: 8px; }
.numbered-card p { font-size: 13px; color: rgba(255,255,255,0.6); line-height: 1.6; }
/* WHAT TO EXPECT */
.expect { background: var(--gray-light); padding: 72px 5%; text-align: center; }
.expect-steps { display: flex; gap: 0; max-width: 1000px; margin: 0 auto; flex-wrap: wrap; justify-content: center; }
.expect-step { flex: 1; min-width: 200px; padding: 28px 20px; text-align: center; position: relative; }
.expect-step::after { content: '→'; position: absolute; right: -8px; top: 50%; transform: translateY(-50%); font-size: 20px; color: var(--orange); font-weight: 900; }
.expect-step:last-child::after { display: none; }
.expect-step .step-num { width: 48px; height: 48px; border-radius: 50%; background: var(--orange); color: #fff; font-size: 20px; font-weight: 900; display: flex; align-items: center; justify-content: center; margin: 0 auto 14px; }
.expect-step h4 { font-size: 15px; font-weight: 800; color: var(--navy); margin-bottom: 6px; }
.expect-step p { font-size: 13px; color: var(--gray-text); line-height: 1.5; }
/* WHY IT MATTERS */
.matters { background: var(--navy-light); padding: 72px 5%; }
.matters-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; max-width: 1100px; margin: 0 auto; align-items: center; }
.matters-text h2 { font-size: clamp(24px, 3vw, 36px); font-weight: 800; color: #fff; margin-bottom: 16px; }
.matters-text p { font-size: 15px; color: rgba(255,255,255,0.7); line-height: 1.7; margin-bottom: 12px; }
.stat-block { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.stat-item { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 24px 20px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
.stat-item .num { font-size: 36px; font-weight: 900; color: var(--orange); }
.stat-item .label { font-size: 13px; color: rgba(255,255,255,0.55); margin-top: 4px; }
/* WHY GUARDIAN */
.why { background: var(--gray-light); padding: 72px 5%; text-align: center; }
.why-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; max-width: 1100px; margin: 0 auto; }
.why-card { background: var(--white); border-radius: 10px; padding: 28px 24px; text-align: left; border: 1px solid #e2e8f0; }
.why-card .icon { font-size: 28px; margin-bottom: 12px; }
.why-card h4 { font-size: 16px; font-weight: 800; color: var(--navy); margin-bottom: 8px; }
.why-card p { font-size: 13px; color: var(--gray-text); line-height: 1.6; }
/* INSURANCE EXPLAINED */
.insurance { background: var(--white); padding: 72px 5%; }
.insurance-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; max-width: 1100px; margin: 0 auto; }
.insurance-text h2 { font-size: clamp(22px, 2.8vw, 32px); font-weight: 800; color: var(--navy); margin-bottom: 16px; }
.insurance-text p { font-size: 15px; color: var(--gray-text); line-height: 1.7; margin-bottom: 12px; }
.checkpoint-list { list-style: none; }
.checkpoint-list li { padding: 16px 20px 16px 52px; position: relative; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: var(--gray-text); line-height: 1.5; }
.checkpoint-list li::before { content: '✓'; position: absolute; left: 16px; top: 50%; transform: translateY(-50%); background: var(--orange); color: #fff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 900; }
/* FAQ */
.faq { background: var(--gray-light); padding: 72px 5%; }
.faq-inner { max-width: 860px; margin: 0 auto; }
.faq-title { font-size: clamp(26px, 3.5vw, 38px); font-weight: 800; color: var(--navy); margin-bottom: 36px; text-align: center; }
.faq-item { background: var(--white); border-radius: 8px; margin-bottom: 12px; border: 1px solid #e2e8f0; overflow: hidden; }
.faq-q { width: 100%; padding: 20px 24px; background: none; border: none; text-align: left; font-size: 16px; font-weight: 700; color: var(--navy); cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px; font-family: inherit; }
.faq-q:hover { background: #f8fafc; }
.faq-q .arrow { color: var(--orange); font-size: 18px; flex-shrink: 0; transition: transform 0.2s; }
.faq-item.open .faq-q .arrow { transform: rotate(180deg); }
.faq-a { display: none; padding: 0 24px 20px; font-size: 14px; color: var(--gray-text); line-height: 1.7; border-top: 1px solid #f1f5f9; }
.faq-item.open .faq-a { display: block; padding-top: 16px; }
/* FINAL CTA */
.final-cta { background: linear-gradient(135deg, var(--orange) 0%, var(--orange-light) 100%); padding: 80px 5%; text-align: center; }
.final-cta h2 { font-size: clamp(26px, 3.5vw, 42px); font-weight: 900; color: #fff; margin-bottom: 14px; }
.final-cta p { font-size: 17px; color: rgba(255,255,255,0.88); margin-bottom: 32px; max-width: 540px; margin-left: auto; margin-right: auto; }
.btn-white { background: var(--white); color: var(--orange); padding: 16px 42px; border-radius: 8px; font-size: 17px; font-weight: 800; text-decoration: none; display: inline-block; transition: all 0.2s; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
.btn-white:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.2); }
/* FOOTER */
.footer { background: #06111f; padding: 48px 5% 28px; }
.footer-simple { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; margin-bottom: 28px; }
.footer-simple p { color: rgba(255,255,255,0.5); font-size: 14px; max-width: 400px; line-height: 1.6; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; }
.footer-bottom p { color: rgba(255,255,255,0.3); font-size: 12px; }
/* RESPONSIVE */
@media (max-width: 768px) {
  .nav { padding: 0 16px; height: 64px; }
  .hero { padding: 48px 20px 56px; }
  .hero-ctas { flex-direction: column; align-items: stretch; }
  .btn-primary, .btn-secondary { text-align: center; }
  .trust-bar { flex-direction: column; align-items: flex-start; padding: 16px 20px; }
  .split-inner, .matters-inner, .insurance-inner { grid-template-columns: 1fr; gap: 32px; }
  .expect-step::after { display: none; }
  .footer-simple { flex-direction: column; }
  .split, .problem, .scope, .how-helps, .expect, .matters, .why, .insurance, .faq { padding: 48px 20px; }
  .mid-cta, .final-cta { padding: 48px 20px; }
}
"""

# ─── SHARED HTML COMPONENTS ──────────────────────────────────────────────────

def conversion_nav():
    """City page nav — conversion only. No dropdown."""
    return f"""<nav class="nav">
  <a href="/" class="nav-logo" aria-label="{BRAND} Home">{NAV_LOGO}</a>
  <div class="nav-right">
    <a href="tel:{PHONE_TEL}" class="nav-phone" aria-label="Call {BRAND}">📞 {PHONE_DISPLAY}</a>
    <a href="/contact/" class="btn-nav" aria-label="Get Help Now">Get Help Now</a>
  </div>
</nav>"""

def conversion_footer():
    """City page footer — conversion only. No nav columns."""
    return f"""<footer class="footer">
  <div class="footer-simple">
    <a href="/" aria-label="{BRAND} Home">{FOOTER_LOGO}</a>
    <p>America's trusted insurance claim management and restoration network. Available 24/7 at {PHONE_DISPLAY}.</p>
    <a href="tel:{PHONE_TEL}" class="btn-primary" aria-label="Call {BRAND}">📞 Call {PHONE_DISPLAY}</a>
  </div>
  <div class="footer-bottom">
    <p>© 2025 {LEGAL}. All rights reserved. Contractor dispatch subject to availability in your area. You are responsible for your deductible per your policy.</p>
  </div>
</footer>"""

def ghl_widget():
    return f"""<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="{GHL_WIDGET}"></script>"""

def faq_js():
    return """<script>
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    item.classList.toggle('open');
  });
});
</script>"""

# ─── SERVICE DEFINITIONS ─────────────────────────────────────────────────────

SERVICES = {
    "water-damage": {
        "name": "Water Damage Restoration",
        "slug": "water-damage-restoration",
        "national_url": "/water-damage-restoration/",
        "city_slug_prefix": "water-damage-restoration",
        "icon": "💧",
        "h1_national": "Water Damage Restoration — <span>Nationwide Coverage</span>",
        "hero_sub": "Burst pipes, flooding, appliance leaks, or sewage backup — we confirm your coverage, manage your claim, and dispatch vetted local contractors fast.",
        "badge": "24/7 Emergency Water Damage Response",
        "trust_items": ["Coverage Confirmed Fast", "We Manage Your Claim", "Licensed Contractors Dispatched", "Rapid Response Dispatch", "All 50 States Served"],
        "damage_types": [
            ("💧", "Burst Pipes"), ("🌊", "Flooding"), ("🚿", "Appliance Overflow"),
            ("🏗️", "Structural Water Damage"), ("⚠️", "Sewage Backup"), ("❄️", "Frozen Pipe Burst"),
            ("🌧️", "Roof Leak"), ("🏠", "Foundation Seepage"),
        ],
        "scope_items": [
            ("Emergency Water Extraction", "Industrial pumps and vacuums remove standing water immediately to stop further damage."),
            ("Structural Drying", "Commercial dehumidifiers and air movers dry walls, floors, and ceilings to prevent mold growth."),
            ("Moisture Mapping", "Thermal imaging and moisture meters locate hidden water in walls and subfloors."),
            ("Mold Prevention Treatment", "Anti-microbial treatments applied immediately after drying to prevent mold colonization."),
            ("Contents Protection", "Furniture, electronics, and personal items moved and dried or stored during restoration."),
            ("Flooring Removal & Replacement", "Damaged hardwood, carpet, and tile removed and replaced after structural drying is complete."),
            ("Drywall & Insulation Repair", "Wet drywall and saturated insulation removed and replaced to restore structural integrity."),
            ("Full Documentation", "Photos, moisture readings, and scope of work documented throughout for your insurance claim."),
        ],
        "how_helps": [
            ("01", "Verify Property Ownership", "We confirm you are the property owner or authorized representative before proceeding."),
            ("02", "Confirm Active Coverage", "We confirm your homeowners or commercial property insurance policy is active and covers the damage type."),
            ("03", "Document the Damage", "We guide you through photographing and documenting damage for your insurance file."),
            ("04", "Contact Your Carrier", "We become your single point of contact with your insurance carrier — you don't have to navigate the claim alone."),
            ("05", "Dispatch Vetted Contractor", "We connect you with a licensed, vetted local contractor and coordinate their arrival."),
            ("06", "Work Directly with Insurer", "We work directly with your insurance carrier on billing. You handle your deductible — we handle the rest."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666 anytime. Tell us your location and damage type. We start immediately."),
            ("Coverage Confirmed", "We confirm your active policy and document your claim within minutes."),
            ("Contractor Dispatched", "A vetted local contractor is dispatched to your property."),
            ("Claim Managed", "We manage your claim from start to finish — you focus on your family."),
        ],
        "matters_stats": [
            ("48hrs", "Mold can begin growing within 48 hours of water damage"),
            ("$12K+", "Average water damage claim when not addressed immediately"),
            ("24/7", "Guardian is available around the clock"),
            ("500+", "Vetted contractors in our network"),
        ],
        "why_cards": [
            ("🛡️", "Licensed Contractors Only", "Every contractor in our network is licensed, insured, and vetted before dispatch."),
            ("📋", "Full Claim Management", "We handle the paperwork, documentation, and communication with your insurer."),
            ("⚡", "Rapid Response Dispatch", "We move fast — water damage worsens by the hour."),
            ("🌎", "Nationwide Network", "We serve all 50 states with local vetted contractors in every major market."),
            ("📞", "Single Point of Contact", "One number, one team — from first call to completed restoration."),
            ("✅", "No Surprises", "We work directly with your insurer. You are responsible only for your deductible per your policy."),
        ],
        "checkpoints": [
            "We confirm your policy is active before dispatching any contractor",
            "We become your advocate with your insurance carrier throughout the process",
            "We work directly with your insurer on billing — you pay your deductible only",
            "All contractor work is documented and submitted to your carrier",
        ],
        "faqs": [
            ("Does homeowners insurance cover water damage restoration?",
             "Most standard homeowners insurance policies cover sudden and accidental water damage, such as burst pipes or appliance overflow. Gradual leaks and flooding from outside are typically excluded. We confirm your active coverage fast — call us and we will check your policy right away. Call 888-625-0666 and we will help you right away."),
            ("How quickly do I need to act after water damage?",
             "Immediately. Mold can begin growing within 48 hours of water damage. The longer water sits, the more structural damage occurs and the more expensive the repair becomes. Even if you are waiting for an adjuster, water extraction should begin as soon as possible. Call 888-625-0666 and we will help you right away."),
            ("What is the water damage restoration process?",
             "The process begins with emergency water extraction, followed by structural drying using commercial dehumidifiers and air movers. Moisture mapping identifies hidden moisture in walls and floors. Once fully dry, repairs begin — flooring, drywall, and any structural components. All work is documented for your insurance claim. Call 888-625-0666 and we will help you right away."),
            ("Will my insurance cover the full cost of water damage restoration?",
             "Coverage depends on your specific policy, the cause of damage, and your deductible. We work directly with your insurance carrier to maximize your covered claim. You are responsible for your deductible — we manage the rest of the process. Call 888-625-0666 and we will help you right away."),
            ("Can I stay in my home during water damage restoration?",
             "It depends on the severity. Minor water damage may allow you to remain at home while drying equipment runs. Major flooding, sewage backup, or mold risk may require temporary relocation. We will advise you based on the contractor's assessment. Call 888-625-0666 and we will help you right away."),
            ("What causes most water damage claims?",
             "The most common causes are burst pipes (especially in freezing temperatures), water heater failures, washing machine hose failures, dishwasher leaks, roof leaks, and sewage backups. Any of these may be covered under your homeowners policy depending on your coverage. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian work with my insurance company?",
             "We confirm your active coverage, document your claim, and become your single point of contact with your carrier. We coordinate the contractor, submit documentation, and work directly with your insurer on billing. You handle your deductible — we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },

    "fire-damage": {
        "name": "Fire Damage Restoration",
        "slug": "fire-damage-restoration",
        "national_url": "/fire-damage-restoration/",
        "city_slug_prefix": "fire-damage-restoration",
        "icon": "🔥",
        "h1_national": "Fire Damage Restoration — <span>Nationwide Coverage</span>",
        "hero_sub": "Fire, smoke, and soot damage require immediate action. We confirm your coverage, manage your claim, and dispatch vetted restoration contractors — fast.",
        "badge": "24/7 Emergency Fire Damage Response",
        "trust_items": ["Coverage Confirmed Fast", "We Manage Your Claim", "Board-Up & Secure", "Rapid Response Dispatch", "All 50 States Served"],
        "damage_types": [
            ("🔥", "Structural Fire Damage"), ("💨", "Smoke Damage"), ("⚫", "Soot Contamination"),
            ("💧", "Water Damage from Firefighting"), ("☠️", "Odor & Toxins"), ("🏠", "Roof & Structural Collapse"),
            ("⚡", "Electrical Fire Damage"), ("🧯", "Kitchen Fire"),
        ],
        "scope_items": [
            ("Emergency Board-Up & Securing", "We immediately secure your property — windows, doors, and roof openings — to prevent further damage and unauthorized entry."),
            ("Smoke & Soot Removal", "Specialized equipment and techniques remove smoke residue and soot from all surfaces, including HVAC systems."),
            ("Odor Elimination", "Thermal fogging, ozone treatment, and hydroxyl generators neutralize smoke odor at the molecular level."),
            ("Water Damage Mitigation", "Water used by firefighters is extracted and dried immediately to prevent secondary mold damage."),
            ("Contents Cleaning & Pack-Out", "Personal belongings are professionally cleaned, packed, and stored during restoration."),
            ("Structural Repair", "Burned framing, flooring, drywall, and roofing are removed and replaced by licensed contractors."),
            ("HVAC Cleaning", "Ductwork and HVAC systems are cleaned to remove smoke particles that spread throughout the structure."),
            ("Full Insurance Documentation", "All damage is photographed, scoped, and documented for your insurance carrier."),
        ],
        "how_helps": [
            ("01", "Verify Property Ownership", "We confirm you are the authorized property owner or representative before proceeding."),
            ("02", "Confirm Active Coverage", "We confirm your insurance policy covers fire, smoke, and related water damage."),
            ("03", "Emergency Board-Up Coordination", "We dispatch contractors to immediately secure your property if needed."),
            ("04", "Document All Damage", "Every room, every item, every structural element documented for your claim file."),
            ("05", "Manage Your Carrier", "We become your advocate with your insurance carrier throughout the entire claim."),
            ("06", "Dispatch & Oversee Restoration", "We connect you with vetted local contractors and work directly with your insurer on billing."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666 immediately after fire is out. We begin coordinating right away."),
            ("Coverage Confirmed", "We confirm your active policy covers fire and smoke damage."),
            ("Property Secured", "Board-up and securing contractors dispatched if needed."),
            ("Restoration Managed", "Full restoration managed with your insurance carrier from start to finish."),
        ],
        "matters_stats": [
            ("72hrs", "Critical window to prevent smoke damage from becoming permanent"),
            ("$80K+", "Average fire damage insurance claim"),
            ("24/7", "Guardian available around the clock"),
            ("500+", "Vetted restoration contractors nationwide"),
        ],
        "why_cards": [
            ("🛡️", "Licensed Contractors Only", "Every contractor dispatched is licensed, insured, and vetted."),
            ("📋", "Full Claim Management", "We handle documentation and communication with your insurer."),
            ("⚡", "Rapid Dispatch", "Fire damage worsens fast — we move immediately."),
            ("🌎", "Nationwide Network", "Vetted contractors in every major market across all 50 states."),
            ("📞", "Single Point of Contact", "One call, one team — from emergency board-up to final restoration."),
            ("✅", "No Surprises", "We work with your insurer directly. You pay your deductible only."),
        ],
        "checkpoints": [
            "We confirm your fire and smoke damage coverage before dispatching any contractor",
            "We manage your claim with your insurance carrier from first call to completion",
            "We work directly with your insurer on billing — you pay your deductible only",
            "All damage documentation submitted to your carrier on your behalf",
        ],
        "faqs": [
            ("Does homeowners insurance cover fire damage restoration?",
             "Yes — fire damage is one of the most commonly covered perils in standard homeowners insurance policies. This typically includes the structure, smoke damage, water damage from firefighting, and temporary housing costs. We confirm your specific coverage fast. Call 888-625-0666 and we will help you right away."),
            ("What should I do immediately after a fire?",
             "First, ensure everyone is safe and the fire department has cleared the scene. Do not re-enter until it is declared safe. Call us immediately — we coordinate emergency board-up, secure the property, and begin documenting damage for your claim before anything deteriorates further. Call 888-625-0666 and we will help you right away."),
            ("How long does fire damage restoration take?",
             "Minor fire damage can be restored in days to weeks. Major structural fires can take months. The timeline depends on the extent of structural damage, smoke penetration, and the scope of reconstruction required. We manage the entire timeline with your insurance carrier. Call 888-625-0666 and we will help you right away."),
            ("Is smoke damage covered by insurance?",
             "Yes, smoke damage is typically covered under standard homeowners policies as part of fire coverage. This includes soot removal, odor elimination, HVAC cleaning, and contents cleaning. We document and submit all smoke-related damage to your carrier. Call 888-625-0666 and we will help you right away."),
            ("Can my belongings be restored after a fire?",
             "Many contents can be professionally cleaned and restored — furniture, clothing, electronics, documents, and personal items. Items that cannot be restored are documented for your contents claim. Our contractors use specialized cleaning techniques to recover as much as possible. Call 888-625-0666 and we will help you right away."),
            ("What is emergency board-up and why does it matter?",
             "Emergency board-up secures your property immediately after fire damage — covering broken windows, damaged doors, and roof openings. This prevents weather damage, vandalism, and unauthorized entry while restoration planning proceeds. It is typically covered under your insurance claim. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian handle fire damage claims with my insurance?",
             "We confirm your active coverage, document every element of damage, and become your single point of contact with your carrier. We coordinate the contractor, manage the scope of work, and work directly with your insurer on billing. You handle your deductible — we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },

    "mold-remediation": {
        "name": "Mold Remediation",
        "slug": "mold-remediation",
        "national_url": "/mold-remediation/",
        "city_slug_prefix": "mold-remediation",
        "icon": "🍃",
        "h1_national": "Mold Remediation — <span>Nationwide Coverage</span>",
        "hero_sub": "Mold spreads fast and creates serious health risks. We confirm your coverage, manage your claim, and dispatch licensed mold remediation contractors.",
        "badge": "Licensed Mold Remediation — All 50 States",
        "trust_items": ["Coverage Confirmed Fast", "We Manage Your Claim", "Licensed Remediation Contractors", "Certified Testing & Removal", "All 50 States Served"],
        "damage_types": [
            ("🍃", "Black Mold (Stachybotrys)"), ("🌿", "Attic Mold"), ("🏠", "Basement Mold"),
            ("🚿", "Bathroom Mold"), ("🧱", "Wall Cavity Mold"), ("❄️", "HVAC Mold"),
            ("💧", "Post-Water Damage Mold"), ("⚠️", "Crawl Space Mold"),
        ],
        "scope_items": [
            ("Mold Testing & Assessment", "Air quality and surface samples taken by certified inspectors to identify mold species and extent of contamination."),
            ("Containment Setup", "Negative air pressure containment zones established to prevent mold spores from spreading to unaffected areas."),
            ("HEPA Air Filtration", "Commercial HEPA air scrubbers run continuously during remediation to capture airborne mold spores."),
            ("Mold Removal", "Affected materials removed — drywall, insulation, flooring — following EPA and IICRC guidelines."),
            ("Anti-Microbial Treatment", "All surfaces treated with EPA-registered anti-microbial agents after removal."),
            ("Structural Repair", "Replaced drywall, insulation, and framing after mold removal is complete and clearance testing passed."),
            ("Clearance Testing", "Independent post-remediation testing confirms mold levels are within acceptable limits before containment is removed."),
            ("Root Cause Correction", "Moisture source identified and corrected — whether plumbing, roof, or vapor barrier — to prevent recurrence."),
        ],
        "how_helps": [
            ("01", "Confirm Property Ownership", "We verify you are the authorized owner or representative before proceeding."),
            ("02", "Confirm Active Coverage", "We confirm your policy covers mold remediation — coverage varies by carrier and cause."),
            ("03", "Dispatch Certified Inspector", "A certified mold inspector is dispatched to assess extent and type of contamination."),
            ("04", "Document for Claim", "All testing results, photos, and scope of work documented for your insurance carrier."),
            ("05", "Manage Your Carrier", "We coordinate with your insurer throughout the remediation process."),
            ("06", "Dispatch Remediation Contractor", "Licensed remediation contractors dispatched and overseen through completion and clearance testing."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666. We confirm your coverage and dispatch an inspector."),
            ("Testing & Scope", "Certified inspector assesses mold type, extent, and source of moisture."),
            ("Remediation", "Licensed contractor removes mold under containment with HEPA filtration."),
            ("Clearance Testing", "Independent clearance test confirms successful remediation before completion."),
        ],
        "matters_stats": [
            ("48hrs", "Mold begins growing within 48 hours of water damage"),
            ("300+", "Known mold species — some cause serious health effects"),
            ("24/7", "Guardian available around the clock"),
            ("500+", "Vetted contractors in our network"),
        ],
        "why_cards": [
            ("🛡️", "Certified Contractors Only", "Every remediation contractor is licensed, certified, and vetted."),
            ("📋", "Full Claim Management", "We handle all documentation and coordination with your insurer."),
            ("🔬", "Clearance Testing Included", "Independent post-remediation testing is part of every job."),
            ("🌎", "Nationwide Network", "Certified remediators in every major market."),
            ("📞", "Single Point of Contact", "One call manages everything — testing, remediation, and claim."),
            ("✅", "No Surprises", "We work with your insurer on billing. You pay your deductible only."),
        ],
        "checkpoints": [
            "We confirm your mold remediation coverage before dispatching any contractor",
            "All remediation follows EPA and IICRC S520 guidelines",
            "Independent clearance testing confirms successful remediation",
            "We work directly with your insurer on billing — you pay your deductible only",
        ],
        "faqs": [
            ("Does homeowners insurance cover mold remediation?",
             "Coverage depends on the cause of mold. If mold resulted from a covered water damage event — like a burst pipe — it is typically covered. Mold from gradual leaks, flooding, or poor maintenance may not be covered. We confirm your specific coverage fast. Call 888-625-0666 and we will help you right away."),
            ("How serious is black mold?",
             "Black mold (Stachybotrys chartarum) produces mycotoxins that can cause respiratory issues, chronic fatigue, and other health problems with prolonged exposure. Any suspected black mold should be tested and remediated by certified professionals immediately. Do not disturb mold growth before testing. Call 888-625-0666 and we will help you right away."),
            ("Can I clean mold myself?",
             "Small surface mold under 10 square feet may be addressed with proper precautions. Larger infestations, mold inside walls, black mold, or mold affecting HVAC systems requires certified professional remediation. DIY cleaning without containment can spread spores throughout your home. Call 888-625-0666 and we will help you right away."),
            ("How long does mold remediation take?",
             "Minor mold removal can take 1–3 days. Larger infestations requiring containment, structural removal, and clearance testing can take 1–2 weeks. Timeline depends on the area affected and moisture source correction required. Call 888-625-0666 and we will help you right away."),
            ("What is clearance testing and why is it important?",
             "Clearance testing is an independent post-remediation air quality test that confirms mold spore levels have returned to acceptable limits. It is conducted by a separate party from the remediation contractor. Clearance testing proves the job was done correctly and protects you legally. Call 888-625-0666 and we will help you right away."),
            ("How do I know if I have mold in my walls?",
             "Signs include musty odor without visible mold, unexplained allergy-like symptoms, water stains on walls or ceilings, peeling paint or wallpaper, and warped surfaces. Certified mold inspectors use moisture meters and air sampling to detect hidden mold. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian handle mold claims with insurance?",
             "We confirm your active coverage, dispatch a certified inspector, document the scope of contamination, and manage your claim with your insurance carrier. We work directly with your insurer on billing — you handle your deductible, we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },

    "storm-damage": {
        "name": "Storm Damage Restoration",
        "slug": "storm-damage-restoration",
        "national_url": "/storm-damage-restoration/",
        "city_slug_prefix": "storm-damage-restoration",
        "icon": "⛈️",
        "h1_national": "Storm Damage Restoration — <span>Nationwide Coverage</span>",
        "hero_sub": "Hail, wind, tornado, or hurricane damage — we confirm your coverage, manage your claim, and dispatch vetted local contractors for emergency response and full restoration.",
        "badge": "24/7 Emergency Storm Damage Response",
        "trust_items": ["Coverage Confirmed Fast", "We Manage Your Claim", "Emergency Tarping Available", "Rapid Response Dispatch", "All 50 States Served"],
        "damage_types": [
            ("⛈️", "Hail Damage"), ("🌪️", "Tornado Damage"), ("🌀", "Hurricane Damage"),
            ("💨", "High Wind Damage"), ("🌧️", "Rain Intrusion"), ("❄️", "Ice & Snow Load"),
            ("⚡", "Lightning Strike"), ("🌲", "Tree & Debris Impact"),
        ],
        "scope_items": [
            ("Emergency Tarping & Board-Up", "Immediate protection of damaged roof, windows, and openings to prevent further weather intrusion."),
            ("Roof Damage Assessment", "Certified inspectors document all hail impacts, wind damage, and structural compromise for your claim."),
            ("Structural Damage Repair", "Damaged framing, trusses, and load-bearing elements assessed and repaired by licensed contractors."),
            ("Siding & Exterior Restoration", "Hail-damaged siding, gutters, and exterior components replaced and matched to existing materials."),
            ("Window & Door Replacement", "Broken windows, damaged frames, and compromised doors replaced to restore envelope integrity."),
            ("Water Intrusion Mitigation", "Interior water damage from storm intrusion extracted and dried to prevent mold."),
            ("HVAC & Mechanical Assessment", "Storm damage to HVAC units, condenser coils, and mechanical equipment documented and repaired."),
            ("Full Insurance Documentation", "Complete damage report with photos, measurements, and scope submitted to your insurance carrier."),
        ],
        "how_helps": [
            ("01", "Confirm Property Ownership", "We verify you are the authorized owner or representative."),
            ("02", "Confirm Active Coverage", "We confirm your windstorm, hail, and storm coverage is active."),
            ("03", "Emergency Tarping Dispatch", "If your roof is compromised, we dispatch emergency tarping contractors immediately."),
            ("04", "Document All Damage", "Every element of storm damage photographed and documented for your claim."),
            ("05", "Manage Your Carrier", "We become your advocate with your insurance carrier throughout the entire claim process."),
            ("06", "Full Restoration Managed", "We connect you with vetted local contractors and manage the restoration from start to finish."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666 after the storm. We respond immediately."),
            ("Coverage Confirmed", "We confirm your storm and wind coverage is active."),
            ("Emergency Response", "Tarping and board-up dispatched if your property is exposed."),
            ("Full Restoration", "Claim managed and restoration completed through your insurance carrier."),
        ],
        "matters_stats": [
            ("$22K+", "Average storm damage insurance claim nationwide"),
            ("Hours", "Window before secondary damage begins after roof breach"),
            ("24/7", "Guardian available around the clock"),
            ("500+", "Vetted contractors in our network"),
        ],
        "why_cards": [
            ("🛡️", "Licensed Contractors Only", "Every contractor in our network is licensed, insured, and vetted."),
            ("📋", "Full Claim Management", "We handle all documentation and communication with your insurer."),
            ("⚡", "Rapid Response", "Storm damage worsens fast — we move immediately."),
            ("🌎", "Nationwide Network", "Vetted contractors in every major market across all 50 states."),
            ("📞", "Single Point of Contact", "One call manages everything from emergency response to final restoration."),
            ("✅", "No Surprises", "We work with your insurer on billing. You pay your deductible only."),
        ],
        "checkpoints": [
            "We confirm your storm and wind coverage before dispatching any contractor",
            "Emergency tarping and board-up coordinated immediately if needed",
            "All damage documented and submitted to your insurance carrier",
            "We work directly with your insurer on billing — you pay your deductible only",
        ],
        "faqs": [
            ("Does homeowners insurance cover storm damage?",
             "Standard homeowners insurance policies typically cover wind damage, hail, lightning, and damage from falling trees. Flooding from storm surge is generally excluded and requires separate flood insurance. We confirm your specific storm coverage fast. Call 888-625-0666 and we will help you right away."),
            ("What should I do immediately after storm damage?",
             "Ensure your family is safe first. Then call us — we coordinate emergency tarping or board-up to prevent further damage before an adjuster arrives. Document damage with photos if it is safe to do so. Do not make permanent repairs before your insurance claim is filed and documented. Call 888-625-0666 and we will help you right away."),
            ("Can I make temporary repairs before my insurance adjuster arrives?",
             "Yes — you should make reasonable temporary repairs like tarping to prevent further damage. Keep all receipts. Do not make permanent repairs until the adjuster has documented the damage. We help coordinate temporary repairs that are typically reimbursable under your claim. Call 888-625-0666 and we will help you right away."),
            ("How long does storm damage restoration take?",
             "Minor storm damage like broken windows or partial roof damage can be repaired in days. Major structural damage from tornadoes or hurricanes can take weeks to months. We manage the entire timeline with your insurance carrier. Call 888-625-0666 and we will help you right away."),
            ("What is emergency tarping and is it covered?",
             "Emergency tarping protects a damaged roof from further rain intrusion until permanent repairs can be made. It is typically covered as a reasonable temporary repair under your homeowners policy. We coordinate tarping immediately when your roof is compromised. Call 888-625-0666 and we will help you right away."),
            ("How does hail damage affect my roof?",
             "Hail impacts crack asphalt shingles, dent metal roofing and gutters, and damage HVAC equipment. Hail damage is not always visible from the ground and requires a professional inspection. Undocumented hail damage can void roof warranties and lead to water intrusion. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian handle storm damage claims?",
             "We confirm your active coverage, dispatch licensed inspectors, document all damage, and manage your claim with your insurance carrier. We work directly with your insurer on billing — you handle your deductible, we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },

    "biohazard-cleanup": {
        "name": "Sewage Cleanup & Biohazard Remediation",
        "slug": "biohazard-cleanup",
        "national_url": "/biohazard-cleanup/",
        "city_slug_prefix": "sewage-cleanup",
        "icon": "⚠️",
        "h1_national": "Sewage Cleanup & Biohazard Remediation — <span>Nationwide</span>",
        "hero_sub": "Sewage backup, biohazard contamination, crime scene cleanup, and hazardous material remediation — we confirm your coverage, manage your claim, and dispatch certified contractors.",
        "badge": "24/7 Biohazard & Sewage Emergency Response",
        "trust_items": ["Coverage Confirmed Fast", "Certified Biohazard Contractors", "Full PPE & Safe Disposal", "Rapid Response Dispatch", "All 50 States Served"],
        "damage_types": [
            ("⚠️", "Sewage Backup"), ("🚽", "Drain Overflow"), ("🔧", "Pipe Backup"),
            ("☣️", "Biohazard Contamination"), ("🔬", "Crime Scene Cleanup"), ("💀", "Unattended Death"),
            ("🏠", "Hoarding Cleanup"), ("⚗️", "Chemical & Hazmat"),
        ],
        "scope_items": [
            ("Sewage Extraction & Removal", "Contaminated sewage and wastewater removed using specialized pumping equipment and PPE protocols."),
            ("Biohazard Containment", "Affected areas sealed and negative air pressure established to prevent cross-contamination."),
            ("Contaminated Material Removal", "All affected flooring, drywall, insulation, and contents removed following OSHA and EPA disposal guidelines."),
            ("Level 2 & 3 Biological Decontamination", "Certified technicians decontaminate all surfaces with hospital-grade EPA-registered disinfectants."),
            ("Crime Scene & Trauma Cleanup", "Trained and certified technicians handle blood, bodily fluids, and trauma residue with full regulatory compliance."),
            ("Hoarding Cleanup with Hazmat Protocols", "Biohazardous hoarding situations managed with proper PPE, disposal, and health authority coordination."),
            ("Odor Elimination", "Ozone treatment and hydroxyl generators neutralize contamination-related odors at the molecular level."),
            ("Full Regulatory Documentation", "All work documented to OSHA, EPA, and state health authority standards for insurance and compliance."),
        ],
        "how_helps": [
            ("01", "Confirm Property Ownership", "We verify you are the authorized owner or representative before proceeding."),
            ("02", "Confirm Active Coverage", "We confirm your policy covers sewage backup, biohazard, or the specific contamination event."),
            ("03", "Dispatch Certified Technicians", "Certified biohazard technicians dispatched with full PPE and required equipment."),
            ("04", "Document for Your Claim", "All contamination, scope, and remediation documented for your insurance file."),
            ("05", "Manage Your Carrier", "We coordinate with your insurance carrier throughout the entire remediation process."),
            ("06", "Regulatory Compliance Managed", "All work completed in compliance with OSHA, EPA, and local health authority requirements."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666 immediately. Do not enter contaminated areas."),
            ("Coverage Confirmed", "We confirm your sewage or biohazard coverage is active."),
            ("Certified Dispatch", "Certified technicians arrive with full PPE and containment equipment."),
            ("Fully Remediated", "All contamination removed, surfaces decontaminated, and documentation submitted to your carrier."),
        ],
        "matters_stats": [
            ("24hrs", "Window before sewage contamination causes permanent structural damage"),
            ("Category 3", "Sewage is Category 3 water — the most hazardous classification"),
            ("24/7", "Guardian available around the clock"),
            ("500+", "Vetted contractors in our network"),
        ],
        "why_cards": [
            ("🛡️", "Certified Technicians Only", "Every biohazard contractor is OSHA-trained, certified, and vetted."),
            ("📋", "Full Claim Management", "We handle all documentation and coordination with your insurer."),
            ("⚡", "Rapid Dispatch", "Biohazard situations worsen quickly — we respond immediately."),
            ("🌎", "Nationwide Network", "Certified biohazard contractors in every major market."),
            ("📞", "Single Point of Contact", "One call manages everything from first response to final clearance."),
            ("✅", "Regulatory Compliance", "All work documented to OSHA, EPA, and state health authority standards."),
        ],
        "checkpoints": [
            "We confirm your sewage or biohazard coverage before dispatching any contractor",
            "All work performed by OSHA-trained certified biohazard technicians",
            "Full regulatory documentation provided for insurance and compliance",
            "We work directly with your insurer on billing — you pay your deductible only",
        ],
        "faqs": [
            ("Does homeowners insurance cover sewage backup?",
             "Standard homeowners policies typically do not cover sewage backup unless you have added a sewage backup endorsement or rider. Some policies include it automatically. We confirm your specific coverage fast. Call 888-625-0666 and we will help you right away."),
            ("Is sewage backup dangerous?",
             "Yes — sewage is classified as Category 3 water (black water), the most hazardous level. It contains bacteria, viruses, and parasites that pose serious health risks. Do not enter or attempt to clean sewage-contaminated areas without proper PPE and training. Call 888-625-0666 and we will help you right away."),
            ("What is biohazard remediation?",
             "Biohazard remediation is the professional cleanup and decontamination of areas affected by blood, bodily fluids, sewage, crime scenes, unattended death, hoarding with contamination, or chemical hazards. All work follows OSHA and EPA guidelines with certified technicians and proper disposal. Call 888-625-0666 and we will help you right away."),
            ("What causes sewage backups?",
             "The most common causes are tree root intrusion in sewer lines, blockages from grease or debris, heavy rain overwhelming combined sewer systems, pipe collapses in older homes, and municipal sewer main backups. Call 888-625-0666 and we will help you right away."),
            ("How long does sewage cleanup take?",
             "Minor sewage backup affecting a small area can be remediated in 1–2 days. Larger contamination events requiring structural removal and decontamination can take several days to a week. All work must pass post-remediation testing before completion. Call 888-625-0666 and we will help you right away."),
            ("What is unattended death cleanup?",
             "Unattended death cleanup is the professional decontamination of a space following a death that was not immediately discovered. It requires certified biohazard technicians, full PPE, and regulatory-compliant disposal. This service is often covered under homeowners insurance. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian handle biohazard claims with insurance?",
             "We confirm your active coverage, dispatch certified technicians, document all contamination and remediation work, and manage your claim with your insurance carrier. We work directly with your insurer on billing — you handle your deductible, we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },

    "asbestos-abatement": {
        "name": "Asbestos Abatement",
        "slug": "asbestos-abatement",
        "national_url": "/asbestos-abatement/",
        "city_slug_prefix": "asbestos-removal",
        "icon": "🏗️",
        "h1_national": "Asbestos Abatement — <span>Licensed Removal Nationwide</span>",
        "hero_sub": "Pre-1980 homes are at elevated risk. Asbestos must be removed by licensed contractors before any restoration work begins. We confirm coverage, manage the process, and dispatch certified abatement contractors.",
        "badge": "Licensed Asbestos Abatement — All 50 States",
        "trust_items": ["Licensed Abatement Contractors", "Coverage Confirmed Fast", "EPA & State Compliant", "Testing Through Clearance", "All 50 States Served"],
        "damage_types": [
            ("🏗️", "Popcorn Ceiling (ACM)"), ("🏠", "Floor Tile & Mastic"), ("🔧", "Pipe Insulation"),
            ("🧱", "Drywall & Joint Compound"), ("🌡️", "HVAC Insulation"), ("🏚️", "Roofing Shingles"),
            ("⚠️", "Vermiculite Insulation"), ("🔬", "Textured Paint"),
        ],
        "scope_items": [
            ("Asbestos Testing & Bulk Sampling", "Certified inspectors collect bulk samples from suspected asbestos-containing materials and submit for laboratory analysis."),
            ("Pre-Abatement Clearance Air Testing", "Air samples taken before abatement to establish baseline fiber counts per regulatory requirements."),
            ("Containment Setup", "Full containment with plastic sheeting and negative air pressure units established before any removal begins."),
            ("Licensed Asbestos Removal", "State-licensed abatement contractors remove all identified asbestos-containing materials per EPA NESHAP and state regulations."),
            ("Proper Waste Disposal", "All asbestos waste double-bagged, labeled, and disposed of at licensed Class I landfill facilities."),
            ("Post-Abatement Clearance Testing", "Independent air samples confirm fiber counts are within EPA clearance levels before containment is removed."),
            ("Regulatory Documentation", "Complete abatement documentation including permits, waste manifests, and clearance results provided for your records."),
            ("Restoration Coordination", "We coordinate with your restoration contractor to ensure abatement is complete before any reconstruction begins."),
        ],
        "how_helps": [
            ("01", "Confirm Property Ownership", "We verify you are the authorized owner or representative."),
            ("02", "Confirm Active Coverage", "We confirm whether your policy covers asbestos testing and abatement."),
            ("03", "Dispatch Licensed Inspector", "A certified asbestos inspector collects bulk samples and provides a written assessment."),
            ("04", "Document for Your Claim", "All testing results, abatement scope, and clearance documentation submitted to your carrier."),
            ("05", "Manage Your Carrier", "We coordinate with your insurance carrier if asbestos abatement is part of a covered restoration claim."),
            ("06", "Oversee Abatement to Clearance", "We ensure all work meets EPA, state, and insurance requirements before restoration proceeds."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666. We dispatch a licensed inspector."),
            ("Testing & Assessment", "Bulk sampling confirms presence and scope of asbestos-containing materials."),
            ("Licensed Abatement", "State-licensed contractors remove all ACMs under full containment."),
            ("Clearance Testing", "Independent air testing confirms clearance before containment is removed."),
        ],
        "matters_stats": [
            ("Pre-1980", "Homes built before 1980 are primary asbestos risk"),
            ("OSHA", "Asbestos is federally regulated by OSHA and EPA"),
            ("24/7", "Guardian available around the clock"),
            ("500+", "Vetted contractors in our network"),
        ],
        "why_cards": [
            ("🛡️", "State-Licensed Contractors Only", "All abatement contractors hold required state licensing and EPA certification."),
            ("📋", "Full Documentation", "Permits, waste manifests, and clearance reports provided for insurance and compliance."),
            ("🔬", "Clearance Testing Included", "Independent post-abatement air testing is part of every project."),
            ("🌎", "Nationwide Network", "Licensed abatement contractors in every major market."),
            ("📞", "Single Point of Contact", "One call manages testing, abatement, clearance, and claim coordination."),
            ("✅", "Regulatory Compliance", "All work meets EPA NESHAP, OSHA, and applicable state regulations."),
        ],
        "checkpoints": [
            "All abatement contractors hold required state licenses and EPA certification",
            "Work performed under full containment with negative air pressure",
            "Independent clearance testing required before containment removal",
            "Complete regulatory documentation provided for insurance and legal compliance",
        ],
        "faqs": [
            ("Does homeowners insurance cover asbestos abatement?",
             "Coverage depends on the cause. If asbestos is discovered during a covered restoration event — like fire or water damage — abatement is often covered as part of that claim. Standalone asbestos removal without a triggering event is typically not covered. We confirm your specific situation. Call 888-625-0666 and we will help you right away."),
            ("How do I know if my home has asbestos?",
             "You cannot tell by looking. Asbestos-containing materials (ACMs) require laboratory testing to confirm. Materials at elevated risk include popcorn ceilings, vinyl floor tiles, pipe insulation, drywall joint compound, and roofing shingles in homes built before 1980. We dispatch licensed inspectors for bulk sampling. Call 888-625-0666 and we will help you right away."),
            ("Is asbestos dangerous if left alone?",
             "Asbestos that is in good condition and not disturbed is generally lower risk. Asbestos that is deteriorating or will be disturbed by renovation or restoration work must be tested and abated before work begins. Disturbing asbestos releases fibers that cause mesothelioma and asbestosis. Call 888-625-0666 and we will help you right away."),
            ("Why must asbestos be removed before restoration?",
             "Any restoration work — sanding, cutting, demolition — that disturbs asbestos-containing materials releases carcinogenic fibers. Federal and state regulations require licensed abatement before any renovation or restoration work in buildings with identified ACMs. Call 888-625-0666 and we will help you right away."),
            ("How long does asbestos abatement take?",
             "A single room can take 1–3 days for testing, abatement, and clearance. Whole-house abatement can take 1–2 weeks. Timeline depends on the number of materials affected and regulatory clearance requirements. Call 888-625-0666 and we will help you right away."),
            ("What is post-abatement clearance testing?",
             "Clearance testing is an independent air quality test performed after abatement is complete. It confirms that airborne asbestos fiber counts are within EPA clearance levels before containment is removed and the space is re-occupied. Clearance testing is required by law in most jurisdictions. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian handle asbestos abatement claims?",
             "We confirm your active coverage, dispatch a licensed inspector, document the scope and testing results, and coordinate with your insurance carrier if abatement is part of a covered claim. We work directly with your insurer on billing where covered — you handle your deductible, we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },

    "general-contractor": {
        "name": "Reconstruction & General Contracting",
        "slug": "general-contractor",
        "national_url": "/general-contractor/",
        "city_slug_prefix": "general-contractor",
        "icon": "🔨",
        "h1_national": "Reconstruction & General Contracting — <span>Nationwide</span>",
        "hero_sub": "Post-damage reconstruction, new construction, and direct-pay projects. Insurance rebuilds and all trades. We confirm your coverage, manage your claim, and dispatch vetted licensed general contractors.",
        "badge": "Licensed General Contractors — All 50 States",
        "trust_items": ["Coverage Confirmed Fast", "Insurance Reconstruction", "All Trades Coordinated", "Residential & Commercial", "All 50 States Served"],
        "damage_types": [
            ("🔥", "Post-Fire Reconstruction"), ("💧", "Post-Water Damage Rebuild"), ("🌪️", "Storm Damage Rebuild"),
            ("🏗️", "Post-Asbestos Abatement"), ("🏠", "Full Home Reconstruction"), ("🏢", "Commercial Rebuild"),
            ("🔨", "New Construction"), ("💰", "Direct-Pay Projects"),
        ],
        "scope_items": [
            ("Roofing — All Materials", "Asphalt shingle, metal, tile, and flat roof systems. Insurance replacement and new construction."),
            ("Framing & Structural Repair", "Load-bearing walls, trusses, and structural members repaired or replaced per engineering specifications."),
            ("Electrical Systems", "Licensed electricians handle full panel replacement, wiring, and code compliance upgrades."),
            ("Plumbing Systems", "Licensed plumbers handle pipe replacement, fixture installation, and water heater replacement."),
            ("HVAC Systems", "Full HVAC replacement, ductwork, and ventilation systems by certified technicians."),
            ("Drywall, Insulation & Interior", "Drywall installation, taping, texturing, insulation, and interior finish work."),
            ("Flooring — All Types", "Hardwood, LVP, tile, carpet, and concrete flooring installation and replacement."),
            ("Windows, Doors & Exterior", "Window and door replacement, siding, trim, and exterior finish work to match existing."),
        ],
        "how_helps": [
            ("01", "Confirm Property Ownership", "We verify you are the authorized owner or representative."),
            ("02", "Confirm Active Coverage", "We confirm your policy covers reconstruction following the triggering damage event."),
            ("03", "Scope of Work Development", "We coordinate with your insurance adjuster to develop a comprehensive scope of work."),
            ("04", "Document for Your Claim", "All pre-construction damage documentation submitted to your carrier before work begins."),
            ("05", "Manage Your Carrier", "We coordinate with your insurance carrier throughout the entire reconstruction project."),
            ("06", "Dispatch Licensed GC", "We connect you with a vetted, licensed general contractor and manage the project through completion."),
        ],
        "expect_steps": [
            ("Call Us", "Call 888-625-0666. We confirm your coverage and begin coordinating your rebuild."),
            ("Coverage Confirmed", "We confirm your reconstruction coverage and work with your adjuster on scope."),
            ("Licensed GC Dispatched", "A vetted, licensed general contractor is assigned to your project."),
            ("Project Managed", "We manage the rebuild with your insurance carrier from demo to final walk-through."),
        ],
        "matters_stats": [
            ("$80K+", "Average major damage reconstruction claim"),
            ("All Trades", "Roofing, framing, electrical, plumbing, HVAC, and finish work"),
            ("24/7", "Guardian available around the clock"),
            ("500+", "Vetted contractors in our network"),
        ],
        "why_cards": [
            ("🛡️", "Licensed Contractors Only", "Every GC in our network is licensed, insured, bonded, and vetted."),
            ("📋", "Full Claim Management", "We handle all documentation and coordination with your insurer throughout the rebuild."),
            ("🔨", "All Trades Covered", "Roofing, framing, electrical, plumbing, HVAC, drywall, flooring, and exterior."),
            ("🌎", "Nationwide Network", "Licensed general contractors in every major market."),
            ("📞", "Single Point of Contact", "One team manages everything — insurance, contractor, and project completion."),
            ("✅", "Insurance & Direct-Pay", "We handle insurance reconstruction and direct-pay projects. Residential and commercial."),
        ],
        "checkpoints": [
            "We confirm your reconstruction coverage and work with your adjuster on scope",
            "All contractors are licensed, insured, bonded, and vetted by Guardian",
            "We manage the project with your insurance carrier from start to final inspection",
            "We work directly with your insurer on billing — you pay your deductible only",
        ],
        "faqs": [
            ("Does homeowners insurance cover reconstruction after damage?",
             "Yes — standard homeowners insurance policies include dwelling coverage that pays to rebuild or repair your home after a covered loss. Coverage typically includes all trades necessary to restore the property to pre-loss condition. We confirm your specific reconstruction coverage fast. Call 888-625-0666 and we will help you right away."),
            ("What is the difference between restoration and reconstruction?",
             "Restoration refers to returning a property to its pre-damage condition through cleaning, drying, and minor repairs. Reconstruction involves rebuilding structural elements — framing, roofing, electrical, plumbing — that cannot be restored. Major damage events typically require both. Call 888-625-0666 and we will help you right away."),
            ("How long does home reconstruction take after major damage?",
             "Minor reconstruction can take weeks. Major fire, storm, or flood damage requiring full or partial rebuilds can take several months depending on scope, permitting, and materials availability. We manage the timeline with your insurance carrier. Call 888-625-0666 and we will help you right away."),
            ("Can I hire my own contractor for insurance reconstruction?",
             "Yes — you have the right to choose your own contractor. Your insurance carrier cannot require you to use their preferred contractors. We help you navigate that process and advocate on your behalf with your carrier. Call 888-625-0666 and we will help you right away."),
            ("Does insurance cover code upgrades during reconstruction?",
             "Many policies include ordinance or law coverage, which pays for code-required upgrades during reconstruction. This varies by policy. We review your coverage and document any code upgrade requirements for your claim. Call 888-625-0666 and we will help you right away."),
            ("Do you handle commercial reconstruction?",
             "Yes — Guardian dispatches licensed general contractors for both residential and commercial reconstruction. Insurance rebuilds, direct-pay projects, tenant improvement, and post-damage commercial restoration are all within our contractor network's capabilities. Call 888-625-0666 and we will help you right away."),
            ("How does Guardian handle reconstruction claims with insurance?",
             "We confirm your active dwelling coverage, coordinate the scope of work with your adjuster, dispatch a vetted licensed GC, and manage the project with your insurance carrier from demolition to final inspection. You handle your deductible — we handle the rest. Call 888-625-0666 and we will help you right away."),
        ],
    },
}


# ─── CITY DEFINITIONS ────────────────────────────────────────────────────────

CITIES = {

    # ── OREGON ──────────────────────────────────────────────────────────────
    "portland-or": {
        "city": "Portland",
        "state": "Oregon",
        "abbrev": "OR",
        "context": {
            "water-damage": "Portland receives over 40 inches of annual rainfall with an extended wet season from October through May. Atmospheric rivers, Pacific windstorms, and occasional ice storms create significant water damage risk. The combined sewer system causes sewage backups during heavy rain events. Older housing stock — particularly pre-1980 homes in Southeast and Northeast Portland — carries elevated mold and asbestos risk.",
            "fire-damage": "Portland's older housing stock, including bungalows and Craftsman homes dating to the early 1900s, carries elevated fire risk from aging electrical systems. Dry summer conditions increase wildfire smoke intrusion risk in surrounding areas.",
            "mold-remediation": "Portland's wet climate and older housing stock create significant mold risk. Extended periods of high humidity combined with poor ventilation in older homes allow mold to establish in walls, crawl spaces, and attics. Post-water damage mold is a common secondary issue in the Portland metro area.",
            "storm-damage": "Portland experiences Pacific windstorms, atmospheric rivers, and ice storms that cause significant roof and structural damage. The Columbia River Gorge acts as a wind tunnel, amplifying storm impacts in the east metro area.",
            "biohazard-cleanup": "Portland's combined sewer system causes basement sewage backups during heavy rain events, particularly in older neighborhoods. The city also has a significant population requiring unattended death and hoarding cleanup services.",
            "asbestos-abatement": "A large percentage of Portland's housing stock predates 1980, making asbestos a significant concern in popcorn ceilings, floor tiles, pipe insulation, and drywall compound in older homes across all Portland neighborhoods.",
            "general-contractor": "Portland has a strong demand for insurance reconstruction contractors following water, fire, and storm damage events. The city's older housing stock requires contractors experienced in working with historic materials and current code requirements.",
        }
    },
    "salem-or": {
        "city": "Salem",
        "state": "Oregon",
        "abbrev": "OR",
        "context": {
            "water-damage": "Salem sits in the Willamette Valley and receives over 40 inches of annual rainfall. Seasonal flooding from the Willamette River and its tributaries creates significant water intrusion risk for homes in low-lying areas. Older housing stock throughout the city is susceptible to foundation seepage and pipe failures during hard freezes.",
            "fire-damage": "Salem's older residential neighborhoods contain Craftsman and Victorian-era homes with aging electrical systems that carry elevated fire risk. Dry Willamette Valley summers increase wildfire smoke exposure and the risk of structure fires.",
            "mold-remediation": "Salem's valley location and high annual rainfall create persistent moisture conditions ideal for mold growth. Older rental housing near Willamette University and downtown Salem is particularly susceptible to wall cavity and crawl space mold.",
            "storm-damage": "Salem experiences Pacific windstorms and atmospheric river events that cause roof damage and downed trees throughout the area. Ice storms occur periodically in winter, causing structural damage to older roofing systems.",
            "biohazard-cleanup": "Salem's older sewer infrastructure causes backups during heavy rainfall events. The city also has consistent demand for unattended death, hoarding, and biohazard cleanup services across its residential and commercial properties.",
            "asbestos-abatement": "Salem has a substantial inventory of pre-1980 housing, particularly in its historic neighborhoods. Asbestos is commonly found in popcorn ceilings, vinyl floor tiles, pipe insulation, and joint compound throughout older Salem homes.",
            "general-contractor": "Salem's role as Oregon's state capital brings steady demand for licensed general contractors handling insurance reconstruction for both residential properties and government-adjacent commercial buildings damaged by water, fire, or storm events.",
        }
    },
    "eugene-or": {
        "city": "Eugene",
        "state": "Oregon",
        "abbrev": "OR",
        "context": {
            "water-damage": "Eugene receives over 47 inches of annual rainfall and sits near the Willamette River, creating significant flood and water intrusion risk. High-density older rental housing near the University of Oregon is particularly vulnerable to deferred maintenance water damage, pipe failures, and appliance overflow events.",
            "fire-damage": "Eugene's large stock of older rental housing near the University of Oregon carries elevated fire risk from aging electrical systems and deferred maintenance. Dry Lane County summers create wildfire risk in surrounding areas that can affect air quality and cause smoke intrusion.",
            "mold-remediation": "Eugene's high annual rainfall and large population of older rental homes create persistent mold problems. Poor ventilation in older structures near the university and downtown Eugene allows mold to establish quickly after any water event.",
            "storm-damage": "Eugene experiences powerful Pacific windstorms and atmospheric river events that cause significant roof damage, fallen trees, and structural impacts. The Willamette Valley's geography funnels storm systems through the Eugene area with regularity.",
            "biohazard-cleanup": "Eugene's combined sewer areas and older residential neighborhoods experience sewage backups during major rain events. The city also has demand for crime scene, unattended death, and hoarding cleanup services.",
            "asbestos-abatement": "Eugene has a high concentration of pre-1980 housing stock, particularly in older neighborhoods and student rental areas near the University of Oregon. Asbestos is present in many of these homes in popcorn ceilings, floor tiles, pipe insulation, and drywall compound.",
            "general-contractor": "Eugene's mix of older residential housing, university-adjacent properties, and commercial buildings creates consistent demand for licensed general contractors managing insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "bend-or": {
        "city": "Bend",
        "state": "Oregon",
        "abbrev": "OR",
        "context": {
            "water-damage": "Bend's high desert climate brings cold winters with hard freezes that cause pipe bursts — the number one source of water damage in the area. Rapid spring snowmelt creates roof leak and foundation seepage events. The city's fast growth means many newer homes alongside older structures with varying maintenance histories.",
            "fire-damage": "Bend sits in the wildland-urban interface with significant wildfire risk during dry Central Oregon summers. The surrounding Deschutes National Forest creates ongoing ember and smoke intrusion risk. Many Bend homes have sustained fire and smoke damage from nearby wildfires in recent years.",
            "mold-remediation": "While Bend is drier than western Oregon, pipe burst events and roof leaks during winter create localized moisture conditions that lead to mold growth if not addressed immediately. Crawl spaces and attics in older Bend homes are common mold sites.",
            "storm-damage": "Bend experiences winter snow loads that can cause roof collapse or damage in older structures. Wind events are common in spring and fall. Hail storms in summer cause roof and siding damage throughout the Bend metro area.",
            "biohazard-cleanup": "Bend has consistent demand for biohazard, unattended death, and hoarding cleanup services across its residential and vacation rental property market. The area's short-term rental inventory creates unique cleanup needs.",
            "asbestos-abatement": "Bend has a mix of pre-1980 housing in its older core neighborhoods and newer construction in surrounding developments. Pre-1980 homes contain asbestos in common materials including popcorn ceilings, floor tiles, and pipe insulation.",
            "general-contractor": "Bend's rapidly growing real estate market and wildland-urban interface location create strong demand for licensed general contractors handling insurance reconstruction after fire, storm, and water damage events.",
        }
    },
    "medford-or": {
        "city": "Medford",
        "state": "Oregon",
        "abbrev": "OR",
        "context": {
            "water-damage": "Medford's Rogue Valley location brings cold winters with periodic hard freezes that cause pipe bursts and water damage. The city serves as the regional hub for all of southern Oregon, with a mix of older downtown housing and newer suburban development across the valley.",
            "fire-damage": "Medford and the surrounding Rogue Valley have sustained significant wildfire damage in recent years, including the 2020 Almeda Fire that destroyed thousands of homes in nearby Talent and Phoenix. Wildfire smoke and ember intrusion remain major risks for Medford properties during dry summers.",
            "mold-remediation": "Medford's Rogue Valley location with hot dry summers and cold wet winters creates seasonal moisture fluctuations that drive mold growth in older homes. Post-water damage mold is a common issue in the area's aging residential stock.",
            "storm-damage": "Medford experiences winter ice storms, wind events, and occasional heavy snowfall that cause roof and structural damage. The valley's geography can concentrate storm impacts in specific neighborhoods.",
            "biohazard-cleanup": "Medford serves as the regional center for southern Oregon, creating demand for biohazard, crime scene, unattended death, and hoarding cleanup services across a wide geographic area including surrounding rural communities.",
            "asbestos-abatement": "Medford's older downtown and established residential neighborhoods contain significant pre-1980 housing stock with asbestos in popcorn ceilings, vinyl floor tiles, pipe insulation, and drywall compound.",
            "general-contractor": "Medford's role as the commercial and services hub for southern Oregon creates strong demand for licensed general contractors handling insurance reconstruction after the region's frequent fire, storm, and water damage events.",
        }
    },
    "corvallis-or": {
        "city": "Corvallis",
        "state": "Oregon",
        "abbrev": "OR",
        "context": {
            "water-damage": "Corvallis receives over 44 inches of annual rainfall and has a large stock of older rental housing near Oregon State University that is particularly vulnerable to deferred maintenance water damage. The Willamette River creates flood risk for properties in low-lying areas of the city.",
            "fire-damage": "Corvallis has a large inventory of older residential and academic buildings near Oregon State University with aging electrical systems. Dry Willamette Valley summers increase fire risk in surrounding areas.",
            "mold-remediation": "Corvallis's high rainfall and large population of older rental properties near Oregon State University create persistent mold problems. Poor ventilation in older homes and student housing allows mold to establish quickly after water events.",
            "storm-damage": "Corvallis experiences Pacific windstorms and atmospheric river events that cause roof damage and structural impacts throughout the city. Older campus-area housing is particularly vulnerable to storm damage.",
            "biohazard-cleanup": "Corvallis has consistent demand for biohazard, unattended death, and hoarding cleanup services in its residential and rental property market, particularly in older student housing areas.",
            "asbestos-abatement": "Corvallis has a high concentration of pre-1980 housing, particularly in older neighborhoods and student rental areas near Oregon State University. Asbestos is commonly present in these homes in popcorn ceilings, floor tiles, pipe insulation, and drywall compound.",
            "general-contractor": "Corvallis's mix of older residential housing, university-adjacent properties, and commercial buildings creates demand for licensed general contractors managing insurance reconstruction after water, storm, and fire damage events.",
        }
    },

    # ── WASHINGTON ───────────────────────────────────────────────────────────
    "seattle-wa": {
        "city": "Seattle",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Seattle receives 38 inches of annual rainfall with an extended wet season from October through June. The marine climate creates persistent moisture conditions. Combined sewer systems in Capitol Hill, Central District, and the International District cause sewage backups during heavy rain. Significant pre-1980 housing stock throughout the city.",
            "fire-damage": "Seattle's older neighborhoods — Capitol Hill, Queen Anne, Ballard — contain housing stock dating to the early 1900s with aging electrical systems. Dry summers increase fire risk in residential structures.",
            "mold-remediation": "Seattle's extended wet season and marine climate create persistent mold risk in crawl spaces, attics, and wall cavities. Older rental housing in university-adjacent neighborhoods is particularly susceptible.",
            "storm-damage": "Seattle experiences Pacific windstorms, atmospheric rivers, and occasional heavy snowfall that cause roof and structural damage. The Puget Sound area is subject to convergence zone weather patterns that intensify local storm impacts.",
            "biohazard-cleanup": "Seattle's combined sewer areas in older neighborhoods experience sewage backups during major rain events. The city also has demand for crime scene, unattended death, and biohazard cleanup services.",
            "asbestos-abatement": "Seattle has a significant inventory of pre-1980 housing across all neighborhoods, with asbestos present in popcorn ceilings, floor tiles, pipe insulation, and HVAC systems common to that era.",
            "general-contractor": "Seattle's strong real estate market and older housing stock create consistent demand for licensed general contractors handling insurance reconstruction and renovation projects.",
        }
    },
    "spokane-wa": {
        "city": "Spokane",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Spokane's continental climate brings cold winters with hard freezes that cause pipe bursts and water damage throughout the city. Spring snowmelt from the surrounding mountains creates flood risk in low-lying areas. The Spokane River runs through the city, adding flood exposure for riverside properties.",
            "fire-damage": "Spokane sits in Eastern Washington where dry summers and wind-driven conditions create significant wildfire risk. The city's older South Hill and West Central neighborhoods contain pre-1900s housing with aging electrical systems that carry elevated fire risk.",
            "mold-remediation": "Spokane's climate swings — wet winters and dry summers — create seasonal moisture conditions that drive mold growth in older homes. Crawl spaces and basements in Spokane's older housing stock are common mold sites following pipe burst or water intrusion events.",
            "storm-damage": "Spokane experiences severe winter storms with heavy snow loads that cause roof damage in older structures. Windstorms are common in spring and fall and cause significant roof and structural damage throughout the Spokane metro area.",
            "biohazard-cleanup": "Spokane has consistent demand for biohazard, crime scene, unattended death, and hoarding cleanup services across its residential neighborhoods. The city serves as the regional hub for eastern Washington and northern Idaho.",
            "asbestos-abatement": "Spokane has a large inventory of pre-1980 housing, particularly in its established South Hill, Browne's Addition, and West Central neighborhoods. Asbestos is commonly found in popcorn ceilings, floor tiles, pipe insulation, and drywall compound in these older homes.",
            "general-contractor": "Spokane's position as eastern Washington's largest city creates strong demand for licensed general contractors handling insurance reconstruction after the region's frequent water, fire, and storm damage events.",
        }
    },
    "tacoma-wa": {
        "city": "Tacoma",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Tacoma receives over 38 inches of annual rainfall and has a large inventory of older housing in neighborhoods like Hilltop, South End, and the Dome District that are vulnerable to water intrusion and pipe failures. Combined sewer areas experience backups during major rain events.",
            "fire-damage": "Tacoma's older residential neighborhoods contain Craftsman and Victorian-era homes with aging electrical systems that carry elevated fire risk. Industrial history in parts of the city adds complexity to fire restoration in mixed-use areas.",
            "mold-remediation": "Tacoma's marine climate and extended wet season create persistent mold risk in older homes. Crawl spaces and basements in Tacoma's established neighborhoods are common mold sites, particularly following water damage events.",
            "storm-damage": "Tacoma is exposed to Pacific windstorms and atmospheric river events that cause significant roof and structural damage. The city's location on Puget Sound amplifies storm impacts in waterfront and elevated neighborhoods.",
            "biohazard-cleanup": "Tacoma has consistent demand for biohazard, unattended death, crime scene, and hoarding cleanup services across its diverse residential neighborhoods. Older multi-family housing creates recurring sewage backup cleanup needs.",
            "asbestos-abatement": "Tacoma has a substantial inventory of pre-1980 housing across all neighborhoods, with asbestos present in popcorn ceilings, vinyl floor tiles, pipe insulation, and HVAC insulation in older structures throughout the city.",
            "general-contractor": "Tacoma's strong real estate market and large stock of older housing create consistent demand for licensed general contractors managing insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "vancouver-wa": {
        "city": "Vancouver",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Vancouver WA receives over 42 inches of annual rainfall and sits directly across the Columbia River from Portland. The city's rapid growth has brought a mix of older established neighborhoods and newer developments, all subject to the Pacific Northwest's extended wet season and storm-driven water intrusion events.",
            "fire-damage": "Vancouver WA's older neighborhoods contain aging housing stock with elevated fire risk from outdated electrical systems. The city's proximity to the Columbia River Gorge creates exposure to wind-driven fire conditions during dry eastern wind events.",
            "mold-remediation": "Vancouver WA's wet climate and mix of older and newer housing stock create consistent mold risk. Crawl spaces, attics, and wall cavities in older Vancouver neighborhoods are common mold sites following water damage events.",
            "storm-damage": "Vancouver WA experiences the same Pacific windstorms and atmospheric river events as Portland, with the Columbia River Gorge amplifying wind impacts in eastern parts of the city. Ice storms occur periodically in winter.",
            "biohazard-cleanup": "Vancouver WA has consistent demand for biohazard, unattended death, sewage backup, and hoarding cleanup services across its rapidly growing residential market.",
            "asbestos-abatement": "Vancouver WA has a significant inventory of pre-1980 housing in its established neighborhoods. Asbestos is commonly found in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout older Vancouver homes.",
            "general-contractor": "Vancouver WA's rapid population growth and mix of older and newer housing stock create strong demand for licensed general contractors handling insurance reconstruction after the region's frequent water, fire, and storm damage events.",
        }
    },
    "bellevue-wa": {
        "city": "Bellevue",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Bellevue's Eastside location receives significant annual rainfall and is subject to the same extended Pacific Northwest wet season as Seattle. Hillside properties in Bellevue face elevated landslide and water intrusion risk during atmospheric river events.",
            "fire-damage": "Bellevue's mix of older residential neighborhoods and newer high-value construction creates diverse fire risk profiles. Aging electrical systems in older Bellevue homes and dry summer conditions increase fire exposure.",
            "mold-remediation": "Bellevue's wet climate and hillside topography create persistent moisture conditions that drive mold growth in crawl spaces, attics, and wall cavities. High-value homes in Bellevue require careful, professional mold remediation to protect property values.",
            "storm-damage": "Bellevue experiences Pacific windstorms and heavy rainfall events that cause roof damage, fallen trees, and landslides on hillside properties. The city's tree canopy creates significant storm damage risk during wind events.",
            "biohazard-cleanup": "Bellevue has consistent demand for biohazard, unattended death, and hoarding cleanup services across its residential and commercial properties.",
            "asbestos-abatement": "Bellevue has older residential neighborhoods with pre-1980 housing stock containing asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Many renovation and restoration projects require abatement before work can begin.",
            "general-contractor": "Bellevue's high-value real estate market creates strong demand for licensed general contractors managing insurance reconstruction to pre-loss quality standards after water, fire, and storm damage events.",
        }
    },
    "kent-wa": {
        "city": "Kent",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Kent sits in the Green River Valley and has a history of flooding risk. The city receives significant annual rainfall and has older residential neighborhoods vulnerable to water intrusion and pipe failures during extended wet season events.",
            "fire-damage": "Kent's mix of older residential housing and industrial areas creates diverse fire risk. Older residential neighborhoods contain aging electrical systems that increase structure fire risk.",
            "mold-remediation": "Kent's valley location and wet climate create persistent moisture conditions that drive mold growth in older homes. Crawl spaces in Kent's established residential neighborhoods are common mold sites following water damage.",
            "storm-damage": "Kent experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage throughout the city. The Green River Valley's geography can concentrate storm impacts in low-lying areas.",
            "biohazard-cleanup": "Kent has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services across its diverse residential and commercial properties.",
            "asbestos-abatement": "Kent has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, vinyl floor tiles, pipe insulation, and drywall compound throughout its older residential neighborhoods.",
            "general-contractor": "Kent's large residential market creates consistent demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events throughout the Green River Valley.",
        }
    },
    "everett-wa": {
        "city": "Everett",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Everett receives significant annual rainfall as part of the Puget Sound region's extended wet season. The city's older residential neighborhoods and proximity to waterways create water intrusion, flooding, and pipe failure risks throughout the year.",
            "fire-damage": "Everett's older residential neighborhoods in the downtown core and Bayside area contain aging housing stock with elevated fire risk. Industrial history near the waterfront adds complexity to fire restoration in mixed-use areas.",
            "mold-remediation": "Everett's wet climate and older housing stock create persistent mold risk in crawl spaces, attics, and wall cavities. Post-water damage mold is a common secondary issue in Everett's established residential neighborhoods.",
            "storm-damage": "Everett is exposed to Pacific windstorms and convergence zone weather events that intensify local storm impacts. The city's Puget Sound waterfront location amplifies wind and rain damage during major storm events.",
            "biohazard-cleanup": "Everett has consistent demand for biohazard, unattended death, crime scene, and sewage backup cleanup services across its residential and commercial properties.",
            "asbestos-abatement": "Everett has a large inventory of pre-1980 housing throughout its established neighborhoods, with asbestos commonly present in popcorn ceilings, floor tiles, pipe insulation, and HVAC systems.",
            "general-contractor": "Everett's residential market and older housing stock create strong demand for licensed general contractors handling insurance reconstruction after the region's frequent water, fire, and storm damage events.",
        }
    },
    "spokane-valley-wa": {
        "city": "Spokane Valley",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Spokane Valley shares Eastern Washington's continental climate, with cold winters that cause pipe bursts and spring snowmelt that creates flood risk. The Spokane River runs through the area, adding water intrusion exposure for nearby properties.",
            "fire-damage": "Spokane Valley's location in eastern Washington's dry climate zone creates significant wildfire risk during summer months. The city's residential neighborhoods contain older homes with aging electrical systems that carry elevated fire risk.",
            "mold-remediation": "Spokane Valley's climate — wet winters and dry summers — creates seasonal moisture conditions that drive mold in older homes. Crawl spaces and basements following pipe burst or water intrusion events are common mold sites.",
            "storm-damage": "Spokane Valley experiences severe winter storms with heavy snow loads that damage older roofing systems. Spring and fall windstorms cause roof and structural damage throughout the community.",
            "biohazard-cleanup": "Spokane Valley has consistent demand for biohazard, unattended death, and hoarding cleanup services. As a large suburban community east of Spokane, it generates significant residential cleanup needs.",
            "asbestos-abatement": "Spokane Valley has pre-1980 housing stock throughout its established residential areas, with asbestos present in popcorn ceilings, floor tiles, pipe insulation, and drywall compound in older homes.",
            "general-contractor": "Spokane Valley's large residential market creates steady demand for licensed general contractors managing insurance reconstruction after the area's frequent water, fire, and storm damage events.",
        }
    },
    "renton-wa": {
        "city": "Renton",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Renton sits at the south end of Lake Washington and receives significant annual rainfall. The city's hillside neighborhoods face landslide and water intrusion risk during heavy rain events. Cedar River flooding creates water damage exposure for properties in low-lying areas.",
            "fire-damage": "Renton's mix of older residential neighborhoods and newer commercial development creates diverse fire risk profiles. Older homes in established Renton neighborhoods carry elevated risk from aging electrical systems.",
            "mold-remediation": "Renton's wet climate and hillside topography create persistent moisture conditions that drive mold in crawl spaces and wall cavities. Post-water damage mold is a common issue in older Renton residential properties.",
            "storm-damage": "Renton experiences Pacific windstorms and heavy rainfall that cause roof damage and landslides on hillside properties. The Cedar River corridor creates flood risk during major storm events.",
            "biohazard-cleanup": "Renton has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services across its growing residential and commercial market.",
            "asbestos-abatement": "Renton has older residential neighborhoods with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Renovation and restoration projects frequently require abatement.",
            "general-contractor": "Renton's strong real estate market creates consistent demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "federal-way-wa": {
        "city": "Federal Way",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Federal Way receives significant annual rainfall as part of the Puget Sound region's extended wet season. The city's residential neighborhoods include older housing stock vulnerable to water intrusion and pipe failures during prolonged wet weather.",
            "fire-damage": "Federal Way's older residential neighborhoods contain aging housing stock with elevated fire risk from outdated electrical systems. The city's mix of housing types creates diverse fire restoration needs.",
            "mold-remediation": "Federal Way's wet climate and older housing stock create persistent mold risk in crawl spaces and wall cavities. Post-water damage mold is a common issue in the city's established residential neighborhoods.",
            "storm-damage": "Federal Way experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage throughout the city. The area's tree canopy creates significant storm damage risk during wind events.",
            "biohazard-cleanup": "Federal Way has consistent demand for biohazard, unattended death, sewage backup, and hoarding cleanup services across its large residential market.",
            "asbestos-abatement": "Federal Way has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, vinyl floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Federal Way's large residential market creates strong demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "yakima-wa": {
        "city": "Yakima",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Yakima's semi-arid high desert climate brings cold winters with hard freezes that cause pipe bursts — the primary source of water damage in the area. Irrigation infrastructure throughout the Yakima Valley creates additional water intrusion risk for agricultural and residential properties.",
            "fire-damage": "Yakima sits in central Washington's dry climate zone with significant wildfire risk during hot dry summers. The city's older residential neighborhoods contain pre-1960s housing with aging electrical systems that carry elevated fire risk.",
            "mold-remediation": "While Yakima is drier than western Washington, pipe burst events and irrigation leaks create localized moisture conditions that lead to mold growth if not addressed immediately. Older homes in Yakima's historic neighborhoods are common mold sites.",
            "storm-damage": "Yakima experiences wind events, dust storms, and occasional heavy snow that cause roof and structural damage. Spring windstorms are particularly damaging to older roofing systems throughout the Yakima Valley.",
            "biohazard-cleanup": "Yakima has consistent demand for biohazard, unattended death, and hoarding cleanup services as the regional hub for central Washington's agricultural communities.",
            "asbestos-abatement": "Yakima has a significant inventory of pre-1980 housing, particularly in its historic downtown neighborhoods. Asbestos is present in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout older Yakima homes.",
            "general-contractor": "Yakima's role as central Washington's commercial hub creates demand for licensed general contractors handling insurance reconstruction for both residential properties and agricultural support facilities.",
        }
    },
    "bellingham-wa": {
        "city": "Bellingham",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Bellingham receives over 35 inches of annual rainfall and has an extended wet season as part of the Pacific Northwest marine climate. The city's hillside neighborhoods face water intrusion and landslide risk during major storm events. Whatcom Creek and other waterways create flood exposure for low-lying properties.",
            "fire-damage": "Bellingham's older Fairhaven and Sehome neighborhoods contain historic housing with aging electrical systems that carry elevated fire risk. Dry eastern slope conditions during summer increase wildfire smoke exposure.",
            "mold-remediation": "Bellingham's wet marine climate creates persistent mold risk in crawl spaces, attics, and wall cavities throughout the city. Older housing near Western Washington University is particularly susceptible to mold following water damage events.",
            "storm-damage": "Bellingham experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage. The city's hillside topography and proximity to the Strait of Georgia amplify storm impacts in elevated neighborhoods.",
            "biohazard-cleanup": "Bellingham has consistent demand for biohazard, unattended death, and hoarding cleanup services as the primary city in Whatcom County and the regional hub near the Canadian border.",
            "asbestos-abatement": "Bellingham has a large inventory of pre-1980 housing in its historic neighborhoods, with asbestos present in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout older Bellingham homes.",
            "general-contractor": "Bellingham's growing real estate market and older housing stock create strong demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "kirkland-wa": {
        "city": "Kirkland",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Kirkland's Lake Washington waterfront location and hillside neighborhoods create elevated water intrusion risk during the Pacific Northwest's extended wet season. Hillside properties face landslide risk during heavy rain events.",
            "fire-damage": "Kirkland's older residential neighborhoods contain aging housing stock with elevated fire risk. High-value waterfront and hillside properties require specialized fire restoration contractors experienced with premium finishes.",
            "mold-remediation": "Kirkland's wet climate and hillside topography create persistent moisture conditions that drive mold in crawl spaces and wall cavities. High-value homes in Kirkland require professional mold remediation to protect property values.",
            "storm-damage": "Kirkland experiences Pacific windstorms and heavy rainfall events that cause roof damage, fallen trees, and landslides on hillside properties. The city's mature tree canopy creates significant storm damage risk during wind events.",
            "biohazard-cleanup": "Kirkland has consistent demand for biohazard, unattended death, and hoarding cleanup services across its affluent residential market.",
            "asbestos-abatement": "Kirkland has older residential neighborhoods with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, and pipe insulation. Renovation and restoration projects regularly require abatement before work can proceed.",
            "general-contractor": "Kirkland's high-value real estate market creates strong demand for licensed general contractors managing insurance reconstruction to premium standards after water, fire, and storm damage events.",
        }
    },
    "kennewick-wa": {
        "city": "Kennewick",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Kennewick's semi-arid Tri-Cities climate brings cold winters with hard freezes that cause pipe bursts. The Columbia River creates flood risk for riverside properties, and irrigation infrastructure throughout the region adds water intrusion exposure.",
            "fire-damage": "Kennewick sits in eastern Washington's dry climate zone with significant wildfire risk during hot dry summers. The city's older residential neighborhoods contain aging housing stock with elevated fire risk.",
            "mold-remediation": "While Kennewick is dry, pipe burst events and Columbia River flooding create localized moisture conditions that lead to mold if not addressed quickly. Older homes in Kennewick's established neighborhoods are common mold sites.",
            "storm-damage": "Kennewick experiences wind events and occasional heavy snow that cause roof and structural damage. The Columbia Basin's open geography amplifies wind impacts throughout the Tri-Cities area.",
            "biohazard-cleanup": "Kennewick serves as one of the three Tri-Cities commercial hubs, creating consistent demand for biohazard, unattended death, and hoarding cleanup services across the region.",
            "asbestos-abatement": "Kennewick has pre-1980 housing in its established neighborhoods with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. The area's older ranch-style homes frequently contain these materials.",
            "general-contractor": "Kennewick's Tri-Cities market creates demand for licensed general contractors handling insurance reconstruction for both residential properties and commercial facilities after water, fire, and storm damage events.",
        }
    },
    "auburn-wa": {
        "city": "Auburn",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Auburn sits in the Green River Valley and has a history of flooding risk. The city receives significant annual rainfall and has older residential neighborhoods vulnerable to water intrusion and pipe failures during extended wet season events.",
            "fire-damage": "Auburn's mix of older residential housing and industrial areas creates diverse fire risk profiles. Older residential neighborhoods contain aging electrical systems that increase structure fire risk.",
            "mold-remediation": "Auburn's valley location and wet climate create persistent moisture conditions that drive mold growth in older homes. Crawl spaces in Auburn's established residential neighborhoods are common mold sites following water damage.",
            "storm-damage": "Auburn experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage throughout the city. Green River flooding during major storm events creates water damage risk for low-lying properties.",
            "biohazard-cleanup": "Auburn has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services across its diverse residential and commercial properties.",
            "asbestos-abatement": "Auburn has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, vinyl floor tiles, pipe insulation, and drywall compound throughout its older residential neighborhoods.",
            "general-contractor": "Auburn's large residential market creates consistent demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events throughout the Green River Valley.",
        }
    },
    "redmond-wa": {
        "city": "Redmond",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Redmond's Eastside location receives significant annual rainfall and is subject to the Pacific Northwest's extended wet season. Hillside properties and areas near the Sammamish River face water intrusion and flooding risk during heavy rain events.",
            "fire-damage": "Redmond's mix of older residential neighborhoods and newer tech campus development creates diverse fire risk profiles. Older homes in established Redmond neighborhoods carry elevated risk from aging electrical systems.",
            "mold-remediation": "Redmond's wet climate and hillside topography create persistent moisture conditions that drive mold in crawl spaces and wall cavities. Post-water damage mold is a common issue in older Redmond residential properties.",
            "storm-damage": "Redmond experiences Pacific windstorms and heavy rainfall that cause roof damage and tree falls throughout the city. The Sammamish River corridor creates flood risk during major storm events.",
            "biohazard-cleanup": "Redmond has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services across its growing residential and commercial market.",
            "asbestos-abatement": "Redmond has older residential neighborhoods with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Renovation projects frequently require abatement.",
            "general-contractor": "Redmond's strong real estate market and mix of older and newer housing create consistent demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "pasco-wa": {
        "city": "Pasco",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Pasco's Tri-Cities location in eastern Washington brings cold winters with hard freezes that cause pipe bursts. The Columbia and Snake River confluence creates flood risk for riverside properties and irrigation infrastructure adds additional water exposure.",
            "fire-damage": "Pasco sits in eastern Washington's dry climate zone with significant wildfire risk during hot dry summers. The city's rapidly growing residential areas include both older homes with aging systems and newer construction.",
            "mold-remediation": "While Pasco is semi-arid, pipe burst events and river flooding create localized moisture conditions that lead to mold if not addressed promptly. Newer construction with improper moisture barriers is also a mold risk factor.",
            "storm-damage": "Pasco experiences wind events and occasional heavy snow that cause roof and structural damage. The Columbia Basin's open geography creates strong wind exposure throughout the Tri-Cities area.",
            "biohazard-cleanup": "Pasco serves as one of the fastest-growing Tri-Cities communities, creating consistent demand for biohazard, unattended death, and hoarding cleanup services.",
            "asbestos-abatement": "Pasco has older housing in established neighborhoods with asbestos in popcorn ceilings, floor tiles, and pipe insulation. Pre-1980 homes require testing and abatement before any renovation or restoration work.",
            "general-contractor": "Pasco's rapid growth and Tri-Cities market create demand for licensed general contractors handling insurance reconstruction for both residential properties and commercial facilities.",
        }
    },
    "marysville-wa": {
        "city": "Marysville",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Marysville receives significant annual rainfall as part of the Puget Sound region's extended wet season. The city sits in the Snohomish River delta area with flood risk for low-lying properties. Older and newer residential neighborhoods both face water intrusion risk during atmospheric river events.",
            "fire-damage": "Marysville's rapidly growing residential areas include older homes with aging electrical systems alongside newer construction. The city's proximity to forested areas creates wildfire smoke exposure during dry summers.",
            "mold-remediation": "Marysville's wet climate and growing residential base create persistent mold risk in crawl spaces and attics. Post-water damage mold is a common secondary issue following the area's frequent rainfall events.",
            "storm-damage": "Marysville experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage. Snohomish River flooding during major storms creates water damage risk for low-lying neighborhoods.",
            "biohazard-cleanup": "Marysville has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services as one of Snohomish County's fastest-growing communities.",
            "asbestos-abatement": "Marysville has older residential neighborhoods with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, and pipe insulation alongside newer construction.",
            "general-contractor": "Marysville's rapid growth creates strong demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events throughout northern Snohomish County.",
        }
    },
    "sammamish-wa": {
        "city": "Sammamish",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Sammamish's hillside location on the Sammamish Plateau receives significant annual rainfall. Hillside properties face water intrusion and landslide risk during heavy rain events. Lake Sammamish waterfront properties face additional water exposure.",
            "fire-damage": "Sammamish's newer planned community development includes homes with modern electrical systems, but older areas and dry summer conditions create fire risk. The city's forested setting increases wildfire smoke exposure.",
            "mold-remediation": "Sammamish's wet climate and hillside topography create persistent moisture conditions that drive mold in crawl spaces. High-value homes in Sammamish require professional mold remediation to protect property values.",
            "storm-damage": "Sammamish experiences Pacific windstorms and heavy rainfall that cause roof damage, fallen trees, and landslides on hillside properties. The Plateau's elevation amplifies wind impacts during major storm events.",
            "biohazard-cleanup": "Sammamish has consistent demand for biohazard, unattended death, and hoarding cleanup services across its affluent residential community.",
            "asbestos-abatement": "Sammamish has older residential areas with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, and pipe insulation. Renovation and restoration projects require abatement before work can begin.",
            "general-contractor": "Sammamish's high-value real estate market creates strong demand for licensed general contractors managing insurance reconstruction to premium standards after water, fire, and storm damage events.",
        }
    },
    "richland-wa": {
        "city": "Richland",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Richland's Tri-Cities location in eastern Washington brings cold winters with hard freezes that cause pipe bursts. The Columbia River creates flood risk for riverside properties and Richland's irrigation infrastructure adds additional water exposure for residential properties.",
            "fire-damage": "Richland sits adjacent to the Hanford Site in eastern Washington's dry climate zone with significant wildfire risk during hot summers. The city's residential neighborhoods include both historic post-war housing and newer construction.",
            "mold-remediation": "While Richland is semi-arid, pipe burst events and Columbia River flooding create localized moisture conditions that lead to mold growth if not addressed quickly. Older post-war ranch homes are common mold sites.",
            "storm-damage": "Richland experiences wind events and occasional heavy snow that cause roof and structural damage. The Columbia Basin's open geography creates strong wind exposure throughout the Tri-Cities area.",
            "biohazard-cleanup": "Richland serves one of the Tri-Cities communities with consistent demand for biohazard, unattended death, and hoarding cleanup services.",
            "asbestos-abatement": "Richland has significant pre-1980 housing stock from its post-war Atomic City development era. Many Richland homes contain asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound.",
            "general-contractor": "Richland's Tri-Cities market and historic post-war housing create demand for licensed general contractors handling insurance reconstruction for both residential properties and commercial facilities.",
        }
    },
    "lakewood-wa": {
        "city": "Lakewood",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Lakewood's location in Pierce County receives significant annual rainfall as part of the Puget Sound region's extended wet season. The city's older residential neighborhoods and proximity to American Lake create water intrusion risk during heavy rain events.",
            "fire-damage": "Lakewood's older residential neighborhoods contain aging housing stock with elevated fire risk from outdated electrical systems. Joint Base Lewis-McChord adjacency creates a large residential market with diverse restoration needs.",
            "mold-remediation": "Lakewood's wet climate and older housing stock create persistent mold risk in crawl spaces and wall cavities. Post-water damage mold is a common issue in Lakewood's established residential neighborhoods.",
            "storm-damage": "Lakewood experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage throughout the city. Older roofing systems in established neighborhoods are particularly vulnerable.",
            "biohazard-cleanup": "Lakewood has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services across its large residential market near Joint Base Lewis-McChord.",
            "asbestos-abatement": "Lakewood has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, vinyl floor tiles, pipe insulation, and drywall compound throughout its older residential neighborhoods.",
            "general-contractor": "Lakewood's large residential market near Joint Base Lewis-McChord creates consistent demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "shoreline-wa": {
        "city": "Shoreline",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Shoreline's location on the north edge of Seattle receives significant annual rainfall throughout the Pacific Northwest wet season. Older residential neighborhoods throughout Shoreline face water intrusion and pipe failure risk during extended wet weather.",
            "fire-damage": "Shoreline's established residential neighborhoods contain older housing stock with aging electrical systems that carry elevated fire risk. The city's suburban character creates a large single-family home restoration market.",
            "mold-remediation": "Shoreline's wet climate and older housing stock create persistent mold risk in crawl spaces, attics, and wall cavities. Post-water damage mold is a common secondary issue in Shoreline's established neighborhoods.",
            "storm-damage": "Shoreline experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage. The city's mature tree canopy creates significant storm damage risk during wind events.",
            "biohazard-cleanup": "Shoreline has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large residential market.",
            "asbestos-abatement": "Shoreline has a large inventory of pre-1980 housing throughout its established neighborhoods, with asbestos present in popcorn ceilings, floor tiles, pipe insulation, and drywall compound.",
            "general-contractor": "Shoreline's large residential market creates strong demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "lacey-wa": {
        "city": "Lacey",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Lacey's location in the South Puget Sound area receives significant annual rainfall. The city's rapidly growing residential base includes both older housing and new construction, all subject to the Pacific Northwest's extended wet season and storm-driven water events.",
            "fire-damage": "Lacey's residential neighborhoods include older homes with aging electrical systems alongside newer construction. The city's proximity to forested areas creates wildfire smoke exposure during dry summers.",
            "mold-remediation": "Lacey's wet climate and mix of housing ages create consistent mold risk in crawl spaces and wall cavities. Post-water damage mold is a common issue in both older and newer Lacey properties.",
            "storm-damage": "Lacey experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage throughout the city. Proximity to Puget Sound amplifies storm impacts.",
            "biohazard-cleanup": "Lacey has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services as one of Thurston County's growing communities adjacent to Olympia.",
            "asbestos-abatement": "Lacey has older residential neighborhoods with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, and pipe insulation alongside newer construction.",
            "general-contractor": "Lacey's growing residential market in the South Puget Sound area creates demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "olympia-wa": {
        "city": "Olympia",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Olympia receives over 50 inches of annual rainfall — one of the wettest cities in Washington — with an extended wet season from October through June. The capital city's older residential and government-adjacent properties face significant water intrusion and pipe failure risk.",
            "fire-damage": "Olympia's older residential neighborhoods and historic Capitol campus area contain aging housing stock with elevated fire risk. Dry South Puget Sound summers increase fire risk in surrounding forested areas.",
            "mold-remediation": "Olympia's extremely wet climate creates persistent mold risk throughout the city. Older homes, state government buildings, and commercial properties all face significant mold challenges in the region's moisture-heavy environment.",
            "storm-damage": "Olympia experiences Pacific windstorms and atmospheric river events that cause significant roof and structural damage. The city's location at the southern tip of Puget Sound creates exposure to converging storm systems.",
            "biohazard-cleanup": "Olympia has consistent demand for biohazard, unattended death, and hoarding cleanup services as Washington's state capital and the primary city in Thurston County.",
            "asbestos-abatement": "Olympia has a significant inventory of pre-1980 housing and government buildings with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout the capital area.",
            "general-contractor": "Olympia's role as Washington's state capital creates strong demand for licensed general contractors handling insurance reconstruction for both residential properties and government-adjacent commercial buildings.",
        }
    },
    "burien-wa": {
        "city": "Burien",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Burien's location south of Seattle and adjacent to Puget Sound receives significant annual rainfall throughout the Pacific Northwest wet season. Older residential neighborhoods face water intrusion and pipe failure risk during extended wet weather.",
            "fire-damage": "Burien's established residential neighborhoods contain older housing stock with aging electrical systems that carry elevated fire risk. The city's suburban character creates a large single-family home restoration market.",
            "mold-remediation": "Burien's wet climate and older housing stock create persistent mold risk in crawl spaces and wall cavities. Post-water damage mold is a common issue in Burien's established neighborhoods.",
            "storm-damage": "Burien experiences Pacific windstorms and heavy rainfall events that cause roof and structural damage. The city's Puget Sound proximity amplifies storm impacts in waterfront areas.",
            "biohazard-cleanup": "Burien has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large residential market near Seattle-Tacoma International Airport.",
            "asbestos-abatement": "Burien has a large inventory of pre-1980 housing with asbestos in popcorn ceilings, vinyl floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Burien's large residential market creates consistent demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },
    "bothell-wa": {
        "city": "Bothell",
        "state": "Washington",
        "abbrev": "WA",
        "context": {
            "water-damage": "Bothell's location on the north end of Lake Washington receives significant annual rainfall throughout the Pacific Northwest wet season. The North Creek and Sammamish River corridors create flood risk for low-lying properties during major storm events.",
            "fire-damage": "Bothell's mix of older residential neighborhoods and newer development creates diverse fire risk profiles. Older homes in established Bothell neighborhoods carry elevated risk from aging electrical systems.",
            "mold-remediation": "Bothell's wet climate and mix of housing ages create persistent mold risk in crawl spaces and wall cavities. Post-water damage mold is a common issue in both older and newer Bothell properties.",
            "storm-damage": "Bothell experiences Pacific windstorms and heavy rainfall that cause roof damage and flooding along creek corridors. The city's tree canopy creates significant storm damage risk during wind events.",
            "biohazard-cleanup": "Bothell has consistent demand for biohazard, sewage backup, unattended death, and hoarding cleanup services across its growing residential and commercial market.",
            "asbestos-abatement": "Bothell has older residential neighborhoods with pre-1980 housing containing asbestos in popcorn ceilings, floor tiles, and pipe insulation alongside newer construction.",
            "general-contractor": "Bothell's growing real estate market creates strong demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events.",
        }
    },

    # ── CALIFORNIA ───────────────────────────────────────────────────────────
    "los-angeles-ca": {
        "city": "Los Angeles",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Los Angeles receives sporadic but intense rainfall during its wet season, with atmospheric river events causing catastrophic flooding and water intrusion. The city's vast stock of older homes — many pre-1960 — face significant water damage risk during major rain events after long dry periods when ground cannot absorb water quickly.",
            "fire-damage": "Los Angeles is one of the nation's highest wildfire risk markets, with devastating fires in the hills, canyons, and wildland-urban interface occurring regularly. Wind-driven fires move rapidly through residential neighborhoods, creating massive insurance restoration demand across LA County.",
            "mold-remediation": "Los Angeles's aging housing stock and periodic water intrusion events create significant mold risk. Homes that sustain water damage during infrequent but intense rain events often develop mold if not properly dried and remediated quickly.",
            "storm-damage": "Los Angeles experiences wind-driven storm events including Santa Ana winds, which cause roof damage, downed trees, and structural damage throughout the region. Atmospheric river events cause flooding and mudslides in hillside communities.",
            "biohazard-cleanup": "Los Angeles has enormous demand for biohazard, unattended death, crime scene, and hoarding cleanup services across its diverse residential and commercial properties. The city's large population creates consistent restoration and cleanup needs.",
            "asbestos-abatement": "Los Angeles has an enormous inventory of pre-1980 housing and commercial buildings containing asbestos. Popcorn ceilings, floor tiles, pipe insulation, and drywall compound in older LA homes and apartment buildings require professional testing and abatement before any restoration work.",
            "general-contractor": "Los Angeles is one of the largest insurance reconstruction markets in the country, driven by ongoing wildfire, water, and storm damage events. Licensed general contractors are in constant demand for insurance reconstruction throughout LA County.",
        }
    },
    "san-diego-ca": {
        "city": "San Diego",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "San Diego's Mediterranean climate brings intense atmospheric river events during the wet season that cause flooding and water intrusion in homes not prepared for heavy rain. Older residential neighborhoods in Mission Hills, North Park, and downtown are particularly vulnerable.",
            "fire-damage": "San Diego County is one of the highest wildfire risk areas in the United States. Santa Ana wind-driven fires have destroyed thousands of homes in communities like Rancho Bernardo, Scripps Ranch, and Julian. Wildfire insurance restoration is a major market in the San Diego region.",
            "mold-remediation": "San Diego's older housing stock and periodic water intrusion from atmospheric river events create mold risk. Coastal humidity in waterfront neighborhoods also contributes to mold growth in poorly ventilated older homes.",
            "storm-damage": "San Diego experiences Santa Ana wind events and atmospheric river storms that cause roof damage, flooding, and mudslides in hillside communities. Storm damage is most severe in canyonside neighborhoods.",
            "biohazard-cleanup": "San Diego has significant demand for biohazard, unattended death, crime scene, and hoarding cleanup services across its large residential and commercial market.",
            "asbestos-abatement": "San Diego has a substantial inventory of pre-1980 housing and commercial buildings with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Fire restoration projects in older neighborhoods frequently require asbestos abatement.",
            "general-contractor": "San Diego's wildfire exposure and large housing market create strong demand for licensed general contractors handling insurance reconstruction after fire, water, and storm damage events throughout the county.",
        }
    },
    "san-jose-ca": {
        "city": "San Jose",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "San Jose and the Santa Clara Valley experience flooding during atmospheric river events, with the Guadalupe River and Coyote Creek causing significant flood damage in residential areas. The 2017 Coyote Creek flood impacted thousands of homes. Older residential neighborhoods throughout San Jose are vulnerable to water intrusion.",
            "fire-damage": "San Jose sits adjacent to the Santa Cruz Mountains and Diablo Range with significant wildland-urban interface fire risk. Diablo wind events drive fire conditions that threaten hillside neighborhoods in the city.",
            "mold-remediation": "San Jose's older housing stock and periodic flooding events create significant mold risk. Silicon Valley's high-value real estate market demands professional mold remediation to protect property values.",
            "storm-damage": "San Jose experiences atmospheric river events and wind-driven storms that cause flooding, roof damage, and structural impacts throughout the valley. Hillside neighborhoods face landslide risk during heavy rain.",
            "biohazard-cleanup": "San Jose has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large and diverse residential market.",
            "asbestos-abatement": "San Jose has a significant inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Silicon Valley's renovation and reconstruction activity frequently requires asbestos abatement.",
            "general-contractor": "San Jose's high-value real estate market and ongoing exposure to fire, flood, and storm events create strong demand for licensed general contractors managing insurance reconstruction to premium standards.",
        }
    },
    "san-francisco-ca": {
        "city": "San Francisco",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "San Francisco receives significant winter rainfall and experiences atmospheric river events that cause flooding, water intrusion, and sewer backups throughout the city. The city's aging combined sewer system causes backups in older neighborhoods during heavy rain. Victorian and Edwardian housing stock requires specialized water damage restoration.",
            "fire-damage": "San Francisco's dense historic housing stock — Victorian and Edwardian row homes — carries elevated fire risk from aging electrical systems and close building proximity. Smoke damage restoration is a major market throughout the city.",
            "mold-remediation": "San Francisco's coastal fog, winter rainfall, and historic housing stock create persistent mold risk. Poor ventilation in Victorian and Edwardian homes allows mold to establish in wall cavities, basements, and crawl spaces.",
            "storm-damage": "San Francisco experiences Pacific windstorms and atmospheric river events that cause roof and structural damage throughout the city. Hillside neighborhoods like Twin Peaks and Diamond Heights face elevated storm exposure.",
            "biohazard-cleanup": "San Francisco has significant demand for biohazard, unattended death, crime scene, and hoarding cleanup services across its dense urban residential and commercial market.",
            "asbestos-abatement": "San Francisco has an enormous inventory of pre-1980 Victorian and Edwardian buildings with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Every major restoration project in older SF buildings requires asbestos assessment.",
            "general-contractor": "San Francisco's historic housing stock, high property values, and ongoing exposure to water, fire, and seismic events create one of the most demanding insurance reconstruction markets in California.",
        }
    },
    "fresno-ca": {
        "city": "Fresno",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Fresno's San Joaquin Valley location brings atmospheric river events that cause flooding and water intrusion in older residential neighborhoods. The city's large stock of aging housing is particularly vulnerable to pipe failures during cold winter freezes.",
            "fire-damage": "Fresno sits at the gateway to the Sierra Nevada foothills with significant wildfire exposure. Surrounding communities and foothill neighborhoods face regular wildfire threat during California's dry season.",
            "mold-remediation": "Fresno's periodic flooding and hot humid summers create mold risk in older homes. Post-water damage mold grows rapidly in Central Valley heat if remediation is delayed.",
            "storm-damage": "Fresno experiences atmospheric river events, valley fog, and occasional wind storms that cause roof and structural damage throughout the metro area. Winter flooding in low-lying areas creates water damage risk.",
            "biohazard-cleanup": "Fresno has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large residential market as the Central Valley's largest city.",
            "asbestos-abatement": "Fresno has a large inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Fresno's large residential market and exposure to fire, flood, and storm damage events create strong demand for licensed general contractors handling insurance reconstruction throughout the Central Valley.",
        }
    },
    "sacramento-ca": {
        "city": "Sacramento",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Sacramento sits at the confluence of the Sacramento and American Rivers and has a long history of flooding. Atmospheric river events create major flood risk for residential neighborhoods throughout the metro area. The city's aging housing stock is particularly vulnerable to water intrusion and pipe failures.",
            "fire-damage": "Sacramento sits adjacent to the Sierra Nevada foothills with significant wildfire exposure. Surrounding foothill communities face ongoing wildfire risk and smoke intrusion that affects Sacramento properties during California's fire season.",
            "mold-remediation": "Sacramento's flooding history and hot humid summers create significant mold risk in older homes. Post-flood mold remediation is a major market in the Sacramento Valley following atmospheric river events.",
            "storm-damage": "Sacramento experiences atmospheric river events and valley wind storms that cause flooding, roof damage, and structural impacts. The Sacramento River and American River flood plains create ongoing storm damage risk.",
            "biohazard-cleanup": "Sacramento has consistent demand for biohazard, unattended death, and hoarding cleanup services as California's state capital and the Central Valley's second largest city.",
            "asbestos-abatement": "Sacramento has a large inventory of pre-1980 housing and state government buildings with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. The capital region's renovation market frequently requires asbestos abatement.",
            "general-contractor": "Sacramento's flood history, wildfire exposure, and large residential market create strong demand for licensed general contractors handling insurance reconstruction throughout the Sacramento Valley.",
        }
    },
    "long-beach-ca": {
        "city": "Long Beach",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Long Beach's coastal and port location makes it subject to atmospheric river flooding and stormwater backup events. The city's large stock of older bungalows and mid-century housing is vulnerable to water intrusion and pipe failures during wet season events.",
            "fire-damage": "Long Beach's older residential neighborhoods contain aging housing stock with elevated fire risk from outdated electrical systems. Wind-driven fire conditions during Santa Ana events create fire risk throughout the area.",
            "mold-remediation": "Long Beach's coastal humidity and older housing stock create persistent mold risk in crawl spaces and wall cavities. Post-water damage mold grows quickly in the city's mild climate if not immediately remediated.",
            "storm-damage": "Long Beach experiences atmospheric river events and Santa Ana wind conditions that cause flooding, roof damage, and structural impacts in residential neighborhoods.",
            "biohazard-cleanup": "Long Beach has significant demand for biohazard, unattended death, crime scene, and hoarding cleanup services across its large and diverse urban residential market.",
            "asbestos-abatement": "Long Beach has an extensive inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Every major restoration project in older Long Beach homes requires asbestos assessment.",
            "general-contractor": "Long Beach's large residential market and ongoing exposure to water, fire, and storm damage events create strong demand for licensed general contractors managing insurance reconstruction throughout the city.",
        }
    },
    "oakland-ca": {
        "city": "Oakland",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Oakland's winter rainfall and older housing stock create persistent water intrusion risk. The city's hillside neighborhoods face landslide risk during atmospheric river events. Older flatland neighborhoods with aging sewer infrastructure experience backups during heavy rain.",
            "fire-damage": "Oakland Hills has experienced catastrophic wildfires, including the 1991 firestorm that destroyed nearly 3,000 homes. The Oakland Hills remain a high wildfire risk zone. Wind-driven fire conditions threaten hillside neighborhoods regularly.",
            "mold-remediation": "Oakland's coastal fog, winter rainfall, and large inventory of older housing create persistent mold risk. Pre-war housing in West Oakland, Fruitvale, and other flatland neighborhoods is particularly susceptible to mold following water events.",
            "storm-damage": "Oakland experiences atmospheric river events and Pacific windstorms that cause roof damage, landslides, and flooding in hillside and flatland neighborhoods. The city's aging infrastructure amplifies storm damage impacts.",
            "biohazard-cleanup": "Oakland has significant demand for biohazard, unattended death, crime scene, and hoarding cleanup services across its diverse urban residential and commercial market.",
            "asbestos-abatement": "Oakland has an extensive inventory of pre-1980 housing and commercial buildings with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. Oakland's active renovation and restoration market requires frequent asbestos abatement.",
            "general-contractor": "Oakland's fire history, flooding risk, and large stock of older housing create one of the Bay Area's strongest markets for licensed general contractors managing insurance reconstruction.",
        }
    },
    "bakersfield-ca": {
        "city": "Bakersfield",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Bakersfield's San Joaquin Valley location brings sporadic but intense atmospheric river events that cause flooding and water intrusion in residential neighborhoods. Hard winter freezes cause pipe bursts in older housing stock throughout the city.",
            "fire-damage": "Bakersfield sits near the Tehachapi Mountains and foothills with significant wildfire risk during California's dry season. Surrounding agricultural and foothill areas create fire exposure for residential properties on the city's edges.",
            "mold-remediation": "Bakersfield's periodic flooding and hot Central Valley summers create significant mold risk. Post-water damage mold grows rapidly in extreme heat if remediation is delayed, making immediate response critical.",
            "storm-damage": "Bakersfield experiences atmospheric river events and wind storms that cause flooding, roof damage, and structural impacts. Valley floor flooding during major rain events creates water damage risk for low-lying neighborhoods.",
            "biohazard-cleanup": "Bakersfield has consistent demand for biohazard, unattended death, and hoarding cleanup services as Kern County's largest city and the central hub for California's oil country.",
            "asbestos-abatement": "Bakersfield has a large inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Bakersfield's large residential market and exposure to fire, flood, and storm damage events create strong demand for licensed general contractors handling insurance reconstruction throughout Kern County.",
        }
    },
    "anaheim-ca": {
        "city": "Anaheim",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Anaheim's Orange County location experiences atmospheric river flooding events that cause water intrusion and sewer backups in older residential neighborhoods. The city's aging housing stock is vulnerable to pipe failures and water damage during wet season events.",
            "fire-damage": "Anaheim Hills and the city's eastern foothills face significant wildfire risk during Santa Ana wind events. Wind-driven fires have threatened Anaheim residential neighborhoods on multiple occasions.",
            "mold-remediation": "Anaheim's coastal proximity and older housing stock create mold risk following water damage events. Post-water damage mold grows quickly in Southern California's mild climate if not immediately remediated.",
            "storm-damage": "Anaheim experiences atmospheric river events and Santa Ana wind conditions that cause flooding, roof damage, and structural impacts in both flatland and hillside neighborhoods.",
            "biohazard-cleanup": "Anaheim has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large residential and commercial market as Orange County's largest city.",
            "asbestos-abatement": "Anaheim has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Anaheim's large residential market and wildfire exposure create strong demand for licensed general contractors handling insurance reconstruction throughout Orange County.",
        }
    },
    "santa-ana-ca": {
        "city": "Santa Ana",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Santa Ana's dense urban location in Orange County experiences atmospheric river flooding that causes water intrusion and sewer backups in older residential neighborhoods. The city's large stock of older housing is particularly vulnerable to water damage.",
            "fire-damage": "Santa Ana's position in the path of Santa Ana wind events creates significant fire risk. The strong seasonal winds that bear the city's name drive fire conditions that threaten residential neighborhoods throughout Orange County.",
            "mold-remediation": "Santa Ana's older, densely packed housing stock and periodic water intrusion events create significant mold risk. Post-water damage mold grows rapidly in Southern California's mild climate if remediation is delayed.",
            "storm-damage": "Santa Ana experiences atmospheric river events and its namesake wind conditions that cause flooding, roof damage, and structural impacts in residential neighborhoods throughout the city.",
            "biohazard-cleanup": "Santa Ana has significant demand for biohazard, unattended death, and hoarding cleanup services across its densely populated urban residential market.",
            "asbestos-abatement": "Santa Ana has an extensive inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound. The city's older housing stock frequently requires asbestos testing and abatement before restoration work.",
            "general-contractor": "Santa Ana's large residential market and exposure to water, fire, and storm damage events create strong demand for licensed general contractors handling insurance reconstruction throughout Orange County.",
        }
    },
    "riverside-ca": {
        "city": "Riverside",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Riverside's Inland Empire location experiences atmospheric river flooding events that cause significant water intrusion in residential neighborhoods. The Santa Ana River creates flood risk for low-lying properties. Cold winter temperatures cause pipe bursts in older housing.",
            "fire-damage": "Riverside sits in the Inland Empire at the edge of Southern California's high wildfire risk zone. Wind-driven fires during Santa Ana conditions have threatened Riverside neighborhoods. The city's foothills and surrounding areas create ongoing fire exposure.",
            "mold-remediation": "Riverside's periodic flooding and hot Inland Empire summers create mold risk in older homes. Post-water damage mold grows rapidly in extreme heat if remediation is not immediate.",
            "storm-damage": "Riverside experiences atmospheric river events and Santa Ana wind conditions that cause flooding, roof damage, and structural impacts throughout the Inland Empire metro area.",
            "biohazard-cleanup": "Riverside has consistent demand for biohazard, unattended death, and hoarding cleanup services as the Inland Empire's primary city and the seat of Riverside County.",
            "asbestos-abatement": "Riverside has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Riverside's large residential market and exposure to fire, flood, and storm damage events create strong demand for licensed general contractors handling insurance reconstruction throughout the Inland Empire.",
        }
    },
    "stockton-ca": {
        "city": "Stockton",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Stockton's San Joaquin Delta location creates significant flood risk. Atmospheric river events cause major flooding in low-lying residential areas. The Delta's complex waterway system creates ongoing water intrusion risk for properties throughout the city.",
            "fire-damage": "Stockton sits near the Sierra Nevada foothills with wildfire exposure during California's dry season. Surrounding agricultural areas and foothill communities create fire risk that affects Stockton's eastern residential neighborhoods.",
            "mold-remediation": "Stockton's flooding history and hot Central Valley summers create significant mold risk. Post-flood mold remediation is a major market following atmospheric river events, and Central Valley heat accelerates mold growth dramatically.",
            "storm-damage": "Stockton experiences atmospheric river flooding and wind events that cause significant damage in low-lying residential neighborhoods. Delta flooding during major storms creates water damage risk across wide residential areas.",
            "biohazard-cleanup": "Stockton has consistent demand for biohazard, unattended death, and hoarding cleanup services as the Central Valley's third largest city and San Joaquin County's seat.",
            "asbestos-abatement": "Stockton has a large inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Stockton's flood history and large residential market create strong demand for licensed general contractors handling insurance reconstruction after the region's frequent water and storm damage events.",
        }
    },
    "chula-vista-ca": {
        "city": "Chula Vista",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Chula Vista's location in South San Diego County experiences atmospheric river events that cause flooding and water intrusion in residential neighborhoods. The city's rapid growth includes both older housing and new construction vulnerable to water damage.",
            "fire-damage": "Chula Vista's eastern foothills face wildfire risk during Santa Ana wind events. The city's wildland-urban interface creates fire exposure for residential developments on the eastern edge of the city.",
            "mold-remediation": "Chula Vista's coastal proximity and periodic water intrusion events create mold risk in older and newer homes. Post-water damage mold grows quickly in Southern California's mild climate.",
            "storm-damage": "Chula Vista experiences atmospheric river events and Santa Ana wind conditions that cause flooding, roof damage, and structural impacts in residential neighborhoods.",
            "biohazard-cleanup": "Chula Vista has consistent demand for biohazard, unattended death, and hoarding cleanup services as San Diego County's second largest city with a rapidly growing residential market.",
            "asbestos-abatement": "Chula Vista has pre-1980 housing in its established western neighborhoods with asbestos in popcorn ceilings, floor tiles, and pipe insulation alongside newer construction in eastern developments.",
            "general-contractor": "Chula Vista's rapidly growing residential market creates strong demand for licensed general contractors handling insurance reconstruction after water, fire, and storm damage events in San Diego's South Bay.",
        }
    },
    "fremont-ca": {
        "city": "Fremont",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Fremont's East Bay location experiences atmospheric river flooding events that cause water intrusion in residential neighborhoods. The city's proximity to San Francisco Bay creates flood risk in low-lying areas, and older housing in established neighborhoods is vulnerable to water damage.",
            "fire-damage": "Fremont's Mission Hills and Niles Canyon areas sit in the wildland-urban interface with significant wildfire risk during dry season wind events. The Diablo Range creates ongoing fire exposure for eastern Fremont neighborhoods.",
            "mold-remediation": "Fremont's coastal Bay Area climate and older housing stock create persistent mold risk in crawl spaces and wall cavities. Post-water damage mold is a common issue in the city's established residential neighborhoods.",
            "storm-damage": "Fremont experiences atmospheric river events and wind storms that cause flooding, roof damage, and structural impacts throughout the city. Bay-adjacent low-lying areas face elevated flood risk.",
            "biohazard-cleanup": "Fremont has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large and diverse residential market in the South Bay.",
            "asbestos-abatement": "Fremont has a substantial inventory of pre-1980 housing with asbestos in popcorn ceilings, floor tiles, pipe insulation, and drywall compound throughout its established residential neighborhoods.",
            "general-contractor": "Fremont's large residential market and exposure to fire, flood, and storm damage events create strong demand for licensed general contractors managing insurance reconstruction throughout the East Bay.",
        }
    },
    "irvine-ca": {
        "city": "Irvine",
        "state": "California",
        "abbrev": "CA",
        "context": {
            "water-damage": "Irvine's planned community design includes extensive drainage infrastructure, but atmospheric river events still cause flooding and water intrusion in residential neighborhoods. Older sections of Irvine face pipe failure risk during wet season events.",
            "fire-damage": "Irvine sits adjacent to the Santa Ana Mountains and Laguna Coast with significant wildfire risk during Santa Ana wind events. Wind-driven fires have threatened Irvine residential neighborhoods and the city's wildland-urban interface creates ongoing fire exposure.",
            "mold-remediation": "Irvine's coastal proximity and periodic water intrusion events create mold risk in both older and newer homes. High-value Irvine properties require professional mold remediation to protect significant real estate values.",
            "storm-damage": "Irvine experiences atmospheric river events and Santa Ana wind conditions that cause flooding, roof damage, and structural impacts in residential communities throughout the planned city.",
            "biohazard-cleanup": "Irvine has consistent demand for biohazard, unattended death, and hoarding cleanup services across its large and affluent residential market.",
            "asbestos-abatement": "Irvine's older residential sections contain pre-1980 housing with asbestos in popcorn ceilings, floor tiles, and pipe insulation. Restoration and renovation projects in older Irvine communities require asbestos assessment.",
            "general-contractor": "Irvine's high-value real estate market and wildfire exposure create strong demand for licensed general contractors managing insurance reconstruction to premium standards after fire, water, and storm damage events.",
        }
    },
}
# ─── PAGE BUILDERS ───────────────────────────────────────────────────────────

def build_national_page(svc_key):
    s = SERVICES[svc_key]
    canonical = f"{DOMAIN}{s['national_url']}"
    title = f"{s['name']} | {BRAND}"
    meta_desc = f"Need {s['name'].lower()}? {BRAND} confirms your active insurance coverage, manages your claim with your carrier, and dispatches vetted licensed contractors nationwide. Call {PHONE_DISPLAY}."

    # JSON-LD
    faq_schema = "\n".join([
        f'''    {{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}{"," if i < len(s["faqs"])-1 else ""}'''
        for i, (q, a) in enumerate(s["faqs"])
    ])

    schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "HomeAndConstructionBusiness",
      "name": "{BRAND}",
      "url": "{DOMAIN}",
      "telephone": "{PHONE_FULL}",
      "areaServed": {{"@type": "Country", "name": "United States"}}
    }},
    {{
      "@type": "Service",
      "name": "{s['name']}",
      "provider": {{"@type": "HomeAndConstructionBusiness", "name": "{BRAND}"}},
      "areaServed": {{"@type": "Country", "name": "United States"}},
      "url": "{canonical}"
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_schema}
      ]
    }}
  ]
}}
</script>"""

    # Damage types grid
    damage_cards = "\n".join([
        f'<div class="damage-card"><div class="icon">{icon}</div><h4>{label}</h4></div>'
        for icon, label in s["damage_types"]
    ])

    # Scope grid
    scope_cards = "\n".join([
        f'<div class="scope-card"><h4>{h}</h4><p>{p}</p></div>'
        for h, p in s["scope_items"]
    ])

    # How Guardian helps
    numbered_cards = "\n".join([
        f'<div class="numbered-card"><div class="num">{num}</div><h4>{h}</h4><p>{p}</p></div>'
        for num, h, p in s["how_helps"]
    ])

    # Expect steps
    expect_cards = "\n".join([
        f'<div class="expect-step"><div class="step-num">{i+1}</div><h4>{h}</h4><p>{p}</p></div>'
        for i, (h, p) in enumerate(s["expect_steps"])
    ])

    # Stats
    stat_items = "\n".join([
        f'<div class="stat-item"><div class="num">{num}</div><div class="label">{label}</div></div>'
        for num, label in s["matters_stats"]
    ])

    # Why cards
    why_cards_html = "\n".join([
        f'<div class="why-card"><div class="icon">{icon}</div><h4>{h}</h4><p>{p}</p></div>'
        for icon, h, p in s["why_cards"]
    ])

    # Checkpoints
    checkpoints_html = "\n".join([
        f'<li>{c}</li>'
        for c in s["checkpoints"]
    ])

    # FAQ
    faqs_html = "\n".join([
        f'''<div class="faq-item">
  <button class="faq-q">{q}<span class="arrow">▼</span></button>
  <div class="faq-a">{a}</div>
</div>'''
        for q, a in s["faqs"]
    ])

    # Trust bar
    trust_bar_html = "\n".join([
        f'<div class="trust-item">{t}</div>' for t in s["trust_items"]
    ])

    # Footer nav (national pages get full footer)
    full_footer = f"""<footer class="footer">
  <div class="footer-simple">
    <a href="/" aria-label="{BRAND} Home">{FOOTER_LOGO}</a>
    <p>{BRAND} — National insurance claim management and restoration network. Available 24/7 at {PHONE_DISPLAY}.</p>
    <a href="tel:{PHONE_TEL}" class="btn-primary" aria-label="Call {BRAND}">📞 Call {PHONE_DISPLAY}</a>
  </div>
  <div class="footer-bottom">
    <p>© 2025 {LEGAL}. All rights reserved. Contractor dispatch subject to availability in your area. You are responsible for your deductible per your policy.</p>
  </div>
</footer>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{canonical}" />
<meta name="description" content="{meta_desc}" />
<meta name="robots" content="index, follow" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{BRAND}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{meta_desc}" />
<meta name="twitter:site" content="@GuardianRestoration" />
{schema}
<style>{SHARED_CSS}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&family=Barlow+Condensed:wght@700;800;900&display=swap" rel="stylesheet">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
</head>
<body>

{conversion_nav()}

<nav aria-label="breadcrumb" class="breadcrumb">Home › {s["name"]}</nav>

<section class="hero">
  <div class="hero-badge">{s["badge"]}</div>
  <h1>{s["h1_national"]}</h1>
  <p class="hero-sub">{s["hero_sub"]}</p>
  <div class="hero-ctas">
    <a href="tel:{PHONE_TEL}" class="btn-primary" aria-label="Call {BRAND}">
      📞 Call Now — {PHONE_DISPLAY}
    </a>
    <a href="/contact/" class="btn-secondary" aria-label="Get help online">Get Help Online →</a>
  </div>
</section>

<div class="trust-bar">{trust_bar_html}</div>

<div class="urgency"><p>⚡ Emergency response available 24/7 — <a href="tel:{PHONE_TEL}" aria-label="Call now">Call {PHONE_DISPLAY}</a> now. Subject to contractor availability in your area.</p></div>

<section class="problem">
  <p class="section-label">Types of {s["name"]}</p>
  <h2 class="section-title">What We Cover</h2>
  <p class="section-sub">We manage claims and dispatch contractors for all types of {s["name"].lower()} events.</p>
  <div class="damage-grid">{damage_cards}</div>
</section>

<section class="scope">
  <p class="section-label">Scope of Work</p>
  <h2 class="section-title">What Restoration Includes</h2>
  <p class="section-sub">Vetted contractors handle every element of the restoration process — managed through your insurance claim.</p>
  <div class="scope-grid">{scope_cards}</div>
</section>

<div class="mid-cta">
  <h3>Ready to Get Started? Call {PHONE_DISPLAY}</h3>
  <a href="tel:{PHONE_TEL}" class="btn-white" aria-label="Call {BRAND}">📞 Call Now — Available 24/7</a>
</div>

<section class="how-helps">
  <p class="section-label">How It Works</p>
  <h2 class="section-title">How Guardian Helps</h2>
  <p class="section-sub">From first call to completed restoration — we manage every step.</p>
  <div class="numbered-grid">{numbered_cards}</div>
</section>

<section class="expect">
  <p class="section-label">The Process</p>
  <h2 class="section-title">What to Expect</h2>
  <p class="section-sub">Four steps from damage to restoration.</p>
  <div class="expect-steps">{expect_cards}</div>
</section>

<section class="matters">
  <div class="matters-inner">
    <div class="matters-text">
      <h2>Why Acting Fast Matters</h2>
      <p>Every hour after damage occurs, the situation gets worse and the cost of restoration increases. We respond fast to minimize damage, stop the clock on secondary losses, and protect your claim value.</p>
      <p>Our network of vetted contractors is ready to respond nationwide — subject to contractor availability in your area.</p>
    </div>
    <div class="stat-block">{stat_items}</div>
  </div>
</section>

<section class="why">
  <p class="section-label">Why Guardian</p>
  <h2 class="section-title">Why Choose Guardian Restoration Network</h2>
  <p class="section-sub">We are your advocate — from first call to completed restoration.</p>
  <div class="why-grid">{why_cards_html}</div>
</section>

<section class="insurance">
  <div class="insurance-inner">
    <div class="insurance-text">
      <h2>How Insurance Works With Guardian</h2>
      <p>{GUARDIAN_ENTITY}</p>
    </div>
    <ul class="checkpoint-list">{checkpoints_html}</ul>
  </div>
</section>

<section class="faq">
  <div class="faq-inner">
    <h2 class="faq-title">Frequently Asked Questions</h2>
    {faqs_html}
  </div>
</section>

<section class="final-cta">
  <h2>Need {s["name"]}?</h2>
  <p>One call puts us in your corner. We confirm your coverage, manage your claim, and dispatch a vetted contractor — fast.</p>
  <a href="tel:{PHONE_TEL}" class="btn-white" aria-label="Call {BRAND}">📞 Call {PHONE_DISPLAY} — Free, 24/7</a>
</section>

{full_footer}

{ghl_widget()}
{faq_js()}
</body>
</html>"""

    return html


def build_city_page(svc_key, city_key):
    s = SERVICES[svc_key]
    c = CITIES[city_key]
    city = c["city"]
    state = c["state"]
    abbrev = c["abbrev"]
    context = c["context"].get(svc_key, "")

    slug = f"{s['city_slug_prefix']}-{city_key}"
    canonical = f"{DOMAIN}/{slug}/"
    wp_title = f"{s['name']} {city}, {abbrev}"
    seo_title = f"{s['name']} {city}, {abbrev} | {BRAND}"
    meta_desc = f"Need {s['name'].lower()} {city}, {abbrev}? {BRAND} confirms your active coverage, manages your insurance carrier, and dispatches vetted local contractors for rapid response. Call {PHONE_DISPLAY}."

    # JSON-LD
    faq_schema = "\n".join([
        f'''    {{"@type":"Question","name":{repr(q)},"acceptedAnswer":{{"@type":"Answer","text":{repr(a)}}}}}{"," if i < len(s["faqs"])-1 else ""}'''
        for i, (q, a) in enumerate(s["faqs"])
    ])

    # HowTo steps from expect_steps
    howto_steps = "\n".join([
        f'''      {{"@type":"HowToStep","position":{i+1},"name":{repr(h)},"text":{repr(p)}}}{"," if i < len(s["expect_steps"])-1 else ""}'''
        for i, (h, p) in enumerate(s["expect_steps"])
    ])

    schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "HomeAndConstructionBusiness",
      "name": "{BRAND}",
      "url": "{DOMAIN}",
      "telephone": "{PHONE_FULL}",
      "areaServed": {{"@type": "City", "name": "{city}", "addressRegion": "{abbrev}"}}
    }},
    {{
      "@type": "Service",
      "name": "{s['name']} {city}, {abbrev}",
      "provider": {{"@type": "HomeAndConstructionBusiness", "name": "{BRAND}"}},
      "areaServed": {{"@type": "City", "name": "{city}", "addressRegion": "{abbrev}"}},
      "url": "{canonical}"
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/"}},
        {{"@type": "ListItem", "position": 2, "name": "{s['name']}", "item": "{DOMAIN}{s['national_url']}"}},
        {{"@type": "ListItem", "position": 3, "name": "{city}, {abbrev}", "item": "{canonical}"}}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_schema}
      ]
    }},
    {{
      "@type": "HowTo",
      "name": "How to Get {s['name']} in {city}, {abbrev}",
      "description": "How Guardian Restoration Network confirms your coverage, manages your insurance carrier, and dispatches vetted local contractors for {s['name'].lower()} in {city}, {abbrev}.",
      "step": [
{howto_steps}
      ]
    }},
    {{
      "@type": "SpeakableSpecification",
      "@id": "{canonical}#speakable",
      "cssSelector": [".hero h1", ".hero-sub", ".section-title", ".faq-q"]
    }}
  ]
}}
</script>"""

    # Hero H1
    h1 = f"{s['name']} <span>{city}, {abbrev}</span>"

    # Damage types grid
    damage_cards = "\n".join([
        f'<div class="damage-card"><div class="icon">{icon}</div><h4>{label}</h4></div>'
        for icon, label in s["damage_types"]
    ])

    # Scope grid
    scope_cards = "\n".join([
        f'<div class="scope-card"><h4>{h}</h4><p>{p}</p></div>'
        for h, p in s["scope_items"]
    ])

    # How Guardian helps
    numbered_cards = "\n".join([
        f'<div class="numbered-card"><div class="num">{num}</div><h4>{h}</h4><p>{p}</p></div>'
        for num, h, p in s["how_helps"]
    ])

    # Expect steps
    expect_cards = "\n".join([
        f'<div class="expect-step"><div class="step-num">{i+1}</div><h4>{h}</h4><p>{p}</p></div>'
        for i, (h, p) in enumerate(s["expect_steps"])
    ])

    # Stats
    stat_items = "\n".join([
        f'<div class="stat-item"><div class="num">{num}</div><div class="label">{label}</div></div>'
        for num, label in s["matters_stats"]
    ])

    # Why cards
    why_cards_html = "\n".join([
        f'<div class="why-card"><div class="icon">{icon}</div><h4>{h}</h4><p>{p}</p></div>'
        for icon, h, p in s["why_cards"]
    ])

    # Checkpoints
    checkpoints_html = "\n".join([f'<li>{c}</li>' for c in s["checkpoints"]])

    # FAQ
    faqs_html = "\n".join([
        f'''<div class="faq-item">
  <button class="faq-q">{q}<span class="arrow">▼</span></button>
  <div class="faq-a">{a}</div>
</div>'''
        for q, a in s["faqs"]
    ])

    # Trust bar
    trust_bar_html = "\n".join([
        f'<div class="trust-item">{t}</div>' for t in s["trust_items"]
    ])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{seo_title}</title>
<link rel="canonical" href="{canonical}" />
<meta name="description" content="{meta_desc}" />
<meta name="robots" content="index, follow" />
<meta property="og:title" content="{seo_title}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{BRAND}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{seo_title}" />
<meta name="twitter:description" content="{meta_desc}" />
<meta name="twitter:site" content="@GuardianRestoration" />
{schema}
<style>{SHARED_CSS}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&family=Barlow+Condensed:wght@700;800;900&display=swap" rel="stylesheet">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
</head>
<body>

{conversion_nav()}

<nav aria-label="breadcrumb" class="breadcrumb">Home › {s["name"]} › {city}, {abbrev}</nav>

<section class="hero">
  <div class="hero-badge">24/7 Emergency Response — {city}, {abbrev}</div>
  <h1>{h1}</h1>
  <p class="hero-sub">We confirm your active coverage, manage your insurance carrier, and dispatch vetted local {s["name"].lower()} contractors in {city}, {abbrev}. {s["hero_sub"]}</p>
  <div class="hero-ctas">
    <a href="tel:{PHONE_TEL}" class="btn-primary" aria-label="Call {BRAND} in {city}">
      📞 Call Now — {PHONE_DISPLAY}
    </a>
    <a href="/contact/" class="btn-secondary" aria-label="Get help online">Get Help Online →</a>
  </div>
</section>

<div class="trust-bar">{trust_bar_html}</div>

<div class="urgency"><p>⚡ Emergency response available 24/7 in {city}, {abbrev} — <a href="tel:{PHONE_TEL}" aria-label="Call now">Call {PHONE_DISPLAY}</a>. Subject to contractor availability in your area.</p></div>

<section class="split">
  <div class="split-inner">
    <div class="split-block">
      <h3>Residential {s["name"]} {city}, {abbrev}</h3>
      <p>Homeowners in {city} face unique challenges — {context[:200]}...</p>
      <ul>
        <li>Single-family homes, condos, and townhomes</li>
        <li>Insurance claim management from first call to completion</li>
        <li>All trades — licensed and vetted local contractors</li>
        <li>24/7 emergency response dispatch</li>
      </ul>
    </div>
    <div class="split-block">
      <h3>Commercial {s["name"]} {city}, {abbrev}</h3>
      <p>Commercial property owners and managers in {city} need fast, reliable response. We manage commercial claims and dispatch licensed contractors for:</p>
      <ul>
        <li>Office buildings and retail spaces</li>
        <li>Multi-family residential buildings</li>
        <li>Industrial and warehouse facilities</li>
        <li>Property management companies and HOAs</li>
      </ul>
    </div>
  </div>
</section>

<section class="problem">
  <p class="section-label">{s["name"]} {city}, {abbrev}</p>
  <h2 class="section-title">What Is {s["name"]} in {city}, {abbrev}?</h2>
  <p class="section-sub">{context}</p>
  <div class="damage-grid">{damage_cards}</div>
</section>

<section class="scope">
  <p class="section-label">Scope of Work</p>
  <h2 class="section-title">What {s["name"]} Includes in {city}</h2>
  <p class="section-sub">Our vetted {city} contractors handle every element of restoration — managed through your insurance claim.</p>
  <div class="scope-grid">{scope_cards}</div>
</section>

<div class="mid-cta">
  <h3>Need {s["name"]} in {city}? Call {PHONE_DISPLAY}</h3>
  <a href="tel:{PHONE_TEL}" class="btn-white" aria-label="Call {BRAND}">📞 Call Now — Available 24/7</a>
</div>

<section class="how-helps">
  <p class="section-label">How It Works</p>
  <h2 class="section-title">How Guardian Helps in {city}</h2>
  <p class="section-sub">From your first call to completed restoration — we manage every step with your insurance carrier.</p>
  <div class="numbered-grid">{numbered_cards}</div>
</section>

<section class="expect">
  <p class="section-label">The Process</p>
  <h2 class="section-title">What to Expect</h2>
  <p class="section-sub">Four steps from damage to restoration in {city}, {abbrev}.</p>
  <div class="expect-steps">{expect_cards}</div>
</section>

<section class="matters">
  <div class="matters-inner">
    <div class="matters-text">
      <h2>Why Acting Fast Matters in {city}</h2>
      <p>{context}</p>
      <p>Our vetted {city} contractors are ready to respond — subject to contractor availability in your area. Call {PHONE_DISPLAY} to get started immediately.</p>
    </div>
    <div class="stat-block">{stat_items}</div>
  </div>
</section>

<section class="why">
  <p class="section-label">Why Guardian</p>
  <h2 class="section-title">Why {city} Property Owners Choose Guardian</h2>
  <p class="section-sub">We are your advocate in {city} — from first call to completed restoration.</p>
  <div class="why-grid">{why_cards_html}</div>
</section>

<section class="insurance">
  <div class="insurance-inner">
    <div class="insurance-text">
      <h2>How Insurance Works With Guardian in {city}</h2>
      <p>{GUARDIAN_ENTITY}</p>
    </div>
    <ul class="checkpoint-list">{checkpoints_html}</ul>
  </div>
</section>

<section class="faq">
  <div class="faq-inner">
    <h2 class="faq-title">Frequently Asked Questions — {s["name"]} {city}, {abbrev}</h2>
    {faqs_html}
  </div>
</section>

<section class="final-cta">
  <h2>Need {s["name"]} in {city}, {abbrev}?</h2>
  <p>One call puts us in your corner. We confirm your coverage, manage your claim, and dispatch a vetted {city} contractor — fast.</p>
  <a href="tel:{PHONE_TEL}" class="btn-white" aria-label="Call {BRAND}">📞 Call {PHONE_DISPLAY} — Free, 24/7</a>
</section>

{conversion_footer()}

{ghl_widget()}
{faq_js()}
</body>
</html>"""

    return html, wp_title, slug, s["name"], city, abbrev


# ─── VERCEL ROUTING ──────────────────────────────────────────────────────────

def build_vercel_json():
    routes = []

    # Homepage
    routes.append({"src": "^/$", "dest": "/grn-homepage-v7.html"})

    # National service pages
    national_slugs = {
        "water-damage-restoration": "water-damage",
        "fire-damage-restoration": "fire-damage",
        "mold-remediation": "mold-remediation",
        "storm-damage-restoration": "storm-damage",
        "biohazard-cleanup": "biohazard-cleanup",
        "asbestos-abatement": "asbestos-abatement",
        "general-contractor": "general-contractor",
    }
    for slug, key in national_slugs.items():
        routes.append({"src": f"^/{slug}/?$", "dest": f"/grn-{key}-v1.html"})

    # City pages
    for svc_key, svc_data in SERVICES.items():
        for city_key in CITIES.keys():
            prefix = svc_data["city_slug_prefix"]
            slug = f"{prefix}-{city_key}"
            filename = f"grn-{slug}-v1.html"
            routes.append({"src": f"^/{slug}/?$", "dest": f"/{filename}"})

    import json
    return json.dumps({"routes": routes}, indent=2)


# ─── MAIN BUILD ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building GRN site...")
    rankmath_output = []

    # Copy homepage (already exists in output)
    shutil.copy("./grn-homepage-v7.html", f"{OUTPUT_DIR}/grn-homepage-v7.html")
    print("✓ grn-homepage-v7.html (copied)")

    # National service pages
    for svc_key, svc_data in SERVICES.items():
        html = build_national_page(svc_key)
        filename = f"grn-{svc_key}-v1.html"
        with open(f"{OUTPUT_DIR}/{filename}", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ {filename}")

    # City pages
    for city_key in CITIES.keys():
        for svc_key, svc_data in SERVICES.items():
            html, wp_title, slug, svc_name, city, abbrev = build_city_page(svc_key, city_key)
            filename = f"grn-{slug}-v1.html"
            with open(f"{OUTPUT_DIR}/{filename}", "w", encoding="utf-8") as f:
                f.write(html)

            meta_desc = f"Need {svc_name.lower()} {city}, {abbrev}? {BRAND} confirms your active coverage, manages your insurance carrier, and dispatches vetted local contractors for rapid response. Call {PHONE_DISPLAY}."
            seo_title = f"{svc_name} {city}, {abbrev} | {BRAND}"
            focus_kw = f"{svc_name} {city} {abbrev}"

            rankmath_output.append({
                "wp_title": wp_title,
                "slug": slug,
                "focus_kw": focus_kw,
                "seo_title": seo_title,
                "meta_desc": meta_desc,
                "canonical": f"{DOMAIN}/{slug}/",
            })
            print(f"✓ {filename}")

    # vercel.json
    with open(f"{OUTPUT_DIR}/vercel.json", "w", encoding="utf-8") as f:
        f.write(build_vercel_json())
    print("✓ vercel.json")

    # RankMath output file
    rm_lines = []
    for r in rankmath_output:
        rm_lines.append(f"\n{'='*60}")
        rm_lines.append(r["wp_title"])
        rm_lines.append(f"  Slug:     {r['slug']}")
        rm_lines.append(f"  Keyword:  {r['focus_kw']}")
        rm_lines.append(f"  Title:    {r['seo_title']}")
        rm_lines.append(f"  Desc:     {r['meta_desc']}")
        rm_lines.append(f"  URL:      {r['canonical']}")

    with open(f"{OUTPUT_DIR}/rankmath-blocks.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rm_lines))
    print("✓ rankmath-blocks.txt")

    # File count
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.html')]
    print(f"\nDone. {len(files)} HTML files + vercel.json + rankmath-blocks.txt in {OUTPUT_DIR}/")
    print("\nNext step: push ./output/ contents to GitHub repo, then deploy to Vercel.")
