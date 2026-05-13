# UX content audit report — live page

**URL:** https://ubuntu.com/about
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** Informational page about Ubuntu project and its history

---

## Summary

| Check | ✅ Pass | 🔴 Critical | 🟡 Needs Work | 🔵 Minor |
|---|---|---|---|---|
| UX quality check | 5 | 1 | 5 | 3 |

**Total issues:** 9 (1 critical, 5 needs work, 3 minor)
**Total passes:** 5

---

## UX quality check

### Structure & hierarchy

#### 🔴 Critical
- **[No primary CTA]** — The page explains Ubuntu's story but lacks a clear action for users to take
  - *Found:* Multiple sections without primary call-to-action | *Recommendation:* Add clear CTA such as "Download Ubuntu", "Join the community", or "Get Ubuntu Pro"

#### 🟡 Needs Work
- **[Release table: Mobile responsiveness]** — Release table may not render correctly on mobile devices
  - *Found:* Release information table with multiple columns | *Recommendation:* Test table on mobile and consider horizontal scroll or stacked layout

- **[Navigation links: No breadcrumbs]** — Users may lose context of where they are in site hierarchy
  - *Found:* No breadcrumb trail visible | *Recommendation:* Add breadcrumbs: Home > About

- **[External link indicators missing]** — Links to external sites (wiki.ubuntu.com) don't indicate they're external
  - *Found:* Link to wiki.ubuntu.com/DerivativeTeam/Derivatives | *Recommendation:* Add icon or text indicator for external links

- **[Video content: No transcripts]** — Video content lacks text alternatives for accessibility
  - *Found:* "Download now" CTA with video reference | *Recommendation:* Provide transcripts or captions for video content

- **[Form visibility]** — Contact form is at bottom but may be missed
  - *Found:* Contact form at page end | *Recommendation:* Consider adding secondary CTA earlier in page

#### 🔵 Minor
- **[Footer: Dense navigation]** — Footer contains extensive links that may overwhelm users on mobile
  - *Found:* Multiple columns of links in footer | *Recommendation:* Consider accordion or collapsible sections for mobile

- **[Image optimization]** — Hero image could be optimized for web performance
  - *Found:* Hero image at top | *Recommendation:* Use WebP format and lazy loading

- **[Loading states]** — Blog section shows "*Loading...*" which provides no feedback on content availability
  - *Found:* "*Loading...*" in blog section | *Recommendation:* Add skeleton loader or empty state message

### CTAs

#### 🔴 Critical
- **[No primary CTA]** — The page explains Ubuntu's story but lacks a clear action for users to take
  - *Found:* Multiple sections without primary call-to-action | *Recommendation:* Add clear CTA such as "Download Ubuntu 24.04" or "Get Ubuntu Pro"

#### 🟡 Needs Work
- **[Download CTA: Buried at bottom]** — Primary conversion point is at page end
  - *Found:* "Download Ubuntu ›" at bottom | *Recommendation:* Add secondary CTA earlier in page

- **[Contact CTA: Not prominent]** — Contact option is in footer, not as primary action
  - *Found:* Footer links | *Recommendation:* Consider adding contact CTA in main content

#### 🔵 Minor
- **[CTA consistency]** — Some CTAs use button style, others use link style
  - *Found:* Mix of "Download Ubuntu ›" and "Find out more... ›" | *Recommendation:* Standardize CTA styling across page

### Links

#### 🔴 Critical
- **[No broken links detected]** — All extracted links appear to be valid internal or external references

#### 🟡 Needs Work
- **[External link indicators missing]** — Links to third-party sites don't indicate they lead outside ubuntu.com
  - *Found:* Links to wiki.ubuntu.com/DerivativeTeam/Derivatives | *Recommendation:* Add external link indicator

- **[Anchor text could be more descriptive]** — Some links use generic text
  - *Found:* "Find out more about the Ubuntu lifecycle ›" | *Recommendation:* Consider more specific anchor text

#### 🔵 Minor
- **[Link grouping]** — Related links could be grouped more clearly
  - *Found:* Multiple links scattered throughout | *Recommendation:* Group related links together

### Forms & inputs

#### 🔴 Critical
- **[No forms on this page]** — Page is informational without form elements

#### 🟡 Needs Work
- **[N/A]** — Not applicable

#### 🔵 Minor
- **[N/A]** — Not applicable

### Error & feedback states

#### 🔴 Critical
- **[No error states tested]** — This is a content page, not a form or interactive element

