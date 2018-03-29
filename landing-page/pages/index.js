import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/index/Header";
import CommentCaMarche from "../components/index/CommentCaMarche";
import Chronophage from "../components/index/Chronophage";
import Benefices from "../components/index/Benefices";
import TypeAides from "../components/index/TypesAides";
import FormPorteurProjetQuartierDurable from "../components/index/FormPorteurProjetQuartierDurable";
import ContactForm from "../components/common/ContactForm";

class HomePage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <Header />
        <CommentCaMarche />
        <Chronophage />
        <Benefices />
        <hr />
        <TypeAides />
        <FormPorteurProjetQuartierDurable />
        <ContactForm />
      </DefaultLayout>
    );
  }
}

export default HomePage;
