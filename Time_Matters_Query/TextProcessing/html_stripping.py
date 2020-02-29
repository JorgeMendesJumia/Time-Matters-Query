from bs4 import BeautifulSoup

def html_stripping(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text
