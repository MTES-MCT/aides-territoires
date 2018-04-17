import React from "react";
import Header from "./Header";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("Header", module).add("Header", () => <Header />);
