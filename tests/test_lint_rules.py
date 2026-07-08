#!/usr/bin/env python3
"""
Regression tests for scripts/page_lint.py and scripts/ticketable.py.

These exist because every rule in this pipeline has already produced at
least one false positive that shipped in a report before being caught
(AOSP, ISO/IEC standard numbers, em-dash dividers, "bare metal"/"form
factor"/"end user" as banned words, a "going forward" finding that leaked
a garbage literal replacement into the ticketable list). Each fix here
gets a permanent case so it can't silently regress.

Run:
    python3 tests/test_lint_rules.py
    python3 -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from page_lint import lint_content, Finding
from ticketable import is_ticketable, ticket_id, to_bauer, parse_approved_ids, render_markdown


def findings_for(text: str) -> list[Finding]:
    """Run the full check pipeline on a single line of prose."""
    return lint_content([text])


def rules_found(text: str) -> set[str]:
    return {f.rule for f in findings_for(text)}


class TestProductNames(unittest.TestCase):
    def test_mid_sentence_open_source_is_flagged(self):
        findings = findings_for("This is an Open Source project you can use.")
        self.assertTrue(any(f.rule == "product-names" and f.found == "Open Source"
                             for f in findings))

    def test_aosp_is_not_flagged(self):
        # Regression: the linter used to lowercase "Open Source" inside
        # "Android Open Source Project", which is a proper noun, not prose.
        findings = findings_for("This device ships with the Android Open Source Project.")
        self.assertFalse(any(f.rule == "product-names" for f in findings),
                          "AOSP should not trigger the open-source lowercasing rule")


class TestNumberFormatting(unittest.TestCase):
    def test_large_plain_number_is_flagged(self):
        findings = findings_for("We support up to 15000 concurrent users.")
        self.assertTrue(any(f.rule == "number-formatting" and f.found == "15000"
                             for f in findings))

    def test_standard_identifiers_are_not_flagged(self):
        # Regression: ISO 27001, IEC 21434 etc. are names, not quantities.
        for text in ["Certified to ISO 27001.", "Compliant with IEC 21434.",
                     "See RFC 1918 for details.",
                     # Regression: found live on canonical.com/data/kafka/managed
                     # — a colon separator ("ISO:27001") wasn't in the
                     # exemption's trailing-punctuation set, so it slipped
                     # through as a plain number needing a thousands comma.
                     "Compliant with GDPR, ISO:27001 and SOC-2 Type II."]:
            findings = findings_for(text)
            self.assertFalse(any(f.rule == "number-formatting" for f in findings),
                              f"standard identifier wrongly flagged in: {text!r}")

    def test_years_are_not_flagged(self):
        findings = findings_for("Founded in 2004.")
        self.assertFalse(any(f.rule == "number-formatting" for f in findings))


class TestUkSpellingCasing(unittest.TestCase):
    # Regression: found this while running a real scan → approve cycle
    # end to end. The UK-word check used to match against a fully-
    # lowercased copy of the text, so `found` came back lowercase even
    # when the source word was capitalized. That broke anchor-matching
    # (which searches the original-case text for the literal `found`
    # string) silently — findings still passed is_ticketable with empty
    # preceding/following context, meaning Bauer would have received a
    # submission with no way to locate the edit, whose "original text"
    # didn't even match what's really on the page.
    def test_capitalized_word_gets_capitalized_suggestion_and_anchor(self):
        findings = findings_for("Choose your Colour scheme carefully before you launch.")
        uk = [f for f in findings if f.rule == "uk-spelling"]
        self.assertTrue(uk)
        f = uk[0]
        self.assertEqual(f.found, "Colour")
        self.assertEqual(f.suggestion, "Color")
        self.assertNotEqual(f.preceding, "", "anchor context must not be silently dropped")

    def test_all_caps_word_gets_all_caps_suggestion(self):
        findings = findings_for("OUR FAVOURITE COLOUR IS BLUE AND BOLD TODAY.")
        by_found = {f.found: f.suggestion for f in findings if f.rule == "uk-spelling"}
        self.assertEqual(by_found.get("COLOUR"), "COLOR")
        self.assertEqual(by_found.get("FAVOURITE"), "FAVORITE")

    def test_title_case_data_centre_is_not_lowercased(self):
        # Regression: this used to always suggest lowercase "data center"
        # even for a Title Case source like "Data Centre" in a heading
        # or nav label, which would introduce a new casing error.
        findings = findings_for("Private Cloud/Data Centre choices for your workload.")
        uk = [f for f in findings if f.rule == "uk-spelling" and f.found == "Data Centre"]
        self.assertTrue(uk)
        self.assertEqual(uk[0].suggestion, "Data Center")

    def test_lowercase_word_is_unaffected(self):
        findings = findings_for("We support your favourite colour combos every day.")
        by_found = {f.found: f.suggestion for f in findings if f.rule == "uk-spelling"}
        self.assertEqual(by_found.get("favourite"), "favorite")
        self.assertEqual(by_found.get("colour"), "color")


class TestIseVerbSuffix(unittest.TestCase):
    # Regression: found live on canonical.com/data/relational-databases and
    # /data/kafka/what-is-kafka while reviewing a wider real scan. The
    # -ise -> -ize rules always suggested the bare present-tense form
    # regardless of the matched word's actual suffix, so "optimised"
    # suggested "optimize" and "minimised" suggested "minimize" — a
    # ticketable, exact-replacement fix that would have broken the
    # sentence's grammar (e.g. "data loss is minimize") while "fixing"
    # the spelling.
    def test_past_tense_suffix_is_preserved(self):
        findings = findings_for("Data loss is minimised when a server goes offline.")
        uk = [f for f in findings if f.rule == "uk-spelling" and f.found == "minimised"]
        self.assertTrue(uk)
        self.assertEqual(uk[0].suggestion, "minimized")

    def test_capitalized_past_tense_is_preserved(self):
        findings = findings_for("Specialised engineers deploy the database.")
        uk = [f for f in findings if f.rule == "uk-spelling" and f.found == "Specialised"]
        self.assertTrue(uk)
        self.assertEqual(uk[0].suggestion, "Specialized")

    def test_bare_form_is_unaffected(self):
        findings = findings_for("You can customise every dashboard widget you like.")
        uk = [f for f in findings if f.rule == "uk-spelling" and f.found == "customise"]
        self.assertTrue(uk)
        self.assertEqual(uk[0].suggestion, "customize")

    def test_utilise_suggestion_has_no_leaked_parenthetical(self):
        # Regression: this used to suggest the literal string
        # "utilize (or better: use)" — the same bug class as "going
        # forward", just missed by the original hint-pattern fix.
        findings = findings_for("Learn how you can utilise our platform today.")
        uk = [f for f in findings if f.rule == "uk-spelling" and f.found == "utilise"]
        self.assertTrue(uk)
        self.assertEqual(uk[0].suggestion, "utilize")

    def test_utilise_style_hint_is_not_ticketable_defense_in_depth(self):
        # Even if a future rule embeds an "(or better: ...)" hint again,
        # the ticketable filter should catch it as a backstop.
        f = Finding(rule="uk-spelling", severity="needs-work", section="Intro",
                    message="x", found="utilise",
                    suggestion="utilize (or better: use)")
        self.assertFalse(is_ticketable(f))


class TestPunctuation(unittest.TestCase):
    def test_isolated_em_dash_is_flagged(self):
        findings = findings_for("We build software—and we do it well.")
        self.assertTrue(any(f.rule == "punctuation" for f in findings))

    def test_decorative_divider_is_not_flagged(self):
        # Regression: a run of em dashes used as a divider line is not prose.
        findings = findings_for("——————————————")
        self.assertFalse(any(f.rule == "punctuation" for f in findings))


class TestBannedWords(unittest.TestCase):
    def test_removed_terms_are_no_longer_flagged(self):
        # Regression: these are legitimate Canonical product/technical terms,
        # not marketing fluff, and were producing false positives.
        for text in [
            "Provision bare metal servers with MAAS.",
            "Choose the form factor that fits your device.",
            "Built for the end user, not just IT.",
        ]:
            findings = findings_for(text)
            self.assertFalse(any(f.rule == "banned-words" for f in findings),
                              f"legitimate technical term wrongly banned in: {text!r}")

    def test_technical_verbs_are_no_longer_flagged(self):
        for text in ["Execute the command to deploy.", "Terminate the instance when done.",
                     "Kill the process if it hangs."]:
            findings = findings_for(text)
            self.assertFalse(any(f.rule == "banned-words" for f in findings),
                              f"technical verb wrongly banned in: {text!r}")

    def test_eliminate_is_still_flagged(self):
        findings = findings_for("This will eliminate downtime.")
        self.assertTrue(any(f.rule == "banned-words" and f.found == "eliminate"
                             for f in findings))


class TestTicketableFilter(unittest.TestCase):
    def test_uk_spelling_is_ticketable(self):
        f = Finding(rule="uk-spelling", severity="needs-work", section="Intro",
                    message="x", found="colour", suggestion="color")
        self.assertTrue(is_ticketable(f))

    def test_flowery_language_is_never_ticketable(self):
        # Which words read as "flowery" is a judgement call, not an
        # objective style-guide violation like UK spelling — kept out of
        # the auto-ticketable list entirely.
        f = Finding(rule="flowery-language", severity="needs-work", section="Intro",
                    message="x", found="utilize", suggestion="use")
        self.assertFalse(is_ticketable(f))

    def test_going_forward_suggestion_is_not_ticketable(self):
        # Regression: this used to slip through and would have told Bauer
        # to insert the literal string "remove — adds nothing" into the page.
        f = Finding(rule="banned-words", severity="needs-work", section="Intro",
                    message='Avoid "going forward" — remove — adds nothing',
                    found="going forward", suggestion="remove — adds nothing")
        self.assertFalse(is_ticketable(f))

    def test_judgement_prompts_are_not_ticketable(self):
        f = Finding(rule="link-text", severity="needs-work", section="CTA",
                    message="x", found="click here", suggestion="use descriptive link text")
        self.assertFalse(is_ticketable(f))


class TestApprovalGate(unittest.TestCase):
    def _make_tickets(self):
        tickets = [
            {"url": "https://x.com/a", "path": "/a", "section": "Intro",
             "rule": "uk-spelling", "found": "colour", "suggestion": "color",
             "message": "m", "preceding": "the ", "following": " scheme"},
            {"url": "https://x.com/a", "path": "/a", "section": "Intro",
             "rule": "punctuation", "found": "-", "suggestion": "\u2013",
             "message": "m", "preceding": "a ", "following": " b"},
        ]
        for t in tickets:
            t["id"] = ticket_id(t)
        return tickets

    def test_only_checked_items_reach_bauer(self, tmp_path=None):
        import tempfile
        tickets = self._make_tickets()
        md = render_markdown(tickets, "x.com", 1)
        approved_line_id = tickets[0]["id"]
        reviewed = "\n".join(
            line.replace("- [ ]", "- [x]") if approved_line_id in line and "- [ ]" in line else line
            for line in md.splitlines()
        )
        with tempfile.TemporaryDirectory() as d:
            review_path = Path(d) / "x-com-tickets-2026-07-02.md"
            review_path.write_text(reviewed)
            approved = parse_approved_ids(review_path)
            self.assertEqual(approved, {tickets[0]["id"]})
            bauer = to_bauer(tickets, approved)
            self.assertEqual(len(bauer), 1)
            self.assertEqual(len(bauer[0]["suggestions"]), 1)
            self.assertEqual(bauer[0]["suggestions"][0]["change"]["original_text"], "colour")

    def test_no_approvals_yields_nothing(self):
        tickets = self._make_tickets()
        self.assertEqual(to_bauer(tickets, set()), [])

    def test_unfiltered_bauer_includes_everything(self):
        tickets = self._make_tickets()
        bauer = to_bauer(tickets)
        self.assertEqual(sum(len(p["suggestions"]) for p in bauer), 2)


if __name__ == "__main__":
    unittest.main()
