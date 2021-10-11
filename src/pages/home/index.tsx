import React, { useState } from "react";
import cookie from "react-cookies";
import "./home.less";

function HomePage() {
  const [showResetPasswordDiv, setShowResetPasswordDiv] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const confirmResetPassword = async (username: string, password: string) => {
    if (newPassword !== confirmPassword) {
      console.log(
        "new password and confirm password should be equal. please try again."
      );
      return;
    }
    await fetch("api/reset_password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
  };

  const resetPasswordDiv = (username: string) => {
    return (
      <div>
        <p>reset password</p>
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
        <button onClick={() => confirmResetPassword(username, newPassword)}>
          Reset
        </button>
      </div>
    );
  };

  return (
    <div>
      <h2>HomePage</h2>
      <button onClick={() => setShowResetPasswordDiv(true)}>
        Reset Password
      </button>
      {showResetPasswordDiv && (
          <button onClick={() => setShowResetPasswordDiv(false)}>hide</button>
        ) &&
        resetPasswordDiv(cookie.load("username"))}
    </div>
  );
}

export default HomePage;
