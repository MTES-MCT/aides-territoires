import React from "react";
import "bulma/css/bulma.css";

import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { linkTo } from "@storybook/addon-links";

import { Button, Welcome } from "@storybook/react/demo";
import SearchForm from "../features/search/components/presentationals/searchForm/SearchForm";
import SearchFormContainer from "../features/search/components/containers/searchFormContainer/SearchFormContainer";

storiesOf("SearchForm", module).add("SearchForm", () => (
  <SearchForm
    suggestions={[]}
    onSearchSubmit={() => {}}
    onSearchChange={() => {}}
  />
));

storiesOf("SearchFormContainer", module).add(
  "SearchForm connected to Api",
  () => <SearchFormContainer />
);
