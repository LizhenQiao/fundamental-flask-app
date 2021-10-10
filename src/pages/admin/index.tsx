import React, { useEffect, useState } from "react";
import Register from "./components/register";
import "./admin.less";

/* Home page of admin users.
   
   - Register / Add new accounts
   - delete accounts
   - reset passwords

*/
function AdminPage() {
  const [showRegisterDiv, setShowRegisterDiv] = useState(false);
  const [showResetPasswordDiv, setShowResetPasswordDiv] = useState(false);
  const [accountsList, setAccountsList] = useState([]);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  useEffect(() => {
    async function getAccountsList() {
      await fetch("api/accounts", {
        method: "GET",
      })
        .then((res) => res.json())
        .then((data) => setAccountsList(data.accounts));
    }
    getAccountsList();
  }, []);

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

  const clickDelete = async (username: string) => {
    await fetch("api/delete_account", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username }),
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

  const accountItem = (username: string) => {
    return (
      <div>
        <span>{username}</span>
        <button onClick={() => setShowResetPasswordDiv(true)}>
          reset password
        </button>
        <button onClick={() => clickDelete(username)}>delete</button>
        {showResetPasswordDiv && (
            <button onClick={() => setShowResetPasswordDiv(false)}>hide</button>
          ) &&
          resetPasswordDiv(username)}
      </div>
    );
  };

  return (
    <div>
      <h2>AdminHomePage</h2>
      <h3>Place for admin users to manage accounts.</h3>
      {accountsList && accountsList.map((username) => accountItem(username))}
      {showRegisterDiv ? (
        <div>
          <button onClick={() => setShowRegisterDiv(false)}>hide</button>
          <Register></Register>
        </div>
      ) : (
        <button onClick={() => setShowRegisterDiv(true)}>Register</button>
      )}
    </div>
  );
}

export default AdminPage;
