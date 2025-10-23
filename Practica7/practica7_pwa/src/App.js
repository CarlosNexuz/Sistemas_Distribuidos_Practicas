import React, { useState, useEffect } from 'react';

// --- Componente para el formulario de subida ---
function PostForm({ onAddPost }) {
  const [title, setTitle] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim() || !imageFile) {
      setError('Por favor, añade un título y una imagen.');
      return;
    }
    
    const reader = new FileReader();
    reader.onload = (event) => {
      onAddPost(title, event.target.result);
      setTitle('');
      setImageFile(null);
      setPreview(null);
      setError('');
      e.target.reset();
    };
    reader.readAsDataURL(imageFile);
  };

  return (
    <form onSubmit={handleSubmit} className="post-form">
      {error && <p className="error-message">{error}</p>}
      <input
        type="text"
        placeholder="Título de la publicación..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="input-title"
      />
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="input-file"
      />
      {preview && <img src={preview} alt="Previsualización" className="image-preview" />}
      <button type="submit" className="submit-button">
        Publicar
      </button>
    </form>
  );
}

// --- Componente para mostrar una publicación ---
function Post({ post, onDelete, onLike }) {
  return (
    <div className="post-card">
      <img src={post.image} alt={post.title} className="post-image" />
      <div className="post-content">
        <h2 className="post-title">{post.title}</h2>
        <div className="post-actions">
          <button onClick={() => onLike(post.id)} className={`like-button ${post.liked ? 'liked' : ''}`}>
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <span>{post.liked ? 'Te gusta' : 'Me gusta'}</span>
          </button>
          <button onClick={() => onDelete(post.id)} className="delete-button">
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}


// --- Componente Principal App ---
function App() {
  const [posts, setPosts] = useState(() => {
    try {
      const savedPosts = localStorage.getItem('posts');
      return savedPosts ? JSON.parse(savedPosts) : [];
    } catch (error) {
      console.error("Error al cargar posts desde localStorage", error);
      return [];
    }
  });

  // Efecto para inyectar los estilos directamente en el DOM y evitar el error de importación.
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
          'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
          sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        background-color: #f0f2f5;
        color: #1c1e21;
      }

      .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
      }

      .app-header {
        text-align: center;
        margin-bottom: 32px;
      }

      .app-title {
        font-size: 3rem;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #1976d2ff, #14e4ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
      }

      .app-subtitle {
        font-size: 1rem;
        color: #65676b;
      }

      .post-form {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .error-message {
        color: #38fab3ff;
        font-size: 0.9rem;
      }

      .input-title {
        width: 100%;
        padding: 12px;
        border: 1px solid #ccd0d5;
        border-radius: 6px;
        font-size: 1rem;
        box-sizing: border-box;
      }
      .input-title:focus {
        outline: none;
        border-color: #2be2d3ff;
      }

      .input-file {
        font-size: 0.9rem;
      }

      .image-preview {
        width: 100%;
        max-height: 300px;
        border-radius: 8px;
        object-fit: cover;
        margin-top: 8px;
      }

      .submit-button {
        background: linear-gradient(45deg, #2be243ff, #91ff14ff);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 1rem;
        cursor: pointer;
        transition: opacity 0.2s;
      }
      .submit-button:hover {
        opacity: 0.9;
      }

      .posts-container {
        display: flex;
        flex-direction: column;
        gap: 24px;
      }

      .no-posts-message {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 32px;
        text-align: center;
        color: #65676b;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
      }

      .post-card {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        overflow: hidden;
      }

      .post-image {
        width: 100%;
        height: auto;
        display: block;
      }

      .post-content {
        padding: 16px;
      }

      .post-title {
        margin: 0 0 12px 0;
        font-size: 1.2rem;
      }

      .post-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .like-button, .delete-button {
        background: none;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #65676b;
        font-size: 0.9rem;
        font-weight: 600;
        padding: 8px;
        border-radius: 6px;
        transition: background-color 0.2s, color 0.2s;
      }

      .like-button:hover, .delete-button:hover {
        background-color: #f0f2f5;
      }

      .like-button.liked {
        color: #ff1493;
      }

      .like-button.liked .icon {
        fill: #ff1493;
      }

      .delete-button:hover {
        color: #fa383e;
      }

      .icon {
        width: 24px;
        height: 24px;
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  useEffect(() => {
    localStorage.setItem('posts', JSON.stringify(posts));
  }, [posts]);

  const handleAddPost = (title, image) => {
    const newPost = { id: Date.now(), title, image, liked: false };
    setPosts(prevPosts => [newPost, ...prevPosts]);
  };

  const handleDeletePost = (id) => {
    setPosts(posts.filter(post => post.id !== id));
  };

  const handleToggleLike = (id) => {
    setPosts(posts.map(post =>
      post.id === id ? { ...post, liked: !post.liked } : post
    ));
  };

  return (
    <div className="container">
      <header className="app-header">
        <h1 className="app-title">Galeria Zigma</h1>
      </header>

      <main>
        <PostForm onAddPost={handleAddPost} />
        <div className="posts-container">
          {posts.length > 0 ? (
            posts.map(post => (
              <Post
                key={post.id}
                post={post}
                onDelete={handleDeletePost}
                onLike={handleToggleLike}
              />
            ))
          ) : (
            <div className="no-posts-message">
              <p>No hay publicaciones todavía.</p>
              <p>¡Sube tu primera foto!</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

