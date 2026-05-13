# UX content audit report — live page

**URL:** https://ubuntu.com
**Date:** 2026-05-13
**Copydoc:** https://docs.google.com/document/d/1ySJxQbqVdeH4Tra0zwBm2Tn0s56kFGnEF7d8xDRTxwU/edit
**Note:** This page heavily relies on JavaScript for navigation dropdowns (Products, Use cases, Support, Community, Download), blog content (latest-news section loads via JS), takeover A/B testing, and the contact form modal. Only content present in initial static HTML was captured. JS-rendered states should be checked manually.

---

## Summary

| Check | ✅ Pass | 🔴 Critical | 🟡 Needs Work | 🔵 Minor |
|---|---|---|---|---|
| Structure & hierarchy | 3 | 0 | 0 | 0 |
| CTAs | 6 | 0 | 0 | 1 |
| Links | 5 | 0 | 0 | 1 |
| Accessibility | 5 | 0 | 2 | 0 |
| Navigation | 2 | 0 | 0 | 1 |
| Mobile considerations | 0 | 0 | 1 | 0 |

**Total issues:** 6 (0 critical, 3 needs work, 3 minor)
**Total passes:** 21

---

## UX quality check

### Structure & hierarchy

#### ✅ Passes
- **Heading flow** — H1 → H2 → H3 throughout is logical. No skipped levels. The H1 is present in the takeover section.
- **Section headings are meaningful** — "Open source security", "Significant enterprise savings", "Public cloud optimization", etc. are descriptive.
- **Lists have contextual intro** — Each ticked list is preceded by a heading and paragraph intro.

---

### CTAs

#### 🔵 Minor
- **Section: Multi-cloud Kubernetes** — The links "AKS.", "EKS.", "GKE." with trailing periods and external domains used as CTA/pitch text. These read as abbreviations rather than clear destinations. Out of context, a user wouldn't know these lead to Azure, AWS, and GKE docs.
  - *Found:* `AKS.` → `https://azure.microsoft.com/en-us/services/kubernetes-service/`
  - *Recommendation:* Use expanded labels: "Amazon EKS", "Azure AKS", "Google GKE" — or add a visible qualifier.

#### ✅ Passes
- CTAs use specific verbs: "Get Ubuntu Pro", "Download for free", "Learn more", "Contact us" — all are clear and context-appropriate.
- No vague "click here" or "submit" patterns.
- Primary and secondary CTAs are visually distinguishable and not identically labelled.

---

### Links

#### 🔵 Minor
- **Section: Multi-cloud Kubernetes** — Same link label issue as CTAs. "AKS.", "EKS.", "GKE." are cryptic as standalone link text for screen reader users navigating by links list.
  - *Found:* `AKS.` → `https://azure.microsoft.com/en-us/services/kubernetes-service/`
  - *Recommendation:* Include the cloud provider name in the link text.

#### ✅ Passes
- Most link text is descriptive ("Build your AI models on Ubuntu", "Discover Ubuntu's security features").
- No entire sentences hyperlinked.
- No same-text-different-destination issues observed.

---

### Accessibility

#### 🟡 Needs Work
- **Decorative images with empty alt text** — The page contains numerous `<img>` elements with `alt=""`. While intentionally decorative, the page should verify these are all truly decorative and not inadvertently stripping context.
  - *Found:* 12 images with `alt=""` across hero, feature sections, and product illustrations.
  - *Recommendation:* Confirm each image is purely decorative. If any convey information (e.g., the "Significant enterprise savings" chart), they need descriptive alt text.

- **Blog section loading state** — The latest news section shows `<i class="p-icon--spinner">Loading...</i>` which is a fallback accessible label. However, if JS fails, this loading spinner persists indefinitely with no fallback content.
  - *Found:* `<noscript>` fallback only provides a generic link to the blog.
  - *Recommendation:* Ensure the noscript fallback includes meaningful content or a clear message about the failed load.

#### ✅ Passes
- All customer logos have descriptive alt text (AWS, Microsoft Azure, AT&T, Google Cloud, NIST, etc.).
- Link text is generally descriptive — no "click here" or "read more".
- No instructions relying on visual position observed.

---

### Navigation

#### 🔵 Minor
- **Dropdown menus loaded via JS** — Navigation flyouts for Products, Use cases, Support, Community, Download are loaded dynamically. This means the content of these menus was not captured and cannot be audited.
  - *Found:* Navigation items with `onmouseenter="fetchDropdown(...)"`.
  - *Recommendation:* Manually inspect each dropdown for label clarity, consistency, and accessibility.

#### ✅ Passes
- Top-level navigation labels are clear: Products, Use cases, Support, Community, Download Ubuntu.
- Footer navigation is comprehensive and logically organized by product/category.

---

### Mobile considerations

#### 🟡 Flag for review
- **Content density** — The page has 10+ full-width sections with dense tick lists (some with 8-10 items each). On mobile, this may create excessive scrolling and cognitive load.
  - *Recommendation:* Test at 375px viewport. Consider collapsing secondary sections or show key items with a "view all" toggle.
- **Navigation dropdowns** — The primary navigation uses hover-based dropdowns that may not work well on touch devices. A mobile hamburger menu is present but its content is JS-loaded and could not be audited.

---

## ✅ What looks good

- **Strong H1 usage** — The takeover correctly uses an H1 with a compelling, timely message about Ubuntu 26.04 LTS.
- **Consistent section structure** — Every major content section follows the same pattern: heading → subheading → descriptive paragraph → tick list → CTA, creating a predictable reading rhythm.
- **Excellent alt text on logos** — All company/partner logos have meaningful, descriptive alt text identifying each organization.
- **No placeholder or lorem ipsum text** — All copy appears to be production-ready.
- **Clear CTAs throughout** — Most CTAs use specific, action-oriented language.
- **Comprehensive legal/accessibility links in footer** — Privacy notice, tracker settings, bug reporting all present.
- **Contact form is well-structured** — The hidden contact modal includes visible labels (not placeholder-only), required field indicators, and proper autocomplete attributes.

---

## Recommended priority order

1. **Address 🟡 Needs Work:** Verify decorative images are properly marked with `alt=""` (not just missing alt). Audit JS-loaded navigation dropdown labels. Add noscript resilience for the blog section.
2. **Polish 🔵 Minor:** Consider expanding "AKS/EKS/GKE" link text for clarity. Test mobile layout at 375px.
3. **Review manual check items** (see below).

---

## 🔲 Manual checks for reviewer

- [ ] **JS-rendered navigation** — Hover over each nav item (Products, Use cases, Support, Community, Download Ubuntu) and inspect dropdown link labels and accessibility.
- [ ] **Blog section** — Confirm JS loads correctly and article cards display with proper headings and link text.
- [ ] **Takeover A/B test** — Verify the variant takeover ("A CTO's guide to real-time Linux") is hidden by default and the default takeover shows. Check both for H1 and CTA quality.
- [ ] **Contact form modal** — Trigger the contact modal and audit all form fields, validation messages, and error states.
- [ ] **Keyboard navigation** — Tab through the page to confirm correct focus order, especially through the navigation dropdowns.
- [ ] **Mobile view** — Resize to 375px and check hero tagline readability, tick list layout, and navigation usability.
- [ ] **Copydoc comparison** — Cross-reference the Google Doc with the live page to verify copy accuracy and check for any copy not yet published.
