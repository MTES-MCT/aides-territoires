import "./polyfill";
import "raf/polyfill";
import "core-js/es6/map";
import "core-js/es6/set";
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

ReactDOM.render(<App />, document.getElementById("root"));
