class TrafficLight {
  public void carArrived(
      // ID of the car
      int carId,
      // ID of the road the car travels on. Can be 1 (road A) or 2 (road B).
      int roadId,
      // direction of the car
      int direction,
      // Use turnGreen() to turn light to green on current road.
      Runnable turnGreen,
      // Use crossCar() to make car cross the intersection.
      Runnable crossCar) {
    synchronized (this) {
      if (canPassRoadId != roadId) {
        canPassRoadId = roadId;
        turnGreen.run();
      }
      crossCar.run();
    }
  }

  private int canPassRoadId = 1; // 1 := road A, 2 := road B

  public static void main(String[] args) {
    TrafficLight trafficLight = new TrafficLight();
    Runnable turnGreen = () -> System.out.println("Light turned green");
    Runnable crossCar = () -> System.out.println("Car crossed the intersection");
    trafficLight.carArrived(5, 1, 4, turnGreen, crossCar);
  }
}