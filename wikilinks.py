from collections import Counter, defaultdict
import re

def get_article_links_score(article):
    """Function to get article links scores using wikisyns."""
    
    html_links = article.links()
    html_text = re.sub(r"[\n]+", " ", article.text())

    links_text_counter = Counter() #Link text counter
    links_text_dict = defaultdict(list)
    links_case_dict = dict() #Dictionary to store the link original case

    for link, text in html_links:
        links_case_dict[link.lower()] = link
        links_text_dict[text.lower()].append(link.lower())

    for l_text in links_text_dict.keys():
        matches = re.findall('[^a-zA-Z0-9_]' + re.escape(l_text) + '[^a-zA-Z0-9_]', html_text, re.IGNORECASE)
        for _ in range(len(matches)):
            links_weight = 1.0 / len(links_text_dict[l_text])
            for link in links_text_dict[l_text]:
                links_text_counter[link] += links_weight

    #Sort and get tuple
    sorted_links_scores = links_text_counter.most_common()

    sorted_links_scores = [(links_case_dict[link], score) for link, score in sorted_links_scores]

    return sorted_links_scores