package org.example.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

// 1. Mapeamos esta clase a la URL "/inicio"
@WebServlet("/inicio")
public class InicioServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        // 2. Le decimos al navegador que vamos a enviar contenido HTML
        resp.setContentType("text/html; charset=UTF-8");

        // 3. Esta es la línea clave:
        // Reenvía la petición al archivo JSP o HTML para que el servidor lo procese y lo envíe.
        req.getRequestDispatcher("/inicio.html").forward(req, resp);
    }
}