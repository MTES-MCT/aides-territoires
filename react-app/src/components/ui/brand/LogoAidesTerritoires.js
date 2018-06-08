import React from "react";
import image from "../../../images/logo-aides-territoires.png";
import classNames from "classnames";

const Logo = props => {
  return <img {...props} alt="logo" src={image} />;
};

export default Logo;
