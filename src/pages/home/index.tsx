import React, { useState, useRef } from "react";
import cookie from "react-cookies";
import "./home.less";

function HomePage() {
  const [showResetPasswordDiv, setShowResetPasswordDiv] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [uploadImage, setUploadImage] = useState<FormData>();

  const uploadRef = useRef() as React.MutableRefObject<HTMLInputElement>;

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

  const getImg = () => {
    if (uploadRef.current.files) {
      let fileData = uploadRef.current.files[0];
      let formData = new FormData();
      formData.append("uploadImage", fileData);
      setUploadImage(formData);
    }
  };

  const clickSubmit = async () => {
    await fetch("api/upload", {
      method: "POST",
      headers: {},
      body: uploadImage,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          console.log("Image upload successfully.");
        }
      });
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

  const uploadImgDiv = () => {
    return (
      <div>
        <div>Upload Image</div>
        <input
          type="file"
          name="file"
          multiple={true}
          id="uploadimg"
          ref={uploadRef}
          onChange={() => getImg()}
        />
        <br />
        <button onClick={() => clickSubmit()}>Submit</button>
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
      {uploadImgDiv()}
    </div>
  );
}

export default HomePage;
