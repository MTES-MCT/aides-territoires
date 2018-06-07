import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import Navigation from "../components/ui/bulma/Navigation";
import { Route, BrowserRouter, Switch } from "react-router-dom";

const links = [
  {
    title: "Aide-territoires",
    to: "/"
  },
  {
    title: "Rechercher un aide",
    to: "/recherche"
  },
  {
    title: "Contact",
    to: "https://www.aides-territoires.beta.gouv.fr/#contact"
  }
];

storiesOf("Navigation", module).add("Navigation", () => (
  <BrowserRouter>
    <Navigation links={links} />
  </BrowserRouter>
));
