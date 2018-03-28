import React from "react";
import DefaultLayout from "../components/DefaultLayout";
import SectionCommentCaMarche from "../components/SectionCommentCaMarche";
import SectionChronophage from "../components/SectionChronophage";
import SectionBenefices from "../components/SectionBenefices";
import SectionTypeAides from "../components/SectionTypesAides";
import SendInBlueInscrivezVous from "../components/SendInBlueInscrivezVous";
import SendInBlueContactForm from "../components/SendInBlueContactForm";

class HomePage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <SectionCommentCaMarche />
        <SectionChronophage />
        <SectionBenefices />
        <hr />
        <SectionTypeAides />
        <SendInBlueInscrivezVous />
        <section id="contact" className="section container">
          <SendInBlueContactForm />
        </section>
      </DefaultLayout>
    );
  }
}

export default HomePage;
