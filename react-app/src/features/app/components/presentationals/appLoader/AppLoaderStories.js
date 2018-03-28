import React from "react";
import AppLoader from "./AppLoader";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("AppLoader", module).add("AppLoader without text", () => (
  <AppLoader />
));

storiesOf("AppLoader", module).add("AppLoader with text", () => (
  <AppLoader>Chargement en cours ...</AppLoader>
));
