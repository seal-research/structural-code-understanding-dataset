class Solution:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        hostname = urlparse(startUrl).hostname
        seen = set([startUrl])
        lock = Lock()
        unseen = Queue()
        unseen.put(startUrl)

        def worker():
            while True:
                url = unseen.get()  # Get URL from queue
                if url is None:
                    break
                
                # Get all URLs from current page
                for next_url in htmlParser.getUrls(url):
                    # Check hostname and if URL was seen
                    if urlparse(next_url).hostname == hostname:
                        with lock:
                            if next_url not in seen:
                                seen.add(next_url)
                                unseen.put(next_url)
                
                unseen.task_done()

        threads = []
        num_threads = 10 #START
        
        # Start worker threads
        for _ in range(num_threads):
            thread = Thread(target=worker)
            thread.daemon = True  # Set as daemon thread
            thread.start() #START

            threads.append(thread)
        
        # Wait for the queue to be empty
        unseen.join()
        
        # Stop workers
        for _ in range(num_threads):
            unseen.put(None)
            
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return list(seen) #END



if __name__ == "__main__":
    class HtmlParser:
        def getUrls(self, url):
            return ["http://example.com/page1", "http://example.com/page2"]

    solution = Solution()
    result = solution.crawl("http://example.com", HtmlParser())
    print(result)