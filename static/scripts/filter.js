async function filterDropdown(num) {
  const query = document.getElementById("dropdownSearch" + num).value;

  const res = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ q: query }),
  });

  const data = await res.json();

  const select = document.getElementById("languageSelect" + num);
  select.innerHTML = "";

  data.results.forEach((lang) => {
    const option = document.createElement("option");
    option.value = lang.code;
    option.textContent = lang.language;
    option.id = lang.id;
    select.appendChild(option);
  
  });

}

  function initDropdownSearch(index) {
  const input = document.getElementById(`dropdownSearch${index}`);
  if (!input) return;
  input.addEventListener("keyup", () => filterDropdown(index));
}






export {initDropdownSearch}
export { filterDropdown }