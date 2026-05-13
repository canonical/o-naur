# UX content audit report — live page

**URL:** https://ubuntu.com/about/release_cycles/kernel-eol
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** Page contains kernel support information; table-heavy content

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 6 | 1 | 1 | 2 |

**Total issues:** 4 (1 critical, 1 needs work, 2 minor)
**Total passes:** 6

---

## UX Quality Check

### Structure & Hierarchy

#### Critical
- **[Missing page heading]** - Page lacks a clear H1 heading explaining what this page is about
  - Found: No H1 present | Recommendation: Add "Ubuntu Kernel Support Lifecycle" as main heading

#### Needs Work
- **[Section heading unclear]** - "Ubuntu kernel support lifecycle" as H2 without context
  - Found: "### Ubuntu kernel support lifecycle" | Recommendation: Add H1 above this section

#### Minor
- Page title should be more descriptive to indicate kernel-specific EOL information
- Could add summary text explaining what HWE (Hardware Enablement) means

### CTAs

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- Could add CTA linking to Ubuntu Pro for extended kernel support
- Link to kernel documentation would be helpful

### Links

#### Critical
- None identified

#### Needs Work
- None identified

#### Minor
- No links to related kernel resources or support options
- Consider adding link to "Ubuntu Pro" for extended kernel coverage

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
- Consider adding note about where to find the most current kernel information

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

- Comprehensive kernel version support timeline
- Clear distinction between HWE and standard kernels
- Good coverage of Ubuntu version to kernel version mapping
- Clear indication of extended support periods

---

## Recommended Priority Order

1. Fix all Critical issues
   - Add main page heading
2. Address Needs Work items
   - Improve section heading with better context
3. Polish Minor items
   - Add explanatory text for HWE
   - Add accessibility improvements
   - Add relevant links

---

## Manual Checks for Reviewer

- [ ] Authenticated states - Not applicable (public page)
- [ ] JS-rendered content - Verify table data is static or dynamic
- [ ] Keyboard navigation - Tab through table cells
- [ ] Mobile view - Test table rendering on mobile devices
