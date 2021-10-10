import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import cookie from "react-cookies";
import "./login.less";

type AccountInformation = {
  username: string;
  password: string;
};

//TODO: 在页面里若检查到为未登录状态应该给提示并自动跳转到登录页面(这个可以写成一个共有方法放在utils里在每个页面里调用)
function LoginPage() {
  const [currentUsername, setCurrentUsername] = useState("");
  const [currentPassword, setCyrrentPassword] = useState("");
  const [redirectToHomePage, setRedirectToHomePage] = useState(false);

  useEffect(() => {}, []);

  const clickLogin = async (accountInformation: AccountInformation) => {
    await fetch("api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(accountInformation),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          cookie.save("username", accountInformation.username, { path: "/" });
          setRedirectToHomePage(true);
        }
      });
    // TODO: 清空input框; 登陆成功提示；跳转；
  };

  return (
    <div>
      <span>Username:</span>
      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setCurrentUsername(e.target.value)}
      />
      <br />
      <span>Password:</span>
      <input
        type="password"
        onChange={(e) => setCyrrentPassword(e.target.value)}
      />
      <br />
      <button
        onClick={() =>
          clickLogin({ username: currentUsername, password: currentPassword })
        }
      >
        Login
      </button>
      {redirectToHomePage && <Redirect push to="/home" />}
    </div>
  );
}

export default LoginPage;
