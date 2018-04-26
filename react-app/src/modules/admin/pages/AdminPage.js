import React from "react";
import { NavLink } from "react-router-dom";
import AdminLayout from "modules/admin/layouts/AdminLayout";
import Dashboard from "../presentationals/Dashboard";

const AdminPage = () => {
  return (
    <AdminLayout>
      <Dashboard />
    </AdminLayout>
  );
};

export default AdminPage;
