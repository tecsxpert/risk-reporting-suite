import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class UpdateRisk {

    public static void main(String[] args) {

        try {
            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            Connection conn = DriverManager.getConnection(url, user, password);
            Statement stmt = conn.createStatement();

            String sql = "UPDATE risk SET risk_level='Critical', description='Updated high priority system failure risk' WHERE risk_id=4";

            int rows = stmt.executeUpdate(sql);

            if (rows > 0) {
                System.out.println("Risk updated successfully!");
            } else {
                System.out.println("Risk not found!");
            }

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}