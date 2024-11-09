import java.io.BufferedReader;
import java.io.FileReader;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

class SynchronousConcurrency
{
  public static void main(String[] args) throws Exception
  {
    final AtomicLong lineCount = new AtomicLong(0);
    final BlockingQueue<String> queue = new LinkedBlockingQueue<String>();
    final String EOF = new String();

    final Thread writerThread = new Thread(new Runnable() {
        public void run()
        {
          long linesWrote = 0;
          while (true)
          {
            try
            {
              String line = queue.take();
              if (line == EOF)
                break;
              System.out.println(line);
              linesWrote++;
            }
            catch (InterruptedException ie)
            {  }
          }
          lineCount.set(linesWrote);
        }
      }
    );
    writerThread.start();

    BufferedReader br = new BufferedReader(new FileReader("input.txt"));
    String line;
    while ((line = br.readLine()) != null)
      queue.put(line);
    br.close();
    queue.put(EOF);
    writerThread.join();
    System.out.println("Line count: " + lineCount.get());
    return;
  }
}