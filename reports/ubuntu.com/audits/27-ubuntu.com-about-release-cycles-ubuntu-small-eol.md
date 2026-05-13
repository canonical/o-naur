# UX content audit report — live page

**URL:** https://ubuntu.com/about/release_cycles/ubuntu-small-eol
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** Page appears to be a simple reference table; minimal content structure

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 5 | 1 | 1 | 1 |

**Total issues:** 3 (1 critical, 1 needs work, 1 minor)
**Total passes:** 5

---

## UX Quality Check

### Structure & Hierarchy

#### Critical
- **[Missing page heading]** - Page lacks a clear H1 heading explaining what this page is about
  - Found: No H1 present | Recommendation: Add "Ubuntu Small Business EOL Timeline" as main heading

#### Needs Work
- **[Table heading unclear]** - Column headers lack context about what they represent
  - Found: "Released", "End of Standard Support", "End of Ubuntu Pro Support", "End of Legacy add-on coverage" | Recommendation: Add introductory text explaining support tiers

#### Minor
- Page title should be more descriptive to indicate this is specifically about Ubuntu small business EOL

### CTAs

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- Could add CTA linking to Ubuntu Pro for extended support
- Link to Ubuntu download page would be helpful

### Links

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- No links to related Ubuntu resources or support options
- Consider adding link to Ubuntu Pro product page

### Forms & Inputs

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- N/A - No forms present

### Error & Feedback States

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- No error states to evaluate
- Consider adding note about where to find the most current information

### Accessibility

#### Critical
- None identified

#### Needs Work
- **[Table accessibility]** - Table lacks proper caption and scope attributes
  - Found: Basic table structure | Recommendation: Add <caption> and scope="col" to header cells

#### Minor
- None identified

### Navigation

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- No breadcrumb navigation to help users understand context
- Could add link back to main release cycle page

### Mobile Considerations

#### Critical
- None identified

#### Needs Work
- **[Table responsiveness]** - Table may not render well on mobile devices
  - Found: Standard table layout | Recommendation: Implement horizontal scroll or card view for mobile

#### Minor
- None identified

---

## What Looks Good

- Clean, simple table format for quick reference
- Clear date formatting throughout
- Covers important support timelines for Ubuntu versions

---

## Recommended Priority Order

1. Fix all Critical issues
   - Add main page heading
2. Address Needs Work items
   - Improve table headers with explanatory context
3. Polish Minor items
   - Add accessibility improvements
   - Add relevant links

---

## Manual Checks for Reviewer

- [ ] Authenticated states - Not applicable (public page)
- [ ] JS-rendered content - Verify table data is static or dynamic
- [ ] Keyboard navigation - Tab through table cells
- [ ] Mobile view - Test table rendering on mobile devices
