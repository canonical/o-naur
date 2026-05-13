# UX content audit report — live page

**URL:** https://ubuntu.com/404
**Date:** 2026-05-13
**Copydoc:** none found
**Note:** Error page for HTTP 404 Not Found

---

## Summary

| Check | ✅ Pass | 🔴 Critical | 🟡 Needs Work | 🔵 Minor |
|---|---|---|---|---|
| UX quality check | 2 | 4 | 3 | 2 |

**Total issues:** 9 (4 critical, 3 needs work, 2 minor)
**Total passes:** 2

---

## UX quality check

### Structure & hierarchy

#### 🔴 Critical
- **[No helpful error message]** — Message doesn't help user understand why page wasn't found
  - *Found:* "We can't find the page you're looking for." | *Recommendation:* Provide more context: "The page may have been moved, deleted, or the URL is incorrect"

- **[No recovery guidance]** — Page offers limited options for users to recover from the error
  - *Found:* "try refreshing the page or file a bug" | *Recommendation:* Add more recovery steps: check URL spelling, use site search, browse popular pages

- **[No error code explanation]** — HTTP 404 status code is not explained
  - *Found:* "404" displayed prominently | *Recommendation:* Add brief explanation: "This means the page doesn't exist or has been moved"

- **[No link to previous page]** — Users who arrived here by mistake have no easy way to go back
  - *Found:* Only "back to homepage" option | *Recommendation:* Add "Go back" button or browser back link

#### 🟡 Needs Work
- **[No search functionality]** — No site search to help users find what they're looking for
  - *Found:* No search bar on error page | *Recommendation:* Add prominent search bar to help users find content

- **[No suggested content]** — No recommendations for related or popular pages
  - *Found:* No suggested links | *Recommendation:* Add links to popular pages, recent content, or related sections

- **[Technical details hidden]** — No way to see more details about the missing page
  - *Found:* No error details section | *Recommendation:* Add collapsible section with technical details for debugging

#### 🔵 Minor
- **[Page title generic]** — Page title "404: Page not found" is technical
  - *Found:* "404: Page not found | Ubuntu" | *Recommendation:* Make more user-friendly: "Oops! Page not found"

- **[Visual design minimal]** — Page is very plain, which may increase user frustration
  - *Found:* Minimal error page design | *Recommendation:* Add reassuring visual elements or friendly illustration to reduce user anxiety

### CTAs

#### 🔴 Critical
- **[Primary action unclear]** — Two actions (refresh, file bug) with no priority
  - *Found:* "try refreshing the page" and "file a bug" | *Recommendation:* Make "Use site search" or "Browse popular pages" primary action

- **[File bug link: No context]** — Link to file bug doesn't explain when to use it
  - *Found:* "file a bug if you think this might be an error" | *Recommendation:* Add tooltip or context: "If you think this page should exist"

#### 🟡 Needs Work
- **[Homepage link: Only option]** — Homepage is the only navigation option besides refresh
  - *Found:* "back to our homepage" | *Recommendation:* Add more navigation options like "Browse products" or "View sitemap"

#### 🔵 Minor
- **[CTA styling]** — CTAs are plain links without button styling
  - *Found:* "file a bug", "back to our homepage" | *Recommendation:* Consider button styling for primary actions

### Links

#### 🔴 Critical
- **[No contextual links]** — Page lacks links to relevant help resources
  - *Found:* Only bug report link | *Recommendation:* Add links to help center, sitemap, or popular pages

- **[External link indicator missing]** — Bug report link goes to GitHub but doesn't indicate it's external
  - *Found:* Link to github.com/canonical/ubuntu.com | *Recommendation:* Add external link indicator

#### 🟡 Needs Work
- **[No related content]** — Users can't find related pages or products
  - *Found:* No product links | *Recommendation:* Add links to popular pages or products

#### 🔵 Minor
- **[Link text could be clearer]** — "file a bug" is informal
  - *Found:* "file a bug" | *Recommendation:* Consider "Report this issue" for clarity

### Forms & inputs

#### 🔴 Critical
- **[No search form]** — No search form to help users find content
  - *Found:* No search form | *Recommendation:* Add search form prominently on error page

#### 🟡 Needs Work
- **[N/A]** — Not applicable for main content

#### 🔵 Minor
- **[N/A]** — Not applicable

### Error & feedback states

#### 🔴 Critical
- **[No helpful error message]** — Message doesn't help user understand or fix the problem
  - *Found:* "We can't find the page you're looking for." | *Recommendation:* Provide actionable guidance like "Try searching" or "Check the URL"

