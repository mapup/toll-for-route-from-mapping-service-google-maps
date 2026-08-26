# toll-for-route-from-mapping-service-google-maps

Reference implementations showing how to get a route polyline from **Google Maps Directions API** and calculate tolls for it using the **TollGuru Polyline API**. Examples provided in Python, JavaScript, Go, Ruby, and PHP.

## What This Repo Is

A multi-language collection of sample scripts that:

1. Fetch a route polyline from Google Maps for a given origin/destination
2. Send that polyline to TollGuru to get toll costs broken down by payment method

Each language folder is self-contained with its own README, source, and tests.

## Architecture

- No server or framework; each language folder contains a standalone CLI script
- Two-step flow: Google Maps Directions API -> TollGuru Polyline API
- Google Maps returns per-step polylines; scripts decode, merge, and re-encode into a single polyline
- TollGuru `complete-polyline-from-mapping-service` endpoint returns toll costs by payment type
- API keys for both services are read from environment variables
- Vehicle type, departure time, and other params are configurable in-source
- Each language has its own dependency file (`requirements.txt`, `package.json`, `Gemfile`, etc.)
- Tests exist for Python, Go, Ruby, and PHP (CSV-driven, comparing known routes)
- CI: GitHub Actions for Gitleaks, Semgrep, and CodeQL
- No database, no queue, no deployed service

## Prerequisites

| Language   | Runtime     | Dependency Tool  |
| ---------- | ----------- | ---------------- |
| Python     | 3.7+        | pip              |
| JavaScript | Node.js 14+ | npm              |
| Go         | 1.16+       | (stdlib only)    |
| Ruby       | 2.7+        | bundler          |
| PHP        | 7.4+        | (curl extension) |

**API keys required:**

- [Google Maps API key](https://console.cloud.google.com/apis/dashboard) with Directions API enabled
- [TollGuru API key](https://tollguru.com/blog/get-api-key)

## Local Setup

```bash
git clone <repo-url>
cd toll-for-route-from-mapping-service-google-maps

# One-time per clone: wire the gitleaks pre-commit hook (installs gitleaks if
# missing). Without it, git commit is not scanned for secrets. Re-run after
# any fresh clone or new worktree - it is a no-op when already done.
./hooks/install.sh

# Set API keys (all languages read from env)
export GMAPS_API_KEY="your-google-key"
export TOLLGURU_API_KEY="your-tollguru-key"
```

### Per-language install

```bash
# Python
cd python && pip install -r requirements.txt

# JavaScript
cd javascript && npm install

# Ruby
cd ruby && bundle install

# Go / PHP - no install step needed
```

## How to Run

```bash
# Python
python python/google_maps_polyline.py

# JavaScript
node javascript/index.js

# Go
go run go/index.go

# Ruby
ruby ruby/main.rb

# PHP
php php/php_curl_gmaps.php
```

Default route: Philadelphia, PA to New York, NY (configurable in each script).

## How to Run Tests

```bash
# Python
cd python/Testing && python test_google_maps_polyline.py

# Go
cd go/test && go test

# Ruby
cd ruby/TestCases && ruby test_ruby.rb

# PHP
cd php/test && php test_gmaps.php
```

Tests use CSV files with origin/destination pairs and compare results against expected outputs.

## How to Deploy

These are client-side reference scripts, not a deployed service. Copy the relevant function(s) into your application. See each language's README for integration guidance.

## Where Config Lives

| Setting                  | Location                                                       |
| ------------------------ | -------------------------------------------------------------- |
| Google Maps API key      | `GMAPS_API_KEY` env var (Ruby uses `GOOGLE_MAPS_API_KEY`)      |
| TollGuru API key         | `TOLLGURU_API_KEY` env var                                     |
| API base URLs            | Constants at top of each script                                |
| Vehicle/departure params | `request_parameters` / `requestParameters` dict in each script |
| JS dependencies          | `javascript/package.json`                                      |
| Python dependencies      | `python/requirements.txt`                                      |
| Ruby dependencies        | `ruby/Gemfile`                                                 |
| Test fixtures            | `Testing/`, `test/`, `TestCases/` in each language folder      |

## Known Limitations

- Google Directions API returns per-step polylines, not a full-route polyline; the stitching logic differs slightly per language
- PHP version uses `overview_polyline` (approximate) instead of stitching step polylines like the other languages
- Ruby script hardcodes `source: "bing"` instead of `source: "google"` (likely a copy-paste bug)
- No unified test runner across languages
- `request` npm package (JS) is deprecated; consider migrating to `node-fetch` or `axios`
- No CLI argument parsing; origin/destination/vehicle are hardcoded
- No rate-limit handling for either API
- Go version uses deprecated `ioutil.ReadAll`
- Error handling is minimal across all languages

## Further Reading

- [TollGuru API Docs](https://tollguru.com/toll-api-docs)
- [TollGuru API parameter examples](https://github.com/mapup/tollguru-api-parameter-examples/tree/main/request-bodies/02-Complete-Polyline-To-Toll)
- [Vehicle type coverage](https://github.com/mapup/tollguru_vehicle_coverage/wiki/Vehicle-types-supported-by-TollGuru)
- [Supported mapping services](https://github.com/mapup/toll-google-maps/wiki/2.-Map-platform-service-supported-by-TollGuru)
- [Truck parameters](https://github.com/mapup/toll-google-maps/wiki/4.-Truck-parameters-supported-by-TollGuru)
- Per-language READMEs in `python/`, `javascript/`, `go/`, `ruby/`, `php/` folders
