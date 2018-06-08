import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import ButtonSubmitWithLoader from "../../components/ui/bulma/ButtonSubmitWithLoader";
import { Route, BrowserRouter, Switch } from "react-router-dom";

storiesOf("Bulma", module).add("Submit button", () => (
  <ButtonSubmitWithLoader>Clique moi</ButtonSubmitWithLoader>
));

storiesOf("Bulma", module).add("Submit button loading", () => (
  <ButtonSubmitWithLoader isLoading={true}>Clique moi</ButtonSubmitWithLoader>
));
