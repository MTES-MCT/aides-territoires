import React from "react";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";

const Beta = ({ classes }) => <div className={classes.div}>Version bêta</div>;

const styles = {
  div: {
    padding: "1rem",
    background: "#ffdd57",
    color: "black",
    textTransform: "uppercase",
    borderRadius: "5px",
    maxWidth: "200px",
    margin: "auto"
  },
  [uiConfig.breakpoints.smallScreen]: {
    div: {
      marginTop: "1rem"
    }
  }
};

export default injectSheet(styles)(Beta);
