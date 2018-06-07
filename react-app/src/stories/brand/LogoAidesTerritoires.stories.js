import React from "react";
import LogoAidesTerritoires from "../../components/ui/brand/LogoAidesTerritoires";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";

storiesOf("brand", module).add(
  "Logo",
  withInfo()(() => <LogoAidesTerritoires />)
);
