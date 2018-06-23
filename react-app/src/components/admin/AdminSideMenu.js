import React from "react";
import { NavLink } from "react-router-dom";
import gql from "graphql-tag";
import { graphql, compose } from "react-apollo";
import GraphQLError from "../ui/GraphQLError";
import AppLoader from "../ui/AppLoader";

const AdminSideMenu = class extends React.Component {
  render() {
    const { data } = this.props;
    if (data.error) return <GraphQLError error={data.error} />;
    if (data.loading) return <AppLoader />;
    return (
      <div className="SideMenu">
        <aside className="menu">
          <p className="menu-label">AIDES</p>
          <ul className="menu-list">
            {data.menu.links.map(link => (
              <li key={link.href}>
                <NavLink to={link.href}>{link.title}</NavLink>
              </li>
            ))}
          </ul>
        </aside>
      </div>
    );
  }
};

const query = gql`
  query menu {
    menu: getMenu(id: "adminMenu") {
      id
      label
      links {
        href
        title
      }
    }
  }
`;

export default compose(graphql(query))(AdminSideMenu);
