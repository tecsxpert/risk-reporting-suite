import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class InsertRisk {

    public static void main(String[] args) {

        String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
        String user = "postgres";
        String password = "postgres"; // change if your password is different

        try {
            Connection conn = DriverManager.getConnection(url, user, password);

            Statement stmt = conn.createStatement();

            String sql = "INSERT INTO risk (risk_id, risk_name, risk_level, description) VALUES (4, 'System Failure', 'High', 'Main system failure risk')";

            int rows = stmt.executeUpdate(sql);

            if (rows > 0) {
                System.out.println("Risk inserted successfully!");
            }

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}