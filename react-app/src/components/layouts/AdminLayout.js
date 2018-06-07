import React from "react";
import Navigation from "../ui/bulma/Navigation";
import AdminSideMenu from "../admin/AdminSideMenu";
import injectSheet from "react-jss";
import classnames from "classnames";
import "bulma/css/bulma.css";
import withConfig from "../decorators/withConfig";

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
          <Navigation links={this.props.config.navigationLinks} />
        </div>
        <div className="columns">
          <div
            className={classnames(
              "column is-3",
              classes.column,
              classes.sideMenu
            )}
          >
            <AdminSideMenu />
          </div>
          <div className={classnames("column is-9", classes.column)}>
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}

export default injectSheet(styles)(withConfig(DefaultLayout));
