import requests
from bs4 import BeautifulSoup
from newspaper import Article

def bookmark_download(file):
    bookmarks = {}
    with open(file) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        for link in soup.find_all('a', href=True)[:100]:
            bookmarks[link.text] = link['href']
    
    for i in bookmarks:
    try:
        # Handle files
        if any(j in bookmarks[i] for j in ['.pdf', '.doc', '.docx']):
            r = requests.get(bookmarks[i], timeout=10)
            file_name = bookmarks[i].split('/')[-1]
            with open('store/bookmarks/{}'.format(file_name), 'wb') as f:
                f.write(r.content)

        else:
            # Handle plain-text/HTML
            article = Article(bookmarks[i])
            article.download()
            article.parse()
            text = article.text
            with open('store/bookmarks/{}.txt'.format(i), 'w') as f:
                f.write(text)
    except:
        print('{} error'.format(i))


if __name__ == "__main__":
    bookmark_download('bookmarks.html')
