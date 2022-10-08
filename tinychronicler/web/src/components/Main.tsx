import styled from 'styled-components';

type Props = {
  children: React.ReactNode;
};

const MainStyled = styled.main`
  display: flex;
  justify-content: center;
  padding: 75px;
  padding-bottom: 0;

  @media (max-width: 900px) {
    padding-top: 50px;
    padding-left: 0;
    padding-right: 0;
  }
`;

const Main = ({ children }: Props) => {
  return <MainStyled>{children}</MainStyled>;
};

export default Main;
