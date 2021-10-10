import React, { useState, useEffect } from "react";
import "./register.less";

type AccountInformation = {
  username: string;
  password: string;
};

function Register() {
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const clickAdd = async (newAccount: AccountInformation) => {
    if (newPassword !== confirmPassword) {
      console.log(
        "new password and confirm password should be equal. please try again."
      );
      return;
    }
    await fetch("api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newAccount),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success === true) {
          console.log("successfully add new account.");
          // TODO: 清空input框；注册成功/失败提示
          // document.getElementById("username-input")!.value = "";
        } else {
          console.log(data.error);
        }
      });
  };

  return (
    <div>
      <span>New Username:</span>
      <input
        type="text"
        className="username-input"
        id="username-input"
        placeholder="Please input new username"
        onChange={(e) => setNewUsername(e.target.value)}
      />
      <br />
      <span>New Password:</span>
      <input
        type="password"
        className="password-input-new"
        id="password-input__new"
        onChange={(e) => setNewPassword(e.target.value)}
      />
      <br />
      <span>Confirm New Password:</span>
      <input
        type="password"
        className="password-input-confirm"
        id="password-input__confirm"
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      <br />
      <button
        onClick={() =>
          clickAdd({ username: newUsername, password: newPassword })
        }
      >
        add
      </button>
    </div>
  );
}

export default Register;
