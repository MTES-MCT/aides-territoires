import React from "react";
import { NavLink } from "react-router-dom";
import "./SideMenu.css";
const SideMenu = () => {
  return (
    <div className="SideMenu">
      <aside className="menu">
        <p className="menu-label">AIDES</p>
        <ul className="menu-list">
          <li>
            <NavLink to="/aide/create">Créer une aide</NavLink>
          </li>
          <li>
            <NavLink to="/aide/list">Liste des aides</NavLink>
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

export default SideMenu;
