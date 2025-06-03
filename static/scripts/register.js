
const form = document.getElementById("form")


form.addEventListener('submit', async function(e){

  e.preventDefault();
  
  const data = new FormData(form);
  const res = await fetch(form.action,{
    method:form.method,
    body:data
  });

  const payload = await res.json();

  if (res.ok){

    console.log(payload.email)
  
      const response = await fetch("/auth",{
        method: "POST",
        headers:{
          "Content-Type":"application/json"
        },
        body:JSON.stringify({
          email:payload.email,
          first_name:payload.first_name,
          last_name:payload.last_name,
          password:payload.password
        })
      })

      const data = await response.json();
      console.log("Hello")
      console.log(response)
      if (data.status == "sent"){
        window.location.replace("/auth")
      }
    
    
  }
  else{
    errorBar =  document.querySelector(".error-bar")
    errorBar.style.visibility="visible";
    errorBar.innerHTML = `<h3 style="text-align-center">`+ payload.message + `</h3>`
    setTimeout(() => {
        errorBar.style.visibility = 'hidden';
      }, 5000);
  }
})