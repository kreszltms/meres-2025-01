package com.iakk.nevnapkereso;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/api/nevnapok")
public class NevnapServlet extends HttpServlet {

    private static final String DB_URL = "jdbc:mysql://localhost:3306/nevnapok";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "password";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String nap = request.getParameter("nap");
        String nev = request.getParameter("nev");

        response.setContentType("application/json");
        PrintWriter out = response.getWriter();

        if (nap == null && nev == null) {
            out.print("{\"minta1\":\"/?nap=12-31\",\"minta2\":\"/?nev=Szilveszter\"}");
            return;
        }

        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query;
            PreparedStatement stmt;

            if (nap != null) {
                query = "SELECT * FROM nevnapok WHERE datum = ?";
                stmt = conn.prepareStatement(query);
                stmt.setString(1, nap);
            } else {
                query = "SELECT * FROM nevnapok WHERE nevnap1 = ? OR nevnap2 = ?";
                stmt = conn.prepareStatement(query);
                stmt.setString(1, nev);
                stmt.setString(2, nev);
            }

            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                Map<String, String> result = new HashMap<>();
                result.put("datum", rs.getString("datum"));
                result.put("nevnap1", rs.getString("nevnap1"));
                result.put("nevnap2", rs.getString("nevnap2"));

                out.print(mapToJson(result));
            } else {
                out.print("{\"hiba\":\"nincs találat\"}");
            }

        } catch (SQLException e) {
            e.printStackTrace();
            out.print("{\"hiba\":\"Adatbázis hiba\"}");
        }
    }

    private String mapToJson(Map<String, String> map) {
        StringBuilder json = new StringBuilder("{");
        map.forEach((key, value) -> json.append("\"").append(key).append("\":\"").append(value).append("\","));
        json.deleteCharAt(json.length() - 1).append("}");
        return json.toString();
    }
}
