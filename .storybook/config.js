import { configure } from "@storybook/react";
import "bulma/css/bulma.css";

const req = require.context("../src", true, /Stories\.js$/);
function loadStories() {
  req.keys().forEach(req);
}

configure(loadStories, module);
