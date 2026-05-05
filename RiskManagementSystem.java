import java.sql.*;
import java.util.Scanner;

public class RiskManagementSystem {

    static String url = "jdbc:postgresql://localhost:5432/risk_reporting_db";
    static String user = "postgres";
    static String password = "postgres";

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("\n===== Risk Reporting Suite =====");
            System.out.println("1. Add Risk");
            System.out.println("2. View Risks");
            System.out.println("3. Update Risk");
            System.out.println("4. Delete Risk");
            System.out.println("5. Generate Risk Report");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");

            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    addRisk(sc);
                    break;
                case 2:
                    viewRisks();
                    break;
                case 3:
                    updateRisk(sc);
                    break;
                case 4:
                    deleteRisk(sc);
                    break;
                case 5:
                    generateReport();
                    break;
                case 6:
                    System.out.println("Thank you for using Risk Reporting Suite!");
                    sc.close();
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    static Connection getConnection() throws Exception {
        return DriverManager.getConnection(url, user, password);
    }

    static void addRisk(Scanner sc) {
        try {
            System.out.print("Enter Risk ID: ");
            int id = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter Risk Name: ");
            String name = sc.nextLine();

            System.out.print("Enter Risk Level: ");
            String level = sc.nextLine();

            System.out.print("Enter Description: ");
            String description = sc.nextLine();

            Connection conn = getConnection();

            String sql = "INSERT INTO risk (risk_id, risk_name, risk_level, description) VALUES (?, ?, ?, ?)";
            PreparedStatement ps = conn.prepareStatement(sql);

            ps.setInt(1, id);
            ps.setString(2, name);
            ps.setString(3, level);
            ps.setString(4, description);

            ps.executeUpdate();

            System.out.println("Risk added successfully!");

            conn.close();

        } catch (Exception e) {
            System.out.println("Error while adding risk.");
            e.printStackTrace();
        }
    }

    static void viewRisks() {
        try {
            Connection conn = getConnection();

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM risk ORDER BY risk_id");

            System.out.println("\nRisk Records:");
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
            System.out.println("Error while viewing risks.");
            e.printStackTrace();
        }
    }

    static void updateRisk(Scanner sc) {
        try {
            System.out.print("Enter Risk ID to update: ");
            int id = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter New Risk Level: ");
            String level = sc.nextLine();

            System.out.print("Enter New Description: ");
            String description = sc.nextLine();

            Connection conn = getConnection();

            String sql = "UPDATE risk SET risk_level = ?, description = ? WHERE risk_id = ?";
            PreparedStatement ps = conn.prepareStatement(sql);

            ps.setString(1, level);
            ps.setString(2, description);
            ps.setInt(3, id);

            int rows = ps.executeUpdate();

            if (rows > 0) {
                System.out.println("Risk updated successfully!");
            } else {
                System.out.println("Risk not found!");
            }

            conn.close();

        } catch (Exception e) {
            System.out.println("Error while updating risk.");
            e.printStackTrace();
        }
    }

    static void deleteRisk(Scanner sc) {
        try {
            System.out.print("Enter Risk ID to delete: ");
            int id = sc.nextInt();

            Connection conn = getConnection();

            String sql = "DELETE FROM risk WHERE risk_id = ?";
            PreparedStatement ps = conn.prepareStatement(sql);

            ps.setInt(1, id);

            int rows = ps.executeUpdate();

            if (rows > 0) {
                System.out.println("Risk deleted successfully!");
            } else {
                System.out.println("Risk not found!");
            }

            conn.close();

        } catch (Exception e) {
            System.out.println("Error while deleting risk.");
            e.printStackTrace();
        }
    }

    static void generateReport() {
        try {
            Connection conn = getConnection();
            Statement stmt = conn.createStatement();

            ResultSet totalRs = stmt.executeQuery("SELECT COUNT(*) AS total FROM risk");
            totalRs.next();
            int totalRisks = totalRs.getInt("total");

            ResultSet highRs = stmt.executeQuery("SELECT COUNT(*) AS high_count FROM risk WHERE risk_level='High'");
            highRs.next();
            int highRisks = highRs.getInt("high_count");

            ResultSet mediumRs = stmt.executeQuery("SELECT COUNT(*) AS medium_count FROM risk WHERE risk_level='Medium'");
            mediumRs.next();
            int mediumRisks = mediumRs.getInt("medium_count");

            System.out.println("\n----- Risk Report -----");
            System.out.println("Total Risks: " + totalRisks);
            System.out.println("High Risks: " + highRisks);
            System.out.println("Medium Risks: " + mediumRisks);
            System.out.println("-----------------------");

            conn.close();

        } catch (Exception e) {
            System.out.println("Error while generating report.");
            e.printStackTrace();
        }
    }
}