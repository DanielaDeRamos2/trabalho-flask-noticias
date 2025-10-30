document.getElementById('cadastroForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = document.getElementById('cadastroForm');
    const formData = new FormData(form);

    const res = await fetch('/cadastro', {
        method: 'POST',
        body: formData
    });

    const data = await res.json();

    if (data.sucesso) {
        console.log("Notícia cadastrada com sucesso!");
        setTimeout(() => window.location.href = '/', 1500);
    } else {
        console.log("Erro ao cadastrar notícia!");
    }
});
