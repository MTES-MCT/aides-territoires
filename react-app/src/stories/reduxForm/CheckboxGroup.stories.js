import React from "react";
import CheckboxGroup from "../../components/ui/reduxForm/CheckboxGroup";
import { Provider } from "react-redux";
import store from "../../store";
import { reduxForm, Field, change } from "redux-form";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

const options = [
  { label: "option 1", value: "option_1" },
  { label: "option 2", value: "option_2" },
  { label: "option 3", value: "option_3" },
  { label: "option 4", value: "option_4" }
];

let ExampleForm = () => {
  return (
    <div>
      <CheckboxGroup name="type" options={options} />
    </div>
  );
};

ExampleForm = reduxForm({
  // a unique name for the form
  form: "exampleForm"
})(ExampleForm);

storiesOf("Redux form", module).add("CheckboxGroup", () => {
  return (
    <Provider store={store}>
      <ExampleForm />
    </Provider>
  );
});
