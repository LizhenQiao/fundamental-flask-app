import React, { useState } from "react";
import Register from "../../components/register";
import "./home.less";

//TODO: /login页面跳转至此，检测账号性质，如果是admin，选择展示manage_account部分，否则这些部分不展示
function HomePage() {
  const [isAdmin, setIsAdmin] = useState(false);
  
  return (
    <div>
      <h2>HomePage</h2>
      <Register></Register>
    </div>
  );
}

export default HomePage;
