import java.util.List;

public final class DetermineSentenceType {

	private static char sentenceType(String aSentence) {
		if ( aSentence.isEmpty() ) {
			throw new IllegalArgumentException("Cannot classify an empty sentence");
		}
		
		final char lastCharacter = aSentence.charAt(aSentence.length() - 1);
		return switch (lastCharacter) {
			case '?' -> 'Q';
			case '.' -> 'S';
			case '!' -> 'E';
			default  -> 'N';
		};		
	}	
	
	public static void main(String[] aArgs) {
		String testSentence = "Is this a question?";
		System.out.println(testSentence + " -> " + sentenceType(testSentence));
	}
	
}