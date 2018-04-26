import React from "react";
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
