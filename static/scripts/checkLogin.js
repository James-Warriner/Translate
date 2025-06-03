async function userStatus(){
  const res = await fetch("/user_status",{method:"GET"});
  const data = await res.json();
  if (data.status == "true"){
    return true;
  }
  return false;

}

export {userStatus}