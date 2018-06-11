import React from "react";
import image from "../../static/images/logo-aides-territoires.png";

const Logo = props => {
  return <img {...props} alt="logo" src={image} />;
};

export default Logo;
