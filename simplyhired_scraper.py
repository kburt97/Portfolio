from bs4 import BeautifulSoup
import json

keyword = "Data Scientist"

with open("sample_simplyhired.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

jobs = []

for a in soup.find_all("a"):
    title = a.get_text(strip=True)
    if keyword.lower() in title.lower():
        company = None


        parent = a.find_parent()
        if parent:
            for sibling in parent.find_all(["span", "div"], recursive=True):
                classes = " ".join(sibling.get("class") or [])
                if "company" in classes.lower() or "employer" in classes.lower():
                    company = sibling.get_text(strip=True)
                    break

        jobs.append({"title": title, "company": company or "No company"})

output = {
    "keyword": keyword,
    "total_jobs_found": len(jobs),
    "jobs": jobs
}

with open("jobs_from_html.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Keyword: {keyword}")
print(f"Extracted {len(jobs)} jobs and saved to jobs_from_html.json")
