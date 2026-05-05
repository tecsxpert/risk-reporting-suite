import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class ViewRisk {

    public static void main(String[] args) {

        try {
            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            Connection conn = DriverManager.getConnection(url, user, password);

            Statement stmt = conn.createStatement();

            ResultSet rs = stmt.executeQuery("SELECT * FROM risk");

            System.out.println("Risk Records:");
            System.out.println("------------------------------------------");

            while (rs.next()) {

                System.out.println(
                    rs.getInt("risk_id") + " | " +
                    rs.getString("risk_name") + " | " +
                    rs.getString("risk_level") + " | " +
                    rs.getString("description")
                );
            }

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}