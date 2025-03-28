public class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    private final int connectionId;

    private DatabaseConnection() {
        this.connectionId = this.hashCode();
    }

    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }

    public int getConnectionId() {
        return connectionId;
    }

    public static void main(String[] args) {
        DatabaseConnection db1 = DatabaseConnection.getInstance();
        DatabaseConnection db2 = DatabaseConnection.getInstance();

        System.out.println(db1.getConnectionId());
        System.out.println(db2.getConnectionId());
        System.out.println(db1 == db2);
    }
}
