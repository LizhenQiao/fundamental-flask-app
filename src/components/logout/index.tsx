import React from "react";
import cookie from "react-cookies";
import "./logout.less";

function Logout() {
  const clickLogout = () => {
    cookie.remove("username", { path: "/" });
    window.location.reload();
  };

  return (
    <div>
      <button onClick={() => clickLogout()}>Logout</button>
    </div>
  );
}

export default Logout;
