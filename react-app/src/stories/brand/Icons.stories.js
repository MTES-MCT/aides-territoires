import React from "react";
import { ArrowDown, ArrowUp } from "../../components/ui/bulma/Icons";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("Bulma icons", module).add("ArrowDown", () => <ArrowDown />);
storiesOf("Bulma icons", module).add("ArrowUp", () => <ArrowUp />);
