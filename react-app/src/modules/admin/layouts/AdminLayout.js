import React from "react";
import Navigation from "modules/common/presentationals/Navigation";
import SideMenu from "../presentationals/SideMenu";
import injectSheet from "react-jss";
import classnames from "classnames";
import "bulma/css/bulma.css";

const styles = {
  column: {
    padding: "2rem",
    paddingTop: "4rem",
    minHeight: "100%"
  },
  sideMenu: {
    backgroundColor: "rgb(247, 249, 250)",
    borderRight: "1px solid rgb(211, 220, 224)"
  },
  appMainMenu: {
    boxShadow: "0px 0px 40px 0px rgba(0, 0, 0, 0.3)"
  }
};

class DefaultLayout extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div className="AdminLayout">
        <div className={classes.appMainMenu}>
          <Navigation />
        </div>
        <div className="columns">
          <div
            className={classnames(
              "column is-3",
              classes.column,
              classes.sideMenu
            )}
          >
            <SideMenu />
          </div>
          <div className={classnames("column is-9", classes.column)}>
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}

export default injectSheet(styles)(DefaultLayout);
