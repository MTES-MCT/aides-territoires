import React from "react";
import AppLoader from "../components/ui/AppLoader";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("AppLoader", module).add("AppLoade simple", () => <AppLoader />);

storiesOf("AppLoader", module).add("AppLoader with text", () => (
  <AppLoader>Chargement en cours ...</AppLoader>
));
