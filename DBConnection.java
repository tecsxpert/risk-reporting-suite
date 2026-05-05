import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class DBConnection {
    public static void main(String[] args) {

        try {
            // Database details
            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            // Connect to database
            Connection conn = DriverManager.getConnection(url, user, password);

            System.out.println("Connected to PostgreSQL successfully!");

            // Create statement
            Statement stmt = conn.createStatement();

            // Execute query
            ResultSet rs = stmt.executeQuery("SELECT * FROM users1");

            // Display data
            while (rs.next()) {
                System.out.println(
                    rs.getInt("id") + " | " +
                    rs.getString("username") + " | " +
                    rs.getString("password")
                );
            }

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}