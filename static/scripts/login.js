document.addEventListener('DOMContentLoaded',function(){

    const form = document.getElementById("form");

    form.addEventListener('submit', async function(e) {
      e.preventDefault()
      const data = new FormData(form);
      const res = await fetch("/login",{method:form.method,
        body: data
      });

      const payload = await res.json();
      console.log(payload)
      if (payload.status == "success"){
        window.location.href = "/";
      }
      else{
        const errorBar = document.querySelector(".error-bar");
        errorBar.style.visibility = "visible";
        errorBar.innerHTML = `Incorrect credentials`

        setTimeout(()=>{
          errorBar.style.visibility = "hidden";
        },5000)
      }
    })
  
})