#### 🟡 Needs Work
- **[N/A]** — Not applicable

#### 🔵 Minor
- **[N/A]** — Not applicable

### Accessibility

#### 🔴 Critical
- **[No skip links]** — Page lacks "Skip to main content" link for keyboard users
  - *Found:* No skip link in navigation | *Recommendation:* Add skip link at page top

- **[No ARIA landmarks identified]** — Page structure may lack semantic landmarks
  - *Found:* Standard HTML structure but no visible ARIA | *Recommendation:* Ensure proper role attributes and landmarks

#### 🟡 Needs Work
- **[Image alt text unclear]** — Some images may lack descriptive alt text (content extraction limitation)
  - *Found:* Hero image | *Recommendation:* Audit all images for descriptive alt text

- **[Color contrast for CTAs]** — Need to verify CTA colors meet WCAG AA standards
  - *Found:* Various CTA links | *Recommendation:* Test contrast ratios

- **[Heading hierarchy]** — Need to verify H1-H6 hierarchy is logical for this informational page
  - *Found:* "# The story of Ubuntu" as H1 | *Recommendation:* Audit full heading structure

#### 🔵 Minor
- **[Focus indicators unclear]** — Focus states may not be visible for all interactive elements
  - *Found:* Various links | *Recommendation:* Ensure visible focus indicators

- **[Table accessibility]** — Release table may need ARIA attributes for screen readers
  - *Found:* Release information table | *Recommendation:* Add proper table semantics

### Navigation

#### 🔴 Critical
- **[No breadcrumbs]** — Page lacks breadcrumb navigation to help users understand their location
  - *Found:* No breadcrumb trail visible | *Recommendation:* Add breadcrumbs: Home > About

- **[No site search visible]** — Search functionality not prominent
  - *Found:* Search icon in header | *Recommendation:* Ensure search is accessible from all pages

#### 🟡 Needs Work
- **[Navigation depth]** — User must navigate through multiple levels to reach this page
  - *Found:* Path may require clicking through About section | *Recommendation:* Consider cross-linking from main navigation

#### 🔵 Minor
- **[Mobile menu]** — Hamburger menu may hide important navigation options
  - *Found:* "Menu" toggle in header | *Recommendation:* Test mobile navigation usability

### Mobile considerations

#### 🔵 Flag for review
- **[Table responsiveness]** — Release table needs mobile verification
  - *Found:* Release information table | *Recommendation:* Test on various screen sizes

- **[CTA touch targets]** — Buttons need adequate size for touch interaction
  - *Found:* "Download Ubuntu ›" CTA | *Recommendation:* Ensure minimum 44x44px touch targets

- **[Content readability]** — Text size and line length need mobile verification
  - *Found:* Body text throughout page | *Recommendation:* Test on mobile devices

- **[Hero image scaling]** — Hero image needs mobile verification
  - *Found:* Hero image at top | *Recommendation:* Test on various screen sizes

---

## ✅ What looks good

1. **Clear mission statement** — The definition of Ubuntu ("humanity to others") is beautifully explained

2. **Comprehensive release information** — Release table provides clear dates for all LTS versions

3. **Governance transparency** — Page explains how Ubuntu is governed independently of Canonical

4. **Historical context** — Page covers Ubuntu's history from 2004 to present

5. **Call to action at end** — Download CTA is provided for users ready to take action

6. **Consistent branding** — Page maintains Ubuntu branding throughout

---

## Recommended priority order

1. Fix all 🔴 Critical issues
   - Add primary CTA to drive user action

2. Address 🟡 Needs Work items
   - Add breadcrumbs
   - Improve table mobile responsiveness
   - Add external link indicators
   - Provide video transcripts
   - Add secondary CTA earlier in page

3. Polish 🔵 Minor items
   - Optimize images for web performance
   - Standardize CTA styling
   - Improve form visibility
   - Add skip links

---

## 🔲 Manual checks for reviewer

- [ ] **Authenticated states** — Check if logged-in users see different content or CTAs
- [ ] **JS-rendered content** — Verify blog section loads properly and doesn't show "*Loading...*" indefinitely
- [ ] **Keyboard navigation** — Tab through page to confirm correct focus order
- [ ] **Mobile view** — Resize or use device emulation to check layout and readability
- [ ] **Table rendering** — Test release table on various screen sizes
- [ ] **External links** — Verify all external links open in new tab appropriately
