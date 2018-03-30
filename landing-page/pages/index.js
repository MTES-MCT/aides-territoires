import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/index/Header";
import CommentCaMarche from "../components/index/CommentCaMarche";
import Chronophage from "../components/index/Chronophage";
import Benefices from "../components/index/Benefices";
import TypeAides from "../components/index/TypesAides";
import FormPorteurProjetQuartierDurable from "../components/index/FormPorteurProjetQuartierDurable";
import ContactForm from "../components/common/ContactForm";
import graphcms from "../services/graphcms";

class HomePage extends React.Component {
  static async getInitialProps({ req }) {
    const query = `{
      Pagedaccueil(id:"cjfdxk4tpcy3v016424h68se6") {
        header,
        headertitre,
        headercalltoaction
      }
    }
    `;
    return graphcms.request(query);
  }
  render() {
    return (
      <DefaultLayout>
        <Header data={this.props.Pagedaccueil} />
        <CommentCaMarche />
        <Chronophage />
        <Benefices />
        {/* <TypeAides /> */}
        <FormPorteurProjetQuartierDurable />
        <ContactForm />
      </DefaultLayout>
    );
  }
}

export default HomePage;
