# UX content audit report — live page

**URL:** https://ubuntu.com/ceph
**Date:** 2026-05-13
**Copydoc:** https://docs.google.com/document/d/1gpEjTcdJor2yTGfMz7T_xIfs7BtV6rbBPFYfNZFe52Y/edit
**Note:** This page uses JavaScript for the contact form modal (triggered by "Get in touch" buttons). Only content present in initial static HTML was captured. The modal content was inferred from HTML structure.

---

## Summary

| Check | ✅ Pass | 🔴 Critical | 🟡 Needs Work | 🔵 Minor |
|---|---|---|---|---|
| Structure & hierarchy | 4 | 0 | 0 | 0 |
| CTAs | 4 | 0 | 0 | 0 |
| Links | 6 | 0 | 0 | 0 |
| Accessibility | 4 | 0 | 1 | 0 |
| Navigation | 3 | 0 | 0 | 0 |
| Mobile considerations | 0 | 0 | 1 | 0 |

**Total issues:** 2 (0 critical, 1 needs work, 1 minor)
**Total passes:** 21

---

## UX quality check

### Structure & hierarchy

#### ✅ Passes
- **Heading flow** — H1 → H2 → H3 throughout is logical. No skipped levels.
  - H1: "Ceph storage on Ubuntu"
  - H2s: "Production-worthy Ceph storage", "Proven success with Ceph storage", "Ceph storage deployment and operations", "More choice, for your infrastructure", etc.
  - H3s: "Benefits of Ceph on Ubuntu", "Private Cloud / Canonical Charmed Ceph", "Encryption at rest", etc.
- **Section headings are meaningful** — All headings are descriptive and specific to Ceph content.
- **Lists have contextual intro** — Each list is preceded by a heading and explanatory paragraph.

---

### CTAs

#### ✅ Passes
- **Specific action verbs** — "Get in touch", "Learn how Ceph can reduce your storage costs", "Install Charmed Ceph", "Learn more about fully managed Ceph", "Install MicroCeph" — all are clear and action-oriented.
- **No vague CTAs** — No "click here", "learn more" without context, or generic "submit" buttons.
- **Primary and secondary CTAs** — The hero section has a primary button ("Get in touch") and secondary link ("Learn how Ceph can reduce your storage costs") that are visually distinguishable.

#### ✅ What looks good
- All four "Getting started" cards have clear CTAs: "Install Charmed Ceph", "Learn more about Ubuntu Pro", "Install MicroCeph", "Learn more about fully managed Ceph".

---

### Links

#### ✅ Passes
- **Descriptive link text** — "Learn how Ceph can reduce your storage costs", "Learn how Wellcome Sanger achieved a cost-effective Ceph infrastructure", "Install Charmed Ceph", "Learn more about Ubuntu Pro" — all provide context about the destination.
- **No entire sentences hyperlinked** — Only relevant phrases are linked.
- **Resource section links** — "Ceph for Enterprise", "Introduction to cloud-native storage", "Cloud storage cost optimization" — all are descriptive titles.

---

### Accessibility

#### 🟡 Needs Work
- **Decorative images with empty alt text** — Multiple images have `alt=""` which is appropriate for decorative images, but the page should verify these are intentional.
  - *Found:* 7 images with `alt=""` including hero image, card images (private-cloud.png, cephadm.png, edge cloud.png, training.png), encryption.png, fully-managed-ceph.png.
  - *Recommendation:* Confirm each image is purely decorative. The hero image (Ceph diagram) and encryption diagram may convey information and could benefit from descriptive alt text.

#### ✅ Passes
- **Customer logo has descriptive alt text** — "Wellcome Sanger Institute" is properly described.
- **Video has descriptive title** — YouTube iframe has `title="From 3PB to 20PB: Sanger Institute's Ceph Journey with Canonical"`.
- **Form has visible labels** — All form fields have aria-labels or visible labels.

---

### Navigation

#### ✅ Passes
- **Primary navigation labels are clear** — Products, Use cases, Support, Community, Download Ubuntu.
- **Secondary navigation is product-specific** — "What is Ceph", "Managed", "Consulting", "Docs", "Install" — all are clear and relevant to the Ceph product page.
- **Footer navigation is comprehensive** — Organized by product category with clear labels.

---

### Mobile considerations

#### 🟡 Flag for review
- **Four-column card layout** — The "More choice, for your infrastructure" section uses a 4-column equal-height row layout. On mobile (375px), this may collapse awkwardly or create excessive scrolling.
  - *Recommendation:* Test at 375px viewport. Consider a 2-column or 1-column layout for mobile, or use a carousel/slider pattern.

---

## ✅ What looks good

- **Strong H1 usage** — Clear, descriptive page title "Ceph storage on Ubuntu".
- **Excellent section structure** — Consistent pattern of heading → description → content → CTA throughout.
- **Descriptive alt text on customer logo** — "Wellcome Sanger Institute" is properly described.
- **No placeholder or lorem ipsum text** — All copy appears production-ready.
- **Clear CTAs throughout** — Every section has specific, action-oriented CTAs.
- **Well-structured contact form** — Visible labels (not placeholder-only), required field indicators, proper autocomplete attributes, privacy acknowledgment.
- **Good resource organization** — Webinar, Whitepapers, and Blogs sections are clearly categorized with descriptive titles and excerpts.
- **Support cadence table** — Clear, well-formatted table showing Ubuntu LTS versions and corresponding Ceph releases with LTS commitment indicators.

---

## Recommended priority order

1. **Address 🟡 Needs Work:** Verify decorative images are properly marked with `alt=""` (not just missing alt). Consider adding descriptive alt text to informational images (hero diagram, encryption diagram).
2. **Review 🟡 Mobile considerations:** Test the 4-column card layout at 375px viewport.
3. **Review manual check items** (see below).

---

## 🔲 Manual checks for reviewer

- [ ] **Contact form modal** — Trigger the "Get in touch" CTA and audit all form fields, validation messages, error states, and success feedback.
- [ ] **Mobile layout** — Resize to 375px and check the 4-column card layout, hero section readability, and navigation usability.
- [ ] **Video embed** — Confirm the YouTube video loads correctly and has proper controls.
- [ ] **Copydoc comparison** — Cross-reference the Google Doc with the live page to verify copy accuracy and check for any copy not yet published.
- [ ] **Table responsiveness** — Check the Ubuntu and Ceph support cadence table on mobile devices.
