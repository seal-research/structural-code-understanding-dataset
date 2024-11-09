public class FizzBuzz {

    private static class Sound {
        private final int trigger;
        private final String onomatopoeia;

        public Sound(int trigger, String onomatopoeia) {
            this.trigger = trigger;
            this.onomatopoeia = onomatopoeia;
        }

        public String generate(int i) {
            return i % trigger == 0 ? onomatopoeia : "";
        }
    }

    public static void main(String[] args) {
        Sound sound = new Sound(5, "Buzz");
        System.out.println(sound.generate(10));
    }
}