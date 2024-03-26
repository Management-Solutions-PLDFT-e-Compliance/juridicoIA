var resumoProcesso = document.getElementById('resumoProcesso').innerText.trim();

  // Inicializando o Typed.js
  var typed = new Typed('#typed-text-container', {
    strings: [resumoProcesso],
    typeSpeed: 5, // Velocidade de digitação em milissegundos
    loop: false, // Não repetir o efeito de digitação
    showCursor: false
  });

  document.getElementById('fileInputLabel').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('fileInputLabel').innerText = fileName;
});

// function submitForm() {
//     document.getElementById('uploadForm').submit();
// // }
// function submitForm() {
//     document.getElementById('uploadForm2').submit();
// }
// function submitForm() {
//     document.getElementById('uploadForm3').submit();
// }

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


function perguntar() {
  var pergunta = document.getElementById("texto").value;
  var valor = document.getElementById("valor").value;
  fetch('/pergunta', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ pergunta: pergunta, valor: valor }),
  })
  .then(response => response.json())
  .then(data => {
      console.log(data);
      alert("Pergunta enviada com sucesso!");
  })
  .catch((error) => {
      console.error('Error:', error);
      alert("Ocorreu um erro ao enviar a pergunta.");
  });
}

document.getElementById("respostaCurta").addEventListener("click", function() {
  document.getElementById("valor").value = 100;
});

document.getElementById("respostaMedia").addEventListener("click", function() {
  document.getElementById("valor").value = 250;
});

document.getElementById("respostaLonga").addEventListener("click", function() {
  document.getElementById("valor").value = 500;
});

// Seleciona o botão padrão (Média) e remove a classe btn-sintese-active
document.getElementById('respostaMedia').classList.remove('btn-sintese-active');

// Adiciona um evento de clique para cada botão
document.getElementById('respostaCurta').addEventListener('click', function() {
  // Remove a classe btn-sintese-active de todos os botões
  document.getElementById('respostaCurta').classList.add('btn-sintese-active');
  document.getElementById('respostaMedia').classList.remove('btn-sintese-active');
  document.getElementById('respostaLonga').classList.remove('btn-sintese-active');
});

document.getElementById('respostaMedia').addEventListener('click', function() {
  // Remove a classe btn-sintese-active de todos os botões
  document.getElementById('respostaCurta').classList.remove('btn-sintese-active');
  document.getElementById('respostaMedia').classList.add('btn-sintese-active');
  document.getElementById('respostaLonga').classList.remove('btn-sintese-active');
});

document.getElementById('respostaLonga').addEventListener('click', function() {
  // Remove a classe btn-sintese-active de todos os botões
  document.getElementById('respostaCurta').classList.remove('btn-sintese-active');
  document.getElementById('respostaMedia').classList.remove('btn-sintese-active');
  document.getElementById('respostaLonga').classList.add('btn-sintese-active');
});

const showLoading = function() {
  Swal.fire({
    title: 'Gerando resposta...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });
};

document.getElementById('perguntar').addEventListener('click', showLoading);
