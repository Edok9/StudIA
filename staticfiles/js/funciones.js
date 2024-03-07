function openCalculator() {
  var baseUrl = window.location.protocol + "//" + window.location.host;
  var calculatorUrl = baseUrl + "/Calculadora.html";
  window.open(calculatorUrl, "Calculadora", "width=600,height=800");
}
document.addEventListener("DOMContentLoaded", function() {
    var navLinks = document.getElementsByClassName("nav-link");
    
    for (var i = 0; i < navLinks.length; i++) {
      navLinks[i].addEventListener("mouseover", function() {
        this.style.color = "red"; // Cambia el color al pasar el mouse por encima (puedes personalizarlo)
      });
      
      navLinks[i].addEventListener("mouseout", function() {
        this.style.color = "forestgreen"; // Restaura el color original al salir el mouse
      });
    }
  });
  function Acerca(){
    alert("Usted ya se encuentra en acerca de nosotros :(");
}
function Galeria(){
  alert("Usted ya se encuentra en Galeria :(");
}
function fFormulario(){
  alert("Usted ya se encuentra en Formulario :(");
}
function Prove(){
  alert("Usted ya se encuentra en Proveedores :(");
}
function myFunction(x) {
  x.style.background = "yellow";
}
function restoreBackground(x) {
  x.style.background = "";
}
function openFlappy() {
  window.open("index.html", "Flappy", "width=700,height=600");
}