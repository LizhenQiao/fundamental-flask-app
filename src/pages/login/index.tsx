import React, { useState, useEffect } from "react";
import "./login.less";

function Login() {
  const [accountRight, setAccountRight] = useState(11);
  useEffect(() => {
    fetch("api/account/verify_login?password=1122")
      .then((res) => res.json())
      .then((data) => {
        setAccountRight(data.result);
      });
  }, []);

  const login = (accountName: string, password: string) => {
    // const res = fetch("api/account/verify_login?" + accountName);
    // if (res.password == password) {
    //   //TODO: 登陆成功
    // } else {
    //   //TODO: 登陆失败弹窗
    // }
  };

  return (
    <div>
      <span>Username:</span><input type="text" />
      <div></div>
      <span>Password:</span><input type="text" />
      <div></div>
      <button>Login</button>
    </div>
  );
}

export default Login;
