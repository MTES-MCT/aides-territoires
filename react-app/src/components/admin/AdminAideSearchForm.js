import React from "react";
import { reduxForm, Field } from "redux-form";
import { compose } from "react-apollo";
import ButtonSubmitWithLoader from "../ui/bulma/ButtonSubmitWithLoader";
import Text from "../ui/finalFormBulma/Text";

class AdminAideSearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    const { handleSubmit, submitting } = this.props;
    return (
      <form onSubmit={handleSubmit}>
        <div className="columns">
          <div className="column">
            <Field className="" label="nom" name="nom" component={Text} />
          </div>
          <div className="column">
            <ButtonSubmitWithLoader
              style={{ marginTop: "32px" }}
              className="button is-info"
              type="submit"
              isLoading={submitting}
            >
              Chercher
            </ButtonSubmitWithLoader>
          </div>
        </div>
      </form>
    );
  }
}

export default compose(
  reduxForm({
    form: "adminSearchAide",
    initialValues: {
      nom: ""
    }
  })
)(AdminAideSearchForm);
