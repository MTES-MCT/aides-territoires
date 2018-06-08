import React from "react";
import LogoFabNum from "../../components/ui/brand/LogoFabNum";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";

storiesOf("brand", module).add("LogoFabNum", withInfo()(() => <LogoFabNum />));
