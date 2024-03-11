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