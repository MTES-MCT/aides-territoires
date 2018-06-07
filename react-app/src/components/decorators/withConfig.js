import React from "react";
import config from "../../config";
const withConfig = Component => props => (
  <Component {...props} config={config} />
);

export default withConfig;
