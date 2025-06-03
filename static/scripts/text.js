  import { filterDropdown } from "./filter.js"
  import { recents } from "./fetchRecents.js"
  import { initDropdownSearch } from "./filter.js"
  import "./loadRecent.js"
  
  document.addEventListener("DOMContentLoaded",function(){
    filterDropdown(1);
    filterDropdown(2);
    initDropdownSearch(1);
    initDropdownSearch(2);
    recents();
    document.getElementById("translate").addEventListener('click', async function(){

      const text = document.getElementById("text").value;
      const inp_lang = document.getElementById("languageSelect1").value;
      const out_lang = document.getElementById("languageSelect2").value;
      const inp_lang_id  = document.querySelector("#languageSelect1 option:checked").id;
      const out_lang_id  = document.querySelector("#languageSelect2 option:checked").id;

      const res = await fetch("/translate_text",{
        method:"POST",
        headers:{
          "Content-Type":"application/json"
        },
        body: JSON.stringify({
          text:text,
          inp_lang:inp_lang,
          out_lang:out_lang,
          inp_lang_id:inp_lang_id,
          out_lang_id:out_lang_id

        })
      });

      const data = await res.json();
      if (data.translated){
        document.getElementById("out").innerText = data.translated;
      }
      else{
        document.getElementById("out").innerText = "Error, reload";
      }
      recents()
      
    });


  })


