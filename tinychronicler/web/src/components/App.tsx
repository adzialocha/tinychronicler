import { Fragment } from 'react';
import { HashRouter } from 'react-router-dom';
import { createGlobalStyle } from 'styled-components';

import Footer from '~/components/Footer';
import Header from '~/components/Header';
import Main from '~/components/Main';
import Router from '~/Router';

const GlobalStyle = createGlobalStyle`
  body {
    font-family: Arial, sans-serif;
  }
`;

type Props = {
  version: string;
};

const App = ({ version }: Props) => {
  return (
    <Fragment>
      <GlobalStyle />
      <HashRouter>
        <Header />
        <Main>
          <Router />
        </Main>
        <Footer version={version} />
      </HashRouter>
    </Fragment>
  );
};

export default App;
