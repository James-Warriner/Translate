import { userStatus } from "./checkLogin.js";

async function recents(){
  const sidebarRecents = document.getElementById("recents");
  sidebarRecents.innerHTML="";
  const notLoggedIn = `            <p style="text-align:center" class="mt-5">You must be logged in to view history</p>
            <a href="/login">Login</a>`;
  const noContent = `<p>No content</p>`;
  const res = await fetch("/recents",{
    method:"GET"
  });

  const data = await res.json();


  const recents = data.results

  let count = 0;

  if (Array.isArray(recents) && recents.length > 0){recents.forEach(recent => {

      count +=1;

      sidebarRecents.insertAdjacentHTML(
  "beforeend",
  `
  <div class="card mb-2 shadow-sm" data-id="${recent.id}">
  <div class="card-header p-2 bg-light d-flex justify-content-between align-items-center">
    <div>
      <strong>${recent.input_language} &rarr; ${recent.output_language}</strong>
      – ${recent.type}
    </div>
    <button class="imagebtn" aria-label="Delete">
      <img src="/static/image.png">
    </button>
  </div>
  <div class="card-body p-2">
    <p class="card-text mb-1">
      ${recent.original_text.substring(0, 30)}…
    </p>
    <small class="text-muted">
      ${new Date(recent.date).toLocaleString()}
    </small>
  </div>
</div>

  `
);

sidebarRecents.addEventListener("click", e => {

  if (e.target.closest(".imagebtn")) return;

  const card = e.target.closest(".card[data-id]");
  if (!card) return;

  const translationId = card.dataset.id;
  window.location.href = `/translation/${translationId}`;
});
  }
    

    
  );}

  
  const user_status = await userStatus();
  console.log(user_status);
  if (count == 0 && user_status != true){
    sidebarRecents.insertAdjacentHTML("beforeend",notLoggedIn);
  }

  sidebarRecents.insertAdjacentHTML("beforeend",noContent);
}


export {recents}