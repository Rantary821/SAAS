async function buscarEndereco() {
    const cep = document.querySelector('input[name="cep"]').value.replace(/\D/g, '');
    if (cep.length !== 8) return;

    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();

        if (!data.erro) {
            document.querySelector('input[name="rua"]').value = data.logradouro;
            document.querySelector('input[name="bairro"]').value = data.bairro;
            document.querySelector('input[name="cidade"]').value = data.localidade;
            document.querySelector('input[name="estado"]').value = data.uf;
        }
    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
    }
}
