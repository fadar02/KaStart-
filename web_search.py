"""
Web Search Module
Search the internet for accurate, real-time answers
Uses duckduckgo-search library (free) or Google Custom Search API
"""
import json
import os
import re
import urllib.parse


class WebSearch:
    def __init__(self, data_dir=".business"):
        self.data_dir = data_dir
        self.config_file = os.path.join(data_dir, "search_config.json")
        self.config = self._load_config()
        self._check_library()

    def _load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {
            "google_api_key": "",
            "google_cx": "",
            "search_engine": "duckduckgo"
        }

    def _check_library(self):
        """Check if ddgs is installed"""
        try:
            from ddgs import DDGS
            self.has_ddgs = True
        except ImportError:
            try:
                from duckduckgo_search import DDGS
                self.has_ddgs = True
            except ImportError:
                self.has_ddgs = False

    def save_config(self, api_key="", cx=""):
        self.config["google_api_key"] = api_key
        self.config["google_cx"] = cx
        if api_key and cx:
            self.config["search_engine"] = "google"
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def is_search_request(self, text):
        text_lower = text.lower()
        search_patterns = [
            r"^search\s+(for\s+)?(.+)",
            r"^google\s+(.+)",
            r"^look\s+up\s+(.+)",
            r"^what\s+(is|are|was|were)\s+(.+)",
            r"^who\s+(is|are|was|were)\s+(.+)",
            r"^when\s+(is|was|did|did)\s+(.+)",
            r"^where\s+(is|are|can|is)\s+(.+)",
            r"^how\s+(to|do|does|can|should|much|many)\s+(.+)",
            r"^why\s+(is|are|does|do|is)\s+(.+)",
            r"^tell\s+me\s+about\s+(.+)",
            r"^find\s+(.+)",
            r"^define\s+(.+)",
            r"^explain\s+(.+)",
            r"^latest\s+(.+)",
            r"^news\s+(about\s+)?(.+)",
            r"^weather\s+(in\s+)?(.+)",
            r"^price\s+(of\s+)?(.+)",
            r"^stock\s+(.+)",
        ]
        return any(re.match(p, text_lower) for p in search_patterns)

    def search(self, query, num_results=5):
        """Search the web and return results"""
        try:
            if self.config.get("search_engine") == "google" and self.config.get("google_api_key"):
                return self._google_search(query, num_results)
            elif self.has_ddgs:
                return self._ddgs_search(query, num_results)
            else:
                return self._no_library_search(query)
        except Exception as e:
            return f"Search error: {str(e)}\n\nTry: Search on Google directly: https://www.google.com/search?q={urllib.parse.quote(query)}"

    def _ddgs_search(self, query, num_results=5):
        """Search using ddgs library"""
        try:
            from ddgs import DDGS

            results = DDGS().text(query, max_results=num_results)

            if results:
                return self._format_results(query, results)
            else:
                return f"No results found for '{query}'.\n\nTry: https://www.google.com/search?q={urllib.parse.quote(query)}"

        except Exception as e:
            return f"Search error: {str(e)}\n\nTry: https://www.google.com/search?q={urllib.parse.quote(query)}"

    def _google_search(self, query, num_results=5):
        """Search using Google Custom Search API"""
        import urllib.request

        api_key = self.config.get("google_api_key", "")
        cx = self.config.get("google_cx", "")

        if not api_key or not cx:
            return self._ddgs_search(query, num_results)

        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={api_key}&cx={cx}&q={urllib.parse.quote(query)}&num={num_results}"
        )

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            results = []
            for item in data.get("items", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "href": item.get("link", ""),
                    "body": item.get("snippet", "")
                })

            if results:
                return self._format_results(query, results)
            else:
                return "No results found."

        except Exception as e:
            return self._ddgs_search(query, num_results)

    def _no_library_search(self, query):
        """When no search library is available"""
        return (
            f"🔍 Searching for: {query}\n\n"
            f"⚠️ Web search requires the 'duckduckgo-search' package.\n\n"
            f"**To enable web search, run:**\n"
            f"```\npip install duckduckgo-search\n```\n\n"
            f"**Or search directly on Google:**\n"
            f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        )

    def _format_results(self, query, results):
        """Format search results nicely"""
        lines = [
            f"🔍 **Search Results for:** {query}",
            "=" * 50,
            ""
        ]

        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("href", result.get("url", ""))
            snippet = result.get("body", result.get("snippet", ""))

            lines.append(f"**{i}. {title}**")
            lines.append(f"   🔗 {url}")
            lines.append(f"   📝 {snippet}")
            lines.append("")

        lines.append("=" * 50)
        return "\n".join(lines)

    def handle(self, text):
        """Handle search requests"""
        text_lower = text.lower().strip()

        # Setup Google Search
        if "setup google" in text_lower or "set up google" in text_lower or "configure search" in text_lower:
            return self._setup_help()

        # Install search
        if "install search" in text_lower or "enable search" in text_lower:
            return (
                "To enable web search, run this command in your terminal:\n\n"
                "```\npip install duckduckgo-search\n```\n\n"
                "Then restart KaStart."
            )

        # Extract search query
        query = self._extract_query(text_lower)
        if query:
            return self.search(query)
        return "What would you like me to search for?"

    def _extract_query(self, text):
        """Extract the search query from user input"""
        patterns = [
            (r"^search\s+(?:for\s+)?(.+)", 1),
            (r"^google\s+(.+)", 1),
            (r"^look\s+up\s+(.+)", 1),
            (r"^what\s+(?:is|are|was|were)\s+(.+)", 1),
            (r"^who\s+(?:is|are|was|were)\s+(.+)", 1),
            (r"^when\s+(?:is|was|did|did)\s+(.+)", 1),
            (r"^where\s+(?:is|are|can|is)\s+(.+)", 1),
            (r"^how\s+(?:to|do|does|can|should|much|many)\s+(.+)", 1),
            (r"^why\s+(?:is|are|does|do|is)\s+(.+)", 1),
            (r"^tell\s+me\s+about\s+(.+)", 1),
            (r"^find\s+(.+)", 1),
            (r"^define\s+(.+)", 1),
            (r"^explain\s+(.+)", 1),
            (r"^latest\s+(.+)", 1),
            (r"^news\s+(?:about\s+)?(.+)", 1),
            (r"^weather\s+(?:in\s+)?(.+)", 1),
            (r"^price\s+(?:of\s+)?(.+)", 1),
            (r"^stock\s+(.+)", 1),
        ]

        for pattern, group in patterns:
            match = re.match(pattern, text)
            if match:
                return match.group(group).strip()
        return None

    def _setup_help(self):
        """Provide setup instructions for Google Custom Search"""
        return """
**Google Custom Search Setup Guide:**

1. **Get API Key:**
   - Go to: https://console.cloud.google.com/
   - Create a new project
   - Enable "Custom Search API"
   - Create credentials → API Key

2. **Create Custom Search Engine:**
   - Go to: https://cse.google.com/cse/all
   - Click "Create a new search engine"
   - Enter websites to search (or leave blank for all)
   - Get your Search Engine ID (cx)

3. **Configure KaStart:**
   Say: "Configure search with API_KEY and CX"
   Example: "Configure search with AIza... and 8a3b..."

**Note:** Install `duckduckgo-search` for free web search:
```
pip install duckduckgo-search
```
"""