- **[No retry mechanism]** — Users must manually navigate away
  - *Found:* Manual navigation options | *Recommendation:* Consider auto-suggestions based on URL pattern

- **[No error tracking provided]** — Users can't reference error ID when reporting
  - *Found:* No error ID or reference | *Recommendation:* Display error ID for support reference

- **[No support contact]** — No way to contact support for help
  - *Found:* Only bug report link | *Recommendation:* Add support contact option

#### 🟡 Needs Work
- **[Error logging not user-facing]** — Technical details not available to users
  - *Found:* No technical error details | *Recommendation:* Provide basic error context for debugging

- **[No status indicator]** — Page doesn't indicate if issue is being resolved
  - *Found:* No status message | *Recommendation:* Add message if known issue

#### 🔵 Minor
- **[Error icon]** — No visual icon to indicate error type
  - *Found:* No error icon | *Recommendation:* Add appropriate error icon for visual recognition

### Accessibility

#### 🔴 Critical
- **[No skip links]** — Page lacks "Skip to main content" link for keyboard users
  - *Found:* No skip link in navigation | *Recommendation:* Add skip link at page top

- **[Error not announced to screen readers]** — Error status may not be properly announced
  - *Found:* Standard HTML structure | *Recommendation:* Use proper ARIA live region for error announcement

#### 🟡 Needs Work
- **[Color contrast]** — Error message colors need verification for WCAG compliance
  - *Found:* Error message styling | *Recommendation:* Test contrast ratios

- **[Heading hierarchy]** — H1 should clearly indicate error state
  - *Found:* "# Page not found" as H1 | *Recommendation:* Ensure proper heading structure

#### 🔵 Minor
- **[Focus indicators unclear]** — Focus states may not be visible for all interactive elements
  - *Found:* Links on page | *Recommendation:* Ensure visible focus indicators

- **[Image alt text]** — Any images should have descriptive alt text
  - *Found:* No images visible | *Recommendation:* N/A

### Navigation

#### 🔴 Critical
- **[No breadcrumbs]** — Page lacks breadcrumb navigation
  - *Found:* No breadcrumb trail visible | *Recommendation:* Add breadcrumbs if possible (may not apply to error pages)

- **[No site search visible]** — Search functionality not prominent
  - *Found:* Search icon in header | *Recommendation:* Ensure search is accessible from all pages

- **[Navigation limited]** — Only homepage link available
  - *Found:* "back to our homepage" | *Recommendation:* Add more navigation options

#### 🟡 Needs Work
- **[No return path]** — No easy way to return to where user was
  - *Found:* No "Go back" button | *Recommendation:* Add browser back link or "Return to previous page"

#### 🔵 Minor
- **[Mobile menu]** — Hamburger menu may be difficult to access on error page
  - *Found:* "Menu" toggle in header | *Recommendation:* Ensure menu is accessible

### Mobile considerations

#### 🔵 Flag for review
- **[CTA touch targets]** — Buttons need adequate size for touch interaction
  - *Found:* Links on page | *Recommendation:* Ensure minimum 44x44px touch targets

- **[Content readability]** — Text size and line length need mobile verification
  - *Found:* Error message text | *Recommendation:* Test on mobile devices

- **[Layout responsiveness]** — Page layout needs mobile verification
  - *Found:* Standard page layout | *Recommendation:* Test on various screen sizes

---

## ✅ What looks good

1. **Clear error code display** — The "404" status code is prominently displayed

2. **Simple, clear message** — Message is concise and easy to understand

3. **Bug report option** — Users can report the issue if they believe it's a site problem

4. **Known issue reference** — Page mentions this may be a known issue on GitHub

5. **Consistent branding** — Page maintains Ubuntu branding and footer navigation

---

## Recommended priority order

1. Fix all 🔴 Critical issues
   - Add helpful error explanation
   - Provide more recovery guidance
   - Add error code explanation
   - Add "Go back" option

2. Address 🟡 Needs Work items
   - Add site search functionality
   - Suggest related content
   - Provide technical details option
   - Add more navigation options

3. Polish 🔵 Minor items
   - Improve page title
   - Add error icon
   - Standardize CTA styling

---

## 🔲 Manual checks for reviewer

- [ ] **Error reproduction** — Try to reproduce the 404 error to understand triggers
- [ ] **Refresh functionality** — Test that page refresh works correctly
- [ ] **Bug report link** — Verify GitHub link opens correctly
- [ ] **Keyboard navigation** — Tab through page to confirm correct focus order
- [ ] **Mobile view** — Resize or use device emulation to check layout and readability
- [ ] **Screen reader** — Test with screen reader to ensure error is announced
- [ ] **External links** — Verify all external links open in new tab appropriately
