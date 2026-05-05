import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class RiskReport {

    public static void main(String[] args) {

        try {
            String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
            String user = "postgres";
            String password = "postgres";

            Connection conn = DriverManager.getConnection(url, user, password);
            Statement stmt = conn.createStatement();

            ResultSet totalRs = stmt.executeQuery("SELECT COUNT(*) AS total FROM risk");
            totalRs.next();
            int totalRisks = totalRs.getInt("total");

            ResultSet highRs = stmt.executeQuery("SELECT COUNT(*) AS high_count FROM risk WHERE risk_level='High'");
            highRs.next();
            int highRisks = highRs.getInt("high_count");

            System.out.println("----- Risk Report -----");
            System.out.println("Total Risks: " + totalRisks);
            System.out.println("High Risks: " + highRisks);
            System.out.println("-----------------------");

            ResultSet rs = stmt.executeQuery("SELECT * FROM risk");

            while (rs.next()) {
                System.out.println(
                    rs.getInt("risk_id") + " | " +
                    rs.getString("risk_name") + " | " +
                    rs.getString("risk_level")
                );
            }

            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}