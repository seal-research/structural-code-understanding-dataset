import java.util.Scanner;
import java.util.Random;

public class CheckpointSync{
	private static void runTasks(int nTasks){
		for(int i = 0; i < nTasks; i++){
			System.out.println("Starting task number " + (i+1) + ".");
			runThreads();
			Worker.checkpoint();
		}
	}
	
	private static void runThreads(){
		for(int i = 0; i < Worker.nWorkers; i ++){
			new Thread(new Worker(i+1)).start();
		}
	}
	
	public static class Worker implements Runnable{
		public Worker(int threadID){
			this.threadID = threadID;
		}
		public void run(){
			work();
		}
		
		private synchronized void work(){
			try {
				int workTime = rgen.nextInt(900) + 100;
				System.out.println("Worker " + threadID + " will work for " + workTime + " msec.");
				Thread.sleep(workTime);
				nFinished++;
				System.out.println("Worker " + threadID + " is ready");
			} catch (InterruptedException e) {
				System.err.println("Error: thread execution interrupted");
				e.printStackTrace();
			}
		}
		
		public static synchronized void checkpoint(){
			while(nFinished != nWorkers){
				try {
					Thread.sleep(10);
				} catch (InterruptedException e) {
					System.err.println("Error: thread execution interrupted");
					e.printStackTrace();
				}
			}
			nFinished = 0;
		}
	
		private int threadID;
		private static Random rgen = new Random();
		private static int nFinished = 0;
		public static int nWorkers = 0;
	}
	
	public static void main(String[] args){
		Worker.nWorkers = 6;
		runTasks(1);
	}
}