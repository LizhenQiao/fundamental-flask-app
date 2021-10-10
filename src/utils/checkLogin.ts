import cookie from "react-cookies";

export default function checkLogin() {
  if (cookie.load("username")) {
    return true;
  } else {
    return false;
  }
}
