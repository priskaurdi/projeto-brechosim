document.getElementById('sidebar-link').addEventListener('click', function(event) {
    // Impede o comportamento padrão do link (navegar para outra página)
    event.preventDefault();
    // Mostra a tabela dentro da sidebar
    document.getElementById('catalogo-table').style.display = 'block';
  });

  
  