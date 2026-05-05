import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class InsertUser {

    public static void main(String[] args) {

        try {

            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            Connection conn = DriverManager.getConnection(url, user, password);

            Statement stmt = conn.createStatement();

            String sql = "INSERT INTO users1 VALUES (5, 'developer', 'dev123')";

            stmt.executeUpdate(sql);

            System.out.println("User inserted successfully!");

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}