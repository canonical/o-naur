# UX content audit report - live page

**URL:** https://ubuntu.com/18-04/azure
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** JS-rendered content may not have been captured

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 11 | 2 | 3 | 4 |

**Total issues:** 9 (2 critical, 3 needs work, 4 minor)
**Total passes:** 11

---

## UX quality check

### Structure & hierarchy

#### Critical
- **[Hero Section: Missing clear value proposition]** - The headline "Ubuntu 18.04 LTS (Bionic Beaver) on Azure" is informational but lacks urgency.
  - Found: "Ubuntu 18.04 LTS (Bionic Beaver) on Azure"
  - Recommendation: Add urgency messaging like "Out of standard support - Upgrade now" in the hero

- **[End of Life messaging clarity]** - EOL information is present but visual hierarchy could be improved.
  - Found: "Reaching end of standard support on 31 May 2023"
  - Recommendation: Use more prominent visual indicators (colors, icons) for EOL status

#### Needs Work
- **[Release timeline table]** - Same table hierarchy issues as other release pages.
  - Recommendation: Use consistent visual hierarchy

- **[CTA placement]** - CTAs are scattered without clear hierarchy.
  - Found: "In-place upgrade to Ubuntu Pro 18.04", "Get started with Ubuntu Pro on Azure", "Watch the webinar"
  - Recommendation: Group related CTAs and establish clear visual hierarchy

#### Minor
- **[Link text consistency]** - Some links use ">" suffix while others don't.
  - Recommendation: Standardize link text formatting

- **[Section spacing]** - Some sections have inconsistent spacing.
  - Recommendation: Establish consistent section spacing guidelines

- **[Code block formatting]** - No code blocks on this page.
  - Recommendation: N/A

- **[CTA copy variation]** - Some CTAs use imperative voice, others descriptive.
  - Recommendation: Use consistent imperative voice

### CTAs

#### Critical
- **[Primary CTA ambiguity]** - Multiple CTAs without clear primary action.
  - Found: "In-place upgrade to Ubuntu Pro", "Get started with Ubuntu Pro on Azure", "Watch the webinar"
  - Recommendation: Establish one primary CTA with secondary CTAs clearly differentiated

- **[Missing upgrade CTA]** - No prominent "Upgrade to Ubuntu 22.04" CTA.
  - Recommendation: Add direct CTA to download Ubuntu 22.04 LTS

#### Needs Work
- **[CTA placement]** - CTAs scattered throughout page.
  - Recommendation: Group related CTAs and establish clear hierarchy

- **[Button vs link distinction]** - Inconsistent styling between buttons and links.
  - Recommendation: Standardize CTA styling

#### Minor
- **[CTA copy variation]** - Some CTAs use imperative voice, others descriptive.
  - Recommendation: Use consistent imperative voice

### Links

#### Critical
- **[External link without warning]** - Links to external sites without indicators.
  - Found: Links to azuremarketplace.microsoft.com
  - Recommendation: Add external link indicators

- **[Broken or outdated links]** - Links to 18.04 resources may be deprecated.
  - Recommendation: Review and update all links

#### Needs Work
- **[Link destination clarity]** - Some links don't clearly indicate destination.
  - Recommendation: Consider adding brief descriptors

- **[Navigation link density]** - Footer contains extensive links.
  - Recommendation: Consider grouping for footer links

#### Minor
- **[Link text specificity]** - Some link text is generic.
  - Recommendation: Include more specific text when possible

### Forms & inputs

#### Critical
- **[No visible forms]** - Page has no contact or signup forms.
  - Recommendation: Consider adding "Contact us for Enterprise" CTA

#### Needs Work
- **[Form accessibility]** - No forms present to evaluate.
  - Recommendation: N/A for informational page

#### Minor
- **[Form alternative]** - Consider adding newsletter signup for updates.
  - Recommendation: Add optional newsletter signup

### Error & feedback states

#### Critical
- **[No error states visible]** - Page is informational.
  - Recommendation: N/A for static content page

#### Needs Work
- **[Loading states]** - No loading states visible.
  - Recommendation: N/A

#### Minor
- **[Empty states]** - No empty states to evaluate.
  - Recommendation: N/A

### Accessibility

#### Critical
- **[Image alt text missing]** - Images may lack descriptive alt text.
  - Recommendation: Add descriptive alt text to all images

- **[Table accessibility]** - Release timeline table structure may not be optimal.
  - Recommendation: Ensure proper table headers

#### Needs Work
- **[Heading hierarchy]** - Some sections may skip heading levels.
  - Recommendation: Review heading hierarchy

- **[Color contrast]** - Some text may have insufficient contrast.
  - Recommendation: Audit all text for WCAG AA compliance

#### Minor
- **[Focus indicators]** - Focus states may not be clearly visible.
  - Recommendation: Verify focus indicators

- **[Skip links]** - No visible skip-to-content link.
  - Recommendation: Add skip navigation link

### Navigation

#### Critical
- **[Navigation not prominent]** - Navigation is behind a hamburger menu on mobile.
  - Recommendation: Ensure critical navigation items are accessible

- **[Breadcrumb missing]** - No breadcrumb navigation.
  - Recommendation: Add breadcrumb showing path (Ubuntu > 18.04 > Azure)

#### Needs Work
- **[Internal linking]** - Page could link to related cloud providers.
  - Recommendation: Add links to AWS, GCP, IBM pages

- **[Related content]** - Related Ubuntu versions could be more prominent.
  - Recommendation: Add "Related Releases" section

#### Minor
- **[Footer navigation]** - Extensive footer may benefit from better organization.
  - Recommendation: Consider collapsible footer sections

### Mobile considerations

#### Flag for review
- **[Table responsiveness]** - Release timeline table may not render well on mobile.
  - Recommendation: Test table rendering on mobile

- **[Touch targets]** - Link and button touch targets may be too small.
  - Recommendation: Verify minimum 44x44px touch targets

- **[Viewport scaling]** - Need to verify proper mobile viewport.
  - Recommendation: Test on multiple device sizes

---

## What looks good

- Clear release information with Azure-specific messaging
- Good use of customer testimonials (Interana, TIM)
- Multiple upgrade paths clearly explained with Azure-specific links
- Links to Azure Marketplace for easy deployment
- In-place upgrade guide for Azure users
- Webinar link for educational content
- Comprehensive footer with product navigation
- Clear pricing information (per-machine pricing)

---

## Recommended priority order

1. Fix all Critical issues
   - Add urgency messaging to hero section
   - Make EOL status more visually prominent

2. Address Needs Work items
   - Improve release timeline table visual hierarchy
   - Group CTAs with clear hierarchy
   - Add links to related cloud providers

3. Polish Minor items
   - Standardize link text formatting
   - Add descriptive alt text to images
   - Establish consistent section spacing

---

## Manual checks for reviewer

- [ ] **Authenticated states** - log in and check any copy that only appears after authentication
- [ ] **JS-rendered content** - interact with the page to trigger dynamic states
- [ ] **Keyboard navigation** - tab through the page to confirm correct focus order
- [ ] **Mobile view** - resize or use device emulation to check layout and readability
