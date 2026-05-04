#!/usr/bin/env python3
"""
GRN Site Builder — Guardian Restoration Network
Generates all national service pages and city pages from master template.
Run: python3 build_grn.py
Output: ./output/ directory
"""

import json, os, shutil

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
.nav-logo { text-decoration: none; display: flex; align-items: center; flex-shrink: 0; }
.nav-right { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }
.nav-phone { color: #ff5500; font-size: 14px; font-weight: 700; text-decoration: none; white-space: nowrap; }
.nav-phone:hover { color: #ff7a00; }
.btn-nav { background: var(--orange); color: var(--white); padding: 10px 22px; border-radius: 6px; font-size: 14px; font-weight: 700; text-decoration: none; text-transform: uppercase; letter-spacing: 0.5px; transition: background 0.2s; white-space: nowrap; }
.btn-nav:hover { background: var(--orange-light); }
.nav-link { color: var(--white); font-size: 14px; font-weight: 600; text-decoration: none; padding: 8px 12px; border-radius: 4px; transition: background 0.2s, color 0.2s; white-space: nowrap; }
.nav-link:hover { background: rgba(255,85,0,0.15); color: var(--orange); }
.nav-link-active { color: var(--orange) !important; }
.nav-dropdown { position: relative; }
.nav-dropdown-menu { display: none; position: absolute; top: 100%; left: 0; background: var(--navy-light); border: 1px solid rgba(255,85,0,0.3); border-radius: 6px; min-width: 220px; padding: 8px 0; z-index: 999; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
.nav-dropdown:hover .nav-dropdown-menu { display: block; }
.nav-dropdown-label { font-size: 10px; font-weight: 700; letter-spacing: 2px; color: var(--orange); padding: 10px 16px 4px; }
.nav-dropdown-menu a { display: block; padding: 8px 16px; font-size: 13px; color: rgba(255,255,255,0.85); text-decoration: none; transition: background 0.2s; }
.nav-dropdown-menu a:hover { background: rgba(255,85,0,0.12); color: var(--white); }
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
    """City page nav — conversion only. No links away from page."""
    return f"""<nav class="nav">
  <span class="nav-logo" aria-label="{BRAND}">{NAV_LOGO}</span>
  <div class="nav-right">
    <a href="tel:{PHONE_TEL}" class="nav-phone" aria-label="Call {BRAND}">📞 {PHONE_DISPLAY}</a>
    <a href="/contact/" class="btn-nav" aria-label="Get Help Now">Get Help Now</a>
  </div>
</nav>"""

def full_nav(active=""):
    """Full nav for national/site pages with dropdown and all links."""
    return f"""<nav class="nav">
  <a href="/" class="nav-logo" aria-label="{BRAND} Home"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 132" height="48" width="auto">
  <path d="M54 0 L108 20 L108 66 C108 97 82 116 54 128 C26 116 0 97 0 66 L0 20 Z" fill="#ff5500"/>
  <path d="M54 9 L99 27 L99 66 C99 93 75 111 54 120 C33 111 9 93 9 66 L9 27 Z" fill="none" stroke="#000000" stroke-width="2.8" opacity="0.75"/>
  <text x="54" y="93" font-family="Arial Black, sans-serif" font-size="70" font-weight="900" fill="white" text-anchor="middle">G</text>
  <text x="122" y="52" font-family="Arial, sans-serif" font-size="44" font-weight="700" fill="white" letter-spacing="-0.5">GUARDIAN</text>
  <text x="124" y="78" font-family="Arial, sans-serif" font-size="15" font-weight="400" fill="#ff5500" letter-spacing="3.5">RESTORATION NETWORK</text>
  <rect x="124" y="86" width="338" height="1.5" rx="1" fill="#ff5500" opacity="0.5"/>
  <text x="124" y="102" font-family="Arial, sans-serif" font-size="10.5" fill="#ff7a00" letter-spacing="1.2">DAMAGE COVERED. EXPERT DISPATCHED.</text>
</svg></a>
  <div class="nav-right" style="gap:6px;">
    <div class="nav-dropdown">
      <a href="/services/" class="nav-link">Services ▾</a>
      <div class="nav-dropdown-menu">
        <div class="nav-dropdown-label">RESTORATION</div>
        <a href="/water-damage-restoration/">Water Damage</a>
        <a href="/fire-damage-restoration/">Fire Damage</a>
        <a href="/mold-remediation/">Mold Remediation</a>
        <a href="/storm-damage-restoration/">Storm Damage</a>
        <a href="/biohazard-cleanup/">Biohazard Cleanup</a>
        <a href="/asbestos-abatement/">Asbestos Abatement</a>
        <div class="nav-dropdown-label">CONSTRUCTION</div>
        <a href="/general-contractor/">Reconstruction &amp; GC Work</a>
      </div>
    </div>
    <a href="/how-it-works/" class="nav-link{"" if active != "how-it-works" else " nav-link-active"}">How It Works</a>
    <a href="/about/" class="nav-link{"" if active != "about" else " nav-link-active"}">About</a>
    <a href="/faq/" class="nav-link{"" if active != "faq" else " nav-link-active"}">FAQ</a>
    <a href="/contact/" class="nav-link{"" if active != "contact" else " nav-link-active"}">Contact</a>
    <a href="tel:{PHONE_TEL}" class="nav-phone" aria-label="Call {BRAND}">📞 {PHONE_DISPLAY}</a>
    <a href="/contact/" class="btn-nav" aria-label="Get Help Now">Get Help Now</a>
  </div>
</nav>"""

def full_footer():
    """Full footer for national/site pages with nav columns."""
    return f"""<footer class="footer" style="background:#06111f;padding:60px 5% 32px;">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:40px;max-width:1100px;margin:0 auto 40px;">
    <div>
      <a href="/" aria-label="{BRAND} Home" style="display:block;margin-bottom:14px;">{FOOTER_LOGO}</a>
      <p style="color:rgba(255,255,255,0.5);font-size:14px;line-height:1.6;">America's trusted insurance claim management and restoration network. Available 24/7 at {PHONE_DISPLAY}.</p>
    </div>
    <div>
      <h4 style="color:#fff;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Services</h4>
      <a href="/water-damage-restoration/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Water Damage</a>
      <a href="/fire-damage-restoration/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Fire Damage</a>
      <a href="/mold-remediation/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Mold Remediation</a>
      <a href="/storm-damage-restoration/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Storm Damage</a>
      <a href="/biohazard-cleanup/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Biohazard Cleanup</a>
      <a href="/asbestos-abatement/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Asbestos Abatement</a>
    </div>
    <div>
      <h4 style="color:#fff;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Company</h4>
      <a href="/how-it-works/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">How It Works</a>
      <a href="/about/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">About</a>
      <a href="/faq/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">FAQ</a>
      <a href="/contact/" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">Contact</a>
      <a href="tel:{PHONE_TEL}" style="display:block;color:rgba(255,255,255,0.55);font-size:14px;text-decoration:none;margin-bottom:8px;">{PHONE_DISPLAY}</a>
    </div>
  </div>
  <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:20px;max-width:1100px;margin:0 auto;">
    <p style="color:rgba(255,255,255,0.3);font-size:12px;">&copy; 2026 {LEGAL}. All rights reserved. Contractor dispatch subject to availability in your area. You are responsible for your deductible per your policy.</p>
  </div>
</footer>"""

def conversion_footer():
    """City page footer — conversion only. No nav columns."""
    return f"""<footer class="footer">
  <div class="footer-simple">
    <span aria-label="{BRAND}">{FOOTER_LOGO}</span>
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


# ─── PAGE BUILDERS ───────────────────────────────────────────────────────────

def build_national_page(svc_key):
    s = SERVICES[svc_key]
    canonical = f"{DOMAIN}{s['national_url']}"
    title = f"{s['name']} | {BRAND}"
    meta_desc = f"Need {s['name'].lower()}? {BRAND} confirms your active insurance coverage, manages your claim with your carrier, and dispatches vetted licensed contractors nationwide. Call {PHONE_DISPLAY}."

    # JSON-LD
    faq_schema = "\n".join([
        f'''    {{"@type":"Question","name":{json.dumps(q)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a)}}}}}{"," if i < len(s["faqs"])-1 else ""}'''
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
{schema}
<style>{SHARED_CSS}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&family=Barlow+Condensed:wght@700;800;900&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
</head>
<body>

{full_nav()}

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

{full_footer()}

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
        f'''    {{"@type":"Question","name":{json.dumps(q)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a)}}}}}{"," if i < len(s["faqs"])-1 else ""}'''
        for i, (q, a) in enumerate(s["faqs"])
    ])

    # HowTo steps from expect_steps
    howto_steps = "\n".join([
        f'''      {{"@type":"HowToStep","position":{i+1},"name":{json.dumps(h)},"text":{json.dumps(p)}}}{"," if i < len(s["expect_steps"])-1 else ""}'''
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
  </div>
</section>

<div class="trust-bar">{trust_bar_html}</div>

<div class="urgency"><p>⚡ Emergency response available 24/7 in {city}, {abbrev} — <a href="tel:{PHONE_TEL}" aria-label="Call now">Call {PHONE_DISPLAY}</a>. Subject to contractor availability in your area.</p></div>

<section style="background:#f8fafc;padding:56px 5%;">
  <div style="max-width:780px;margin:0 auto;">
    <h2 style="font-size:clamp(22px,3vw,32px);font-weight:900;color:#0b1d3a;margin-bottom:8px;text-align:center;">Get Help Now — Coverage Confirmed Fast</h2>
    <p style="font-size:15px;color:#64748b;text-align:center;margin-bottom:28px;">Fill out the form below or call <a href="tel:{PHONE_TEL}" style="color:#ff5500;font-weight:700;">{PHONE_DISPLAY}</a>. A Guardian specialist will confirm your coverage and dispatch a contractor fast.</p>
    <iframe
      src="https://api.leadconnectorhq.com/widget/form/ooQzkbZcqnXMsSX8FgKQ"
      style="width:100%;min-height:700px;border:none;border-radius:4px;"
      id="inline-ooQzkbZcqnXMsSX8FgKQ"
      data-layout="{{'id':'INLINE'}}"
      data-trigger-type="alwaysShow"
      data-activation-type="alwaysActivated"
      data-deactivation-type="neverDeactivate"
      data-form-name="GRN Contact Form"
      data-form-id="ooQzkbZcqnXMsSX8FgKQ"
      title="GRN Contact Form">
    </iframe>
    <script src="https://link.msgsndr.com/js/form_embed.js"></script>
  </div>
</section>

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

    return json.dumps({"routes": routes}, indent=2)


# ─── MAIN BUILD ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building GRN site...")
    rankmath_output = []

    # Copy homepage (already exists in output)
    # shutil.copy("./grn-homepage-v7.html", f"{OUTPUT_DIR}/grn-homepage-v7.html")
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
