import { recents } from "./fetchRecents.js"
import { filterDropdown,initDropdownSearch } from "./filter.js"

document.addEventListener('DOMContentLoaded',function(){
    filterDropdown(1);
    filterDropdown(2);
    initDropdownSearch(1);
    initDropdownSearch(2);
    recents();

  let img = null







  document.getElementById("ImgInput").addEventListener("change",function(e){

    img = e.target.files[0];
    if (img == null){
      return;
    }


  })

  document.getElementById("translateButton").addEventListener('click',async function(){
    const formData = new FormData();

    const inp_lang = document.getElementById("languageSelect1").value;
    const out_lang = document.getElementById("languageSelect2").value;

    const input = document.getElementById("in");
    const output = document.getElementById("out");

    formData.append("image",img,img.name);
    formData.append("src_code",inp_lang);
    formData.append("trgt_code",out_lang);

    const res = await fetch("/image",{method:"POST",
      body:formData
    });

    if (!res.ok){
      const errorBar = document.getElementById("error-bar");
      errorBar.style.visibility = "visible";
      errorBar.innerText = `Upload of ${img.name} failed`
    }
    else{
      const data = await res.json();
      input.innerText = data.text;
      output.innerText = data.translated;

    }
  })




})