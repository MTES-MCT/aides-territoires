import React from "react";
import { NavLink } from "react-router-dom";
const AdminSideMenu = () => {
  return (
    <div className="SideMenu">
      <aside className="menu">
        <p className="menu-label">AIDES</p>
        <ul className="menu-list">
          <li>
            <NavLink to="/admin/aide/create">Créer une aide</NavLink>
          </li>
          <li>
            <NavLink to="/admin/aide/list">Liste des aides</NavLink>
          </li>
          <li>
            <NavLink to="/admin/aide/permissions">Permissions et rôles</NavLink>
          </li>
          {/*
          <li>
            <NavLink to="/type-de-territoire/create">
              Créer un type de territoire
            </NavLink>
          </li>
          */}
        </ul>
      </aside>
    </div>
  );
};

export default AdminSideMenu;
