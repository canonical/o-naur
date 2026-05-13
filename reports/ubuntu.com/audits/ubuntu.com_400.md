# UX content audit report — live page

**URL:** https://ubuntu.com/400
**Date:** Wed May 13 2026
**Copydoc:** none found
**Note:** Content captured from static HTML; error pages typically have minimal content by design.

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 2 | 0 | 1 | 1 |

**Total issues:** 2 (0 critical, 1 needs work, 1 minor)
**Total passes:** 2

---

## UX quality check

### Structure & hierarchy

#### Critical
- None identified

#### Needs Work
- **[Section: Error explanation]** — The error message "Invalid request" is clear but could provide more actionable guidance
  - *Found:* "We can't process this request."
  - *Recommendation:* Consider adding a brief explanation of common causes (e.g., "This may happen if the request URL is malformed or contains invalid parameters")

#### Minor
- **[Section: Error code visibility]** — The HTTP 400 status code is displayed but could be more prominent for debugging purposes
  - *Found:* "400" displayed as section header
  - *Recommendation:* Consider adding "HTTP 400 Bad Request" for developers who may need the specific status code

### CTAs

#### Critical
- None identified

#### Needs Work
- **[Section: Recovery CTAs]** — Two CTAs present (refresh page, file bug) but could be more visually distinct
  - *Found:* "refresh the page" / "file a bug"
  - *Recommendation:* Make "Try again" the primary CTA and "file a bug" secondary with different visual weight

#### Minor
- **[Section: CTA clarity]** — "file a bug" links to GitHub which may not be obvious without context
  - *Recommendation:* Consider "File a bug report on GitHub" for clarity

### Links

#### Critical
- None identified

#### Needs Work
- **[Section: External link clarity]** — GitHub links for bug reporting could benefit from external link indicators
  - *Found:* Links to github.com/canonical/ubuntu.com/issues
  - *Recommendation:* Add external link icons or "(opens in new tab)" text for clarity

#### Minor
- **[Section: Known issue link]** — The "known issue" link provides helpful context
  - *Found:* "known issue" link to github.com/canonical/ubuntu.com/issues
  - *Recommendation:* Consider making this more prominent as it may resolve the issue without filing a new bug

### Forms & inputs

#### Critical
- None identified

#### Needs Work
- **[Section: Error form accessibility]** — No form present on this error page (forms would be on the bug report page)
  - *Recommendation:* Ensure the linked bug report form has proper accessibility attributes

### Error & feedback states

#### Critical
- None identified

#### Needs Work
- **[Section: Error context]** — The error page could benefit from suggesting what users might try
  - *Found:* "You can try refreshing the page"
  - *Recommendation:* Consider adding "If the problem persists, please file a bug report" as a clearer escalation path

### Accessibility

#### Critical
- None identified

#### Needs Work
- **[Section: Error page ARIA]** — Error pages should have appropriate ARIA labels for screen readers
  - *Recommendation:* Ensure the page has proper role="alert" or similar for the error message

### Navigation

#### Critical
- None identified

#### Needs Work
- **[Section: Home link prominence]** — The link back to homepage could be more prominent
  - *Found:* "file a bug" and "known issue" links, but homepage link less prominent
  - *Recommendation:* Add a clear "Return to homepage" button as the primary recovery option

### Mobile considerations

#### Flag for review
- **[Section: Error page layout]** — Error pages with minimal content should be tested on mobile to ensure proper spacing and readability
  - *Recommendation:* Verify the error message is legible and CTAs are touch-friendly on mobile devices

---

## What looks good

- **Clear error message** — "Invalid request" is concise and understandable
- **Multiple recovery options** — Users can try refreshing or file a bug report
- **Known issue reference** — Link to known issues helps users determine if this is a system-wide problem
- **Consistent branding** — Error page maintains Ubuntu site branding for continuity
- **Minimal design** — Clean, focused error page without unnecessary distractions

---

## Recommended priority order

1. Fix all Critical issues (none identified)
2. Address Needs Work items
   - Add more actionable guidance for users
   - Make "Return to homepage" more prominent
   - Add ARIA labels for accessibility
3. Polish Minor items
   - Add external link indicators
   - Consider making HTTP status code more visible

---

## Manual checks for reviewer

- [ ] **Authenticated states** — log in and check if error behavior differs for authenticated users
- [ ] **JS-rendered content** — interact with the page to trigger dynamic states (errors, success messages, empty states)
- [ ] **Keyboard navigation** — tab through the page to confirm correct focus order and accessible labels
- [ ] **Mobile view** — resize or use device emulation to check layout and readability
