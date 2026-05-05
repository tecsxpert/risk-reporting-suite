import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class DeleteUser {

    public static void main(String[] args) {

        try {

            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            Connection conn = DriverManager.getConnection(url, user, password);

            Statement stmt = conn.createStatement();

            String sql = "DELETE FROM users1 WHERE id=3";

            stmt.executeUpdate(sql);

            System.out.println("User deleted successfully!");

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}