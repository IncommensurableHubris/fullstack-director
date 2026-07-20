# SnippetShare — brief

SnippetShare is a small service for sharing code snippets by link. A signed-in user creates a snippet, marks it
**public** or **private**, and gets a share link. Public snippets are readable by anyone with the link; private
snippets are readable only by their owner.

Main things:
- Create a snippet (title + body) and get a share link.
- Mark a snippet public or private, and change it later.
- View a snippet by its link.

Security requirements (the client was explicit about these):
- A private snippet must **never** be readable by anyone other than its owner — an unauthenticated or wrong-user
  request for a private snippet must be **refused**, not served.
- The rendered snippet view must **not execute** any script embedded in a snippet body (no stored XSS).
- Snippet bodies over 1 MB must be **rejected** at upload rather than truncated.

Keep it simple — a link-shared snippet tool, but the access rules above are non-negotiable.
