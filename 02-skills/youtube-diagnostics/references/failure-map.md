# Failure Map

## youtube-n-challenge
Meaning: YouTube player challenge blocked normal extraction.
Action: prefer diagnostics + browser-assisted fallbacks; do not trust plain yt-dlp retries.

## youtube-po-token
Meaning: YouTube requires PO token for some clients / formats.
Action: prefer subtitles-first, metadata fallback, or manual/browser-assisted retrieval.

## format-unavailable
Meaning: requested format combination is too strict.
Action: use relaxed format or single-file best.

## browser-cookie-failed
Meaning: browser cookie extraction did not work.
Action: try cookies.txt.
