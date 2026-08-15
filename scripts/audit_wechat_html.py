#!/usr/bin/env python3
"""Audit English product terms, casing, and color emphasis in WeChat HTML."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_TERMS = [
    "DeepSeek Harness",
    "Claude Code",
    "Code Agent",
    "DeepSeek",
    "Anthropic",
    "OpenAI",
    "Harness",
    "Codex",
    "Agent",
    "Plugin",
    "Context",
    "Shell",
    "Diff",
    "MCP",
    "CLI",
    "SDK",
]

CASE_PATTERNS = {
    r"\bdeepseek\b": "DeepSeek",
    r"\bclaude\s*code\b": "Claude Code",
    r"\bopen\s*ai\b": "OpenAI",
    r"\banthropic\b": "Anthropic",
    r"\bcodex\b": "Codex",
}

SKIP_TAGS = {"script", "style", "title", "code", "pre"}


def normalize_style(style: str) -> str:
    return re.sub(r"\s+", "", style).lower()


class AuditParser(HTMLParser):
    def __init__(self, terms: list[str], colors: list[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.terms = sorted(terms, key=len, reverse=True)
        self.colors = [color.lower() for color in colors]
        self.stack: list[tuple[str, str]] = []
        self.issues: list[str] = []
        self.all_text: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        self.stack.append((tag, normalize_style(attrs_map.get("style") or "")))
        if tag in SKIP_TAGS:
            self.skip_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if self.skip_depth or not data.strip():
            return
        self.all_text.append(data)
        line, _ = self.getpos()
        styled = any(
            any(f"color:{color}" in style for color in self.colors)
            for _, style in self.stack
        )
        for term in self.terms:
            for _ in re.finditer(re.escape(term), data):
                if not styled:
                    snippet = " ".join(data.strip().split())
                    self.issues.append(
                        f"[UNCOLORED] line {line}: {term!r} in {snippet[:100]!r}"
                    )


def casing_issues(text: str) -> list[str]:
    issues: list[str] = []
    for pattern, canonical in CASE_PATTERNS.items():
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            found = match.group(0)
            if found != canonical:
                issues.append(f"[CASE] {found!r} should be {canonical!r}")
    return sorted(set(issues))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    parser.add_argument(
        "--terms",
        nargs="*",
        default=DEFAULT_TERMS,
        help="Terms that should carry an allowed color",
    )
    parser.add_argument(
        "--allowed-colors",
        nargs="*",
        default=["#5c6fa3", "#c9633f"],
        help="CSS colors accepted as deliberate emphasis",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.html.is_file():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 2

    source = args.html.read_text(encoding="utf-8")
    audit = AuditParser(args.terms, args.allowed_colors)
    audit.feed(source)
    rendered_text = " ".join(audit.all_text)
    issues = casing_issues(rendered_text) + audit.issues

    if issues:
        print("\n".join(issues))
        print(f"FAIL: {len(issues)} issue(s)")
        return 1

    print("PASS: product names, casing, and color emphasis look consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
