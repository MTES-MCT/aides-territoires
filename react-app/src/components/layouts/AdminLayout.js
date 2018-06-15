import React from "react";
import Navigation from "../ui/bulma/Navigation";
import AdminSideMenu from "../admin/AdminSideMenu";
import injectSheet from "react-jss";
import classnames from "classnames";
import "bulma/css/bulma.css";
import withConfig from "../decorators/withConfig";
import withUser from "../decorators/withUser";
import { compose } from "react-apollo";

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
            <h3 className="title is-4">Bienvenue {this.props.user.name}</h3>
            <h4 className="subtitle is-5">{this.props.user.roles.join(",")}</h4>
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

export default compose(
  withConfig,
  withUser({ mandatory: true }),
  injectSheet(styles)
)(DefaultLayout);
