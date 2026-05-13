# UX content audit report — live page

**URL:** https://ubuntu.com/about/release-cycle
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** Page contains interactive elements (product selector, version dropdowns) that may not have been fully captured in static fetch

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 8 | 0 | 2 | 3 |

**Total issues:** 5 (0 critical, 2 needs work, 3 minor)
**Total passes:** 8

---

## UX Quality Check

### Structure & Hierarchy

#### Critical
- None identified

#### Needs Work
- **Main heading** - "Know what's supported" is vague and doesn't clearly communicate page purpose
  - Found: "Know what's supported" | Recommendation: "Ubuntu release cycle and supported versions"
  
- **Section heading** - "Find out your current coverage" lacks specificity
  - Found: "Find out your current coverage" | Recommendation: "Check if your Ubuntu version is still supported"

#### Minor
- Page title could be more descriptive: "Ubuntu release cycle" → "Ubuntu release cycle and support timelines"
- Some table headers could be clearer (e.g., "Standard" vs "Standard security maintenance")
- The "Legacy add-on" terminology may confuse users; consider adding brief explanation

### CTAs

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- CTA "Start a 30-day Ubuntu Pro free trial" appears multiple times; consider consolidating or varying placement
- Could add more contextual CTAs within the release tables

### Links

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- External link to Ubuntu Releases wiki should include rel="noopener noreferrer" for security
- Some section links could use more descriptive anchor text

### Forms & Inputs

#### Critical
- None identified

#### Needs Work
- **Product selector** - Dropdown lacks helpful placeholder or default selection guidance
  - Found: "Select a product" | Recommendation: Add "Choose a product" as placeholder with helpful hint
  
- **Release type selector** - "Select a release" is generic
  - Found: "Select a release type" | Recommendation: "Choose release type: Ubuntu or Ubuntu Pro"

#### Minor
- Form validation messages could be more user-friendly ("Please select a product" → "Please choose a product from the list")
- Consider adding "All versions" as a filter option with clear explanation

### Error & Feedback States

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- Toast messages at top of page (e.g., "Your submission was sent successfully!") appear to be leftover from other page states
- These notification toasts should only appear when relevant actions occur

### Accessibility

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- Image alt text could be more descriptive
- Color-only indicators should have text alternatives

### Navigation

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- Breadcrumb navigation would help users understand their location within the site hierarchy
- "About Ubuntu" navigation could have a dropdown showing all subpages

### Mobile Considerations

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- Release tables may not render well on mobile; consider responsive table design or accordion view
- Product selector dropdown may be difficult to use on small screens

---

## What Looks Good

- Clear visual hierarchy with well-organized sections
- Comprehensive release tables showing all supported versions with dates
- Ubuntu Pro value proposition clearly highlighted
- Good use of visual timeline graphic to explain support periods
- Consistent formatting across all release entries
- Clear distinction between Standard, ESM, and Legacy coverage
- Upgrade paths clearly indicated for each version

---

## Recommended Priority Order

1. Fix all Critical issues
2. Address Needs Work items
   - Improve main heading clarity
   - Make section heading more specific
3. Polish Minor items
   - Refine form labels and placeholders
   - Remove stray notification toasts
   - Improve mobile table rendering

---

## Manual Checks for Reviewer

- [ ] Authenticated states - Not applicable (public page)
- [ ] JS-rendered content - Test product selector interaction and version filtering
- [ ] Keyboard navigation - Tab through form elements to verify focus order
- [ ] Mobile view - Test responsive behavior of release tables and selectors
