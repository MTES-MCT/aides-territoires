import React from "react";
import { NavLink } from "react-router-dom";
import gql from "graphql-tag";
import { graphql, compose } from "react-apollo";
import GraphQLError from "../ui/GraphQLError";
import AppLoader from "../ui/AppLoader";

const AdminSideMenu = ({ data: { error, loading, menu } }) => {
  if (error) return <GraphQLError />;
  if (loading) return <AppLoader />;
  return (
    <div className="SideMenu">
      <aside className="menu">
        <p className="menu-label">AIDES</p>
        <ul className="menu-list">
          {menu.links.map(link => (
            <li key={link.href}>
              <NavLink to={link.href}>{link.title}</NavLink>
            </li>
          ))}
        </ul>
      </aside>
    </div>
  );
};

const query = gql`
  query menu {
    menu(id: "adminMenu") {
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
