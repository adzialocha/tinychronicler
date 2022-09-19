import styled from 'styled-components';

type Props = {
  children: React.ReactNode;
};

const MainStyled = styled.main`
  display: flex;
  justify-content: center;
  padding: 75px;
`;

const Main = ({ children }: Props) => {
  return <MainStyled>{children}</MainStyled>;
};

export default Main;
