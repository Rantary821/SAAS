document.addEventListener("DOMContentLoaded", function () {
    const cpfInput = document.querySelector('input[name="cpf"]');
    if (!cpfInput) return;

    cpfInput.addEventListener("input", function (e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/(\d{3})(\d)/, "$1.$2")
                         .replace(/(\d{3})(\d)/, "$1.$2")
                         .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        } else {
            value = value.replace(/^(\d{2})(\d)/, "$1.$2")
                         .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
                         .replace(/\.(\d{3})(\d)/, ".$1/$2")
                         .replace(/(\d{4})(\d)/, "$1-$2");
        }
        e.target.value = value;
    });
});
