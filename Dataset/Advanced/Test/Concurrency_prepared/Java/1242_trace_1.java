import java.net.URI;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Web_Crawler_Multithreaded {

    class Solution_1_synchronizedList {
        private final Set<String> set = Collections.newSetFromMap(new ConcurrentHashMap<String, Boolean>());
        private final List<String> result = Collections.synchronizedList(new ArrayList<String>());
        private String HOSTNAME = null;

        public List<String> crawl(String startUrl, HtmlParser htmlParser) {
            initHostName(startUrl);
            set.add(startUrl);
            getUrlDfs(startUrl, htmlParser);
            return result;
        }

        private boolean judgeHostname(String url) {
            int idx = url.indexOf('/', 7);
            String hostName = (idx != -1) ? url.substring(0, idx) : url;
            return hostName.equals(HOSTNAME);
        }

        private void initHostName(String url) {
            int idx = url.indexOf('/', 7);
            HOSTNAME = (idx != -1) ? url.substring(0, idx) : url;
        }

        private void getUrlDfs(String startUrl, HtmlParser htmlParser) {
            result.add(startUrl);
            List<String> res = htmlParser.getUrls(startUrl);
            List<Thread> threads = new ArrayList<>();
            for (String url : res) {
                if (judgeHostname(url) && !set.contains(url)) {
                    set.add(url);
                    threads.add(new Thread(() -> {
                        getUrlDfs(url, htmlParser);
                    }));
                }
            }
            for (Thread thread : threads) {
                thread.start();
            }
            try {
                for (Thread thread : threads) {
                    thread.join(); // Waits for this thread to die.
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }

    interface HtmlParser {
        // Return a list of all urls from a webpage of given url.
        // This is a blocking call, that means it will do HTTP request and return when this request is finished.
        List<String> getUrls(String str);
    }


    class Solution_CrawlerClass {
        public List<String> crawl(String startUrl, HtmlParser htmlParser) {
            // 取得startUrl的域名
            String host = URI.create(startUrl).getHost();
            // 新建一个线程，爬取startUrl中的所有链接
            Crawler crawler = new Crawler(startUrl, host, htmlParser);
            // 初始化线程的返回结果
            crawler.res = new ArrayList<>();
            // 开启线程（相当于从起点开始dfs）
            crawler.start();
            // 等待线程执行结束
            Crawler.joinThread(crawler);
            // 返回线程的执行结果
            return crawler.res;
        }
    }

    // 爬虫线程（相当于原始的dfs方法）
    static class Crawler extends Thread {
        String startUrl; // 当前url
        String hostname; // 域名
        HtmlParser htmlParser; // 爬虫接口
        // 返回结果
        public volatile List<String> res = new ArrayList<>();

        // 初始化线程
        public Crawler(String startUrl, String hostname, HtmlParser htmlParser) {
            this.startUrl = startUrl;
            this.hostname = hostname;
            this.htmlParser = htmlParser;
        }

        @Override
        public void run() {
            // 获得当前url的域名
            String host = URI.create(startUrl).getHost();
            // 如果当前域名不属于目标网站，或者当前域名已经爬过，略过
            if (!host.equals(hostname) || res.contains(startUrl)) {
                return;
            }
            // 将当前url加入结果集
            res.add(startUrl);
            // 记录当前url页面包含的链接
            // 每个链接启动一个新的线程继续dfs
            List<Thread> threads = new ArrayList<>();
            for (String s : htmlParser.getUrls(startUrl)) {
                Crawler crawler = new Crawler(s, hostname, htmlParser);
                crawler.start();
                threads.add(crawler);
            }
            // 等待每个子线程执行结束后，再结束当前线程
            for (Thread t : threads) {
                joinThread(t);
            }
        }

        public static void joinThread(Thread thread) {
            try {
                thread.join();
            } catch (InterruptedException e) {
            }
        }

    }

    public static void main(String[] args) {
        Web_Crawler_Multithreaded webCrawler = new Web_Crawler_Multithreaded();
        Solution_1_synchronizedList solution = webCrawler.new Solution_1_synchronizedList();
        HtmlParser htmlParser = new HtmlParser() {
            @Override
            public List<String> getUrls(String str) {
                return List.of("http://example.com/page1", "http://example.com/page2");
            }
        };
        System.out.println(solution.crawl("http://example.com", htmlParser));
    }
}