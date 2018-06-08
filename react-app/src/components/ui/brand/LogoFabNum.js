import React from "react";
import image from "../../../images/logo-fabnum.svg";
import PropTypes from "prop-types";

const LogoFabNum = ({ width }) => {
  return <img width={width} alt="logo fabrique numérique" src={image} />;
};

LogoFabNum.propTypes = {
  width: PropTypes.string
};

LogoFabNum.defaultProps = {
  width: "100px"
};

export default LogoFabNum;
