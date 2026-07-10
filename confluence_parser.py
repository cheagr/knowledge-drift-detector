from bs4 import BeautifulSoup


def parse_confluence(uploaded_file):
    """
    Parses a Confluence HTML export.
    
    """

    try:
        html = uploaded_file.read().decode("utf-8")
    except Exception as ex:
        return False, {
            "error": f"Unable to read HTML file.\n\n{str(ex)}"
        }

    try:
        soup = BeautifulSoup(html, "html.parser")

        title = ""

        if soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)

        if not title:
            return False, {
                "error": "Unable to locate Feature Title (H1) in Confluence page."
            }

        sections = []

        headings = soup.find_all("h2")

        if not headings:
            return False, {
                "error": "No H2 sections found in Confluence page."
            }

        for heading in headings:

            section_title = heading.get_text(strip=True)

            content = []

            node = heading.find_next_sibling()

            while node and node.name != "h2":

                text = node.get_text(" ", strip=True)

                if text:
                    content.append(text)

                node = node.find_next_sibling()

            sections.append(
                {
                    "heading": section_title,
                    "content": "\n".join(content)
                }
            )

        return True, {
            "title": title,
            "sections": sections
        }

    except Exception as ex:

        return False, {
            "error": f"Failed to parse Confluence page.\n\n{str(ex)}"
        }