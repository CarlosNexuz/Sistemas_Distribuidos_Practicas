package org.example.servlets;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.StringJoiner;

@WebServlet("/pokedex")
public class PokedexServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pokemonId = req.getParameter("id");
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest pokeApiRequest = HttpRequest.newBuilder()
                .uri(URI.create("https://pokeapi.co/api/v2/pokemon/" + pokemonId))
                .build();

        try {
            HttpResponse<String> pokeApiResponse = client.send(pokeApiRequest, HttpResponse.BodyHandlers.ofString());
            String jsonResponseString = pokeApiResponse.body();
            JsonObject jsonObject = JsonParser.parseString(jsonResponseString).getAsJsonObject();

            // --- DATOS EXISTENTES ---
            String nombre = jsonObject.get("name").getAsString();
            String imagenUrl = jsonObject.get("sprites").getAsJsonObject()
                    .get("other").getAsJsonObject()
                    .get("official-artwork").getAsJsonObject()
                    .get("front_default").getAsString();

            // --- EXTRACCIÓN DE NUEVOS DATOS ---
            int id = jsonObject.get("id").getAsInt();

            // La API da la altura en decímetros, la convertimos a metros.
            double altura = jsonObject.get("height").getAsInt() / 10.0;

            // La API da el peso en hectogramos, lo convertimos a kilogramos.
            double peso = jsonObject.get("weight").getAsInt() / 10.0;

            // Extraemos los tipos y los unimos con una coma
            StringJoiner tipos = new StringJoiner(", ");
            jsonObject.get("types").getAsJsonArray().forEach(t -> {
                String tipo = t.getAsJsonObject().get("type").getAsJsonObject().get("name").getAsString();
                tipos.add(tipo);
            });

            // Extraemos las habilidades y las unimos con una coma
            StringJoiner habilidades = new StringJoiner(", ");
            jsonObject.get("abilities").getAsJsonArray().forEach(a -> {
                String habilidad = a.getAsJsonObject().get("ability").getAsJsonObject().get("name").getAsString();
                habilidades.add(habilidad);
            });

            // --- CONSTRUCCIÓN DEL JSON DE RESPUESTA ---
            JsonObject respuestaParaCliente = new JsonObject();
            respuestaParaCliente.addProperty("nombre", nombre);
            respuestaParaCliente.addProperty("imagen", imagenUrl);
            respuestaParaCliente.addProperty("id", String.format("#%03d", id)); // Formateado como #001
            respuestaParaCliente.addProperty("tipos", tipos.toString());
            respuestaParaCliente.addProperty("altura", altura + " m");
            respuestaParaCliente.addProperty("peso", peso + " kg");
            respuestaParaCliente.addProperty("habilidades", habilidades.toString());

            resp.setContentType("application/json");
            resp.setCharacterEncoding("UTF-8");
            resp.getWriter().write(respuestaParaCliente.toString());

        } catch (Exception e) {
            resp.setStatus(HttpServletResponse.SC_NOT_FOUND); // Usar 404 para Pokémon no encontrado
            resp.getWriter().write("{\"error\":\"Pokémon no encontrado: " + e.getMessage() + "\"}");
        }
    }
}