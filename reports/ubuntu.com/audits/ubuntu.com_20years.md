# UX content audit report — live page

**URL:** https://ubuntu.com/20years
**Date:** Wed May 13 2026
**Copydoc:** none found
**Note:** Content captured from static HTML; JS-rendered elements (e.g., video embeds, blog loading) may not be fully represented.

---

## Summary

| Check | Pass | Critical | Needs Work | Minor |
|---|---|---|---|---|
| UX quality check | 4 | 0 | 1 | 2 |

**Total issues:** 3 (0 critical, 1 needs work, 2 minor)
**Total passes:** 4

---

## UX quality check

### Structure & hierarchy

#### Critical
- None identified

#### Needs Work
- **[Section: Hero content]** — The headline "20 years of Ubuntu is just the beginning" appears three times in the content which may be a content duplication issue
  - *Found:* "20 years of 20 years of 20 years of is just the beginning"
  - *Recommendation:* Review content management system for duplication issues and ensure unique headline text

#### Minor
- **[Section: Date formatting]** — Inconsistent date format across the page
  - *Found:* "2004", "2005", "2006", "2008", "2011", "2012", etc. (years only) vs "Apr 2026" in footer section
  - *Recommendation:* Standardize date formats throughout (consider "October 2004" for consistency with other sections)

- **[Section: Milestone visual design]** — Milestone section uses visual timeline but could benefit from clearer visual separation between eras
  - *Found:* Years 2004-2024 presented in a scrolling timeline
  - *Recommendation:* Consider adding subtle visual breaks or grouping for each decade or major era

### CTAs

#### Critical
- None identified

#### Needs Work
- **[Section: Secondary CTAs]** — Multiple video and resource CTAs could benefit from clearer prioritization
  - *Found:* "Watch the video", "View the video to hear their stories", "Get all our wallpapers", "Access the poster"
  - *Recommendation:* Consider grouping related CTAs (videos together, downloads together) with clearer visual hierarchy

#### Minor
- **[Section: CTA variety]** — Good variety of engagement options (videos, downloads, social sharing, newsletter signup)
  - *Recommendation:* Ensure all CTAs use consistent styling and visual weight

### Links

#### Critical
- None identified

#### Needs Work
- **[Section: External link clarity]** — External links to X (Twitter), LinkedIn, YouTube, Google Drive could benefit from clearer indication
  - *Found:* Links to x.com, linkedin.com, youtube.com, discourse.ubuntu.com, drive.google.com
  - *Recommendation:* Add external link indicators for all external destinations

#### Minor
- **[Section: Social media links]** — Multiple social media platforms featured with varying levels of integration
  - *Found:* Links to Mastodon, Facebook, LinkedIn, Instagram, YouTube, TikTok, X
  - *Recommendation:* Consider using consistent social media icon set with screen-reader friendly labels

### Forms & inputs

#### Critical
- None identified

#### Needs Work
- **[Section: Newsletter form]** — The newsletter signup form appears at the bottom with extensive fields
  - *Found:* First name, Last name, Email, Company, Job Title, Country dropdown, Mobile/cell phone number
  - *Recommendation:* Consider progressive disclosure or multi-step form to reduce initial cognitive load

### Error & feedback states

#### Critical
- None identified

#### Needs Work
- **[Section: Video loading states]** — Video embeds may have loading states that should be considered
  - *Recommendation:* Ensure placeholder content or loading indicators for video embeds

### Accessibility

#### Critical
- None identified

#### Needs Work
- **[Section: Video accessibility]** — Video content requires proper captions and transcripts for accessibility
  - *Found:* Two embedded YouTube videos (CoDglMST-QQ and F08JUAekB0o)
  - *Recommendation:* Ensure all videos have captions/transcripts available

### Navigation

#### Critical
- None identified

#### Needs Work
- **[Section: Breadcrumb navigation]** — No breadcrumb present to help users understand their location
  - *Found:* Page shows "20 years" theme but no breadcrumb trail
  - *Recommendation:* Add breadcrumb (e.g., Home > About > 20 Years) for better orientation

### Mobile considerations

#### Flag for review
- **[Section: Timeline scrolling]** — The milestone timeline with years and images may require careful mobile layout consideration
  - *Recommendation:* Test timeline on mobile devices to ensure readability and proper image sizing

---

## What looks good

- **Compelling storytelling** — The page effectively tells the story of Ubuntu's 20-year history through milestones
- **Strong social proof** — Customer/partner quotes and testimonials add credibility
- **Rich multimedia** — Videos, images, and downloadable resources provide varied engagement options
- **Community focus** — Emphasizes community contributions and social media engagement
- **Partner showcase** — Well-presented partner logos and quotes demonstrate ecosystem strength
- **Downloadable resources** — Wallpapers and mascot poster provide tangible value for users

---

## Recommended priority order

1. Fix all Critical issues (none identified)
2. Address Needs Work items
   - Fix headline duplication issue in hero section
   - Add external link indicators
   - Review video accessibility and ensure captions
3. Polish Minor items
   - Standardize date formatting
   - Consider visual grouping of timeline milestones

---

## Manual checks for reviewer

- [ ] **Authenticated states** — log in and check any copy that only appears after authentication
- [ ] **JS-rendered content** — interact with the page to trigger dynamic states (errors, success messages, empty states)
- [ ] **Keyboard navigation** — tab through the page to confirm correct focus order and accessible labels
- [ ] **Mobile view** — resize or use device emulation to check layout and readability
