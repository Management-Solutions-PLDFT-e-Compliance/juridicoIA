var resumoProcesso = document.getElementById('resumoProcesso').innerText.trim();

  // Inicializando o Typed.js
  var typed = new Typed('#typed-text-container', {
    strings: [resumoProcesso],
    typeSpeed: 5, // Velocidade de digitação em milissegundos
    loop: false, // Não repetir o efeito de digitação
    showCursor: false
  });

  document.getElementById('uploadForm').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('fileInputLabel').innerText = fileName;
});

function submitForm() {
    document.getElementById('uploadForm').submit();
}

function toggleLike() {
    var likeImg = document.getElementById("likeImg");
    var dislikeImg = document.getElementById("dislikeImg");

    likeImg.src = likeImg.src.includes("likeAtivo.png") ? "/static/assets/like.png" : "/static/assets/likeAtivo.png";
    dislikeImg.src = "/static/assets/dislike.png";
}

function toggleDislike() {
    var likeImg = document.getElementById("likeImg");
    var dislikeImg = document.getElementById("dislikeImg");

    dislikeImg.src = dislikeImg.src.includes("deslikeAtivo.png") ? "/static/assets/dislike.png" : "/static/assets/dislikeAtivo.png";
    likeImg.src = "/static/assets/like.png";
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('perguntar').addEventListener('click', function() {
        var textoPergunta = document.getElementById('texto').value;
        // Envie o texto para o Flask usando AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                console.log('Texto enviado com sucesso!');
            }
        };
        xhr.send('texto=' + encodeURIComponent(textoPergunta));
    });
});