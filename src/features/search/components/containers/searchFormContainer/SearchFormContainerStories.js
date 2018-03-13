import React from "react";
import SearchFormContainer from "./SearchFormContainer";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("SearchFormContainer", module).add(
  "SearchForm with autocompletion via API",
  () => <SearchFormContainer onSearchSubmit={action("onSearchSubmit")} />
);
