import React from "react";

const LogoFabNum = props => {
  return (
    <img
      id="logo-fabrique-numerique"
      style={{ paddingLeft: "1rem" }}
      {...props}
      alt="logo fabrique numérique"
      src={"../../static/images/logo-fabnum.svg"}
    />
  );
};

export default LogoFabNum;
