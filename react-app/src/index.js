import "es6-shim";
import "es7-shim";
import "raf/polyfill";
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

ReactDOM.render(<App />, document.getElementById("root"));
