import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.function.Supplier;

public final class Rendezvous {

	public static void main(String[] args) throws InterruptedException, ExecutionException {		
		List<String> testText = List.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta");
		
		Printer reserve = new Printer("Reserve", Optional.empty(), System.out);
		Printer main = new Printer("Main", Optional.of(reserve), System.out);
				
		Messenger testMessenger = new Messenger(testText, main);
		
		while (CompletableFuture.supplyAsync(testMessenger).get()) { }
	}

}

final class Messenger implements Supplier<Boolean> {
	
    public Messenger(List<String> aMessage, Printer aPrinter) {
    	message = new ArrayList<String>(aMessage);
    	iterator = message.iterator();
        printer = aPrinter;
    }

    @Override
	public Boolean get() {
		if (iterator.hasNext()) {
			try {
				printer.display(iterator.next());
			} catch (OutOfInkException exception) {
				return false;
			}
			return true;
		}	
		return false;
	}

    private List<String> message;
	private Iterator<String> iterator;
    private Printer printer;

}

final class Printer {	
	
    public Printer(String aName, Optional<Printer> aReserve, PrintStream aPrintStream) {
        name = aName;
        reserve = aReserve;
        printStream = aPrintStream;
    }

    public void display(String message) throws OutOfInkException {
    	if (inkLevelForClientUse > 0) {
    		printStream.println("(" + name + ") " + message);
    		inkLevelForClientUse -= 1;
    	} else {
    		if (reserve.isPresent()) {
    			reserve.get().display(message);
    		} else {
    			printStream.println("        Printer out of ink");	
    			throw new OutOfInkException();
    		}
    	}
    	
    }

    private String name;
    private Optional<Printer> reserve;
    private PrintStream printStream;
    private int inkLevelForClientUse = 5;

}

final class OutOfInkException extends Exception { }