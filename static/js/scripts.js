function carregarTipus() {
    let comercial = document.getElementById("comercial");
    let zona = comercial.options[comercial.selectedIndex].dataset.zona;
    let email = comercial.options[comercial.selectedIndex].dataset.email;

    document.getElementById("zona").value = zona;

    fetch("/tipus/" + zona)
        .then(res => res.json())
        .then(data => {
            let selector = document.getElementById("tipus");
            selector.innerHTML = "";
            data.forEach(t => {
                selector.innerHTML += `<option>${t.tipus_animacio}</option>`;
            });
        });
}

function carregarCentre() {
    let nom = document.getElementById("centre").value;
    fetch("/centre/" + nom)
        .then(res => res.json())
        .then(c => {
            document.getElementById("adreca").value = c.adreça;
            document.getElementById("localitat").value = c.localitat;
        });
}

function carregarLlibre() {
    let titol = document.getElementById("llibre").value;
    fetch("/llibre/" + titol)
        .then(res => res.json())
        .then(l => {
            document.getElementById("autor").value = l.author || l.autor;
            document.getElementById("correu_autor").value = l.correu_autor;
        });
}