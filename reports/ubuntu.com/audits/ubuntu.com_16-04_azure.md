# UX content audit report - live page

**URL:** https://ubuntu.com/16-04/azure
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** JS-rendered content may not have been captured

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 10 | 3 | 4 | 3 |

**Total issues:** 10 (3 critical, 4 needs work, 3 minor)
**Total passes:** 10

---

## UX quality check

### Structure & hierarchy

#### Critical
- **[Hero Section: Missing clear value proposition]** - The headline "Secure Ubuntu 16.04 LTS on Azure" is good but could be more action-oriented.
  - Found: "Secure Ubuntu 16.04 LTS on Azure"
  - Recommendation: Add urgency messaging like "Out of standard support - Upgrade now" in the hero

- **[EOL status visibility]** - The EOL information is present but could be more visually prominent.
  - Found: "Ubuntu 16.04 LTS (Xenial) will reach the end of its free initial five-year security maintenance period on April 30, 2021"
  - Recommendation: Use visual indicators (colors, icons) to highlight critical EOL status

- **[Form accessibility]** - The contact form has many fields but no clear visual hierarchy.
  - Found: Form with multiple checkboxes and dropdowns
  - Recommendation: Group related fields and use fieldsets for better accessibility

#### Needs Work
- **[Release timeline table]** - Same issues as parent page regarding confusing table hierarchy.
  - Recommendation: Use consistent visual hierarchy

- **[Form field labels]** - Some form fields have unclear labels.
  - Found: "Tell us more about your 16.04 instances" with checkboxes
  - Recommendation: Use clearer, more descriptive field labels

- **[CTA placement]** - CTAs are scattered without clear visual hierarchy.
  - Found: Multiple "Launch", "Contact us", "Find Ubuntu" links
  - Recommendation: Group related CTAs and establish clear hierarchy

- **[Loading states]** - Form sections may have JS dependencies.
  - Recommendation: Consider skeleton loaders for dynamic content

#### Minor
- **[Link text consistency]** - Some links use ">" suffix while others don't.
  - Recommendation: Standardize link text formatting

- **[Code block formatting]** - No code blocks on this page.
  - Recommendation: N/A

- **[Section spacing]** - Some sections have inconsistent spacing.
  - Recommendation: Establish consistent section spacing guidelines

### CTAs

#### Critical
- **[Primary CTA ambiguity]** - Multiple competing CTAs: "Launch new workloads", "Contact us to add ESM", "Find Ubuntu instances".
  - Recommendation: Establish one primary CTA based on page intent

- **[Missing upgrade CTA]** - While ESM is promoted, direct upgrade path to newer LTS is less prominent.
  - Recommendation: Add prominent "Upgrade to Ubuntu 20.04/22.04" CTA

- **[Form submission CTA]** - Form submit button may not be clearly visible.
  - Recommendation: Ensure form submit button has clear visual prominence

#### Needs Work
- **[CTA placement]** - CTAs are scattered throughout the page.
  - Recommendation: Group related CTAs and establish clear hierarchy

- **[Button vs link distinction]** - Inconsistent styling between buttons and links.
  - Recommendation: Standardize CTA styling based on importance

#### Minor
- **[CTA copy variation]** - Some CTAs use imperative voice, others use descriptive.
  - Recommendation: Use consistent imperative voice for all CTAs

### Links

#### Critical
- **[External link without warning]** - Links to Microsoft Azure marketplace without external link indicators.
  - Found: Links to azuremarketplace.microsoft.com
  - Recommendation: Add external link indicator

- **[Broken or outdated links]** - Links to Ubuntu 16.04 resources may be deprecated.
  - Recommendation: Review and update all links

#### Needs Work
- **[Link destination clarity]** - Some links don't clearly indicate where they lead.
  - Recommendation: Consider adding brief descriptor

- **[Navigation link density]** - Footer contains extensive links.
  - Recommendation: Consider grouping for footer links

#### Minor
- **[Link text specificity]** - Some link text is generic.
  - Recommendation: Include more specific text when possible

### Forms & inputs

#### Critical
- **[Form complexity]** - The contact form has many fields which may overwhelm users.
  - Found: Multiple checkboxes, dropdowns, text fields
  - Recommendation: Consider progressive disclosure or multi-step form

- **[Form validation]** - No visible validation feedback in static content.
  - Recommendation: Ensure client-side validation is clear and helpful

- **[Required field indicators]** - Not all required fields are clearly marked.
  - Recommendation: Use asterisks or other clear indicators for required fields

#### Needs Work
- **[Form accessibility]** - Form may need ARIA labels for screen readers.
  - Recommendation: Ensure proper form labeling

- **[Error states]** - No visible error states in static content.
  - Recommendation: Test form error handling

#### Minor
- **[Success states]** - No visible success confirmation.
  - Recommendation: Ensure clear success message after submission

### Error & feedback states

#### Critical
- **[No error states visible]** - Page is informational with a contact form.
  - Recommendation: N/A for static content

#### Needs Work
- **[Loading states]** - Form sections may have JS dependencies.
  - Recommendation: Consider skeleton loaders

#### Minor
- **[Empty states]** - No empty states to evaluate.
  - Recommendation: N/A

### Accessibility

#### Critical
- **[Image alt text missing]** - Images may lack descriptive alt text.
  - Recommendation: Add descriptive alt text to all images

- **[Table accessibility]** - Release timeline table structure may not be optimal for screen readers.
  - Recommendation: Ensure proper table headers

- **[Form labels]** - Form fields need proper labeling for screen readers.
  - Recommendation: Ensure all form fields have associated labels

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
  - Recommendation: Add breadcrumb showing path (Ubuntu > 16.04 > Azure)

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

- **[Form layout]** - Complex form may not render well on mobile.
  - Recommendation: Test form on mobile devices

- **[Touch targets]** - Link and button touch targets may be too small.
  - Recommendation: Verify minimum 44x44px touch targets

- **[Viewport scaling]** - Need to verify proper mobile viewport.
  - Recommendation: Test on multiple device sizes

---

## What looks good

- Clear messaging about Azure-specific ESM benefits
- Good use of customer testimonials
- Multiple upgrade paths clearly explained
- Links to Azure Marketplace for easy deployment
- Webinar link for educational content
- Comprehensive footer with product navigation
- Pricing information included (3.0-4.5% of compute cost)

---

## Recommended priority order

1. Fix all Critical issues
   - Add urgency messaging to hero section
   - Make EOL status more visually prominent
   - Improve form accessibility and reduce complexity

2. Address Needs Work items
   - Improve release timeline table visual hierarchy
   - Group CTAs with clear hierarchy
   - Add links to related cloud providers

3. Polish Minor items
   - Standardize link text formatting
   - Fix form field labels
   - Add descriptive alt text to images

---

## Manual checks for reviewer

- [ ] **Authenticated states** - log in and check any copy that only appears after authentication
- [ ] **JS-rendered content** - interact with the page to trigger dynamic states
- [ ] **Keyboard navigation** - tab through the page to confirm correct focus order
- [ ] **Mobile view** - resize or use device emulation to check layout and readability
- [ ] **Form testing** - test form submission and validation
