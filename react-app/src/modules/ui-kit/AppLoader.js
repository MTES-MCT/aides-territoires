import React from "react";
import "./AppLoader.css";

const AppLoader = ({ children }) => {
  return (
    <div className="lds-roller-wraper">
      <div className="lds-roller">
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
        <div />
      </div>
    </div>
  );
};

export default AppLoader;
