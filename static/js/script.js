// Navbar hide
let navBar = document.querySelectorAll(".nav-link");
let navCollapse = document.querySelector(".navbar-collapse");
navBar.forEach(function (a) {
  a.addEventListener("click", function () {
    navCollapse.classList.remove("show");
  })
})


document.querySelector(".closeMe").addEventListener("click", () => {
  document.querySelector("#login").classList.remove("openmodal");
});


// Show Password
let eyeicon = document.getElementById("eyeicon");
let password = document.getElementById("password");
eyeicon.onclick = function () {
  if (password.type == "password") {
    password.type = "text";
    eyeicon.className = "fa-regular fa-eye";
  } else {
    password.type = "password";
    eyeicon.className = "fa-regular fa-eye-slash";
  }
};




