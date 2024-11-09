from threading import Thread, Lock
from urllib.parse import urlparse  # To parse URLs and extract hostname for comparison
from typing import List

class Solution:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        hostname = urlparse(startUrl).hostname
        seen = set([startUrl])  # Keep track of seen URLs to avoid re-crawling the same URL
        lock = Lock()  # Lock for thread-safe operations on the seen set

        def dfs(url):
            for next_url in htmlParser.getUrls(url):
                if urlparse(next_url).hostname == hostname and next_url not in seen:
                    with lock:  # Ensure thread-safe write to the seen set
                        if next_url not in seen:
                            seen.add(next_url)
                            dfs(next_url)

        def worker():
            while True:
                with lock:
                    if not unseen:
                        return
                    url = unseen.pop()
                dfs(url)

        unseen = [startUrl]  # Stack of URLs to be crawled
        threads = []
        num_threads = 10  # Or any number you deem appropriate based on the problem constraints

        # Start threads
        for _ in range(num_threads):
            thread = Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return list(seen)

if __name__ == "__main__":
    class HtmlParser:
        def getUrls(self, url):
            return ["http://example.com/page1", "http://example.com/page2", "http://example.com/page3", "http://example.com/page4", "http://example.com/page5"]

    solution = Solution()
    result = solution.crawl("http://example.com", HtmlParser())
    print(result)