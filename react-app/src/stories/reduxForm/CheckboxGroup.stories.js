import React from "react";
import CheckboxGroup from "../../components/ui/reduxFormMaterialUI/CheckboxGroup";
import { Provider } from "react-redux";
import store from "../../store";
import { reduxForm, Field, change } from "redux-form";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import { withInfo } from "@storybook/addon-info";

const options = [
  { label: "option 1", value: "option_1" },
  { label: "option 2", value: "option_2" },
  { label: "option 3", value: "option_3" },
  { label: "option 4", value: "option_4" }
];

storiesOf("Redux form & Material ui", module).add("CheckboxGroup", () => {
  let ExampleForm = () => {
    return (
      <MuiThemeProvider>
        <form onSubmit={() => {}}>
          <div>
            <CheckboxGroup name="type" options={options} />
          </div>
        </form>
      </MuiThemeProvider>
    );
  };

  ExampleForm = reduxForm({
    // a unique name for the form
    form: "exampleForm"
  })(ExampleForm);
  return (
    <Provider store={store}>
      <ExampleForm />
    </Provider>
  );
});
