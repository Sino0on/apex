import re
import json
import datetime

INPUT_FILE = 'templates/index.html'
OUTPUT_FILE = 'universities.json'

def extract_universities():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all commented blocks
    comment_pattern = re.compile(r'<!--(.*?)-->', re.DOTALL)
    comments = comment_pattern.findall(content)

    universities = []
    pk = 1

    for comment in comments:
        if 'class="course-card"' in comment:
            # Extract Logo
            logo_match = re.search(r"url\('{% static '(.*?)' %}'\)", comment)
            logo = logo_match.group(1) if logo_match else ''
            
            # If logo not found with static tag, try direct url or other patterns if needed
            # But based on file content, they are all static tags.
            
            # Extract Title
            title_match = re.search(r'<h3 class="card-title">(.*?)</h3>', comment, re.DOTALL)
            title = title_match.group(1).strip() if title_match else ''
            # Remove any trailing colon if present (e.g. "College Name: ")
            if title.endswith(':'):
                title = title[:-1].strip()

            # Extract Mini Description (card-meta)
            # There might be multiple p tags, we want the card-meta one
            meta_match = re.search(r'<p class="card-meta">(.*?)</p>', comment, re.DOTALL)
            mini_description = meta_match.group(1).strip() if meta_match else ''

            if title and mini_description:
                # Clean up title and description
                title = re.sub(r'\s+', ' ', title)
                mini_description = re.sub(r'\s+', ' ', mini_description)

                # Construct the fixture object
                univer = {
                    "model": "main.university",
                    "pk": pk,
                    "fields": {
                        "title": title,
                        "logo": logo, # Note: This will be relative to MEDIA_ROOT when loaded, but here it's static path.
                        # User might need to move files or we accept broken images for now. 
                        # Ideally we copy these static files to media folder.
                        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                        "mini_description": mini_description,
                        "created_at": datetime.datetime.now().isoformat(),
                        "updated_at": datetime.datetime.now().isoformat()
                    }
                }
                universities.append(univer)
                pk += 1

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(universities, f, indent=4, ensure_ascii=False)

    print(f"Successfully extracted {len(universities)} universities to {OUTPUT_FILE}")

if __name__ == '__main__':
    extract_universities()
