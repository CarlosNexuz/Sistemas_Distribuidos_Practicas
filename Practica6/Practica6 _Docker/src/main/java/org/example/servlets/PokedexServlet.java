package org.example.servlets;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.StringJoiner;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/pokedex")
public class PokedexServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    String pokemonId = req.getParameter("id");
    if (pokemonId == null || pokemonId.isBlank()) {
        resp.setStatus(HttpServletResponse.SC_BAD_REQUEST);
        resp.getWriter().write("{\"error\":\"Se debe proporcionar un id o nombre de Pokémon\"}");
        return;
    }

    HttpClient client = HttpClient.newHttpClient();
    HttpRequest pokeApiRequest = HttpRequest.newBuilder()
            .uri(URI.create("https://pokeapi.co/api/v2/pokemon/" + pokemonId.toLowerCase()))
            .build();

    try {
        HttpResponse<String> pokeApiResponse = client.send(pokeApiRequest, HttpResponse.BodyHandlers.ofString());
        int statusCode = pokeApiResponse.statusCode();

        if (statusCode != 200) {
            resp.setStatus(HttpServletResponse.SC_NOT_FOUND);
            resp.getWriter().write("{\"error\":\"Pokémon no encontrado\"}");
            return;
        }

        String jsonResponseString = pokeApiResponse.body();

        // Parse seguro con Gson
        JsonObject jsonObject = JsonParser.parseString(jsonResponseString).getAsJsonObject();

        // --- DATOS EXISTENTES ---
        String nombre = jsonObject.get("name").getAsString();
        String imagenUrl = jsonObject.get("sprites").getAsJsonObject()
                .get("other").getAsJsonObject()
                .get("official-artwork").getAsJsonObject()
                .get("front_default").getAsString();

        int id = jsonObject.get("id").getAsInt();
        double altura = jsonObject.get("height").getAsInt() / 10.0;
        double peso = jsonObject.get("weight").getAsInt() / 10.0;

        StringJoiner tipos = new StringJoiner(", ");
        jsonObject.get("types").getAsJsonArray().forEach(t -> {
            String tipo = t.getAsJsonObject().get("type").getAsJsonObject().get("name").getAsString();
            tipos.add(tipo);
        });

        StringJoiner habilidades = new StringJoiner(", ");
        jsonObject.get("abilities").getAsJsonArray().forEach(a -> {
            String habilidad = a.getAsJsonObject().get("ability").getAsJsonObject().get("name").getAsString();
            habilidades.add(habilidad);
        });

        JsonObject respuestaParaCliente = new JsonObject();
        respuestaParaCliente.addProperty("nombre", nombre);
        respuestaParaCliente.addProperty("imagen", imagenUrl);
        respuestaParaCliente.addProperty("id", String.format("#%03d", id));
        respuestaParaCliente.addProperty("tipos", tipos.toString());
        respuestaParaCliente.addProperty("altura", altura + " m");
        respuestaParaCliente.addProperty("peso", peso + " kg");
        respuestaParaCliente.addProperty("habilidades", habilidades.toString());

        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        resp.getWriter().write(respuestaParaCliente.toString());

    } catch (Exception e) {
        resp.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        resp.getWriter().write("{\"error\":\"Error interno del servidor: " + e.getMessage() + "\"}");
    }
}

}