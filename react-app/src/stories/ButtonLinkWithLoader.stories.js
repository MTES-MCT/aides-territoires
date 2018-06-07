import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import ButtonLinkWithLoader from "../components/ui/bulma/ButtonLinkWithLoader";
import { Route, BrowserRouter, Switch } from "react-router-dom";

storiesOf("buttons", module).add(
  "Link button displaying loader on click",
  () => (
    <BrowserRouter>
      <ButtonLinkWithLoader to="/test">Clique moi</ButtonLinkWithLoader>
    </BrowserRouter>
  )
);
