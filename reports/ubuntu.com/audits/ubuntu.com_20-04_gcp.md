# UX content audit report — live page

**URL:** https://ubuntu.com/20-04/gcp
**Date:** Wed May 13 2026
**Copydoc:** none found
**Note:** Content captured from static HTML; JS-rendered elements (e.g., blog loading) may not be fully represented.

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 3 | 0 | 2 | 1 |

**Total issues:** 3 (0 critical, 2 needs work, 1 minor)
**Total passes:** 3

---

## UX quality check

### Structure & hierarchy

#### Critical
- None identified

#### Needs Work
- **[Section: Urgency messaging]** — The urgency about EOS (End of Standard Support) on May 31, 2025 is prominent but could be more actionable upfront
  - *Found:* "Ubuntu 20.04 LTS (Focal Fossa) is reaching the end of its 5 years of standard support on May 31, 2025, exposing your systems to unpatched vulnerabilities."
  - *Recommendation:* Add a more prominent CTA button above the fold alongside the urgency message to drive immediate action

- **[Section: Options presentation]** — The two main options are clear but could benefit from visual differentiation to help users compare
  - *Found:* "1. Upgrade to an Ubuntu version with active standard support" / "2. Attach an Ubuntu Pro 20.04 subscription to expand your security maintenance"
  - *Recommendation:* Consider using side-by-side comparison cards or a visual decision tree to help users choose between upgrade paths

#### Minor
- **[Section: Date formatting]** — Inconsistent date format across the page
  - *Found:* "May 31, 2025" vs "2027" vs "2029" vs "2030"
  - *Recommendation:* Standardize date formats throughout (e.g., "May 31, 2025" consistently)

### CTAs

#### Critical
- None identified

#### Needs Work
- **[Section: Primary CTAs]** — Multiple CTAs present but hierarchy could be clearer
  - *Found:* "Upgrade now", "Launch a new instance", "Contact us to purchase annual subscription tokens"
  - *Recommendation:* Establish a clear primary CTA (e.g., "Upgrade now") vs secondary CTAs (contact, learn more) with visual weight differentiation

#### Minor
- **[Section: CTA consistency]** — Some CTAs use "›" suffix, others don't
  - *Found:* "Learn more about the Ubuntu lifecycle and release cadence ›" vs "Launch a new instance of Ubuntu 22.04 LTS on GCP"
  - *Recommendation:* Apply consistent CTA styling (with or without arrow indicator)

### Links

#### Critical
- None identified

#### Needs Work
- **[Section: External link clarity]** — External links to Google Cloud Console could benefit from clearer indication
  - *Found:* Links to console.cloud.google.com without external link indicators
  - *Recommendation:* Add external link icons or "(opens in new tab)" text for clarity

#### Minor
- **[Section: Link text variety]** — Some link text could be more descriptive
  - *Found:* Links to discourse.ubuntu.com forum
  - *Recommendation:* Consider adding "(forum)" or similar indicator for community forum links

### Forms & inputs

#### Critical
- None identified

#### Needs Work
- **[Section: Contact form accessibility]** — No visible form on this page, but contact options are link-based
  - *Found:* "Contact us to purchase annual subscription tokens"
  - *Recommendation:* If forms are embedded on this page, ensure proper ARIA labels and field associations

### Error & feedback states

#### Critical
- None identified

#### Needs Work
- **[Section: EOS warning clarity]** — The End of Support warning is clear but could include more specific consequences
  - *Found:* "exposing your systems to unpatched vulnerabilities"
  - *Recommendation:* Consider adding a brief note about potential compliance impacts for enterprise users

### Accessibility

#### Critical
- None identified

#### Needs Work
- **[Section: Image alt text]** — Images appear to have alt attributes but could be more descriptive
  - *Found:* Various promotional images with generic alt text
  - *Recommendation:* Ensure alt text describes both the image content and its purpose/context

### Navigation

#### Critical
- None identified

#### Needs Work
- **[Section: Breadcrumb navigation]** — No breadcrumb present to help users understand their location
  - *Found:* Page shows "20.04" in nav but no breadcrumb trail
  - *Recommendation:* Add breadcrumb (e.g., Ubuntu 20.04 > Google Cloud) for better orientation

### Mobile considerations

#### Flag for review
- **[Section: Content density]** — The page contains substantial content that may require careful review on mobile
  - *Recommendation:* Test all sections on mobile devices to ensure readability and CTA accessibility

---

## What looks good

- **Clear urgency messaging** — The EOS date and security implications are communicated prominently and early
- **Well-structured options** — The two main paths (upgrade vs Ubuntu Pro) are clearly distinguished with numbered sections
- **Customer testimonials** — Real quotes from Interana and TIM add credibility and social proof
- **Comprehensive information** — Covers upgrade paths, ESM benefits, add-ons, and contact options in one place
- **Multiple engagement points** — Blog links and contact options provide various ways for users to engage

---

## Recommended priority order

1. Fix all Critical issues (none identified)
2. Address Needs Work items
   - Improve visual hierarchy and differentiation between upgrade options
   - Add clearer primary CTA above the fold
   - Consider adding external link indicators
3. Polish Minor items
   - Standardize date formatting
   - Ensure consistent CTA styling

---

## Manual checks for reviewer

- [ ] **Authenticated states** — log in and check any copy that only appears after authentication
- [ ] **JS-rendered content** — interact with the page to trigger dynamic states (errors, success messages, empty states)
- [ ] **Keyboard navigation** — tab through the page to confirm correct focus order and accessible labels
- [ ] **Mobile view** — resize or use device emulation to check layout and readability
