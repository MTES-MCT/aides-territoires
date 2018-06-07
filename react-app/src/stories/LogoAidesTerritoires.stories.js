import React from "react";
import LogoAidesTerritoires from "../components/ui/brand/LogoAidesTerritoires";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("brand", module).add("Logo", () => <LogoAidesTerritoires />);
