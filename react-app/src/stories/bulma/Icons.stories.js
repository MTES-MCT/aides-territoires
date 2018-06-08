import React from "react";
import { ArrowDown, ArrowUp } from "../../components/ui/bulma/Icons";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";

storiesOf("Bulma", module).add("ArrowDown", withInfo()(() => <ArrowDown />));
storiesOf("Bulma", module).add("ArrowUp", withInfo()(() => <ArrowUp />));
