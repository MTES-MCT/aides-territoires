import Document1, { meta } from "../content/a-propos-part-1.md";
import Document2 from "../content/a-propos-part-2.md";
import DocumentEquipe, { meta as metaEquipe } from "../content/equipe.md";
import Header from "../components/ui/Header";
import ButtonLink from "../components/ui/ButtonLink";
import Section from "../components/ui/Section";
import backgroundImageUrl from "../static/images/header.png";
import Layout from "../components/ui/Layout";
import Container from "../components/ui/Container";
import MemberList from "../components/ui/MemberList";

let APropos = ({ classes }) => {
  return (
    <Layout>
      <Header
        backgroundImageUrl={backgroundImageUrl}
        title={meta.header.title}
        subtitle={meta.header.subtitle}
      />
      <Container>
        <Section>
          <Document1 />
          <div
            style={{
              padding: "3rem",
              display: "flex",
              justifyContent: "space-around"
            }}
          >
            <ButtonLink href="/#contact">Contactez nous</ButtonLink>
            <ButtonLink href="https://docs.google.com/forms/d/e/1FAIpQLSd5dkHPbETqMP35SoTPUCwv96cjKvpBckErkh7pBcUzps-Nnw/viewform">
              Référencer une aide
            </ButtonLink>
          </div>
          <Document2 />
          <div>
            <h3>{metaEquipe.title}</h3>
            <p>{metaEquipe.description}</p>
            <MemberList members={metaEquipe.members} />
          </div>
        </Section>
      </Container>
    </Layout>
  );
};

export default APropos;
