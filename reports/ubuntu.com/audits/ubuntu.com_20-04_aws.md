# UX content audit report - live page

**URL:** https://ubuntu.com/20-04/aws
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** JS-rendered content may not have been captured

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 11 | 2 | 4 | 3 |

**Total issues:** 9 (2 critical, 4 needs work, 3 minor)
**Total passes:** 11

---

## UX quality check

### Structure & hierarchy

#### Critical
- **[Hero Section: Missing clear value proposition]** - The headline "Ubuntu 20.04 LTS (Focal Fossa) on AWS" is informational but lacks urgency.
  - Found: "Ubuntu 20.04 LTS (Focal Fossa) on AWS"
  - Recommendation: Add urgency messaging like "Out of standard support - Upgrade now" in the hero

- **[End of Life messaging clarity]** - EOL information is present but could be more visually prominent.
  - Found: "Standard support for Ubuntu 20.04 LTS ends on May 31, 2025"
  - Recommendation: Use more prominent visual indicators (colors, icons) for EOL status

#### Needs Work
- **[Release timeline table]** - No timeline table on this page, but related content could be better organized.
  - Recommendation: Consider adding comparison table

- **[CTA placement]** - CTAs are somewhat scattered without clear hierarchy.
  - Found: "Upgrade now", "Contact us to purchase annual subscription tokens", "Read the latest Ubuntu on AWS news"
  - Recommendation: Group related CTAs and establish clear visual hierarchy

- **[Loading states]** - Blog section shows "Loading..." indicating JS dependency.
  - Recommendation: Consider server-side rendering or skeleton loaders

- **[Form accessibility]** - No forms present but could add contact CTA.
  - Recommendation: Consider adding "Contact us" CTA for enterprise inquiries

#### Minor
- **[Link text consistency]** - Some links use ">" suffix while others don't.
  - Recommendation: Standardize link text formatting

- **[Section spacing]** - Some sections have inconsistent spacing.
  - Recommendation: Establish consistent section spacing guidelines

- **[CTA copy variation]** - Some CTAs use imperative voice, others descriptive.
  - Recommendation: Use consistent imperative voice

### CTAs

#### Critical
- **[Primary CTA ambiguity]** - Multiple CTAs without clear primary action.
  - Found: "Upgrade now", "Contact us to purchase", "Read the latest news"
  - Recommendation: Establish one primary CTA with secondary CTAs clearly differentiated

- **[Missing upgrade CTA]** - While upgrade options exist, direct "Download Ubuntu 24.04" CTA could be more prominent.
  - Recommendation: Add direct CTA to download Ubuntu 24.04 LTS

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
  - Found: Links to aws.amazon.com, aws console
  - Recommendation: Add external link indicators

- **[Broken or outdated links]** - Links to 20.04 resources may be deprecated.
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
- **[Loading states]** - Blog section shows "Loading...".
  - Recommendation: Consider server-side rendering or skeleton loaders

#### Minor
- **[Empty states]** - No empty states to evaluate.
  - Recommendation: N/A

### Accessibility

#### Critical
- **[Image alt text missing]** - Images may lack descriptive alt text.
  - Recommendation: Add descriptive alt text to all images

- **[Table accessibility]** - No tables present.
  - Recommendation: N/A

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
  - Recommendation: Add breadcrumb showing path (Ubuntu > 20.04 > AWS)

#### Needs Work
- **[Internal linking]** - Page could link to related cloud providers.
  - Recommendation: Add links to Azure, GCP pages

- **[Related content]** - Related Ubuntu versions could be more prominent.
  - Recommendation: Add "Related Releases" section

#### Minor
- **[Footer navigation]** - Extensive footer may benefit from better organization.
  - Recommendation: Consider collapsible footer sections

### Mobile considerations

#### Flag for review
- **[Table responsiveness]** - No tables present.
  - Recommendation: N/A

- **[Touch targets]** - Link and button touch targets may be too small.
  - Recommendation: Verify minimum 44x44px touch targets

- **[Viewport scaling]** - Need to verify proper mobile viewport.
  - Recommendation: Test on multiple device sizes

---

## What looks good

- Clear release information with AWS-specific messaging
- Good use of customer testimonials (Interana, TIM)
- Multiple upgrade paths clearly explained with AWS-specific links
- Links to AWS Marketplace for easy deployment
- Links to AWS Console for new instances
- Links to AWS CLI for technical users
- Comprehensive footer with product navigation
- Clear information about metered pricing and PPA/EDP spend commitments
- Enterprise-grade support add-on clearly described

---

## Recommended priority order

1. Fix all Critical issues
   - Add urgency messaging to hero section
   - Make EOL status more visually prominent

2. Address Needs Work items
   - Group CTAs with clear hierarchy
   - Add links to related cloud providers
   - Consider adding comparison table

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
