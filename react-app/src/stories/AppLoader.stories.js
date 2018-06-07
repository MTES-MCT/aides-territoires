import React from "react";
import AppLoader from "../components/ui/AppLoader";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";

storiesOf("AppLoader", module).add(
  "AppLoade simple",
  withInfo()(() => <AppLoader />)
);

storiesOf("AppLoader", module).add(
  "AppLoader with text",
  withInfo()(() => <AppLoader>Chargement en cours ...</AppLoader>)
);
