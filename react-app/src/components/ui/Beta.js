import React from "react";
import injectSheet from "react-jss";

const Beta = ({ classes }) => <div className={classes.div}>Version bêta</div>;

const styles = {
  div: {
    padding: "1rem",
    background: "#ffdd57",
    color: "black",
    textTransform: "uppercase",
    borderRadius: "5px",
    maxWidth: "200px",
    margin: "auto",
    textAlign: "center"
  }
};

export default injectSheet(styles)(Beta);
