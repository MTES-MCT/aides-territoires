import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import SuggestionList from "../components/ui/SuggestionList";
import { withInfo } from "@storybook/addon-info";

const suggestions = [
  { label: "option 1", value: "option_1" },
  { label: "option 2", value: "option_2" },
  { label: "option 3", value: "option_3" },
  { label: "option 4", value: "option_4" }
];

storiesOf("SuggestionList", module).add(
  "SuggestionList",
  withInfo()(() => (
    <div style={{ padding: "2rem" }}>
      <SuggestionList
        onClick={action("on suggestion clicked")}
        suggestions={suggestions}
      />
    </div>
  ))
);
