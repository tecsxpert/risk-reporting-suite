import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class UpdateUser {

    public static void main(String[] args) {

        try {

            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            Connection conn = DriverManager.getConnection(url, user, password);

            Statement stmt = conn.createStatement();

            String sql = "UPDATE users1 SET password='newpass123' WHERE id=2";

            stmt.executeUpdate(sql);

            System.out.println("User updated successfully!");

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}