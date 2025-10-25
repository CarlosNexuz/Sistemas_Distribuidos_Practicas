async function buscarPokemon() {
    const id = document.getElementById('pokemonId').value.toLowerCase().trim();
    if (!id) {
        return; // No hacer nada si el input está vacío
    }

    const card = document.getElementById('pokedex-card');
    const loadingMsg = document.getElementById('loading-message');

    // Prepara la UI para la búsqueda
    card.classList.add('hidden');
    loadingMsg.style.display = 'block';

    try {
        // Llama a tu servicio Java
        const response = await fetch(`/pokedex?id=${id}`);
        if (!response.ok) {
            throw new Error('Pokémon no encontrado. Verifica el número o nombre.');
        }
        const data = await response.json();

        // Llenar todos los campos con la nueva data recibida
        document.getElementById('pokemon-name').innerText = data.nombre;
        document.getElementById('pokemon-image').src = data.imagen;
        document.getElementById('pokemon-id').innerText = data.id;
        document.getElementById('pokemon-types').innerText = 'Tipo: ' + data.tipos;
        document.getElementById('pokemon-altura').innerText = data.altura;
        document.getElementById('pokemon-peso').innerText = data.peso;
        document.getElementById('pokemon-habilidades').innerText = data.habilidades;

        // Muestra la tarjeta actualizada
        card.classList.remove('hidden');

    } catch (error) {
        // Muestra un error simple al usuario si algo falla
        alert(error.message);
    } finally {
        // Siempre oculta el mensaje de carga al terminar
        loadingMsg.style.display = 'none';
    }
}